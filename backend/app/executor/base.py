from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class TestCase:
    id: str
    input: dict[str, Any]
    expected: Any
    hidden: bool = False


@dataclass
class CaseResult:
    id: str
    passed: bool
    hidden: bool = False
    stdout: str | None = None
    stderr: str | None = None
    expected: Any | None = None
    actual: Any | None = None
    error: str | None = None


@dataclass
class ExecutionResult:
    status: str
    passed: bool
    failed: int
    results: list[CaseResult] = field(default_factory=list)
    stdout: str | None = None
    stderr: str | None = None
    time_ms: float | None = None


class CodeExecutor(ABC):
    @abstractmethod
    async def submit(
        self,
        source: str,
        language: str,
        function_name: str,
        tests: list[TestCase],
    ) -> ExecutionResult:
        raise NotImplementedError
