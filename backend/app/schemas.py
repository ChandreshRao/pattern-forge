from typing import Any, Literal

from pydantic import BaseModel, Field


Language = Literal["python", "javascript", "typescript"]
SubmitMode = Literal["run", "submit"]


class ProgressPayload(BaseModel):
    guest_id: str
    campaign_id: str
    xp: int = 0
    unlocked_quest_ids: list[str] = Field(default_factory=list)
    completed_quest_ids: list[str] = Field(default_factory=list)
    last_language: str | None = None


class SubmitRequest(BaseModel):
    guest_id: str
    quest_id: str
    language: Language
    source: str
    mode: SubmitMode = "submit"


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
