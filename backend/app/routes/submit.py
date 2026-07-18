from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import get_settings
from app.content_loader import ContentError, load_quest, next_quest_id
from app.db import get_db
from app.executor import get_executor
from app.executor.base import TestCase
from app.models import Submission
from app.progress_service import apply_quest_completion, get_or_create_progress, progress_to_payload
from app.schemas import ReflectionPayload, SubmitRequest, SubmitResponse, TestResult
from app.xp import xp_for_rank

router = APIRouter()


@router.post("/submit", response_model=SubmitResponse)
async def submit_code(body: SubmitRequest, db: Session = Depends(get_db)):
    settings = get_settings()
    try:
        quest = load_quest(body.quest_id)
    except ContentError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    canon = quest.get("canon") or {}
    languages = canon.get("languages") or {}
    lang_meta = languages.get(body.language)
    if not lang_meta:
        raise HTTPException(status_code=400, detail=f"Language not supported for quest: {body.language}")

    function_name = lang_meta["function_name"]
    all_tests = canon.get("tests") or []
    if body.mode == "run":
        selected = [t for t in all_tests if not t.get("hidden", False)]
    else:
        selected = list(all_tests)

    if not selected:
        raise HTTPException(status_code=400, detail="No tests available for this mode")

    tests = [
        TestCase(
            id=t["id"],
            input=t["input"],
            expected=t["expected"],
            hidden=bool(t.get("hidden", False)),
        )
        for t in selected
    ]

    progress_row = get_or_create_progress(db, body.guest_id, settings.campaign_id)

    executor = get_executor()
    result = await executor.submit(body.source, body.language, function_name, tests)

    visible_results = [
        TestResult(
            id=r.id,
            passed=r.passed,
            hidden=r.hidden,
            stdout=r.stdout,
            stderr=r.stderr,
            expected=None if r.hidden else r.expected,
            actual=None if r.hidden else r.actual,
            error=r.error,
        )
        for r in result.results
    ]

    reflection = None
    progress_payload = progress_to_payload(progress_row)

    if body.mode == "submit" and result.passed:
        completed_before = set(progress_payload.completed_quest_ids)
        first_time = body.quest_id not in completed_before
        rank = canon.get("difficulty_rank") or "explorer"
        xp_award = xp_for_rank(rank) if first_time else 0
        nxt = next_quest_id(body.quest_id)
        story = quest.get("story") or {}
        refl = canon.get("reflection") or {}

        progress_payload = apply_quest_completion(
            db,
            guest_id=body.guest_id,
            campaign_id=settings.campaign_id,
            quest_id=body.quest_id,
            language=body.language,
            xp_award=xp_award,
            next_id=nxt,
        )
        reflection = ReflectionPayload(
            success_line=story.get("success_line") or "Case closed.",
            pattern_reveal_name=canon.get("pattern_reveal_name") or "",
            why=(refl.get("why") or ""),
            reflection_flavor=story.get("reflection_flavor") or "",
            xp_awarded=xp_award,
            next_quest_id=nxt,
        )

    db.add(
        Submission(
            guest_id=body.guest_id,
            quest_id=body.quest_id,
            language=body.language,
            mode=body.mode,
            passed=result.passed,
        )
    )
    db.commit()

    return SubmitResponse(
        status=result.status,
        passed=result.passed,
        failed=result.failed,
        results=visible_results,
        reflection=reflection,
        progress=progress_payload,
    )
