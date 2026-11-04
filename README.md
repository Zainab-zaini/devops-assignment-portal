# Assignment Submission Portal — DevOps Lab Midterm

**Course:** DevOps for Cloud Computing (CSC418)  
**University:** COMSATS University Islamabad, Attock Campus

## 1. Project Overview

The Assignment Submission Portal is a FastAPI-based web application that allows students to submit assignments through GitHub or other submission URLs.

The project implements automated testing, Continuous Integration using GitHub Actions, and automatic delivery of JSON test reports to a local Windows computer.

## 2. Technologies Used

- Python 3.13
- FastAPI
- SQLite
- Pytest
- HTTPX
- Git and GitHub
- GitHub Actions
- Windows Self-Hosted Runner
- JSON reporting
- Python HTTP Server

## 3. Project Structure

```text
devops-assignment-portal/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── schemas.py
│   └── static/
│       └── index.html
│
├── receiver/
│   ├── receiver.py
│   └── send_report.py
│
├── tests/
│   └── test_submissions.py
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── requirements.txt
├── .gitignore
└── README.md
```

## 4. Installation

Clone the repository:

```bash
git clone https://github.com/Zainab-zaini/devops-assignment-portal.git
cd devops-assignment-portal
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 5. Run the Application

```bash
uvicorn app.main:app --reload
```

Open:

`http://127.0.0.1:8000`

API documentation:

`http://127.0.0.1:8000/docs`

## 6. Execute Automated Tests

```bash
pytest -v
```

Generate JSON test results:

```bash
pytest -v --json-report --json-report-file=test-results.json
```

## 7. Start the Local Report Receiver

Configure the authentication token in PowerShell:

```powershell
$env:REPORT_RECEIVER_TOKEN = "YOUR_SECRET_TOKEN"
```

Start the receiver:

```bash
python receiver/receiver.py
```

The receiver listens on:

`http://127.0.0.1:8765`

It automatically saves received reports as:

`test-report.json`

## 8. Continuous Integration

GitHub Actions automatically executes the test suite after every push.

The self-hosted Windows runner executes the workflow on the developer's computer.

The pipeline:
1. Checks out the repository.
2. Verifies Python.
3. Installs dependencies.
4. Executes automated tests.
5. Generates JSON test results.
6. Delivers the report to the local HTTP receiver.

## 9. Automated Testing

The project includes five automated test cases:

1. Valid assignment submission.
2. Missing registration number.
3. Invalid submission URL.
4. Application health check.
5. Empty submission list.

## 10. Failure Demonstration

The CI pipeline is demonstrated through three revisions:

- Successful execution with all tests passing.
- Deliberate submission endpoint failure resulting in a failed test.
- Correction of the defect followed by successful execution.

The local JSON report is automatically updated after each run.

## 11. Test Report Contents

The generated report includes:

- Repository name.
- Branch name.
- Commit SHA.
- Pipeline run identifier.
- Execution timestamp.
- Individual test results.
- Total, passed and failed test counts.
- Overall pipeline status.

## 12. Repository

GitHub: https://github.com/Zainab-zaini/devops-assignment-portal