"""Prometheus text format with the standard library: one counter and one latency histogram."""
import threading

BUCKETS = (0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0)
_lock = threading.Lock()
_deliveries: dict[str, int] = {}
_bucket_counts = [0] * len(BUCKETS)
_sum = 0.0
_count = 0


def record_delivery(outcome: str, seconds: float) -> None:
    global _sum, _count
    with _lock:
        _deliveries[outcome] = _deliveries.get(outcome, 0) + 1
        for i, upper in enumerate(BUCKETS):
            if seconds <= upper:
                _bucket_counts[i] += 1
        _sum += seconds
        _count += 1


def render() -> str:
    with _lock:
        lines = ["# HELP worker_outbox_deliveries_total Outbox events delivered to a consumer, by outcome.",
                 "# TYPE worker_outbox_deliveries_total counter"]
        for outcome, value in sorted(_deliveries.items()):
            lines.append(f'worker_outbox_deliveries_total{{consumer="notifications-api",outcome="{outcome}"}} {value}')
        lines += ["# HELP worker_outbox_delivery_duration_seconds Time of POST /internal/v1/events.",
                  "# TYPE worker_outbox_delivery_duration_seconds histogram"]
        for upper, value in zip(BUCKETS, _bucket_counts):
            lines.append(f'worker_outbox_delivery_duration_seconds_bucket{{consumer="notifications-api",le="{upper}"}} {value}')
        lines.append(f'worker_outbox_delivery_duration_seconds_bucket{{consumer="notifications-api",le="+Inf"}} {_count}')
        lines.append(f'worker_outbox_delivery_duration_seconds_sum{{consumer="notifications-api"}} {_sum:.3f}')
        lines.append(f'worker_outbox_delivery_duration_seconds_count{{consumer="notifications-api"}} {_count}')
    return "\n".join(lines) + "\n"


def metrics_route() -> tuple[int, str, bytes]:
    return 200, "text/plain; version=0.0.4", render().encode()


def reset() -> None:
    global _sum, _count
    with _lock:
        _deliveries.clear()
        _bucket_counts[:] = [0] * len(BUCKETS)
        _sum, _count = 0.0, 0
