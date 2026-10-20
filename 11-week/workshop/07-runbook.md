# 07 - Runbook: PasswordResetAvailabilityFastBurn

Alert from `06-alerts.yml` (`severity: page`). It extends the operating guide of the service,
`09-microservices/services/identity-auth/runbook.md` in barber-saas-docs. Every command runs from
`barber-saas-infra-postgres` with `--env-file env/<env>.env` (shortened below to `$ENV`).

## 1. Symptoms

- More than **7.2 %** of `POST /api/v1/auth/password-reset` answer **5xx** in the last hour and in
  the last 5 minutes (burn rate 14.4; about 2 days to spend the whole 30-day budget).
- Users see an error on the "forgot password" screen of identity-auth-app and get no code.
- Users who cannot reset the password cannot log in, so they cannot book either.
- Not this alert: a `202` whose e-mail never arrives. That is the outbox or SMTP (SLO 3); see
  "Reset code never arrives" in the service runbook.

## 2. Confirm (5 minutes)

**a. Is the error real and still happening?**

```promql
identity:password_reset_error_ratio:rate5m
sum by (status_class) (rate(identity_http_requests_total{route="/api/v1/auth/password-reset"}[5m]))
```

**b. Is the service alive?**

```bash
docker compose $ENV ps identity-auth-api postgres           # expect "healthy"
```

**c. Follow one failed request by `trace_id`.** The gateway writes one JSON access line per request
with the id it sends to the service (`correlationId` today, `trace_id` after the CP3 change):

```bash
docker compose $ENV logs --since 15m api-gateway | grep '"uri":"/api/v1/auth/password-reset"' | grep '"status":5'
# take the trace id of one line and read the whole request in every service:
docker compose $ENV logs --since 15m identity-auth-api worker notifications-api | grep <trace_id>
```

What the identity-auth-api line tells you (`event` field of `02-log-contract.md`): a database
error or `Connection is not available` means PostgreSQL or the pool (`DB_POOL_MAX` = 10); an error
right after a deploy means the new version.

**d. What changed?** `git log --since="2 hours ago"` in barber-saas-identity-auth-api and
barber-saas-identity-auth-db.

## 3. Mitigations, lowest risk first

There is no feature flag for the reset in identity-auth-api, and this endpoint calls no other
service synchronously, so a circuit breaker does not apply. These are the three our architecture
supports:

| Order | Action | Use it when | How | Risk |
|---|---|---|---|---|
| 1 | **Scale** identity-auth-api to 2 replicas | pool exhausted or slow answers, no recent deploy | `docker compose $ENV up -d --scale identity-auth-api=2` (nginx resolves the service name every 10 s, `00-resolver.conf`, so the gateway spreads the load) | Low: no code change. Watch PostgreSQL connections, each replica opens up to 10 |
| 2 | **Restart** identity-auth-api | errors started with no deploy and the container is unhealthy or stuck | `docker compose $ENV restart identity-auth-api` | Low: about 30 s without logins and resets. Nothing is lost: the reset code and the outbox row are saved in one transaction |
| 3 | **Roll back** to the last good release (`v2.0.0`) | errors started right after a deploy | revert the pull request on `develop` and run `./scripts/up.sh <env>`, as in the service runbook; never edit an applied database changeset | Medium: it also removes the other changes of that release |

Stop after the first mitigation that brings the 5-minute error ratio below 7.2 %.

## 4. Escalation

| After | Who | Role in the team (`15-project-control/migration-work-split.md`) |
|---|---|---|
| 0 min | On-call person of the week | receives the page, follows this runbook |
| 15 min without improvement | Daniel Cerquera | owner of identity-auth-api, identity-auth-db, api-gateway, infra and worker |
| 30 min, or PostgreSQL is down for every service | Carlos Leal | tech lead (`04-requirements/non-functional.md`), decides on the rollback and talks to the barbershops |
| e-mail side (SMTP, notifications-api) | Carlos Leal | owner of notifications-api |
| After the incident | Carolay Arraut | documentation: updates this runbook and the service runbook |

## 5. Verify recovery

- `identity:password_reset_error_ratio:rate5m` stays below **0.005** (the SLO) for 15 minutes.
- `PasswordResetAvailabilityFastBurn` is resolved: the 5-minute window clears first.
- A real reset with a test account answers `202` and the e-mail arrives in less than 60 s.
- No `PasswordResetRequested` row is stuck:
  `SELECT count(*) FROM identity_auth.outbox_event WHERE published_at IS NULL AND failed_at IS NULL;`
  goes back to 0 within a few seconds.
- Write down the budget spent and open the postmortem (`08-incident.md`).
