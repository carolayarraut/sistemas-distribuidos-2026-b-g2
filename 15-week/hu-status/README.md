<!-- HU-STATUS TEMPLATE - do NOT remove the <!-- ... --> markers or the table headers.
     Your weekly grade is read AUTOMATICALLY from this file:
       15-week/hu-status/README.md  (inside YOUR fork). English. -->

# Weekly Status - Week 15

<!-- CONFIG-START - must match your profile repo (username/username) CONFIG -->
- FULL_NAME: Carolay Arraut Heredia
- GITHUB_USER: carolayarraut
- TEAM: BarberSaaS
- SPRINT_GOAL: Defend the BarberSaaS project with the team, merge my STRIDE threat model into the team docs repository and finish the HCCDP-Solution Architectures course of the corte 3 certification: chapters, labs, final exam and certificate.
<!-- CONFIG-END -->

## 1. User stories worked this week
| HU ID | Title | Status (todo/doing/done) | Evidence (PR or commit URL) |
|---|---|---|---|
| C3-RELEASE | Team defense of the BarberSaaS project (November 12): my part was the outbox and worker section | done | Oral defense in class on 2026-11-12; [barber-saas-docs](https://github.com/code-corhuila/barber-saas-docs) |
| SEC-TB2a | STRIDE threat model and risk ranking of the boundary api-gateway → identity-auth-api, merged into barber-saas-docs after review | done | [PR #162](https://github.com/code-corhuila/barber-saas-docs/pull/162), [7e66fb0](https://github.com/code-corhuila/barber-saas-docs/commit/7e66fb0), [ca2349e](https://github.com/code-corhuila/barber-saas-docs/commit/ca2349e), [d35cdf7](https://github.com/code-corhuila/barber-saas-docs/commit/d35cdf7) |
| C3-CERT | Corte 3 certification: HCCDP-Solution Architectures, chapters 4 to 14, labs 1 to 3, final exam and certificate | done | [ed8e323](https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/commit/ed8e323cdb34cb6173ba65713c95fce2d1b3149b), [bb690f5](https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/commit/bb690f58a43f93e7d1022ee9a392c11ff6fc88e5), [0f74e1a](https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/commit/0f74e1a70db8e2d07677f5c055ddfa0697cd0138), [b32881e](https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/commit/b32881e57cb400722e38a0b620c58266fbd70633), [068e608](https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/commit/068e608616d96f82e78990bed5c77e9e33a96a2c), [2c4bd86](https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/commit/2c4bd860df234716e57e214e610c704695b6332b) |
| C3-DESIGN | Corte 3 certification: architecture design note and two ADRs for BarberSaaS on Huawei Cloud | todo | [certification/design](https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/tree/main/certification/design) |

## 2. My individual contribution
- My threat model PR #162 was approved and merged into barber-saas-docs on November 11 with three commits: the STRIDE context and first threats (7e66fb0), the complete STRIDE with its risk ranking (ca2349e) and the changes asked in the review (d35cdf7). It is now part of the team security folder, next to the threat models of the other boundaries.
- Finished the HCCDP-Solution Architectures course: chapters 6 to 14 between November 8 and 13, with one screenshot per chapter in `certification/evidence/`.
- Completed three online labs on Huawei Cloud: an O&M solution with Cloud Eye, SMN and LTS (lab 1), a highly reliable database with RDS primary/standby, DRS, a read replica and DCS for Redis (lab 2), and a highly elastic system with ELB and Auto Scaling (lab 3). For each one I wrote what failed first and how I fixed it.
- Passed the final exam on November 14 with 81/100 (passing score 70) and added the Huawei ICT Academy certificate of completion.
- Kept the study log up to date: 41.5 hours in total, from November 3 to 14.

## 3. Blockers and risks
- The architecture design note (1,200 to 2,000 words), the two ADRs, the skills summary and lab 4 of the certification are still templates; they must be finished before the certification deadline.
- Story #166 still depends on proposing `CreateBarberAuthorizationTest` and `security.yml` to identity-auth-api through a PR reviewed by the owner of the service.

## 4. Plan for next week
- Write the architecture design note and the two ADRs for BarberSaaS on Huawei Cloud.
- Write the skills summary and complete lab 4 in `certification/README.md`.
- Propose `CreateBarberAuthorizationTest` and `security.yml` to identity-auth-api to move story #166 forward.

## 5. Compliance self-check
- [x] Conventional Commits - `type(scope): summary`
- [x] Per-environment HU branch + PR to that environment (hu-xxx-dev -> develop, ...) - the docs repository only has `main`; my change went through its own branch and PR #162, approved before the merge
- [x] Testable acceptance criteria - every security story of my STRIDE has an automated test as its criterion
- [ ] Tests added/updated (unit / integration) - not applicable: no project code changed this week
- [ ] DDD / hexagonal boundaries respected (domain has no I/O) - not applicable: no domain code changed this week
- [x] No secrets; config via environment variables

## 6. Evidence links
- STRIDE PR (merged): https://github.com/code-corhuila/barber-saas-docs/pull/162
- My commits in barber-saas-docs: https://github.com/code-corhuila/barber-saas-docs/commit/7e66fb0, https://github.com/code-corhuila/barber-saas-docs/commit/ca2349e, https://github.com/code-corhuila/barber-saas-docs/commit/d35cdf7
- Certification folder: https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/tree/main/certification
- Final exam evidence: https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/blob/main/certification/evidence/19-final-exam.png
- Certificate: https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2/blob/main/certification/certificate.pdf
