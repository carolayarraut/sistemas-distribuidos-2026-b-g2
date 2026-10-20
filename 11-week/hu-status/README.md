<!-- HU-STATUS TEMPLATE - do NOT remove the <!-- ... --> markers or the table headers.
     Your weekly grade is read AUTOMATICALLY from this file:
       11-week/hu-status/README.md  (inside YOUR fork). English. -->

# Weekly Status - Week 11
 
<!-- CONFIG-START - must match your profile repo (username/username) CONFIG -->
- FULL_NAME: Carolay Arraut Heredia
- GITHUB_USER: carolayarraut
- TEAM: BarberSaaS
- SPRINT_GOAL: Make the password reset journey of BarberSaaS (identity-auth-api -> barber-saas-worker -> notifications-api) observable end to end: trace map, log contract, instrumentation code with a test, and a metric catalog (week 11 workshop, delivery 1).
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
| W11-CP6..CP10 | SLOs, burn-rate alerts, runbook, incident drill, implementation plan | todo | delivery 2 (due 2026-10-20 23:59) |
 
## 2. My individual contribution
- Presented the BarberSaaS project in class with my team.
- Chose the password reset journey (`POST /api/v1/auth/password-reset` -> `identity_auth.outbox_event` -> barber-saas-worker -> `POST /internal/v1/events` on notifications-api -> SMTP), different from my teammates' journeys.
- Found in the v2.0.0 code that the trace breaks in barber-saas-worker: it sends a new `X-Correlation-Id` on every run instead of the one stored in the outbox row.
- Defined a JSON log contract with a "never log" list for this journey: the `PasswordResetRequested` payload carries the e-mail and the plain 6-digit code.
- Wrote and ran (Python 3.15, Windows) a minimal barber-saas-worker module that continues the stored `traceparent`, logs in the CP2 format and exposes a counter and a histogram on `/metrics`; 6 tests pass.
- Defined the golden signals for identity-auth-api, barber-saas-worker and notifications-api, with bounded labels and buckets based on the 5 s worker and 10 s SMTP timeouts.
  
## 3. Blockers and risks
- Delivery 1 was pushed after the in-class window (08:40-10:20); I am reporting it to the teacher.
- identity-auth-api has no Actuator or Micrometer dependency and notifications-api has no `/metrics` endpoint, so their metrics are still a proposal.
- The real barber-saas-worker is maintained by another teammate; storing and reusing `traceparent` needs a change agreed in identity-auth-api (outbox column) and in the worker.
  
## 4. Plan for next week
- Delivery 2: SLOs and error budget (CP6), burn-rate alerts (CP7), runbook (CP8), incident drill and blameless postmortem (CP9), implementation plan (CP10).
- Propose to the team a user story to store `traceparent` with each outbox row and forward it in the worker.
  
## 5. Compliance self-check
- [x] Conventional Commits - `type(scope): summary`
- [ ] Per-environment HU branch + PR to that environment (hu-xxx-dev -> develop, ...) - not applicable: the workshop asks for direct commits and pushes on the fork, one per checkpoint
- [x] Testable acceptance criteria - CP3 "done when": the test passes and the logs follow the CP2 contract
- [x] Tests added/updated (unit / integration) - `test_trace_propagation.py`, 6 tests
- [ ] DDD / hexagonal boundaries respected (domain has no I/O) - not applicable to this workshop module
- [x] No secrets; config via environment variables - `APP_VERSION` and `APP_ENV`; no tokens or passwords in code or logs
      
## 6. Evidence links
- Workshop folder: https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/tree/main/11-week/workshop
- Instrumentation code: https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/tree/main/11-week/workshop/03-instrumentation
- Team docs repository: https://github.com/code-corhuila/barber-saas-docs
