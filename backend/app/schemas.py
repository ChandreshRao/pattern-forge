from typing import Any, Literal

from pydantic import BaseModel, EmailStr, Field


Language = Literal["python", "javascript", "typescript"]
SubmitMode = Literal["run", "submit"]


class ProgressPayload(BaseModel):
    user_id: str | None = None
    campaign_id: str
    xp: int = 0
    unlocked_quest_ids: list[str] = Field(default_factory=list)
    completed_quest_ids: list[str] = Field(default_factory=list)
    last_language: str | None = None
    ephemeral: bool = False


class AuthRegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class AuthLoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthUser(BaseModel):
    id: str
    email: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: AuthUser


class SubmitRequest(BaseModel):
    guest_id: str | None = None
    quest_id: str
    language: Language
    source: str
    mode: SubmitMode = "submit"
    # Guest ephemeral session snapshot (ignored when authenticated)
    xp: int | None = None
    unlocked_quest_ids: list[str] | None = None
    completed_quest_ids: list[str] | None = None


class TestResult(BaseModel):
    id: str
    passed: bool
    hidden: bool = False
    stdout: str | None = None
    stderr: str | None = None
    expected: Any | None = None
    actual: Any | None = None
    error: str | None = None


class ReflectionPayload(BaseModel):
    success_line: str
    pattern_reveal_name: str
    why: str
    reflection_flavor: str
    xp_awarded: int
    next_quest_id: str | None = None


class SubmitResponse(BaseModel):
    status: str
    passed: bool
    failed: int
    results: list[TestResult]
    reflection: ReflectionPayload | None = None
    progress: ProgressPayload | None = None


class HintLevel(BaseModel):
    level: int
    text: str


class HintsResponse(BaseModel):
    quest_id: str
    hints: list[HintLevel]


class CodexEntry(BaseModel):
    pattern_id: str
    pattern_reveal_name: str
    why: str
    quest_id: str


class CodexResponse(BaseModel):
    patterns: list[CodexEntry]
