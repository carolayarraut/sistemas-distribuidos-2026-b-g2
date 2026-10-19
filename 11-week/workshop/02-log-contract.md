# 02 - Structured log contract

Applies to every service of the journey in `01-journey.md`: identity-auth-api (Java, SLF4J + MDC),
barber-saas-worker (Python, `logging` + `json`) and notifications-api (Python, FastAPI).
One log line = one JSON object on stdout, UTF-8, no line breaks inside a value.

## Mandatory fields

| Field | Type | Required | Example | Why it exists |
|---|---|---|---|---|
| `timestamp` | string, ISO-8601 UTC with ms | yes | `2026-10-19T23:40:02.118Z` | order lines from three services on one timeline |
| `level` | enum `ERROR` `WARN` `INFO` `DEBUG` | yes | `WARN` | filter what needs a person |
| `service` | string | yes | `barber-saas-worker` | know which container wrote the line |
| `version` | string, semver | yes | `2.0.0` | tie an error to the release tag `v2.0.0` |
| `environment` | enum `dev` `qa` `main` | yes | `qa` | never mix test traffic with real traffic |
| `trace_id` | 32 hex chars | yes | `7d1c0e4b9a2f46c8b3e5a1d09f6b2c74` | join every line of one password reset request |
| `span_id` | 16 hex chars | yes | `a41f9c27e0b85d13` | know which hop of the trace wrote the line |
| `correlation_id` | string | yes | `5f3a9e0c71b24d68a2c4e9b1d7f03a65` | the `X-Correlation-Id` nginx already creates; kept while the team moves to `traceparent` |
| `event` | string, `noun.verb` in snake_case | yes | `outbox.delivery.timeout` | a fixed name to count and alert on, unlike `message` |
| `message` | string, English, no personal data | yes | `notifications-api did not answer in 5 s` | short text for a person |
| `duration_ms` | integer | yes (0 when nothing was measured) | `5003` | see slow hops without a tracing tool |

## Domain fields (password reset journey)

| Field | Type | Required | Example | Why it exists |
|---|---|---|---|---|
| `user_id` | UUID | when known | `3b8e2f61-0c4a-4d9e-9a71-5e2c8f04b1d3` | identify the account WITHOUT writing its e-mail |
| `outbox_event_id` | UUID | in relay lines | `c0f4a812-6e3b-4b57-8d29-7a1e5f90c3b6` | the `identity_auth.outbox_event.id`; also the id notifications-api stores in `processed_event` |
| `event_type` | string | in relay lines | `PasswordResetRequested` | the domain event being moved |
| `delivery_attempt` | integer | in worker lines | `2` | see retries (up to 8, 5 s doubling to 5 min) |
| `consumer_outcome` | enum `PROCESSED` `DUPLICATE` `IGNORED` | in delivery answers | `DUPLICATE` | the answer of `POST /internal/v1/events` |
| `http_status` | integer | in HTTP lines | `202` | spot 4xx (event failed at once) and 5xx (retried) |
| `target_service` | string | in outgoing calls | `notifications-api` | know which dependency failed |
| `email_domain` | string | only before the user is found | `gmail.com` | know which mail provider users have without logging the e-mail |

## Never log

| Data | Where it appears in this journey | Rule |
|---|---|---|
| e-mail address | body of `POST /api/v1/auth/password-reset`, `payload.email` | never; log `user_id` instead. Before the user is found, log `email_domain` only (`gmail.com`) |
| full name | `payload.fullName` | never |
| 6-digit reset code | `payload.code`, the e-mail body | never, not even masked: whoever reads it can change the password |
| code hash | `identity_auth.password_reset_token.code_hash` | never |
| new password | body of `POST /api/v1/auth/password-reset/confirm` | never |
| whole event envelope or payload | `outbox_event.payload`, body of `POST /internal/v1/events` | never dump it: in this event it holds the e-mail AND the plain code. Log `outbox_event_id` and `event_type` only |
| `Authorization` header (user RS256 token, worker service token) | every call | never; log `caller_role` if needed |
| SMTP user and password | notifications-api settings | never |
| client IP | nginx access log | last octet masked: `181.57.12.x` |

## Levels in BarberSaaS

| Level | When | Example from this journey |
|---|---|---|
| `ERROR` | a request or delivery failed and someone may have to act | the worker's call to notifications-api timed out (`outbox.delivery.timeout`) |
| `WARN` | something was refused or degraded, but the system handled it | notifications-api refused to send a code twice (`password_reset.email.rejected_duplicate`) |
| `INFO` | a normal business step finished | identity-auth-api saved the reset code and the outbox row (`password_reset.code.issued`) |
| `DEBUG` | details for a developer, off in `qa` and `main` | the worker fetched 3 pending rows from `GET /internal/v1/outbox-events` |

## Example: one trace, seven lines

Story: a user asks for a reset code. The SMTP server answers slowly (about 6 s), so the worker's
5 s HTTP timeout fires (failure 1, downstream timeout) even though the e-mail went out. On the
retry, notifications-api finds the event in `processed_event` and refuses to send the code a second
time (failure 2, business rule DEC-NOTIF-01: one code is e-mailed once).

```json
{"timestamp":"2026-10-19T23:40:02.118Z","level":"INFO","service":"identity-auth-api","version":"2.0.0","environment":"qa","trace_id":"7d1c0e4b9a2f46c8b3e5a1d09f6b2c74","span_id":"a41f9c27e0b85d13","correlation_id":"5f3a9e0c71b24d68a2c4e9b1d7f03a65","event":"password_reset.request.received","message":"password reset requested","duration_ms":0,"email_domain":"gmail.com"}
{"timestamp":"2026-10-19T23:40:02.164Z","level":"INFO","service":"identity-auth-api","version":"2.0.0","environment":"qa","trace_id":"7d1c0e4b9a2f46c8b3e5a1d09f6b2c74","span_id":"a41f9c27e0b85d13","correlation_id":"5f3a9e0c71b24d68a2c4e9b1d7f03a65","event":"password_reset.code.issued","message":"reset code and outbox row saved in one transaction","duration_ms":46,"user_id":"3b8e2f61-0c4a-4d9e-9a71-5e2c8f04b1d3","outbox_event_id":"c0f4a812-6e3b-4b57-8d29-7a1e5f90c3b6","event_type":"PasswordResetRequested","http_status":202}
{"timestamp":"2026-10-19T23:40:06.502Z","level":"INFO","service":"barber-saas-worker","version":"2.0.0","environment":"qa","trace_id":"7d1c0e4b9a2f46c8b3e5a1d09f6b2c74","span_id":"5e92b0d4c8a17f36","correlation_id":"5f3a9e0c71b24d68a2c4e9b1d7f03a65","event":"outbox.delivery.started","message":"delivering event to consumer","duration_ms":0,"outbox_event_id":"c0f4a812-6e3b-4b57-8d29-7a1e5f90c3b6","event_type":"PasswordResetRequested","delivery_attempt":1,"target_service":"notifications-api"}
{"timestamp":"2026-10-19T23:40:11.505Z","level":"ERROR","service":"barber-saas-worker","version":"2.0.0","environment":"qa","trace_id":"7d1c0e4b9a2f46c8b3e5a1d09f6b2c74","span_id":"5e92b0d4c8a17f36","correlation_id":"5f3a9e0c71b24d68a2c4e9b1d7f03a65","event":"outbox.delivery.timeout","message":"notifications-api did not answer in 5 s, retry scheduled","duration_ms":5003,"outbox_event_id":"c0f4a812-6e3b-4b57-8d29-7a1e5f90c3b6","event_type":"PasswordResetRequested","delivery_attempt":1,"target_service":"notifications-api"}
{"timestamp":"2026-10-19T23:40:12.731Z","level":"INFO","service":"notifications-api","version":"2.0.0","environment":"qa","trace_id":"7d1c0e4b9a2f46c8b3e5a1d09f6b2c74","span_id":"e7b36a09f2d4c518","correlation_id":"5f3a9e0c71b24d68a2c4e9b1d7f03a65","event":"password_reset.email.sent","message":"reset e-mail accepted by the SMTP server","duration_ms":6198,"user_id":"3b8e2f61-0c4a-4d9e-9a71-5e2c8f04b1d3","outbox_event_id":"c0f4a812-6e3b-4b57-8d29-7a1e5f90c3b6","target_service":"smtp"}
{"timestamp":"2026-10-19T23:40:16.540Z","level":"WARN","service":"notifications-api","version":"2.0.0","environment":"qa","trace_id":"7d1c0e4b9a2f46c8b3e5a1d09f6b2c74","span_id":"0d58f1c3b9e26a47","correlation_id":"5f3a9e0c71b24d68a2c4e9b1d7f03a65","event":"password_reset.email.rejected_duplicate","message":"event already in processed_event, code not sent again (DEC-NOTIF-01)","duration_ms":12,"outbox_event_id":"c0f4a812-6e3b-4b57-8d29-7a1e5f90c3b6","consumer_outcome":"DUPLICATE","http_status":200}
{"timestamp":"2026-10-19T23:40:16.587Z","level":"INFO","service":"barber-saas-worker","version":"2.0.0","environment":"qa","trace_id":"7d1c0e4b9a2f46c8b3e5a1d09f6b2c74","span_id":"9c2a47e1d0b3f856","correlation_id":"5f3a9e0c71b24d68a2c4e9b1d7f03a65","event":"outbox.event.published","message":"consumer answered, outbox row marked published","duration_ms":47,"outbox_event_id":"c0f4a812-6e3b-4b57-8d29-7a1e5f90c3b6","event_type":"PasswordResetRequested","delivery_attempt":2,"consumer_outcome":"DUPLICATE","target_service":"identity-auth-api"}
```

Reading the seven lines filtered by `trace_id` tells the whole story: request accepted (1-2),
first delivery timed out (3-4), the e-mail did leave (5), the retry was refused as a duplicate (6)
and the outbox row was closed (7). No line holds the e-mail, the name or the code.
