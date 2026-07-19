from __future__ import annotations

import asyncio
import json
from typing import Any

import httpx

from app.config import Settings, get_settings
from app.executor.base import CaseResult, CodeExecutor, ExecutionResult, TestCase
from app.executor.harness import build_harness

# Judge0 CE language ids (v1.13.x)
LANGUAGE_IDS: dict[str, int] = {
    "python": 71,  # Python 3.8.1
    "javascript": 63,  # Node.js 12.14.0
    "typescript": 74,  # TypeScript 3.7.4
}


class Judge0Executor(CodeExecutor):
    def __init__(self, base_url: str | None = None) -> None:
        settings = get_settings()
        self.base_url = (base_url or settings.judge0_base_url).rstrip("/")
        self._headers = self._build_headers(settings)

    @staticmethod
    def _build_headers(settings: Settings) -> dict[str, str]:
        key = (settings.judge0_rapidapi_key or "").strip()
        if not key:
            return {}
        return {
            "X-RapidAPI-Key": key,
            "X-RapidAPI-Host": settings.judge0_rapidapi_host,
        }

    async def submit(
        self,
        source: str,
        language: str,
        function_name: str,
        tests: list[TestCase],
    ) -> ExecutionResult:
        if language not in LANGUAGE_IDS:
            return ExecutionResult(
                status="error",
                passed=False,
                failed=len(tests),
                results=[
                    CaseResult(
                        id=t.id,
                        passed=False,
                        hidden=t.hidden,
                        expected=t.expected,
                        error=f"Unsupported language: {language}",
                    )
                    for t in tests
                ],
            )

        payload_tests = [
            {"id": t.id, "input": t.input, "expected": t.expected} for t in tests
        ]
        wrapped = build_harness(source, language, function_name, payload_tests)
        language_id = LANGUAGE_IDS[language]

        try:
            raw = await self._create_and_wait(wrapped, language_id)
        except Exception as exc:
            return ExecutionResult(
                status="error",
                passed=False,
                failed=len(tests),
                stderr=str(exc),
                results=[
                    CaseResult(
                        id=t.id,
                        passed=False,
                        hidden=t.hidden,
                        expected=t.expected,
                        error=str(exc),
                    )
                    for t in tests
                ],
            )

        stdout = raw.get("stdout") or ""
        stderr = raw.get("stderr") or ""
        compile_out = raw.get("compile_output") or ""
        message = raw.get("message") or ""
        status_desc = (raw.get("status") or {}).get("description") or "Unknown"

        parsed = self._parse_results(stdout)
        if parsed is None:
            err = stderr or compile_out or message or status_desc
            return ExecutionResult(
                status="error",
                passed=False,
                failed=len(tests),
                stdout=stdout,
                stderr=err,
                results=[
                    CaseResult(
                        id=t.id,
                        passed=False,
                        hidden=t.hidden,
                        expected=t.expected,
                        error=err or "Harness produced no results",
                        stdout=stdout,
                        stderr=stderr,
                    )
                    for t in tests
                ],
            )

        by_id = {r["id"]: r for r in parsed}
        results: list[CaseResult] = []
        failed = 0
        for t in tests:
            row = by_id.get(t.id)
            if not row:
                failed += 1
                results.append(
                    CaseResult(
                        id=t.id,
                        passed=False,
                        hidden=t.hidden,
                        expected=t.expected,
                        error="Missing result from harness",
                    )
                )
                continue
            ok = bool(row.get("passed"))
            if not ok:
                failed += 1
            results.append(
                CaseResult(
                    id=t.id,
                    passed=ok,
                    hidden=t.hidden,
                    expected=row.get("expected", t.expected),
                    actual=row.get("actual"),
                    error=row.get("error"),
                    stdout=stdout if not ok else None,
                    stderr=stderr if not ok else None,
                )
            )

        return ExecutionResult(
            status="ok" if failed == 0 else "failed",
            passed=failed == 0,
            failed=failed,
            results=results,
            stdout=stdout,
            stderr=stderr or None,
        )

    async def _create_and_wait(self, source: str, language_id: int) -> dict[str, Any]:
        body = {
            "source_code": source,
            "language_id": language_id,
            "stdin": "",
        }
        async with httpx.AsyncClient(timeout=120.0, headers=self._headers) as client:
            # Prefer async create + poll; wait=true can hang on TypeScript compiles.
            resp = await client.post(
                f"{self.base_url}/submissions",
                json=body,
                params={"base64_encoded": "false", "wait": "false"},
            )
            resp.raise_for_status()
            token = resp.json()["token"]
            return await self._poll(client, token)

    async def _poll(self, client: httpx.AsyncClient, token: str) -> dict[str, Any]:
        for _ in range(90):
            resp = await client.get(
                f"{self.base_url}/submissions/{token}",
                params={"base64_encoded": "false"},
            )
            resp.raise_for_status()
            data = resp.json()
            status_id = (data.get("status") or {}).get("id", 0)
            if status_id > 2:
                return data
            await asyncio.sleep(0.5)
        raise TimeoutError("Judge0 submission timed out")

    def _parse_results(self, stdout: str) -> list[dict[str, Any]] | None:
        for line in reversed((stdout or "").splitlines()):
            line = line.strip()
            if line.startswith("PF_RESULTS:"):
                payload = line[len("PF_RESULTS:") :]
                try:
                    data = json.loads(payload)
                except json.JSONDecodeError:
                    return None
                if isinstance(data, list):
                    return data
        return None
