<!-- HU-STATUS TEMPLATE - do NOT remove the <!-- ... --> markers or the table headers.
     Your weekly grade is read AUTOMATICALLY from this file:
       13-week/hu-status/README.md  (inside YOUR fork). English. -->

# Weekly Status - Week 13

<!-- CONFIG-START - must match your profile repo (username/username) CONFIG -->
- FULL_NAME: Carolay Arraut Heredia
- GITHUB_USER: carolayarraut
- TEAM: BarberSaaS
- SPRINT_GOAL: Threat model of the boundary api-gateway → identity-auth-api and turn its threats into security stories and CI gates (week 13 workshop, deliveries 1 and 2).
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
| W13-CP6 | Answer the review of PR #162 and finish the STRIDE (row T, Backlog section) | done | [11280a9](https://github.com/code-corhuila/barber-saas-docs/commit/11280a9c3db646aac58226c594097c8e3136131f), [PR #162](https://github.com/code-corhuila/barber-saas-docs/pull/162) |
| W13-CP7 | Refine the security backlog: link #166 with #156 and #167 with #155 | done | [e9ebae8](https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/commit/e9ebae88344e59488d67e50fe71ca6cfe691bede) |
| W13-CP8 | Run the negative test against identity-auth-api and validate security.yml | done | [3fc386e](https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/commit/3fc386edde6b43c7decf2fadd8ea3a7f53181c0a) |
| W13-CP9 | Implementation plan in my reflection document and close the workshop | done | this commit |

## 2. My individual contribution
- Modeled the boundary where anonymous internet traffic reaches identity-auth-api: six STRIDE threats checked against the code (`Rs256Verifier`, `CorrelationFilter`, `AuthController`, the gateway route `identity-auth.conf`).
- Used the library book *La seguridad de la información* (Daltabuit Godás et al., Limusa 2007, 005.8 D147) for rows S, R, D and E and for the ranking.
- Wrote three stories (E role check, I account enumeration, R audit log), each one with an automated test as acceptance criterion.
- Proposed one workflow for identity-auth-api with gitleaks, OWASP dependency-check and a negative test: a `CLIENT` token on `POST /api/v1/auth/barbers` gets 403.
- Reviewed the PR of TB1 and found that the gateway reuses the client `X-Correlation-Id` inside the fixed error bodies.
- Answered the review of my PR: added the token signed with another RSA key to row T and a Backlog section that links every row to its story.
- Ran `CreateBarberAuthorizationTest` in a GitHub Codespace against `develop` of identity-auth-api: 2 tests, 0 failures, `BUILD SUCCESS`. Validated `security.yml` with actionlint 1.7.12: no errors.
- Wrote the implementation plan: #166 first (next sprint, with `security.yml`), then #167 and #168.

## 3. Blockers and risks
- The test passes on the service, but it is still in my fork: it has to be added to identity-auth-api by a PR reviewed by the owner of the service.
- `security.yml` needs the `NVD_API_KEY` secret and team approval before it goes to the identity-auth-api repository.
- The team has no GitHub Project board, so the stories are only labeled (`security`, P1, P2).

## 4. Plan for next week
- Propose `CreateBarberAuthorizationTest` and `security.yml` to the identity-auth-api repository (story #166).
- Prepare the defense of the workshop: my STRIDE rows, the book pages and how the negative test proves #166.
- Continue the corte 3 certification.

## 5. Compliance self-check
- [x] Conventional Commits - `type(scope): summary`
- [x] Per-environment HU branch + PR to that environment - the STRIDE is on branch `security/stride-carolayarraut` with PR #162 to `main` of barber-saas-docs, not merged by me
- [x] Testable acceptance criteria - every story has an automated test as a criterion
- [x] Tests added/updated (unit / integration) - `CreateBarberAuthorizationTest` ran against identity-auth-api: 2 tests, 0 failures
- [ ] DDD / hexagonal boundaries respected (domain has no I/O) - not applicable: no project code changed this week
- [x] No secrets; config via environment variables - the workflow reads `NVD_API_KEY` from the repository secrets

## 6. Evidence links
- Workshop folder: https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/tree/main/13-week/workshop
- STRIDE PR: https://github.com/code-corhuila/barber-saas-docs/pull/162
- Stories: https://github.com/code-corhuila/barber-saas-docs/issues/166, https://github.com/code-corhuila/barber-saas-docs/issues/167, https://github.com/code-corhuila/barber-saas-docs/issues/168
- Review comment: https://github.com/code-corhuila/barber-saas-docs/pull/153#issuecomment-6506219701
- Reflection document: https://docs.google.com/document/d/1tzMX0GS2tkiVWxS3hQO_o9DJGQ7RqmXCDz_-gf-36eQ/edit?usp=sharing
