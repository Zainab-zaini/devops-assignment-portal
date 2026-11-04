from pydantic import BaseModel, Field, field_validator
from urllib.parse import urlsplit


class SubmissionCreate(BaseModel):

    student_name: str = Field(
        min_length=2,
        max_length=100
    )

    registration_number: str = Field(
        min_length=3,
        max_length=30
    )

    assignment_title: str = Field(
        min_length=3,
        max_length=150
    )

    submission_url: str = Field(
        min_length=10,
        max_length=2048
    )

    @field_validator(
        "student_name",
        "registration_number",
        "assignment_title"
    )
    @classmethod
    def validate_required_text(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("This field is required.")

        return value

    @field_validator("submission_url")
    @classmethod
    def validate_submission_url(cls, value):

        value = value.strip()

        try:
            parsed = urlsplit(value)

            if (
                parsed.scheme not in ("http", "https")
                or not parsed.hostname
                or "." not in parsed.hostname
                or any(char.isspace() for char in value)
            ):
                raise ValueError

            parsed.port

        except ValueError:
            raise ValueError(
                "Please enter a valid HTTP or HTTPS URL."
            )

        return value


class SubmissionResponse(BaseModel):
    id: int
    student_name: str
    registration_number: str
    assignment_title: str
    submission_url: str
    submitted_at: str