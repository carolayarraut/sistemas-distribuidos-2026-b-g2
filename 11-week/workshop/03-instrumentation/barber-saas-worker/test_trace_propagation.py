"""The trace_id stored with an outbox event must reach notifications-api unchanged."""
import io
import json
import logging
import threading
import time
import unittest
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import metrics
from health_server import WorkerHandler, serve
from json_logger import JsonFormatter, get_logger
from relay import deliver
from trace_context import new_context, parse

STORED = new_context()
EVENT = {"id": "c0f4a812-6e3b-4b57-8d29-7a1e5f90c3b6", "type": "PasswordResetRequested",
         "correlationId": "5f3a9e0c71b24d68a2c4e9b1d7f03a65", "traceparent": STORED.header(),
         "payload": {"userId": "3b8e2f61-0c4a-4d9e-9a71-5e2c8f04b1d3", "email": "client@example.com",
                     "code": "482913"}}


class FakeNotificationsApi(BaseHTTPRequestHandler):
    received: list = []
    delay = 0.0

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        FakeNotificationsApi.received.append((self.headers.get("traceparent"), body))
        time.sleep(FakeNotificationsApi.delay)
        answer = json.dumps({"eventId": body["id"], "outcome": "PROCESSED"}).encode()
        try:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(answer)
        except ConnectionError:
            pass

    def log_message(self, *args):
        pass


def start(server):
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


class TracePropagationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.consumer = start(ThreadingHTTPServer(("127.0.0.1", 0), FakeNotificationsApi))
        cls.url = f"http://127.0.0.1:{cls.consumer.server_port}"
        WorkerHandler.routes["/metrics"] = metrics.metrics_route
        cls.worker = start(serve(0))

    @classmethod
    def tearDownClass(cls):
        cls.consumer.shutdown()
        cls.worker.shutdown()

    def setUp(self):
        FakeNotificationsApi.received.clear()
        FakeNotificationsApi.delay = 0.0
        metrics.reset()
        self.lines = io.StringIO()
        self.handler = logging.StreamHandler(self.lines)
        self.handler.setFormatter(JsonFormatter())
        get_logger().addHandler(self.handler)

    def tearDown(self):
        get_logger().removeHandler(self.handler)

    def test_trace_id_received_equals_trace_id_sent(self):
        self.assertEqual(deliver(EVENT, self.url), "PROCESSED")
        header, body = FakeNotificationsApi.received[0]
        received = parse(header)
        self.assertEqual(received.trace_id, STORED.trace_id)
        self.assertNotEqual(received.span_id, STORED.span_id)
        self.assertNotIn("traceparent", body)

    def test_event_without_traceparent_starts_a_new_trace(self):
        deliver({k: v for k, v in EVENT.items() if k != "traceparent"}, self.url)
        self.assertIsNotNone(parse(FakeNotificationsApi.received[0][0]))

    def test_logs_follow_the_contract_and_hide_personal_data(self):
        deliver(EVENT, self.url)
        lines = [json.loads(line) for line in self.lines.getvalue().splitlines()]
        self.assertEqual({line["trace_id"] for line in lines}, {STORED.trace_id})
        for field in ("timestamp", "level", "service", "version", "environment", "span_id",
                      "correlation_id", "event", "message", "duration_ms"):
            self.assertIn(field, lines[0])
        self.assertNotIn("client@example.com", self.lines.getvalue())
        self.assertNotIn("482913", self.lines.getvalue())

    def test_timeout_is_counted(self):
        FakeNotificationsApi.delay = 0.5
        self.assertEqual(deliver(EVENT, self.url, timeout=0.2), "TIMEOUT")
        self.assertIn('outcome="TIMEOUT"} 1', metrics.render())

    def test_health_returns_the_incoming_trace(self):
        request = urllib.request.Request(f"http://127.0.0.1:{self.worker.server_port}/health",
                                         headers={"traceparent": STORED.header()})
        with urllib.request.urlopen(request) as response:
            self.assertEqual(parse(response.headers["traceparent"]).trace_id, STORED.trace_id)

    def test_metrics_endpoint_exposes_counter_and_histogram(self):
        deliver(EVENT, self.url)
        with urllib.request.urlopen(f"http://127.0.0.1:{self.worker.server_port}/metrics") as response:
            text = response.read().decode()
        self.assertIn('worker_outbox_deliveries_total{consumer="notifications-api",outcome="PROCESSED"} 1', text)
        self.assertIn("worker_outbox_delivery_duration_seconds_bucket", text)


if __name__ == "__main__":
    unittest.main()
