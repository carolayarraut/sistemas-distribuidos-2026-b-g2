# CP4 - How to run the security gates

## What the negative test proves

| Item | Value |
|---|---|
| Service and endpoint | `identity-auth-api`, `POST /api/v1/auth/barbers` |
| Story | barber-saas-docs [#166](https://github.com/code-corhuila/barber-saas-docs/issues/166): only a barbershop owner can create barbers |
| Criteria covered | 1: a `CLIENT` token gets `403` and no account is created (the e-mail cannot log in afterwards); 2: an `ADMIN_BARBERSHOP` token without `barbershopId` gets `403` |
| Threat | STRIDE E, risk 6, in [PR #162](https://github.com/code-corhuila/barber-saas-docs/pull/162) |
| Test class | `CreateBarberAuthorizationTest` (methods `clientTokenGets403`, `ownerTokenWithoutBarbershopGets403`) |

## Run the test on your computer

You need Java 21, Maven and a clone of `code-corhuila/barber-saas-identity-auth-api` on `develop`.
The test uses `InternalHttpTest.token(...)` and `InternalHttpTest.privateKey(...)` of that
repository, so it goes in the same package:

```bash
cd barber-saas-identity-auth-api
cp <my-fork>/13-week/workshop/04-security-ci/CreateBarberAuthorizationTest.java \
   identity-auth-app/src/test/java/co/edu/corhuila/barbersaas/identityauth/app/
mvn -B -pl identity-auth-app -am test -Dtest=CreateBarberAuthorizationTest -Dsurefire.failIfNoSpecifiedTests=false
```

Expected: `Tests run: 2, Failures: 0`. The check already exists in `AuthController.createBarber`
(`!caller.hasRole("ADMIN_BARBERSHOP") || caller.barbershopId() == null` throws `ForbiddenException`);
the test is the proof that keeps it there. If someone removes the `barbershopId` part, the second
method turns red.

## Run the whole workflow

`security.yml` is a proposal for `.github/workflows/` of `barber-saas-identity-auth-api`. It runs on
every pull request to `develop`, `qa` and `main`, in one job:

1. **gitleaks** on the commits of the pull request only (`--log-opts base..head`).
2. **OWASP dependency-check** on all Maven modules; it fails on CVSS 7 or higher. It needs the
   repository secret `NVD_API_KEY` (free key from nvd.nist.gov), or the first download is very slow.
3. **Negative authorization tests**: `CreateBarberAuthorizationTest` and the existing
   `BarberAccountsHttpTest`.

To try only the secret scan locally: `docker run --rm -v "$PWD:/src" -w /src ghcr.io/gitleaks/gitleaks:v8.21.2 git --redact`.

## Real run (CP8)

Run on 2026-10-30 in a GitHub Codespace, against `barber-saas-identity-auth-api` on branch
`develop`, with Maven 3.10.0 and JDK 21.0.13 (Microsoft build). The test file was copied into the
service only for the run and removed afterwards. Output filtered with
`grep -E "Running|logger\":\"access|Tests run|BUILD|Reactor Summary|SUCCESS \[|Total time|Finished at"`;
the three access lines are the requests of the test:

```text
[INFO] Running co.edu.corhuila.barbersaas.identityauth.app.CreateBarberAuthorizationTest
{"@timestamp":"2026-10-30T13:29:23.283020367Z",...,"logger":"access"},...,"message":"request method=POST path=/api/v1/auth/barbers status=403 durationMs=221","correlationId":"771e3083-d0f7-4b0e-9c1c-ba80d1b092ea",...}
{"@timestamp":"2026-10-30T13:29:23.380336989Z",...,"logger":"access"},...,"message":"request method=POST path=/api/v1/auth/barbers status=403 durationMs=6","correlationId":"cdd2c0f4-1edb-4a9e-99c9-8308b7c142b6",...}
{"@timestamp":"2026-10-30T13:29:23.392427751Z",...,"logger":"access"},...,"message":"request method=POST path=/api/v1/auth/login status=401 durationMs=8","correlationId":"5744ca6c-8fb7-452c-bce9-8a11946bd4cb",...}
[INFO] Tests run: 2, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 5.371 s -- in co.edu.corhuila.barbersaas.identityauth.app.CreateBarberAuthorizationTest
[INFO] Tests run: 2, Failures: 0, Errors: 0, Skipped: 0
[INFO] Reactor Summary for identity-auth 0.1.0:
[INFO] identity-auth ...................................... SUCCESS [  0.003 s]
[INFO] identity-auth-core ................................. SUCCESS [  7.108 s]
[INFO] identity-auth-adapters ............................. SUCCESS [  3.508 s]
[INFO] identity-auth-app .................................. SUCCESS [  9.340 s]
[INFO] BUILD SUCCESS
[INFO] Total time:  25.315 s
[INFO] Finished at: 2026-10-30T13:29:23Z
```

What it proves for story #166: the two `POST /api/v1/auth/barbers` calls (owner token without
`barbershopId`, and `CLIENT` token) both get `403`, and the `POST /api/v1/auth/login` with the
e-mail of the refused client gets `401`, so no account was created in `identity_auth.app_user`.

## Workflow validation (CP8)

`security.yml` checked with actionlint 1.7.12 in the same Codespace:

```text
$ ./actionlint sistemas-distribuidos-2026-b-g2/13-week/workshop/04-security-ci/security.yml; echo "exit code: $?"
exit code: 0
```

No errors were reported: the triggers, the job, the seven steps and the `${{ }}` expressions are
valid. The workflow is still a proposal; it has not run on GitHub Actions because it is not yet in
`.github/workflows/` of the identity-auth-api repository.
