<!-- HU-STATUS TEMPLATE - do NOT remove the <!-- ... --> markers or the table headers.
     Your weekly grade is read AUTOMATICALLY from this file:
       11-week/hu-status/README.md  (inside YOUR fork). English. -->

# Weekly Status - Week 11

<!-- CONFIG-START - must match your profile repo (username/username) CONFIG -->
- FULL_NAME: Carolay Arraut Heredia
- GITHUB_USER: carolayarraut
- TEAM: BarberSaaS
- SPRINT_GOAL: Make the password reset journey of BarberSaaS (identity-auth-api -> barber-saas-worker -> notifications-api) observable end to end: trace map, log contract, instrumentation code with a test, and a metric catalog (delivery 1), then protect it with SLOs, burn-rate alerts, a runbook and an incident drill (delivery 2).
<!-- CONFIG-END -->

## 1. User stories worked this week
| HU ID | Title | Status (todo/doing/done) | Evidence (PR or commit URL) |
|---|---|---|---|
| W11-PRES | BarberSaaS project presentation in class | done | [barber-saas-docs v2.0.0](https://github.com/code-corhuila/barber-saas-docs/releases/tag/v2.0.0) |
| W11-CP0 | Start observability workshop (config + reflection doc) | done | [9b8f13f](https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/commit/9b8f13f4e47372cfc8a2296fdd4cef70543028ae) |
| W11-CP1 | Critical journey and trace map: password reset request | done | [76589d7](https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/commit/76589d77071aae4765eedd83275d15eda2944c3c), [8cb12f4](https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/commit/8cb12f4adf16995a32a2d409d8b8192e822b0abf) |
| W11-CP2 | Structured log contract | done | [e6d878b](https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/commit/e6d878b61d2318e3474bde6a608f9a842181ad9d) |
| W11-CP3 | barber-saas-worker instrumentation: trace context, JSON logger, metrics and test | done | [81800d7](https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/commit/81800d7eec00a33b9fa6c6cb32a1820691cf3531), [f0abf2a](https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/commit/f0abf2a4cb80b9214436bd69990be60362775ec5), [a922982](https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/commit/a922982bffc7d98b11748f741fbbeae93d44cdeb), [e573901](https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/commit/e573901dffc6abcc2fca8041b7e545c75af3e5db) |
| W11-CP4 | Golden signals and metric catalog | done | [4e58b1e](https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/commit/4e58b1e33e7613dd4c89873ceb3a4edbab4290bc) |
| W11-CP6 | SLOs and error budget for the password reset journey | done | [d283613](https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/commit/d28361387e8de0afeff7af6862539fc3a20a0bac) |
| W11-CP7 | Burn-rate alerting rules and alert policy | done | [c7b55db](https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/commit/c7b55dbed020c0bd8a985d4d6be1e6eb96adc3e5) |
| W11-CP8 | Runbook for the fast-burn alert | done | [21103e1](https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/commit/21103e13565803b27b83b27e08412196a94512f8) |
| W11-CP9 | Incident drill and blameless postmortem | done | [b6245ac](https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/commit/b6245ac28ba4dddebf3310e94174aa87235cfd3f) |
| W11-CP10 | Implementation plan (reflection doc) and this status update | done | this commit |

## 2. My individual contribution
- Presented the BarberSaaS project in class with my team.
- Chose the password reset journey (`POST /api/v1/auth/password-reset` -> `identity_auth.outbox_event` -> barber-saas-worker -> `POST /internal/v1/events` on notifications-api -> SMTP), different from my teammates' journeys.
- Found in the v2.0.0 code that the trace breaks in barber-saas-worker: it sends a new `X-Correlation-Id` on every run instead of the one stored in the outbox row.
- Defined a JSON log contract with a "never log" list for this journey: the `PasswordResetRequested` payload carries the e-mail and the plain 6-digit code.
- Wrote and ran (Python 3.15, Windows) a minimal barber-saas-worker module that continues the stored `traceparent`, logs in the CP2 format and exposes a counter and a histogram on `/metrics`; 6 tests pass.
- Defined the golden signals for identity-auth-api, barber-saas-worker and notifications-api, with bounded labels and buckets based on the 5 s worker and 10 s SMTP timeouts.
- Set three SLOs (availability 99.5 %, latency 95 % under 0.5 s, e-mail freshness under 60 s) from the team's NFR-001 and NFR-002 and an estimate of about 10 resets a day.
- Wrote two multi-window burn-rate alerts (14.4 and 6), checked with `promtool check rules` and a `promtool test rules` case.
- Wrote the runbook for the fast alert, extending the identity-auth runbook I wrote in barber-saas-docs, with only the mitigations our architecture supports (scale, restart, roll back).
- Ran an incident drill (SMTP slow for 25 % of e-mails, 40 min): no SLO broke and no alert fired; the postmortem turned the gaps into three user stories.

## 3. Blockers and risks
- Delivery 1 was pushed after the in-class window (08:40-10:20); I am reporting it to the teacher.
- The drill showed that our alerts only see 5xx: a slow e-mail path is invisible until the outbox-age alert exists.
- identity-auth-api has no Actuator or Micrometer dependency and notifications-api has no `/metrics` endpoint, so their metrics are still a proposal.
- The real barber-saas-worker is maintained by another teammate; storing and reusing `traceparent` needs a change agreed in identity-auth-api (outbox column) and in the worker.

## 4. Plan for next week
- Propose to the team the three user stories of `08-incident.md`: forward `traceparent` from the outbox in the worker, an outbox-age alert, and SMTP metrics in notifications-api.
- Load `06-alerts.yml` into the Prometheus of the `observability` profile of barber-saas-infra-postgres.
- Update the identity-auth runbook in barber-saas-docs with the fast-burn steps of `07-runbook.md`.

## 5. Compliance self-check
- [x] Conventional Commits - `type(scope): summary`
- [ ] Per-environment HU branch + PR to that environment (hu-xxx-dev -> develop, ...) - not applicable: the workshop asks for direct commits and pushes on the fork, one per checkpoint
- [x] Testable acceptance criteria - CP3 test, and the three user stories of `08-incident.md` with verifiable criteria
- [x] Tests added/updated (unit / integration) - `test_trace_propagation.py`, 6 tests
- [ ] DDD / hexagonal boundaries respected (domain has no I/O) - not applicable to this workshop module
- [x] No secrets; config via environment variables - `APP_VERSION` and `APP_ENV`; no tokens or passwords in code or logs

## 6. Evidence links
- Workshop folder: https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/tree/main/11-week/workshop
- Instrumentation code: https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/tree/main/11-week/workshop/03-instrumentation
- Alert rules: https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/blob/main/11-week/workshop/06-alerts.yml
- Runbook: https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/blob/main/11-week/workshop/07-runbook.md
- Incident drill and postmortem: https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/blob/main/11-week/workshop/08-incident.md
- Team docs repository: https://github.com/code-corhuila/barber-saas-docs
