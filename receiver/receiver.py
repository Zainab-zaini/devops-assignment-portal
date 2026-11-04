import json
import os
import secrets
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HOST = "127.0.0.1"
PORT = 8765
TOKEN = os.environ.get("REPORT_RECEIVER_TOKEN")

REPORT_PATH = Path(__file__).resolve().parent.parent / "test-report.json"


class ReportHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        if self.path != "/report":
            self.send_error(404, "Endpoint not found")
            return

        authorization = self.headers.get("Authorization", "")
        expected = f"Bearer {TOKEN}"

        if not TOKEN or not secrets.compare_digest(authorization, expected):
            self.send_error(401, "Unauthorized")
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 5_000_000:
                self.send_error(400, "Invalid report size")
                return

            report = json.loads(self.rfile.read(length))
            required = [
                "repository", "branch", "commit_sha",
                "pipeline_run_id", "timestamp",
                "tests", "total", "passed", "failed", "status"
            ]

            if not all(key in report for key in required):
                self.send_error(400, "Incomplete report")
                return

            temporary_path = REPORT_PATH.with_suffix(".tmp")
            temporary_path.write_text(
                json.dumps(report, indent=4),
                encoding="utf-8"
            )
            temporary_path.replace(REPORT_PATH)

            print(f"\nReport received: {report['status']}")
            print(f"Tests: {report['passed']} passed, {report['failed']} failed")
            print(f"Saved to: {REPORT_PATH}")

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Report saved successfully")

        except Exception as error:
            self.send_error(400, str(error))

    def log_message(self, format, *args):
        print(format % args)


if __name__ == "__main__":
    if not TOKEN:
        raise RuntimeError("REPORT_RECEIVER_TOKEN environment variable is missing.")

    server = ThreadingHTTPServer((HOST, PORT), ReportHandler)
    print(f"Report receiver running at http://{HOST}:{PORT}")
    print("Waiting for GitHub Actions reports...")
    server.serve_forever()