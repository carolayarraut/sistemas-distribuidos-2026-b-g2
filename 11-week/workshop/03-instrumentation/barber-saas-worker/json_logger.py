"""One JSON line per log record, with the fields of 02-log-contract.md."""
import json
import logging
import os
import sys
from datetime import datetime, timezone

from trace_context import CORRELATION, CURRENT

SERVICE = "barber-saas-worker"
VERSION = os.environ.get("APP_VERSION", "2.0.0")
ENVIRONMENT = os.environ.get("APP_ENV", "dev")
NEVER_LOG = {"email", "fullName", "code", "payload", "authorization", "password"}


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        ctx = CURRENT.get()
        line = {
            "timestamp": datetime.fromtimestamp(record.created, timezone.utc)
            .isoformat(timespec="milliseconds").replace("+00:00", "Z"),
            "level": "WARN" if record.levelname == "WARNING" else record.levelname,
            "service": SERVICE,
            "version": VERSION,
            "environment": ENVIRONMENT,
            "trace_id": ctx.trace_id if ctx else "",
            "span_id": ctx.span_id if ctx else "",
            "correlation_id": CORRELATION.get(),
            "event": getattr(record, "event", "log"),
            "message": record.getMessage(),
            "duration_ms": int(getattr(record, "duration_ms", 0)),
        }
        for key, value in getattr(record, "fields", {}).items():
            if key not in NEVER_LOG:
                line[key] = value
        return json.dumps(line, separators=(",", ":"))


def get_logger() -> logging.Logger:
    logger = logging.getLogger(SERVICE)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False
    return logger


def log(level: int, event: str, message: str, duration_ms: float = 0, **fields) -> None:
    get_logger().log(level, message, extra={"event": event, "duration_ms": duration_ms, "fields": fields})
