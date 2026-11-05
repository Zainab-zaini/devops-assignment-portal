
import json
import os
import smtplib
from email.message import EmailMessage
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORT_FILE = ROOT / "test-report.json"

report = json.loads(
    REPORT_FILE.read_text(encoding="utf-8")
)

sender = os.environ["EMAIL_ADDRESS"]
password = os.environ["EMAIL_APP_PASSWORD"]
recipient = os.environ["REPORT_EMAIL_TO"]

message = EmailMessage()

message["Subject"] = (
    f"CI Test Report: {report['status']} "
    f"- {report['repository']}"
)

message["From"] = sender
message["To"] = recipient

details = [
    "ASSIGNMENT PORTAL - CI TEST REPORT",
    "",
    f"Repository: {report['repository']}",
    f"Branch: {report['branch']}",
    f"Commit: {report['commit_sha']}",
    f"Pipeline Run: {report['pipeline_run_id']}",
    f"Timestamp: {report['timestamp']}",
    "",
    f"Overall Status: {report['status']}",
    f"Total Tests: {report['total']}",
    f"Passed: {report['passed']}",
    f"Failed: {report['failed']}",
    "",
    "INDIVIDUAL TEST RESULTS:"
]

for test in report["tests"]:
    details.append(
        f"{test['result'].upper()}: {test['name']}"
    )

    if test.get("failure_message"):
        details.append(
            f"Failure: {test['failure_message']}"
        )

message.set_content("\n".join(details))

with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login(sender, password)
    server.send_message(message)

print("Email report sent successfully.")
