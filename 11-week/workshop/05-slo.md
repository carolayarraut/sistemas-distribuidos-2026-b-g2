# 05 - SLOs and error budget: password reset journey

Window for every SLO: **30 rolling days** (43,200 minutes). The metrics come from `04-metrics.md`.
Team targets used as a reference: `04-requirements/non-functional.md` in barber-saas-docs
(NFR-001: p95 < 300 ms on critical endpoints and < 1000 ms on the rest; NFR-002: 99.9 % monthly
availability in production). All are marked there as "not yet measured"; these SLOs are the first
way to measure them for this journey.

## SLO 1 - Availability of the reset request

| Item | Value |
|---|---|
| SLI | good requests / valid requests for `POST /api/v1/auth/password-reset` |
| Good | any answer that is not 5xx (`202 Accepted`, and `400` for a malformed body, which is the client's fault) |
| Valid | every request that reached identity-auth-api |
| Target | **99.5 %** in 30 days |

```promql
sum(rate(identity_http_requests_total{route="/api/v1/auth/password-reset",status_class!="5xx"}[30d]))
/
sum(rate(identity_http_requests_total{route="/api/v1/auth/password-reset"}[30d]))
```

Why 99.5 % and not the 99.9 % of NFR-002: with our traffic (see below) one single failed request
in a month already costs 0.33 %, so 99.9 % could never be met or measured with meaning. 99.9 % stays
as the uptime goal of the whole platform.

## SLO 2 - Latency of the reset request

| Item | Value |
|---|---|
| SLI | requests answered in 0.5 s or less / all requests to `POST /api/v1/auth/password-reset` |
| Target | **95 %** of requests in 0.5 s or less, in 30 days |

```promql
sum(rate(identity_http_request_duration_seconds_bucket{route="/api/v1/auth/password-reset",le="0.5"}[30d]))
/
sum(rate(identity_http_request_duration_seconds_count{route="/api/v1/auth/password-reset"}[30d]))
```

NFR-001 does not list the reset among its critical endpoints (it lists booking and `POST /api/auth/login`),
so its target is p95 < 1000 ms. We hold it to 0.5 s, a bucket of `04-metrics.md`, because it is
the way back into login: a user who cannot log in cannot book.

## SLO 3 - The reset e-mail leaves on time (freshness)

The user does not care about the `202`: they wait for the code on their phone, and the code dies
after 15 minutes (`PasswordResetService.LIFETIME`). So the product SLO is about the outbox.

| Item | Value |
|---|---|
| SLI | minutes in which the oldest pending `PasswordResetRequested` in `identity_auth.outbox_event` is younger than 60 s / all minutes |
| Target | **99 %** of the minutes in 30 days |

```promql
avg_over_time(
  (max(worker_outbox_oldest_pending_age_seconds{producer="identity-auth-api"}) < bool 60)[30d:1m]
)
```

60 s leaves 14 of the 15 minutes of the code for the user. The worker polls every 5 s and retries
up to 8 times, so a normal delivery takes seconds, not minutes.

## Traffic estimate

| Step | Number | Reason |
|---|---|---|
| Registered users | 5,000 | NFR-001 says no load figure has been agreed yet, so we estimate: 40 barbershops in the region x (1 owner + 3 barbers + about 120 clients) |
| Users who forget the password per month | 6 % | users log in a few times a month to book; many save the password in the phone |
| Reset requests per month | 5,000 x 0.06 = **300** | about **10 per day** |
| E-mails per month | 300 | one `PasswordResetRequested` per accepted request of an existing account (an unknown e-mail produces no event) |

## Error budget

| SLO | Budget in requests (30 days) | Budget in minutes (30 days) |
|---|---|---|
| Availability 99.5 % | 0.5 % x 300 = **1.5 failed requests** (1 in practice) | 0.5 % x 43,200 = **216 min** of total outage |
| Latency 95 % | 5 % x 300 = **15 slow requests** | 5 % x 43,200 = **2,160 min** with every request slow |
| Freshness 99 % | 1 % x 300 = **3 e-mails** that leave late (if they are spread out) | 1 % x 43,200 = **432 min** with the outbox stuck |

What these numbers tell the team: with 10 requests a day, **one** failed request uses about two
thirds of the monthly availability budget. A failure in this journey is rare but expensive, and
alerts will need a minimum of traffic to avoid firing on a single request (CP7).

## Error budget policy

It extends the team rule already written in NFR-002 (freeze feature deploys when more than 50 % of
the budget is used in the first half of the month) with the 50 / 75 / 100 % steps below.

| Budget used | Team action |
|---|---|
| **50 %** | Warning in the team channel. The owner of the failing service (identity-auth-api, barber-saas-worker or notifications-api) opens an issue with the trace ids of the failed requests. Features continue. |
| **75 %** | Only low-risk changes to the services of this journey; every pull request to them needs two reviews and a passing test. The next sprint planning reserves at least one user story for reliability. |
| **100 %** | Freeze of new features in identity-auth-api, barber-saas-worker and notifications-api until the budget recovers in the 30-day window. Only fixes, rollbacks and observability work are merged. A blameless postmortem is required (see `08-incident.md`). |
