# 06 - Alert policy: password reset availability

Rules: `06-alerts.yml`. They alert on **how fast the error budget burns**, not on CPU or restarts.
SLO protected: SLO 1 of `05-slo.md`, 99.5 % of `POST /api/v1/auth/password-reset` without 5xx in
30 days. Error budget: **0.5 %** = **216 minutes** or about **1.5 failed requests** in 30 days.

Burn rate = observed error ratio / 0.005. A burn rate of 1 spends the whole budget in exactly 30 days.

## The two alerts with our numbers

| | Fast burn | Slow burn |
|---|---|---|
| Alert | `PasswordResetAvailabilityFastBurn` | `PasswordResetAvailabilitySlowBurn` |
| Burn rate | 14.4 | 6 |
| Error ratio that fires it | 14.4 x 0.5 % = **7.2 %** of 5xx | 6 x 0.5 % = **3 %** of 5xx |
| Long window / confirmation window | 1 h / 5 min | 6 h / 30 min |
| Budget spent before it fires | 14.4 x 1 h / 720 h = **2 %** | 6 x 6 h / 720 h = **5 %** |
| Same, in minutes of our 216 | 2 % x 216 = **4.3 min** | 5 % x 216 = **10.8 min** |
| Same, in requests of our 1.5 | 2 % x 1.5 = **0.03 requests** | 5 % x 1.5 = **0.075 requests** |
| Time to spend the whole budget if nobody acts | 720 h / 14.4 = **50 h (about 2 days)** | 720 h / 6 = **120 h (5 days)** |
| Severity / who gets it | `page`: the on-call person of the week, at any hour (see `07-runbook.md`) | `ticket`: an issue in barber-saas-identity-auth-api, handled in working hours |

The confirmation window stops an alert from staying on after the problem is fixed: both windows
must be above the threshold at the same time.

## What low traffic means for these alerts

With about 10 reset requests a day (0.4 per hour), **one** 5xx inside an hour already gives an error
ratio far above 7.2 %, so a single failure can fire the fast alert. We keep it that way on purpose:
in `05-slo.md` one failed request costs about two thirds of the monthly budget, so it deserves a
person. When there are no requests at all the ratio is 0/0 (no data) and nothing fires, so quiet
nights do not wake anyone.

Next step to make the alerts less sensitive to a single request: a synthetic probe that calls the
endpoint every minute with a test account and gives the SLI a steady base of traffic.

## Alerts on causes that we leave out

| Alert we skip | Why |
|---|---|
| "identity-auth-api CPU above 80 %" | High CPU does not mean users fail: the JVM can be busy and still answer `202`. If it ever hurts users, the 5xx ratio rises and the burn-rate alert fires. A CPU alert would wake people for nothing. |
| "barber-saas-worker container restarted" | Delivery is at-least-once: while the worker restarts, `PasswordResetRequested` waits in `identity_auth.outbox_event` and is sent when it comes back. A short restart is invisible to the user; a long one is caught by the freshness SLO (SLO 3), whose alert we add when `worker_outbox_oldest_pending_age_seconds` exists. |

## How the rules were checked

`promtool check rules 06-alerts.yml` (Prometheus 3.7.2): `SUCCESS: 6 rules found`. A `promtool test
rules` case with 10 % of 5xx for 70 minutes fires `PasswordResetAvailabilityFastBurn`, as expected.
