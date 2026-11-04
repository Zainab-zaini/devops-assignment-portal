from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from pathlib import Path

from app.database import (
    get_connection,
    initialize_database
)

from app.schemas import (
    SubmissionCreate,
    SubmissionResponse
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield


app = FastAPI(
    title="Assignment Submission Portal",
    description=(
        "A DevOps-enabled assignment submission "
        "management system with automated validation."
    ),
    version="1.0.0",
    lifespan=lifespan
)


STATIC_DIR = Path(__file__).parent / "static"


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "application": "Assignment Submission Portal"
    }


@app.post(
    "/api/submissions",
    response_model=SubmissionResponse,
    status_code=201
)
def create_submission(submission: SubmissionCreate):
    raise HTTPException(
        status_code=500,
        detail="Temporary failure for CI demonstration."
    )

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO submissions (
                student_name,
                registration_number,
                assignment_title,
                submission_url
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                submission.student_name,
                submission.registration_number,
                submission.assignment_title,
                submission.submission_url
            )
        )

        connection.commit()

        saved = connection.execute(
            """
            SELECT * FROM submissions
            WHERE id = ?
            """,
            (cursor.lastrowid,)
        ).fetchone()

        return dict(saved)

    except Exception:
        connection.rollback()

        raise HTTPException(
            status_code=500,
            detail="Unable to save submission."
        )

    finally:
        connection.close()


@app.get("/api/submissions")
def get_submissions():

    connection = get_connection()

    try:
        records = connection.execute(
            """
            SELECT * FROM submissions
            ORDER BY id DESC
            """
        ).fetchall()

        return {
            "total": len(records),
            "submissions": [
                dict(record) for record in records
            ]
        }

    finally:
        connection.close()


app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static"
)