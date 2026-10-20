# 08 - Incident drill and blameless postmortem

## The drill

**Supposed incident:** below the async hop marked in `01-journey.md` (barber-saas-worker ->
`POST /internal/v1/events` on notifications-api), the SMTP server answers in **3 s** for **25 %** of
the e-mails during **40 minutes** (10:00 to 10:40). So notifications-api takes about 3 s to answer
the worker for one event in four. Normal time: about 50 ms.

Every timeout of the path is above 3 s (worker HTTP 5 s, notifications SMTP 10 s, gateway
`proxy_read_timeout` 10 s), so **nothing fails: deliveries are only slower.**

## Trace of one slow request (after the CP3 change, one trace_id)

trace_id `4e0b9d27c1f8a635b2d7e94c0a1f5d38`, user asks for a code at 10:12:04.

- `POST /api/v1/auth/password-reset` - api-gateway - **41 ms**
  - `POST /api/v1/auth/password-reset` - identity-auth-api - **37 ms**
    - `INSERT password_reset_token + outbox_event` - identity-auth-api (db) - **9 ms**
- `relay PasswordResetRequested` - barber-saas-worker - **3,046 ms** (starts 10:12:07.2, 3.1 s after the insert: next 5 s poll)
  - `POST /internal/v1/events` - notifications-api - **3,021 ms**
    - `processed_event check` - notifications-api (db) - **4 ms**
    - `SMTP send reset e-mail` - notifications-api (client) - **3,008 ms** <- the slow dependency
  - `POST /internal/v1/outbox-events/{id}/published` - identity-auth-api - **11 ms**

The e-mail leaves **6.1 s** after the user asked (3.1 s waiting for the next poll + 3.0 s of SMTP).
Normal: about 2.5 s on average (half a poll interval + 50 ms).

## Four log lines of that trace (format of `02-log-contract.md`)

```json
{"timestamp":"2026-10-20T15:12:04.116Z","level":"INFO","service":"identity-auth-api","version":"2.0.0","environment":"qa","trace_id":"4e0b9d27c1f8a635b2d7e94c0a1f5d38","span_id":"9a3c51e07b2d4f86","correlation_id":"b71e2c90d4a35f68e1c07a9b3d5f2e14","event":"password_reset.code.issued","message":"reset code and outbox row saved in one transaction","duration_ms":37,"user_id":"8d2f4a61-3b9c-4e07-a5d1-6c0e9f2b7a34","outbox_event_id":"f3a8c1d6-9e24-4b70-8c5f-2d7e1a0b9c63","event_type":"PasswordResetRequested","http_status":202}
{"timestamp":"2026-10-20T15:12:07.204Z","level":"INFO","service":"barber-saas-worker","version":"2.0.0","environment":"qa","trace_id":"4e0b9d27c1f8a635b2d7e94c0a1f5d38","span_id":"2c7e90b4a1d6f358","correlation_id":"b71e2c90d4a35f68e1c07a9b3d5f2e14","event":"outbox.delivery.started","message":"delivering event to consumer","duration_ms":0,"outbox_event_id":"f3a8c1d6-9e24-4b70-8c5f-2d7e1a0b9c63","event_type":"PasswordResetRequested","delivery_attempt":1,"target_service":"notifications-api"}
{"timestamp":"2026-10-20T15:12:10.221Z","level":"INFO","service":"notifications-api","version":"2.0.0","environment":"qa","trace_id":"4e0b9d27c1f8a635b2d7e94c0a1f5d38","span_id":"6f15d8a2c9e04b73","correlation_id":"b71e2c90d4a35f68e1c07a9b3d5f2e14","event":"password_reset.email.sent","message":"reset e-mail accepted by the SMTP server","duration_ms":3008,"user_id":"8d2f4a61-3b9c-4e07-a5d1-6c0e9f2b7a34","outbox_event_id":"f3a8c1d6-9e24-4b70-8c5f-2d7e1a0b9c63","target_service":"smtp"}
{"timestamp":"2026-10-20T15:12:10.250Z","level":"INFO","service":"barber-saas-worker","version":"2.0.0","environment":"qa","trace_id":"4e0b9d27c1f8a635b2d7e94c0a1f5d38","span_id":"2c7e90b4a1d6f358","correlation_id":"b71e2c90d4a35f68e1c07a9b3d5f2e14","event":"outbox.delivery.done","message":"consumer answered 200","duration_ms":3046,"consumer_outcome":"PROCESSED","outbox_event_id":"f3a8c1d6-9e24-4b70-8c5f-2d7e1a0b9c63","event_type":"PasswordResetRequested","delivery_attempt":1,"target_service":"notifications-api"}
```

(Timestamps are UTC: 15:12 UTC = 10:12 in Colombia.)

## What the SLIs reach during the 40 minutes

| SLI (`05-slo.md`) | Normal | During the incident | SLO broken? |
|---|---|---|---|
| SLO 1 availability (no 5xx on the reset) | 100 % | **100 %**: identity-auth-api is not in the slow path | no |
| SLO 2 latency (reset answered in 0.5 s or less) | 100 % | **100 %**: the `202` comes before the e-mail | no |
| SLO 3 freshness (oldest pending event under 60 s) | up to about 5 s (one poll) | **up to about 8 s** (5 s poll + 3 s) | no |
| p95 of `worker_outbox_delivery_duration_seconds` | under 0.1 s | **4.5 s** read from the histogram (75 % in `le=0.1`, 25 % between 2.5 and 5, interpolated); the real value is 3 s | no SLO on it |

**Which alert fires first:** **none.** `PasswordResetAvailabilityFastBurn` and `...SlowBurn` watch the
5xx ratio, which stays at 0 the whole 40 minutes. With about 10 resets a day, only
10 x 40 / 1,440 = **0.28 reset requests** happen in the window anyway.
**Which runbook step stops the damage:** none of `07-runbook.md`, because that runbook is for 5xx in
identity-auth-api. The slowness ends when the SMTP server recovers at minute 40. If it had gone over
5 s, the worker would time out and retry, notifications-api would answer `DUPLICATE` (DEC-NOTIF-01)
and the escalation row "e-mail side -> Carlos Leal, owner of notifications-api" would be the step.

## Blameless postmortem

**Timeline (2026-10-20, Colombia time)**

| Time | Minute | What happened |
|---|---|---|
| 10:00 | 0 | The SMTP server starts answering in 3 s for 25 % of the e-mails |
| 10:12 | 12 | One user asks for a reset code; the e-mail leaves after 6.1 s instead of about 2.5 s |
| 10:00-10:40 | 0-40 | Appointment notices from notifications-api are also 3 s slower for 1 in 4 |
| 10:40 | 40 | The SMTP server is back to about 50 ms; no alert fired, no person acted |
| 11:30 | 90 | Found in the drill review on the worker latency panel, not by an alert |

**Impact:** about **0.07** reset e-mails late by 3 s (0.28 requests x 25 %), **0 failed requests**,
**0 minutes** of error budget spent in SLO 1, 2 and 3. The code (15 minutes of life) was never at risk.

**Root cause:** the SMTP server answered slowly, and notifications-api sends the e-mail inside the
`POST /internal/v1/events` call, so the worker waits for SMTP on every delivery.

**Contributing factors**

- No alert watches delivery latency or the outbox age, only the 5xx ratio of identity-auth-api.
- Today the trace breaks at the worker (new `X-Correlation-Id` per run, `01-journey.md`): finding the
  slow hop would mean matching ids by hand across three services.
- notifications-api exposes no `/metrics` (`04-metrics.md`), so SMTP time is not visible at all.
- The real worker delivers events one after another; a slow consumer delays every producer it relays.

**Actions (user stories for the next sprint)**

1. **As** the on-call person, **I want** barber-saas-worker to send the `traceparent` stored with each
   outbox row on `POST /internal/v1/events`, **so that** one trace shows identity-auth-api, worker,
   notifications-api and SMTP.
   *Acceptance:* given an outbox row with a `traceparent`, when the worker delivers it, then
   notifications-api logs the same `trace_id`; `test_trace_id_received_equals_trace_id_sent` passes in
   barber-saas-worker.
2. **As** a user waiting for a reset code, **I want** an alert on the outbox age, **so that** a slow
   e-mail path is seen before the 15-minute code expires.
   *Acceptance:* `worker_outbox_oldest_pending_age_seconds` is exposed on `/metrics`; an alert fires
   when it is over 60 s for 5 minutes; `promtool test rules` proves it fires at 90 s and stays
   silent at 8 s.
3. **As** the owner of notifications-api, **I want** to expose `notifications_smtp_send_duration_seconds`,
   **so that** a slow SMTP server is visible on the dashboard.
   *Acceptance:* `GET /metrics` returns that histogram with the buckets of `04-metrics.md`
   (0.25 to 10 s); a test with a fake SMTP that waits 3 s puts the sample in the `le="5"` bucket.
