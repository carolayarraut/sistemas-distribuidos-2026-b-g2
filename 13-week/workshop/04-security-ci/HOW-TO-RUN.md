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
