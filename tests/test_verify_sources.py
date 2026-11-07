import http.server
import os
import sys
import threading
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
import verify_sources as vs  # noqa: E402


class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/ok":
            body = b"<html><title>Rust basics</title><body>memory safety and ownership</body></html>"
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, *a):
        pass


class T(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.srv = http.server.HTTPServer(("127.0.0.1", 0), H)
        cls.base = f"http://127.0.0.1:{cls.srv.server_port}"
        threading.Thread(target=cls.srv.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown()

    def test_extract_urls_dedupes_and_strips_punctuation(self):
        t = "See https://a.com/x. Also (https://b.org/y), and https://a.com/x again."
        self.assertEqual(vs.extract_urls(t), ["https://a.com/x", "https://b.org/y"])

    def test_ok_page(self):
        r = vs.check_url(self.base + "/ok", ["memory safety"])
        self.assertTrue(r["ok"])
        self.assertEqual(r["title"], "Rust basics")

    def test_missing_term_fails(self):
        r = vs.check_url(self.base + "/ok", ["quantum"])
        self.assertFalse(r["ok"])
        self.assertEqual(r["missing_terms"], ["quantum"])

    def test_404_fails(self):
        r = vs.check_url(self.base + "/nope")
        self.assertFalse(r["ok"])
        self.assertEqual(r["status"], 404)

    def test_unreachable_fails(self):
        r = vs.check_url("http://127.0.0.1:1/x", timeout=2)
        self.assertFalse(r["ok"])
        self.assertIsNotNone(r["error"])

    def test_cli_exit_codes(self):
        self.assertEqual(vs.main([self.base + "/ok"]), 0)
        self.assertEqual(vs.main([self.base + "/nope"]), 1)


if __name__ == "__main__":
    unittest.main()
