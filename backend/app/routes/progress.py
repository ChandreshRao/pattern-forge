from fastapi import APIRouter, Depends, HTTPException

from app.auth import get_current_user
from app.config import get_settings
from app.db import get_db
from app.models import User
from app.progress_service import get_or_create_progress, progress_to_payload, put_progress
from app.schemas import ProgressPayload
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/progress", response_model=ProgressPayload)
def get_my_progress(
    campaign_id: str | None = None,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    settings = get_settings()
    cid = campaign_id or settings.campaign_id
    row = get_or_create_progress(db, user.id, cid)
    return progress_to_payload(row)


@router.put("/progress", response_model=ProgressPayload)
def upsert_my_progress(
    body: ProgressPayload,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if body.user_id and body.user_id != user.id:
        raise HTTPException(status_code=400, detail="user_id mismatch")
    settings = get_settings()
    payload = body.model_copy(
        update={"user_id": user.id, "campaign_id": body.campaign_id or settings.campaign_id, "ephemeral": False}
    )
    return put_progress(db, user.id, payload)
