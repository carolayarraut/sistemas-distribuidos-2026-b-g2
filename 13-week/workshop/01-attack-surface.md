# 01 - Attack surface and trust boundaries

My boundary: **TB2 · api-gateway → identity-auth-api (public `/api/v1/auth/` endpoints)**, claimed in
barber-saas-docs #151. TB1 (Internet → edge: Caddy + api-gateway) is #150 and TB4 (worker → domain
`/internal` endpoints) is #149.

Sources: barber-saas-docs `05-architecture/overview.md`, `09-microservices/service-catalog.md`,
`02-domain/domain-events.md`, ADR-016, ADR-017, ADR-018, ADR-019, and the nginx routes of
barber-saas-api-gateway (`nginx/routes/identity-auth.conf`).

## Data flow

```mermaid
flowchart LR
  U[Client, barber, owner, SUPER_ADMIN<br/>hybrid app: front + domain apps]
  WOMPI[Wompi sandbox]
  subgraph TB1 [TB1 edge - Oracle host, ADR-019]
    CADDY[Caddy :443 TLS]
    GW[api-gateway nginx :8000]
  end
  subgraph INTERNAL [compose network platform]
    subgraph TB2 [TB2 - MY BOUNDARY]
      IA[identity-auth-api]
    end
    BS[barbershop-api]
    SC[schedule-api]
    AP[appointment-api]
    LY[loyalty-api]
    FI[finance-inventory-api]
    PA[platform-admin-api]
    NT[notifications-api]
    WF[workflow]
    WK[barber-saas-worker]
    PG[(PostgreSQL 16<br/>one schema per domain)]
    MG[(MongoDB 7<br/>notifications)]
  end
  SMTP[SMTP server]
  FCM[Firebase Cloud Messaging]

  U -->|HTTPS| CADDY --> GW
  WOMPI -->|signed event HTTPS| CADDY
  GW ==>|/api/v1/auth/ no token| IA
  GW -->|/api/v1/** RS256 JWT| BS & SC & AP & LY & FI & PA & NT
  IA -->|SQL schema identity_auth| PG
  BS & SC & AP & LY & FI & PA & WF -->|SQL own schema| PG
  NT --> MG
  AP -->|internal REST| BS & SC & LY
  PA -->|internal REST service token| BS
  BS -->|GET /internal/v1/users/id| IA
  WF -->|saga steps service token| IA & BS & PA
  WK -->|GET /internal/v1/outbox-events| IA & AP & LY & PA
  WK -->|POST /internal/v1/events| NT & LY & FI
  NT -->|reset and verification codes| SMTP
  NT -->|push| FCM

  style TB2 fill:#ffe4e1,stroke:#d00,stroke-width:3px
```

TB3 = each service → its own schema in the single PostgreSQL. TB5 = notifications-api → SMTP and
FCM. TB6 = Wompi → platform-admin-api. There is no message broker: events travel by the outbox
relay (ADR-016).

## Asset inventory (my domain: identity-auth)

| Asset | Where it lives | Classification |
|---|---|---|
| User password | request body of `POST /api/v1/auth/login` and `/register`; BCrypt hash in `identity_auth.app_user` | Restricted |
| JWT signing private key (`JWT_PRIVATE_KEY`) | environment of identity-auth-api only | Restricted |
| Access token (RS256, 24 h, `JWT_LIFETIME_SECONDS` 86400) | response of `/login` and `/refresh`, then every request through the gateway | Restricted |
| Refresh token (opaque, 7 days) | response of `/login`; SHA-256 hash in `identity_auth.refresh_token` | Restricted |
| Password reset and e-mail verification codes (6 digits, 15 min) | hash in `identity_auth.password_reset_token` and `identity_auth.email_verification_code`; plain in the outbox payload | Restricted |
| E-mail, full name and role of every user | `identity_auth.app_user` | Confidential |
| Public key set (`GET /api/v1/auth/jwks`) | identity-auth-api | Public |

## Entry points of TB2

| Entry point | Who calls it | Authentication today |
|---|---|---|
| `POST /api/v1/auth/register` | anyone on the internet (owner or client sign-up) | none; gateway rate limit burst 5 |
| `POST /api/v1/auth/login` | any user | none; e-mail + password |
| `POST /api/v1/auth/refresh` | the app | refresh token in the body |
| `POST /api/v1/auth/password-reset` and `/confirm` | anyone | none; 6-digit code, 5 wrong attempts, 1 request per minute |
| `POST /api/v1/auth/email-verification/confirm` and `/resend` | new user | none; 6-digit code (ADR-018) |
| `POST /api/v1/auth/barbershop-token` | signed-in client | RS256 JWT |
| `GET /api/v1/auth/me`, `POST /api/v1/auth/me/password`, `POST /api/v1/auth/logout` | signed-in user | RS256 JWT: the gateway only checks that the header exists, identity-auth-api verifies the signature |
| `GET /api/v1/auth/jwks` | the other services, to verify tokens | none (public keys) |

Port: identity-auth-api listens on 8080 with `expose` only; the gateway is the only way in from the
host. `/internal/v1/**` of identity-auth-api is never routed by the gateway.
