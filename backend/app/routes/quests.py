from fastapi import APIRouter, HTTPException

from app.content_loader import ContentError, load_quest, public_quest_payload

router = APIRouter()


@router.get("/quests/{quest_id}")
def get_quest(quest_id: str):
    try:
        quest = load_quest(quest_id)
        return public_quest_payload(quest)
    except ContentError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
