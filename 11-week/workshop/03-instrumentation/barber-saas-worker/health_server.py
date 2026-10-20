"""The worker's HTTP port (GET /health) with the trace-context middleware."""
import json
import logging
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from json_logger import log
from trace_context import CORRELATION, CURRENT, continue_or_start


def with_trace_context(handle):
    """Reads or creates the trace context and returns it in the response."""
    def wrapped(self):
        ctx = continue_or_start(self.headers.get("traceparent"))
        trace_token = CURRENT.set(ctx)
        corr_token = CORRELATION.set(self.headers.get("X-Correlation-Id") or ctx.trace_id)
        start = time.monotonic()
        try:
            handle(self)
        finally:
            log(logging.INFO, "http.request.handled", f"{self.command} {self.path}",
                duration_ms=(time.monotonic() - start) * 1000, http_status=getattr(self, "status", 0))
            CURRENT.reset(trace_token)
            CORRELATION.reset(corr_token)
    return wrapped


def health() -> tuple[int, str, bytes]:
    return 200, "application/json", json.dumps({"status": "UP"}).encode()


class WorkerHandler(BaseHTTPRequestHandler):
    routes = {"/health": health}

    @with_trace_context
    def do_GET(self):
        route = self.routes.get(self.path.split("?")[0])
        self.status, content_type, body = route() if route else (404, "text/plain", b"not found")
        self.send_response(self.status)
        self.send_header("Content-Type", content_type)
        self.send_header("traceparent", CURRENT.get().header())
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


def serve(port: int = 8090) -> ThreadingHTTPServer:
    return ThreadingHTTPServer(("127.0.0.1", port), WorkerHandler)
