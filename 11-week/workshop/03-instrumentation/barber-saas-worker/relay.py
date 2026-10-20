"""Delivers one PasswordResetRequested from the identity-auth outbox to notifications-api,
continuing the trace stored with the event instead of starting a new one."""
import json
import logging
import time
import urllib.error
import urllib.request

import metrics
from json_logger import log
from trace_context import CORRELATION, CURRENT, continue_or_start

TIMEOUT_SECONDS = 5.0


def deliver(event: dict, consumer_url: str, attempt: int = 1, timeout: float = TIMEOUT_SECONDS) -> str:
    ctx = continue_or_start(event.get("traceparent"))
    trace_token = CURRENT.set(ctx)
    corr_token = CORRELATION.set(event.get("correlationId", ""))
    fields = {"outbox_event_id": event["id"], "event_type": event["type"],
              "delivery_attempt": attempt, "target_service": "notifications-api"}
    envelope = {k: v for k, v in event.items() if k != "traceparent"}
    request = urllib.request.Request(
        consumer_url + "/internal/v1/events", data=json.dumps(envelope).encode(), method="POST",
        headers={"Content-Type": "application/json", "traceparent": ctx.header(),
                 "X-Correlation-Id": CORRELATION.get()})
    log(logging.INFO, "outbox.delivery.started", "delivering event to consumer", **fields)
    start = time.monotonic()
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            outcome = json.loads(response.read()).get("outcome", "PROCESSED")
        level, name, text = logging.INFO, "outbox.delivery.done", "consumer answered 200"
    except urllib.error.HTTPError as error:
        outcome = "FAILED" if error.code < 500 else "RETRY"
        level, name, text = logging.ERROR, "outbox.delivery.rejected", f"consumer answered {error.code}"
    except (TimeoutError, urllib.error.URLError):
        outcome = "TIMEOUT"
        level, name, text = logging.ERROR, "outbox.delivery.timeout", f"no answer in {timeout:g} s, retry scheduled"
    seconds = time.monotonic() - start
    metrics.record_delivery(outcome, seconds)
    log(level, name, text, duration_ms=seconds * 1000, consumer_outcome=outcome, **fields)
    CURRENT.reset(trace_token)
    CORRELATION.reset(corr_token)
    return outcome
