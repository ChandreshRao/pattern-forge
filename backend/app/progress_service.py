from __future__ import annotations

import json
from datetime import datetime

from sqlalchemy.orm import Session

from app.content_loader import first_quest_id
from app.models import Guest, Progress
from app.schemas import ProgressPayload


def _ensure_guest(db: Session, guest_id: str) -> Guest:
    guest = db.get(Guest, guest_id)
    if guest is None:
        guest = Guest(id=guest_id)
        db.add(guest)
        db.flush()
    return guest


def default_unlocked(campaign_id: str) -> list[str]:
    first = first_quest_id(campaign_id)
    return [first] if first else []


def get_or_create_progress(db: Session, guest_id: str, campaign_id: str) -> Progress:
    _ensure_guest(db, guest_id)
    row = db.get(Progress, {"guest_id": guest_id, "campaign_id": campaign_id})
    if row is None:
        unlocked = default_unlocked(campaign_id)
        row = Progress(
            guest_id=guest_id,
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
        guest_id=row.guest_id,
        campaign_id=row.campaign_id,
        xp=row.xp,
        unlocked_quest_ids=json.loads(row.unlocked_quest_ids_json or "[]"),
        completed_quest_ids=json.loads(row.completed_quest_ids_json or "[]"),
        last_language=row.last_language,
    )


def put_progress(db: Session, payload: ProgressPayload) -> ProgressPayload:
    _ensure_guest(db, payload.guest_id)
    row = db.get(Progress, {"guest_id": payload.guest_id, "campaign_id": payload.campaign_id})
    if row is None:
        row = Progress(
            guest_id=payload.guest_id,
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
    guest_id: str,
    campaign_id: str,
    quest_id: str,
    language: str,
    xp_award: int,
    next_id: str | None,
) -> ProgressPayload:
    row = get_or_create_progress(db, guest_id, campaign_id)
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
