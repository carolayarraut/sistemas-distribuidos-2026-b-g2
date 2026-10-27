<!-- HU-STATUS TEMPLATE - do NOT remove the <!-- ... --> markers or the table headers.
     Your weekly grade is read AUTOMATICALLY from this file:
       12-week/hu-status/README.md  (inside YOUR fork). English. -->

# Weekly Status - Week 12

<!-- CONFIG-START - must match your profile repo (username/username) CONFIG -->
- FULL_NAME: Carolay Arraut Heredia
- GITHUB_USER: carolayarraut
- TEAM: BarberSaaS
- SPRINT_GOAL: Finish the week 11 observability workshop on the BarberSaaS password reset journey (delivery 2).
<!-- CONFIG-END -->

## 1. User stories worked this week
| HU ID | Title | Status (todo/doing/done) | Evidence (PR or commit URL) |
|---|---|---|---|
| W11-D2 | Observability workshop, delivery 2: SLOs, burn-rate alerts, runbook, incident drill and implementation plan (2026-10-19 and 2026-10-20) | done | [d283613](https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/commit/d28361387e8de0afeff7af6862539fc3a20a0bac), [c7b55db](https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/commit/c7b55dbed020c0bd8a985d4d6be1e6eb96adc3e5), [21103e1](https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/commit/21103e13565803b27b83b27e08412196a94512f8), [b6245ac](https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/commit/b6245ac28ba4dddebf3310e94174aa87235cfd3f), [5a17000](https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/commit/5a17000697e7901dc01466a8f7f74f800a3af4ac) |
| W11-INDEX | Checkpoint index in the workshop README | done | [432de98](https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/commit/432de986e43914f48d0cdbba922fe696facfa5a7) |

## 2. My individual contribution
- Finished delivery 2 of the workshop on 2026-10-20: three SLOs, two multi-window burn-rate alerts checked with `promtool`, a runbook for the fast alert, an incident drill with a blameless postmortem, and the implementation plan in my reflection document.

## 3. Blockers and risks
- No commits to the BarberSaaS repositories this week: the time went to the workshop.
- Delivery 1 of the workshop was pushed after the in-class window.
- The improvements of my postmortem need changes in identity-auth-api and barber-saas-worker, which other teammates own.

## 4. Plan for next week
- Fill the corte 3 certification templates (`certification/`) synced from the course repository.
- Propose to the team the user story to store `traceparent` in `identity_auth.outbox_event` and forward it in the worker.
- Add the fast-burn steps of my workshop runbook to the identity-auth runbook in barber-saas-docs.

## 5. Compliance self-check
- [x] Conventional Commits - `type(scope): summary`
- [ ] Per-environment HU branch + PR to that environment (hu-xxx-dev -> develop, ...) - not applicable: no project changes this week; the workshop used direct pushes on the fork
- [x] Testable acceptance criteria - the user stories of `08-incident.md` have verifiable criteria
- [ ] Tests added/updated (unit / integration) - not this week (the workshop tests were added in week 11)
- [ ] DDD / hexagonal boundaries respected (domain has no I/O) - not applicable this week
- [x] No secrets; config via environment variables - no secrets in any file or log example

## 6. Evidence links
- Workshop folder: https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/tree/main/11-week/workshop
- Week 11 status (delivery 2): https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/blob/main/11-week/hu-status/README.md
