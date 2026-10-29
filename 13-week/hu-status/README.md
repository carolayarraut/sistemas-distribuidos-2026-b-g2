<!-- HU-STATUS TEMPLATE - do NOT remove the <!-- ... --> markers or the table headers.
     Your weekly grade is read AUTOMATICALLY from this file:
       13-week/hu-status/README.md  (inside YOUR fork). English. -->

# Weekly Status - Week 13

<!-- CONFIG-START - must match your profile repo (username/username) CONFIG -->
- FULL_NAME: Carolay Arraut Heredia
- GITHUB_USER: carolayarraut
- TEAM: BarberSaaS
- SPRINT_GOAL: Threat model of the boundary api-gateway → identity-auth-api and turn its threats into security stories and CI gates (week 13 workshop, delivery 1).
<!-- CONFIG-END -->

## 1. User stories worked this week
| HU ID | Title | Status (todo/doing/done) | Evidence (PR or commit URL) |
|---|---|---|---|
| W13-CP0 | Claim the boundary api-gateway → identity-auth-api | done | [#151](https://github.com/code-corhuila/barber-saas-docs/issues/151), [e1bd639](https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/commit/e1bd639c1cadec21d50f3266d438f7119c5d0307) |
| W13-CP1 | Attack surface map: data flow, trust boundaries, assets and entry points | done | [13d9cd4](https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/commit/13d9cd4632df12baeab16e18694317e9df796144) |
| W13-CP2 | STRIDE of my boundary with risk ranking and the library book | done | [PR #162](https://github.com/code-corhuila/barber-saas-docs/pull/162), [9ac1e85](https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/commit/9ac1e85c805e2aacb822d94159b3876d6b654824) |
| W13-CP3 | Three security stories in the team backlog | done | [#166](https://github.com/code-corhuila/barber-saas-docs/issues/166), [#167](https://github.com/code-corhuila/barber-saas-docs/issues/167), [#168](https://github.com/code-corhuila/barber-saas-docs/issues/168), [b1ab99c](https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/commit/b1ab99c914011ef0c7c0d98f01b19f0192c4fe9d) |
| W13-CP4 | Security gates and negative authorization test for POST /api/v1/auth/barbers | done | [8c94847](https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/commit/8c94847b40aab8bb26c6b621368e066b8883431c), [370ff89](https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/commit/370ff89afbefca9373f766ea3cdd92893d63dc18), [cd9475e](https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/commit/cd9475e656bccda3166498757bb299af45d2fafb) |
| W13-CP5 | Peer review of the STRIDE of TB1 (Daniel, PR #153) | done | https://github.com/code-corhuila/barber-saas-docs/pull/153#issuecomment-6506219701 |

## 2. My individual contribution
- Modeled the boundary where anonymous internet traffic reaches identity-auth-api: six STRIDE threats checked against the code (`Rs256Verifier`, `CorrelationFilter`, `AuthController`, the gateway route `identity-auth.conf`).
- Used the library book *La seguridad de la información* (Daltabuit Godás et al., Limusa 2007, 005.8 D147) for rows S, R, D and E and for the ranking.
- Wrote three stories (E role check, I account enumeration, R audit log), each one with an automated test as acceptance criterion.
- Proposed one workflow for identity-auth-api with gitleaks, OWASP dependency-check and a negative test: a `CLIENT` token on `POST /api/v1/auth/barbers` gets 403.
- Reviewed the PR of TB1 and found that the gateway reuses the client `X-Correlation-Id` inside the fixed error bodies.

## 3. Blockers and risks
- The negative test was not run yet: this week I had no Java 21 and Maven ready. It is checkpoint 8 of delivery 2.
- `security.yml` needs the `NVD_API_KEY` secret and team approval before it goes to the identity-auth-api repository.
- The team has no GitHub Project board, so the stories are only labeled (`security`, P1, P2).

## 4. Plan for next week
- Answer the review of PR #162 and finish the STRIDE (CP6), and refine my three stories (CP7).
- Run the negative test against identity-auth-api and record the output (CP8).
- Write the implementation plan in my reflection document and close the workshop (CP9).

## 5. Compliance self-check
- [x] Conventional Commits - `type(scope): summary`
- [x] Per-environment HU branch + PR to that environment - the STRIDE is on branch `security/stride-carolayarraut` with PR #162 to `main` of barber-saas-docs, not merged by me
- [x] Testable acceptance criteria - every story has an automated test as a criterion
- [x] Tests added/updated (unit / integration) - `CreateBarberAuthorizationTest` proposed for identity-auth-api
- [ ] DDD / hexagonal boundaries respected (domain has no I/O) - not applicable: no project code changed this week
- [x] No secrets; config via environment variables - the workflow reads `NVD_API_KEY` from the repository secrets

## 6. Evidence links
- Workshop folder: https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/tree/main/13-week/workshop
- STRIDE PR: https://github.com/code-corhuila/barber-saas-docs/pull/162
- Stories: https://github.com/code-corhuila/barber-saas-docs/issues/166, https://github.com/code-corhuila/barber-saas-docs/issues/167, https://github.com/code-corhuila/barber-saas-docs/issues/168
- Review comment: https://github.com/code-corhuila/barber-saas-docs/pull/153#issuecomment-6506219701
