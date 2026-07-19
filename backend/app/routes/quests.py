from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth import get_current_user_optional
from app.config import get_settings
from app.content_loader import ContentError, codex_entries_for_quests, hints_up_to, load_quest, public_quest_payload
from app.db import get_db
from app.models import User
from app.progress_service import get_or_create_progress, progress_to_payload
from app.schemas import CodexResponse, HintsResponse

router = APIRouter()


@router.get("/quests/{quest_id}")
def get_quest(quest_id: str):
    try:
        quest = load_quest(quest_id)
        return public_quest_payload(quest)
    except ContentError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/quests/{quest_id}/hints", response_model=HintsResponse)
def get_hints(quest_id: str, max_level: int = Query(default=1, ge=1, le=5)):
    try:
        quest = load_quest(quest_id)
    except ContentError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return HintsResponse(quest_id=quest_id, hints=hints_up_to(quest, max_level))


@router.get("/codex", response_model=CodexResponse)
def get_codex(
    completed: str | None = Query(default=None, description="Comma-separated quest ids (guest)"),
    user: User | None = Depends(get_current_user_optional),
    db: Session = Depends(get_db),
):
    settings = get_settings()
    if user is not None:
        row = get_or_create_progress(db, user.id, settings.campaign_id)
        completed_ids = progress_to_payload(row).completed_quest_ids
    else:
        completed_ids = [x.strip() for x in (completed or "").split(",") if x.strip()]
    return CodexResponse(patterns=codex_entries_for_quests(completed_ids, settings.campaign_id))
