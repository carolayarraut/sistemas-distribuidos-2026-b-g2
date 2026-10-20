# HOW TO RUN - barber-saas-worker instrumentation (CP3)

Minimal module named after **barber-saas-worker**, the service of the password reset journey
(`01-journey.md`) that breaks the trace today: it relays `PasswordResetRequested` from the
identity-auth-api outbox to notifications-api with a new `X-Correlation-Id` on every run.
Like the real worker (ADR-012), it uses only the Python standard library.

## Files

| File | What it does |
|---|---|
| `trace_context.py` | parses, creates and continues a W3C `traceparent` (same `trace_id`, new `span_id`) |
| `json_logger.py` | one JSON line per log with the fields of `02-log-contract.md`; drops e-mail, code and payload |
| `health_server.py` | the worker's HTTP port with the middleware: reads or creates `traceparent` and returns it in the response |
| `relay.py` | delivers one outbox event to `POST /internal/v1/events` of notifications-api with the `traceparent` stored in the outbox row |
| `metrics.py` | `worker_outbox_deliveries_total` (counter by outcome) and `worker_outbox_delivery_duration_seconds` (histogram), served on `GET /metrics` |
| `test_trace_propagation.py` | fake notifications-api; proves the `trace_id` received equals the one sent |

## Requirements

- Python 3.12 or newer (run here with Python 3.15.0 on Windows 11)
- Nothing to install: no `pip install` step

## Commands (Windows PowerShell)

```powershell
git clone https://github.com/carolayarraut/sistemas-distribuidos-2026-b-g2.git
cd sistemas-distribuidos-2026-b-g2\11-week\workshop\03-instrumentation\barber-saas-worker
py --version
py -m unittest -v
```

On Windows, `python` may open the Microsoft Store (app execution alias); `py` is the launcher
installed with Python. On Linux or macOS use `python3 -m unittest -v`.

## What the tests prove

| Test | Proves |
|---|---|
| `test_trace_id_received_equals_trace_id_sent` | the `trace_id` that reaches notifications-api is the one stored with the event; only the `span_id` changes |
| `test_event_without_traceparent_starts_a_new_trace` | an old outbox row without `traceparent` still gets a valid trace |
| `test_logs_follow_the_contract_and_hide_personal_data` | every log line has the CP2 fields and never the e-mail or the reset code |
| `test_timeout_is_counted` | a slow consumer gives `outbox.delivery.timeout` (ERROR) and `outcome="TIMEOUT"` in the counter |
| `test_health_returns_the_incoming_trace` | the middleware returns the incoming trace in the `traceparent` response header |
| `test_metrics_endpoint_exposes_counter_and_histogram` | `GET /metrics` serves both metrics in Prometheus text format |

## Real output (Windows 11, Python 3.15.0, 2026-10-19)

```text
{"timestamp":"2026-10-20T01:08:50.752Z","level":"INFO","service":"barber-saas-worker","version":"2.0.0","environment":"dev","trace_id":"86a4b351f7cbb4801e4fa501fb69fd52","span_id":"f2b48e96fca9c432","correlation_id":"5f3a9e0c71b24d68a2c4e9b1d7f03a65","event":"outbox.delivery.started","message":"delivering event to consumer","duration_ms":0,"outbox_event_id":"c0f4a812-6e3b-4b57-8d29-7a1e5f90c3b6","event_type":"PasswordResetRequested","delivery_attempt":1,"target_service":"notifications-api"}
{"timestamp":"2026-10-20T01:08:50.777Z","level":"INFO","service":"barber-saas-worker","version":"2.0.0","environment":"dev","trace_id":"86a4b351f7cbb4801e4fa501fb69fd52","span_id":"f2b48e96fca9c432","correlation_id":"5f3a9e0c71b24d68a2c4e9b1d7f03a65","event":"outbox.delivery.done","message":"consumer answered 200","duration_ms":24,"consumer_outcome":"PROCESSED","outbox_event_id":"c0f4a812-6e3b-4b57-8d29-7a1e5f90c3b6","event_type":"PasswordResetRequested","delivery_attempt":1,"target_service":"notifications-api"}
test_event_without_traceparent_starts_a_new_trace (test_trace_propagation.TracePropagationTest.test_event_without_traceparent_starts_a_new_trace) ... ok
{"timestamp":"2026-10-20T01:08:50.779Z","level":"INFO","service":"barber-saas-worker","version":"2.0.0","environment":"dev","trace_id":"ac8ced4137a8b95fc1e3b5fd9218431a","span_id":"ed17fae55e660a85","correlation_id":"ac8ced4137a8b95fc1e3b5fd9218431a","event":"http.request.handled","message":"GET /health","duration_ms":0,"http_status":200}
test_health_returns_the_incoming_trace (test_trace_propagation.TracePropagationTest.test_health_returns_the_incoming_trace) ... ok
{"timestamp":"2026-10-20T01:08:50.780Z","level":"INFO","service":"barber-saas-worker","version":"2.0.0","environment":"dev","trace_id":"ac8ced4137a8b95fc1e3b5fd9218431a","span_id":"f826e624e53d11e9","correlation_id":"5f3a9e0c71b24d68a2c4e9b1d7f03a65","event":"outbox.delivery.started","message":"delivering event to consumer","duration_ms":0,"outbox_event_id":"c0f4a812-6e3b-4b57-8d29-7a1e5f90c3b6","event_type":"PasswordResetRequested","delivery_attempt":1,"target_service":"notifications-api"}
{"timestamp":"2026-10-20T01:08:50.783Z","level":"INFO","service":"barber-saas-worker","version":"2.0.0","environment":"dev","trace_id":"ac8ced4137a8b95fc1e3b5fd9218431a","span_id":"f826e624e53d11e9","correlation_id":"5f3a9e0c71b24d68a2c4e9b1d7f03a65","event":"outbox.delivery.done","message":"consumer answered 200","duration_ms":2,"consumer_outcome":"PROCESSED","outbox_event_id":"c0f4a812-6e3b-4b57-8d29-7a1e5f90c3b6","event_type":"PasswordResetRequested","delivery_attempt":1,"target_service":"notifications-api"}
test_logs_follow_the_contract_and_hide_personal_data (test_trace_propagation.TracePropagationTest.test_logs_follow_the_contract_and_hide_personal_data) ... ok
{"timestamp":"2026-10-20T01:08:50.783Z","level":"INFO","service":"barber-saas-worker","version":"2.0.0","environment":"dev","trace_id":"ac8ced4137a8b95fc1e3b5fd9218431a","span_id":"bc38bbd5e5f4cd49","correlation_id":"5f3a9e0c71b24d68a2c4e9b1d7f03a65","event":"outbox.delivery.started","message":"delivering event to consumer","duration_ms":0,"outbox_event_id":"c0f4a812-6e3b-4b57-8d29-7a1e5f90c3b6","event_type":"PasswordResetRequested","delivery_attempt":1,"target_service":"notifications-api"}
{"timestamp":"2026-10-20T01:08:50.785Z","level":"INFO","service":"barber-saas-worker","version":"2.0.0","environment":"dev","trace_id":"ac8ced4137a8b95fc1e3b5fd9218431a","span_id":"bc38bbd5e5f4cd49","correlation_id":"5f3a9e0c71b24d68a2c4e9b1d7f03a65","event":"outbox.delivery.done","message":"consumer answered 200","duration_ms":2,"consumer_outcome":"PROCESSED","outbox_event_id":"c0f4a812-6e3b-4b57-8d29-7a1e5f90c3b6","event_type":"PasswordResetRequested","delivery_attempt":1,"target_service":"notifications-api"}
{"timestamp":"2026-10-20T01:08:50.788Z","level":"INFO","service":"barber-saas-worker","version":"2.0.0","environment":"dev","trace_id":"dcf7e47e8d8fd94c5285ca8f2e948157","span_id":"86e797c5321e2025","correlation_id":"dcf7e47e8d8fd94c5285ca8f2e948157","event":"http.request.handled","message":"GET /metrics","duration_ms":0,"http_status":200}
test_metrics_endpoint_exposes_counter_and_histogram (test_trace_propagation.TracePropagationTest.test_metrics_endpoint_exposes_counter_and_histogram) ... ok
{"timestamp":"2026-10-20T01:08:50.789Z","level":"INFO","service":"barber-saas-worker","version":"2.0.0","environment":"dev","trace_id":"ac8ced4137a8b95fc1e3b5fd9218431a","span_id":"8092add2fd62230d","correlation_id":"5f3a9e0c71b24d68a2c4e9b1d7f03a65","event":"outbox.delivery.started","message":"delivering event to consumer","duration_ms":0,"outbox_event_id":"c0f4a812-6e3b-4b57-8d29-7a1e5f90c3b6","event_type":"PasswordResetRequested","delivery_attempt":1,"target_service":"notifications-api"}
{"timestamp":"2026-10-20T01:08:50.991Z","level":"ERROR","service":"barber-saas-worker","version":"2.0.0","environment":"dev","trace_id":"ac8ced4137a8b95fc1e3b5fd9218431a","span_id":"8092add2fd62230d","correlation_id":"5f3a9e0c71b24d68a2c4e9b1d7f03a65","event":"outbox.delivery.timeout","message":"no answer in 0.2 s, retry scheduled","duration_ms":201,"consumer_outcome":"TIMEOUT","outbox_event_id":"c0f4a812-6e3b-4b57-8d29-7a1e5f90c3b6","event_type":"PasswordResetRequested","delivery_attempt":1,"target_service":"notifications-api"}
test_timeout_is_counted (test_trace_propagation.TracePropagationTest.test_timeout_is_counted) ... ok
{"timestamp":"2026-10-20T01:08:50.991Z","level":"INFO","service":"barber-saas-worker","version":"2.0.0","environment":"dev","trace_id":"ac8ced4137a8b95fc1e3b5fd9218431a","span_id":"b8f9def62e4ffcf0","correlation_id":"5f3a9e0c71b24d68a2c4e9b1d7f03a65","event":"outbox.delivery.started","message":"delivering event to consumer","duration_ms":0,"outbox_event_id":"c0f4a812-6e3b-4b57-8d29-7a1e5f90c3b6","event_type":"PasswordResetRequested","delivery_attempt":1,"target_service":"notifications-api"}
{"timestamp":"2026-10-20T01:08:51.007Z","level":"INFO","service":"barber-saas-worker","version":"2.0.0","environment":"dev","trace_id":"ac8ced4137a8b95fc1e3b5fd9218431a","span_id":"b8f9def62e4ffcf0","correlation_id":"5f3a9e0c71b24d68a2c4e9b1d7f03a65","event":"outbox.delivery.done","message":"consumer answered 200","duration_ms":15,"consumer_outcome":"PROCESSED","outbox_event_id":"c0f4a812-6e3b-4b57-8d29-7a1e5f90c3b6","event_type":"PasswordResetRequested","delivery_attempt":1,"target_service":"notifications-api"}
test_trace_id_received_equals_trace_id_sent (test_trace_propagation.TracePropagationTest.test_trace_id_received_equals_trace_id_sent) ... ok

----------------------------------------------------------------------
Ran 6 tests in 1.083s

OK
```

## Problems found while running it

- `python --version` opened the Microsoft Store instead of Python: solved by using `py`.
- On Windows the timeout test printed a `ConnectionAbortedError` (WinError 10053) from the fake
  consumer, which Linux reports as `BrokenPipeError`. The fake now catches `ConnectionError`, the
  parent of all three.
