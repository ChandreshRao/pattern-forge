from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import get_settings
from app.db import get_db
from app.progress_service import get_or_create_progress, progress_to_payload, put_progress
from app.schemas import ProgressPayload

router = APIRouter()


@router.get("/progress/{guest_id}", response_model=ProgressPayload)
def get_progress(guest_id: str, campaign_id: str | None = None, db: Session = Depends(get_db)):
    settings = get_settings()
    cid = campaign_id or settings.campaign_id
    row = get_or_create_progress(db, guest_id, cid)
    return progress_to_payload(row)


@router.put("/progress/{guest_id}", response_model=ProgressPayload)
def upsert_progress(guest_id: str, body: ProgressPayload, db: Session = Depends(get_db)):
    if body.guest_id != guest_id:
        raise HTTPException(status_code=400, detail="guest_id mismatch")
    return put_progress(db, body)
