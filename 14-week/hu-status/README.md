<!-- HU-STATUS TEMPLATE - do NOT remove the <!-- ... --> markers or the table headers.
     Your weekly grade is read AUTOMATICALLY from this file:
       14-week/hu-status/README.md  (inside YOUR fork). English. -->

# Weekly Status - Week 14

<!-- CONFIG-START - must match your profile repo (username/username) CONFIG -->
- FULL_NAME: Carolay Arraut Heredia
- GITHUB_USER: carolayarraut
- TEAM: BarberSaaS
- SPRINT_GOAL: Defend in Moodle the week 11 observability workshop and the week 13 threat model, follow up the security stories in the team backlog and advance the corte 3 certification.
<!-- CONFIG-END -->

## 1. User stories worked this week
| HU ID | Title | Status (todo/doing/done) | Evidence (PR or commit URL) |
|---|---|---|---|
| W11-DEF | Defense in Moodle of the week 11 observability workshop (password reset journey: SLO, alerts, runbook, incident) | done | [432de98](https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/commit/432de986e43914f48d0cdbba922fe696facfa5a7), [b6245ac](https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/commit/b6245ac28ba4dddebf3310e94174aa87235cfd3f), [c7b55db](https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/commit/c7b55dbed020c0bd8a985d4d6be1e6eb96adc3e5) |
| W13-DEF | Defense in Moodle of the week 13 threat model of the boundary api-gateway → identity-auth-api | done | [PR #162](https://github.com/code-corhuila/barber-saas-docs/pull/162), [ff320aa](https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/commit/ff320aac62e48d0f9d7e893d2b6f06defae9d296), [3fc386e](https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/commit/3fc386edde6b43c7decf2fadd8ea3a7f53181c0a) |
| SEC-BACKLOG | Follow up the three security stories from my STRIDE (#167 closed, #166 and #168 open) | doing | [#166](https://github.com/code-corhuila/barber-saas-docs/issues/166), [#167](https://github.com/code-corhuila/barber-saas-docs/issues/167), [#168](https://github.com/code-corhuila/barber-saas-docs/issues/168) |
| C3-CERT | Corte 3 certification: HCCDP-Solution Architectures, chapters 1 to 5 | doing | [c7a8db3](https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/commit/c7a8db39bc1dcf64f8553de0a557c1d63a14e129), [3184db2](https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/commit/3184db2468565768afbc0294abfed493443d1903) |

## 2. My individual contribution
- Defended in Moodle the week 11 workshop (commits from October 19 to 20): the password reset journey, its log contract, metrics, SLO, burn-rate alerts, runbook and the incident drill.
- Defended in Moodle the week 13 workshop (commits from October 29 to 30): the six STRIDE threats of the boundary api-gateway → identity-auth-api, the risk ranking with the library book and how the negative test proves story #166.
- Followed up the security backlog: story #167 (account enumeration) is closed; #166 (role check) and #168 (audit log) remain open.
- Completed chapters 1 to 5 of the HCCDP-Solution Architectures course (design principles, typical service solutions, compute, storage and network design on Huawei Cloud), with dated evidence and a study log in `certification/`.

## 3. Blockers and risks
- Story #166 is still open: `CreateBarberAuthorizationTest` and `security.yml` are in my fork and still have to reach identity-auth-api through a PR reviewed by the owner of the service.
- Story #168 is still open and has no owner yet.
- The certification is behind the suggested pace: chapters 6 to 14, four labs, the final exam and the design note remain for the last week.

## 4. Plan for next week
- Finish chapters 6 to 14, the four online labs and the final exam of the certification.
- Write the architecture design note and the two ADRs for BarberSaaS on Huawei Cloud.
- Propose `CreateBarberAuthorizationTest` and `security.yml` to identity-auth-api to move story #166 forward.

## 5. Compliance self-check
- [x] Conventional Commits - `type(scope): summary`
- [ ] Per-environment HU branch + PR to that environment (hu-xxx-dev -> develop, ...) - not applicable: no new branch or PR this week
- [x] Testable acceptance criteria - every security story has an automated test as its criterion
- [ ] Tests added/updated (unit / integration) - not applicable: no project code changed this week
- [ ] DDD / hexagonal boundaries respected (domain has no I/O) - not applicable: no domain code changed this week
- [x] No secrets; config via environment variables

## 6. Evidence links
- Week 11 workshop: https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/tree/main/11-week/workshop
- Week 13 workshop: https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/tree/main/13-week/workshop
- STRIDE PR: https://github.com/code-corhuila/barber-saas-docs/pull/162
- Security stories: https://github.com/code-corhuila/barber-saas-docs/issues/166, https://github.com/code-corhuila/barber-saas-docs/issues/167, https://github.com/code-corhuila/barber-saas-docs/issues/168
- Certification folder: https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/tree/main/certification
