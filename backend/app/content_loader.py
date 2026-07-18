from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import yaml

from app.config import get_settings


class ContentError(Exception):
    pass


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise ContentError(f"Missing content file: {path}")
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ContentError(f"Invalid YAML object: {path}")
    return data


def campaign_dir(campaign_id: str) -> Path:
    return get_settings().content_root / "campaigns" / campaign_id


def load_campaign(campaign_id: str) -> dict[str, Any]:
    root = campaign_dir(campaign_id)
    campaign = _load_yaml(root / "campaign.yaml")
    chapters: list[dict[str, Any]] = []
    chapters_root = root / "chapters"
    if not chapters_root.exists():
        raise ContentError(f"No chapters for campaign {campaign_id}")

    for chapter_path in sorted(chapters_root.iterdir()):
        if not chapter_path.is_dir():
            continue
        chapter = _load_yaml(chapter_path / "chapter.yaml")
        quests_meta: list[dict[str, Any]] = []
        quests_dir = chapter_path / "quests"
        if quests_dir.exists():
            for quest_file in sorted(quests_dir.glob("*.yaml")):
                quest = _load_yaml(quest_file)
                quests_meta.append(
                    {
                        "id": quest["id"],
                        "order": quest.get("order", 0),
                        "title": quest.get("canon", {}).get("title", quest["id"]),
                        "beat_id": quest.get("beat_id"),
                        "difficulty_rank": quest.get("canon", {}).get("difficulty_rank"),
                    }
                )
        quests_meta.sort(key=lambda q: q["order"])
        chapter["quests"] = quests_meta
        chapters.append(chapter)

    chapters.sort(key=lambda c: c.get("order", 0))
    campaign["chapters"] = chapters
    return campaign


def load_quest(quest_id: str, campaign_id: str | None = None) -> dict[str, Any]:
    settings = get_settings()
    cid = campaign_id or settings.campaign_id
    root = campaign_dir(cid)
    matches = list(root.glob(f"chapters/*/quests/{quest_id}.yaml"))
    if not matches:
        raise ContentError(f"Quest not found: {quest_id}")
    return _load_yaml(matches[0])


def public_quest_payload(quest: dict[str, Any]) -> dict[str, Any]:
    """Strip hidden tests and hints for client consumption."""
    data = deepcopy(quest)
    canon = data.get("canon", {})
    tests = canon.get("tests", [])
    public_tests = []
    for t in tests:
        if t.get("hidden", False):
            continue
        public_tests.append(
            {
                "id": t.get("id"),
                "input": t.get("input"),
                "expected": t.get("expected"),
                "hidden": False,
            }
        )
    canon["tests"] = public_tests
    canon.pop("hints", None)
    data["canon"] = canon
    return data


def first_quest_id(campaign_id: str) -> str | None:
    campaign = load_campaign(campaign_id)
    for chapter in campaign.get("chapters", []):
        quests = chapter.get("quests") or []
        if quests:
            return quests[0]["id"]
    return None


def next_quest_id(quest_id: str, campaign_id: str | None = None) -> str | None:
    settings = get_settings()
    cid = campaign_id or settings.campaign_id
    campaign = load_campaign(cid)
    ordered: list[str] = []
    for chapter in campaign.get("chapters", []):
        for q in chapter.get("quests") or []:
            ordered.append(q["id"])
    try:
        idx = ordered.index(quest_id)
    except ValueError:
        return None
    if idx + 1 < len(ordered):
        return ordered[idx + 1]
    return None
