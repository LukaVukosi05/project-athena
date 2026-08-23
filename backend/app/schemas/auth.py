"""Request and response contracts for account endpoints."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

GradeId = Literal["grade-8", "grade-9", "grade-10", "grade-11", "grade-12"]
CurriculumMode = Literal["CAPS", "IEB", "I'm not sure"]


class SignUpRequest(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    grade: GradeId
    curriculum_mode: CurriculumMode = "CAPS"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class UpdateMeRequest(BaseModel):
    first_name: str | None = Field(default=None, min_length=1, max_length=100)
    grade: GradeId | None = None
    curriculum_mode: CurriculumMode | None = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    email: EmailStr
    grade: GradeId
    curriculum_mode: CurriculumMode
    role: str
    is_premium: bool
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"
    user: UserResponse
