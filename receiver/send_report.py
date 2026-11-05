import json
import os
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULT_FILE = ROOT / "test-results.json"

if RESULT_FILE.exists():
    raw = json.loads(RESULT_FILE.read_text(encoding="utf-8"))
else:
    raw = {}

tests = []
for test in raw.get("tests", []):
    outcome = test.get("outcome", "unknown")

    failure_message = None
    if outcome in ("failed", "error"):
        for phase in ("call", "setup", "teardown"):
            details = test.get(phase, {})
            failure_message = (
                details.get("longrepr")
                or details.get("crash", {}).get("message")
            )
            if failure_message:
                break

    tests.append({
        "name": test.get("nodeid", "Unknown test"),
        "result": outcome,
        "failure_message": failure_message
    })

failed = sum(t["result"] in ("failed", "error") for t in tests)
passed = sum(t["result"] == "passed" for t in tests)
skipped = sum(t["result"] == "skipped" for t in tests)

step_outcome = os.getenv("TEST_STEP_OUTCOME", "failure")
status = (
    "PASSED"
    if step_outcome == "success" and tests and failed == 0
    else "FAILED"
)

report = {
    "repository": os.getenv("GITHUB_REPOSITORY", "unknown"),
    "branch": os.getenv("GITHUB_REF_NAME", "unknown"),
    "commit_sha": os.getenv("GITHUB_SHA", "unknown"),
    "pipeline_run_id": os.getenv("GITHUB_RUN_ID", "unknown"),
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "tests": tests,
    "total": len(tests),
    "passed": passed,
    "failed": failed,
    "skipped": skipped,
    "status": status
}

url = os.environ["REPORT_RECEIVER_URL"]
token = os.environ["REPORT_RECEIVER_TOKEN"]

(ROOT / "test-report.json").write_text(
    json.dumps(report, indent=4),
    encoding="utf-8"
)

request = urllib.request.Request(
    url,
    data=json.dumps(report).encode("utf-8"),
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    },
    method="POST"
)

with urllib.request.urlopen(request, timeout=15) as response:
    print(response.read().decode("utf-8"))

print(f"Report delivery status: {status}")