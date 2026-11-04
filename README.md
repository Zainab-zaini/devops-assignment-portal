# DevOps Assignment Submission Portal

A professional assignment submission portal developed for the CSC418 DevOps for Cloud Computing laboratory midterm at COMSATS University Islamabad, Attock Campus.

## Features

- Student assignment submission.
- Required-field validation.
- Submission URL validation.
- Persistent SQLite storage.
- Display of saved submissions.
- Automated testing with Pytest.
- Continuous Integration using GitHub Actions.
- Local HTTP test report receiver.
- Automatic JSON test report generation.

## Technology Stack

- Frontend: HTML, CSS, JavaScript
- Backend: Python, FastAPI
- Database: SQLite
- Testing: Pytest, HTTPX
- CI/CD: GitHub Actions
- Reporting: Python HTTP server and JSON

## Project Structure

```text
app/                  Application backend
app/static/           Frontend files
tests/                Automated tests
receiver/             Local report receiver
.github/workflows/    CI pipeline
requirements.txt      Dependencies
```

## Installation

Clone the repository:

```bash
git clone https://github.com/Zainab-zaini/devops-assignment-portal.git
cd devops-assignment-portal
```

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
uvicorn app.main:app --reload
```

Open:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs

## Execute Automated Tests

```bash
pytest -v
```

## Start Local Report Receiver

```bash
python receiver/receiver.py
```

The receiver will save automatically received test results as `test-report.json`.

## CI/CD

GitHub Actions automatically executes the automated test suite after repository pushes.

## Author

GitHub: https://github.com/Zainab-zaini

Course: CSC418 – DevOps for Cloud Computing

University: COMSATS University Islamabad, Attock Campus