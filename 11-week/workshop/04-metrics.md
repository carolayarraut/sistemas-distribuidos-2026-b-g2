# 04 - Metric catalog for the password reset journey

Journey: password reset request (`01-journey.md`). One table per service of the journey, with the
four golden signals as the user feels them. Names follow Prometheus conventions: `snake_case`, a
unit suffix (`_seconds`, `_bytes`), `_total` for counters. The worker metrics are the ones already
exposed by `03-instrumentation/barber-saas-worker` on `GET /metrics`.

## identity-auth-api (Java, Spring Boot)

Today identity-auth-api exposes no metrics: its v2.0.0 `pom.xml` has no Actuator or Micrometer
dependency. These are the metrics to add; the HTTP ones get the `identity_` prefix so the three
services can share one dashboard, and the Hikari pool is named `identity-auth`
(`spring.datasource.hikari.pool-name`).

| Signal | Metric | Type | Labels | PromQL for the dashboard |
|---|---|---|---|---|
| Latency | `identity_http_request_duration_seconds` | histogram | `route`, `method` | `histogram_quantile(0.95, sum by (le) (rate(identity_http_request_duration_seconds_bucket{route="/api/v1/auth/password-reset"}[5m])))` |
| Traffic | `identity_http_requests_total` | counter | `route`, `method`, `status_class` | `sum(rate(identity_http_requests_total{route="/api/v1/auth/password-reset"}[5m]))` |
| Errors | `identity_http_requests_total` | counter | same | `sum(rate(identity_http_requests_total{route="/api/v1/auth/password-reset",status_class="5xx"}[5m])) / sum(rate(identity_http_requests_total{route="/api/v1/auth/password-reset"}[5m]))` |
| Saturation | `hikaricp_connections_active` / `hikaricp_connections_max` | gauge | `pool` | `max(hikaricp_connections_active{pool="identity-auth"}) / max(hikaricp_connections_max{pool="identity-auth"})` |

## barber-saas-worker (Python, standard library)

| Signal | Metric | Type | Labels | PromQL for the dashboard |
|---|---|---|---|---|
| Latency | `worker_outbox_delivery_duration_seconds` | histogram | `consumer` | `histogram_quantile(0.95, sum by (le) (rate(worker_outbox_delivery_duration_seconds_bucket{consumer="notifications-api"}[5m])))` |
| Traffic | `worker_outbox_deliveries_total` | counter | `consumer`, `outcome` | `sum by (outcome) (rate(worker_outbox_deliveries_total{consumer="notifications-api"}[5m]))` |
| Errors | `worker_outbox_deliveries_total` | counter | same | `sum(rate(worker_outbox_deliveries_total{outcome=~"TIMEOUT\|RETRY\|FAILED"}[5m])) / sum(rate(worker_outbox_deliveries_total[5m]))` |
| Saturation | `worker_outbox_oldest_pending_age_seconds` | gauge | `producer` | `max(worker_outbox_oldest_pending_age_seconds{producer="identity-auth-api"})` |

The saturation signal is the age of the oldest `PasswordResetRequested` still in
`identity_auth.outbox_event`: if it grows, codes reach the user late even when nothing "fails".
Latency and traffic are already in the CP3 module; the age gauge is the next metric to add.

## notifications-api (Python, FastAPI)

Like identity-auth-api, it exposes no `/metrics` today; these are the metrics to add.

| Signal | Metric | Type | Labels | PromQL for the dashboard |
|---|---|---|---|---|
| Latency | `notifications_smtp_send_duration_seconds` | histogram | `template` | `histogram_quantile(0.95, sum by (le) (rate(notifications_smtp_send_duration_seconds_bucket{template="password_reset"}[5m])))` |
| Traffic | `notifications_inbound_events_total` | counter | `event_type`, `outcome` | `sum by (outcome) (rate(notifications_inbound_events_total{event_type="PasswordResetRequested"}[5m]))` |
| Errors | `notifications_smtp_send_failures_total` | counter | `template`, `reason` | `sum(rate(notifications_smtp_send_failures_total{template="password_reset"}[5m]))` |
| Saturation | `notifications_smtp_sends_in_flight` | gauge | none | `max(notifications_smtp_sends_in_flight)` |

## Label cardinality

| Label | Values | Estimate | Why it is bounded |
|---|---|---|---|
| `route` | route template from the controller, e.g. `/api/v1/auth/password-reset` | about 15 for identity-auth-api | the template, never the raw URL |
| `method` | GET, POST, PUT, DELETE | 4 | fixed |
| `status_class` | 2xx, 4xx, 5xx | 3 | grouped, not every code |
| `consumer` | notifications-api, loyalty-api | 2 | consumers of ADR-016 |
| `producer` | identity-auth-api, appointment-api, loyalty-api | 3 | the outboxes the worker reads |
| `outcome` | PROCESSED, DUPLICATE, IGNORED, TIMEOUT, RETRY, FAILED | 6 | enum in `relay.py` |
| `event_type` | the 9 events of `event-catalog.md` | 9 | catalog |
| `template` | password_reset, in_app | 2 | fixed |
| `reason` | timeout, refused, auth_error | 3 | fixed |
| `pool` | identity-auth | 1 | one pool per service |

Worst series count for one metric: `identity_http_requests_total` = 15 x 4 x 3 = 180 series.

**Forbidden labels and their replacement**

| Forbidden | Why | Use instead |
|---|---|---|
| `user_id`, `email` | one series per user (unbounded) and personal data | nothing in metrics; `user_id` only in logs |
| raw URL (`/api/v1/appointments/3b8e...`) | one series per id | `route` template |
| `outbox_event_id`, `trace_id`, `correlation_id` | one series per request | logs and traces |
| reset `code` | secret | never anywhere |

## Histogram buckets

| Metric | Buckets (seconds) | Justification with what our users expect |
|---|---|---|
| `identity_http_request_duration_seconds` | 0.05, 0.1, 0.25, 0.5, 1, 2.5 | the screen "send me a code" should answer in under 0.5 s; most requests are a few SQL statements, so the detail is below 0.5 s |
| `worker_outbox_delivery_duration_seconds` | 0.1, 0.25, 0.5, 1, 2.5, 5, 10 | the worker gives up at 5 s (`TIMEOUT_SECONDS`) and SMTP at 10 s, so 5 and 10 must be bucket limits to see how close we get |
| `notifications_smtp_send_duration_seconds` | 0.25, 0.5, 1, 2, 5, 10 | the user waits for the e-mail on the phone; under 2 s feels instant, over 10 s is the SMTP timeout |
