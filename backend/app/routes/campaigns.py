from fastapi import APIRouter, HTTPException

from app.content_loader import ContentError, load_campaign

router = APIRouter()


@router.get("/campaigns/{campaign_id}")
def get_campaign(campaign_id: str):
    try:
        return load_campaign(campaign_id)
    except ContentError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
