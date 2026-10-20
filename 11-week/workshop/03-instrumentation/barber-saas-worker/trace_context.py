"""W3C trace context for barber-saas-worker: read, create and continue a traceparent."""
import re
import secrets
from contextvars import ContextVar
from dataclasses import dataclass

_TRACEPARENT = re.compile(r"^00-([0-9a-f]{32})-([0-9a-f]{16})-([0-9a-f]{2})$")


@dataclass(frozen=True)
class TraceContext:
    trace_id: str
    span_id: str
    flags: str = "01"

    def child(self) -> "TraceContext":
        return TraceContext(self.trace_id, secrets.token_hex(8), self.flags)

    def header(self) -> str:
        return f"00-{self.trace_id}-{self.span_id}-{self.flags}"


def new_context() -> TraceContext:
    return TraceContext(secrets.token_hex(16), secrets.token_hex(8))


def parse(value: str | None) -> TraceContext | None:
    if not value:
        return None
    match = _TRACEPARENT.match(value.strip().lower())
    if not match or set(match.group(1)) == {"0"} or set(match.group(2)) == {"0"}:
        return None
    return TraceContext(match.group(1), match.group(2), match.group(3))


def continue_or_start(traceparent: str | None) -> TraceContext:
    """A child span of the incoming context, or a new trace when there is none or it is invalid."""
    parent = parse(traceparent)
    return parent.child() if parent else new_context()


CURRENT: ContextVar[TraceContext | None] = ContextVar("trace_context", default=None)
CORRELATION: ContextVar[str] = ContextVar("correlation_id", default="")
