from __future__ import annotations

import json
from datetime import datetime

from sqlalchemy.orm import Session

from app.content_loader import first_quest_id
from app.models import Progress
from app.schemas import ProgressPayload


def default_unlocked(campaign_id: str) -> list[str]:
    first = first_quest_id(campaign_id)
    return [first] if first else []


def ephemeral_progress(campaign_id: str) -> ProgressPayload:
    return ProgressPayload(
        user_id=None,
        campaign_id=campaign_id,
        xp=0,
        unlocked_quest_ids=default_unlocked(campaign_id),
        completed_quest_ids=[],
        last_language=None,
        ephemeral=True,
    )


def apply_ephemeral_completion(
    current: ProgressPayload,
    quest_id: str,
    language: str,
    xp_award: int,
    next_id: str | None,
) -> ProgressPayload:
    unlocked = set(current.unlocked_quest_ids)
    completed = set(current.completed_quest_ids)
    first_time = quest_id not in completed
    completed.add(quest_id)
    unlocked.add(quest_id)
    if next_id:
        unlocked.add(next_id)
    xp = int(current.xp or 0) + (xp_award if first_time else 0)
    return ProgressPayload(
        user_id=None,
        campaign_id=current.campaign_id,
        xp=xp,
        unlocked_quest_ids=sorted(unlocked),
        completed_quest_ids=sorted(completed),
        last_language=language,
        ephemeral=True,
    )


def get_or_create_progress(db: Session, user_id: str, campaign_id: str) -> Progress:
    row = db.get(Progress, {"user_id": user_id, "campaign_id": campaign_id})
    if row is None:
        unlocked = default_unlocked(campaign_id)
        row = Progress(
            user_id=user_id,
            campaign_id=campaign_id,
            xp=0,
            unlocked_quest_ids_json=json.dumps(unlocked),
            completed_quest_ids_json=json.dumps([]),
            last_language=None,
        )
        db.add(row)
        db.commit()
        db.refresh(row)
    return row


def progress_to_payload(row: Progress) -> ProgressPayload:
    return ProgressPayload(
        user_id=row.user_id,
        campaign_id=row.campaign_id,
        xp=row.xp,
        unlocked_quest_ids=json.loads(row.unlocked_quest_ids_json or "[]"),
        completed_quest_ids=json.loads(row.completed_quest_ids_json or "[]"),
        last_language=row.last_language,
        ephemeral=False,
    )


def put_progress(db: Session, user_id: str, payload: ProgressPayload) -> ProgressPayload:
    row = db.get(Progress, {"user_id": user_id, "campaign_id": payload.campaign_id})
    if row is None:
        row = Progress(
            user_id=user_id,
            campaign_id=payload.campaign_id,
            xp=payload.xp,
            unlocked_quest_ids_json=json.dumps(payload.unlocked_quest_ids),
            completed_quest_ids_json=json.dumps(payload.completed_quest_ids),
            last_language=payload.last_language,
        )
        db.add(row)
    else:
        row.xp = payload.xp
        row.unlocked_quest_ids_json = json.dumps(payload.unlocked_quest_ids)
        row.completed_quest_ids_json = json.dumps(payload.completed_quest_ids)
        row.last_language = payload.last_language
        row.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(row)
    return progress_to_payload(row)


def apply_quest_completion(
    db: Session,
    user_id: str,
    campaign_id: str,
    quest_id: str,
    language: str,
    xp_award: int,
    next_id: str | None,
) -> ProgressPayload:
    row = get_or_create_progress(db, user_id, campaign_id)
    unlocked = set(json.loads(row.unlocked_quest_ids_json or "[]"))
    completed = set(json.loads(row.completed_quest_ids_json or "[]"))

    first_time = quest_id not in completed
    completed.add(quest_id)
    unlocked.add(quest_id)
    if next_id:
        unlocked.add(next_id)

    if first_time:
        row.xp = int(row.xp or 0) + xp_award

    row.unlocked_quest_ids_json = json.dumps(sorted(unlocked))
    row.completed_quest_ids_json = json.dumps(sorted(completed))
    row.last_language = language
    row.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(row)
    return progress_to_payload(row)
