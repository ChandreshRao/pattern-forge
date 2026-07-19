#!/usr/bin/env python3
"""Validate PatternForge quest story slots against theme + story bible.

Usage:
  python scripts/validate_story.py path/to/quest.yaml

Exit 0 only when every check PASSes. Paste full stdout as proof of completion
when using the write-quest-story skill.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    print("FAIL  dependency: PyYAML is required (pip install pyyaml)", file=sys.stderr)
    sys.exit(2)

REPO_ROOT = Path(__file__).resolve().parents[1]
STORY_BIBLE = REPO_ROOT / "docs" / "STORY_BIBLE.md"
THEMES_DIR = REPO_ROOT / "content" / "themes"

PRE_SOLVE_DEFAULT = (
    "hook",
    "briefing",
    "objective_in_world",
    "success_line",
)
ALL_SLOTS_DEFAULT = PRE_SOLVE_DEFAULT + ("reflection_flavor",)

# Fake I/O patterns in prose (UI owns examples).
FAKE_IO_PATTERNS = [
    (re.compile(r"\[[^\]]*(?:,\s*[^\]]+){1,}\]"), "bracketed array literal"),
    (re.compile(r"\s->\s|\s=>\s"), "arrow mapping (-> or =>)"),
    (
        re.compile(
            r"\b(input|output|returns?|expected)\s*[:=]",
            re.IGNORECASE,
        ),
        "input/output/returns-style phrasing",
    ),
]

COMPLEXITY_O_RE = re.compile(r"\bO\s*\(\s*[a-z0-9+\-*/\s]+\s*\)", re.IGNORECASE)

# Role titles that introduce an NPC name: "Detective Lex", "Agent Vega".
NPC_TITLE_RE = re.compile(
    r"\b("
    r"Captain|Archivist|Detective|Agent|Officer|Sergeant|Lieutenant|"
    r"Inspector|Chief|Commissioner"
    r")\s+([A-Z][a-z]{1,})\b"
)

# Two consecutive Title-Case tokens that look like a full name (e.g. "Captain Mora").
FULL_NAME_RE = re.compile(r"\b([A-Z][a-z]{1,})\s+([A-Z][a-z]{1,})\b")


class Report:
    def __init__(self) -> None:
        self.rows: list[tuple[str, str, str]] = []

    def ok(self, name: str, detail: str = "") -> None:
        self.rows.append(("PASS", name, detail))

    def fail(self, name: str, detail: str) -> None:
        self.rows.append(("FAIL", name, detail))

    @property
    def failed(self) -> bool:
        return any(status == "FAIL" for status, _, _ in self.rows)

    def print(self) -> None:
        width = max((len(n) for _, n, _ in self.rows), default=10)
        for status, name, detail in self.rows:
            line = f"{status:4}  {name:<{width}}  {detail}".rstrip()
            print(line)
        print()
        if self.failed:
            n = sum(1 for s, _, _ in self.rows if s == "FAIL")
            print(f"RESULT: FAIL ({n} check(s) failed)")
        else:
            print("RESULT: PASS")


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def sentence_count(text: str) -> int:
    parts = re.split(r"[.!?]+", text.strip())
    return sum(1 for p in parts if p.strip())


def word_count(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text))


def term_pattern(term: str) -> re.Pattern[str]:
    """Word-boundary-ish match for multi-word or single-token banned terms."""
    escaped = re.escape(term.strip())
    # Allow flexible whitespace between words.
    escaped = re.sub(r"\\\s+", r"\\s+", escaped)
    return re.compile(rf"(?<!\w){escaped}(?!\w)", re.IGNORECASE)


def find_banned(text: str, terms: list[str]) -> list[str]:
    hits: list[str] = []
    for term in terms:
        if term_pattern(term).search(text):
            hits.append(term)
    return hits


def beat_exists_in_bible(beat_id: str, bible_text: str) -> bool:
    """Accept #### B1 headings or table rows like | B4 | ..."""
    bid = beat_id.strip()
    if not bid:
        return False
    heading = re.compile(rf"^####\s+{re.escape(bid)}\b", re.MULTILINE)
    table = re.compile(rf"\|\s*{re.escape(bid)}\s*\|")
    return bool(heading.search(bible_text) or table.search(bible_text))


def pattern_id_variants(pattern_id: str) -> list[str]:
    if not pattern_id:
        return []
    raw = pattern_id.strip()
    spaced = raw.replace("_", " ")
    dashed = raw.replace("_", "-")
    return list({raw, spaced, dashed})


def find_cast_violations(text: str, allowed_full_names: set[str], allowed_tokens: set[str]) -> list[str]:
    """Catch invented NPCs without flagging sentence-initial capitals.

    Flags:
    - Title + Surname not in the theme cast (e.g. Detective Lex)
    - Two-token Title Case names not equal to an allowed full name
    """
    hits: list[str] = []
    for m in NPC_TITLE_RE.finditer(text):
        title, surname = m.group(1), m.group(2)
        full = f"{title} {surname}"
        if full in allowed_full_names:
            continue
        if title in allowed_tokens and surname in allowed_tokens:
            continue
        # "Detective Academy" is the institution, not an NPC.
        if title == "Detective" and surname == "Academy":
            continue
        hits.append(full)

    for m in FULL_NAME_RE.finditer(text):
        full = f"{m.group(1)} {m.group(2)}"
        if full in allowed_full_names:
            continue
        # Skip institution / place-like pairs already covered elsewhere.
        if full in {"Detective Academy"}:
            continue
        # If either token is a known cast token pair matching allowlist full name, ok.
        # Otherwise only flag if first token looks like a role/title or both are unknown cast.
        first, second = m.group(1), m.group(2)
        role_titles = {
            "Captain",
            "Archivist",
            "Detective",
            "Agent",
            "Officer",
            "Sergeant",
            "Lieutenant",
            "Inspector",
            "Chief",
            "Commissioner",
        }
        if first in role_titles and full not in allowed_full_names:
            if full not in hits:
                hits.append(full)
        elif first not in allowed_tokens and second not in allowed_tokens:
            # Two unknown proper nouns in a row — likely invented name.
            if full not in hits:
                hits.append(full)
    return hits


def validate_quest(quest_path: Path, report: Report) -> None:
    try:
        quest = load_yaml(quest_path)
    except Exception as exc:  # noqa: BLE001
        report.fail("quest_load", f"cannot parse {quest_path}: {exc}")
        return

    if not isinstance(quest, dict):
        report.fail("quest_load", "root must be a mapping")
        return
    report.ok("quest_load", str(quest_path))

    theme_id = quest.get("theme_id")
    beat_id = quest.get("beat_id")
    if not theme_id or not isinstance(theme_id, str):
        report.fail("theme_id", "missing or not a string")
        theme: dict[str, Any] = {}
    else:
        theme_path = THEMES_DIR / f"{theme_id}.yaml"
        if not theme_path.is_file():
            report.fail("theme_load", f"missing theme file {theme_path}")
            theme = {}
        else:
            try:
                theme = load_yaml(theme_path)
                if not isinstance(theme, dict):
                    report.fail("theme_load", "theme root must be a mapping")
                    theme = {}
                else:
                    report.ok("theme_load", str(theme_path))
            except Exception as exc:  # noqa: BLE001
                report.fail("theme_load", f"cannot parse theme: {exc}")
                theme = {}

    if not beat_id or not isinstance(beat_id, str):
        report.fail("beat_id", "missing or not a string")
    elif not STORY_BIBLE.is_file():
        report.fail("beat_exists", f"story bible missing: {STORY_BIBLE}")
    else:
        bible = STORY_BIBLE.read_text(encoding="utf-8")
        if beat_exists_in_bible(beat_id, bible):
            report.ok("beat_exists", beat_id)
        else:
            report.fail(
                "beat_exists",
                f"{beat_id} not found as #### heading or table row in STORY_BIBLE.md",
            )

    story = quest.get("story")
    if not isinstance(story, dict):
        report.fail("story_schema", "story key missing or not a mapping")
        return

    all_slots = theme.get("all_story_slots") or list(ALL_SLOTS_DEFAULT)
    pre_solve = theme.get("pre_solve_slots") or list(PRE_SOLVE_DEFAULT)
    budgets = theme.get("slot_budgets") or {}

    missing = [s for s in all_slots if s not in story]
    empty = [
        s
        for s in all_slots
        if s in story and (not isinstance(story.get(s), str) or not str(story.get(s)).strip())
    ]
    if missing or empty:
        bits = []
        if missing:
            bits.append(f"missing={missing}")
        if empty:
            bits.append(f"empty={empty}")
        report.fail("story_schema", "; ".join(bits))
    else:
        report.ok("story_schema", f"slots={list(all_slots)}")

    # Slot budgets
    for slot in all_slots:
        text = story.get(slot)
        if not isinstance(text, str) or not text.strip():
            continue
        budget = budgets.get(slot) or {}
        sc = sentence_count(text)
        wc = word_count(text)
        problems: list[str] = []
        if "min_sentences" in budget and sc < budget["min_sentences"]:
            problems.append(f"sentences={sc} < min {budget['min_sentences']}")
        if "max_sentences" in budget and sc > budget["max_sentences"]:
            problems.append(f"sentences={sc} > max {budget['max_sentences']}")
        if "max_words" in budget and wc > budget["max_words"]:
            problems.append(f"words={wc} > max {budget['max_words']}")
        check_name = f"budget_{slot}"
        if problems:
            report.fail(check_name, "; ".join(problems))
        else:
            report.ok(check_name, f"sentences={sc} words={wc}")

    banned = list(theme.get("banned_spoiler_terms") or [])
    banned_complexity = list(theme.get("banned_complexity_phrases") or [])
    canon = quest.get("canon") if isinstance(quest.get("canon"), dict) else {}
    reveal = str(canon.get("pattern_reveal_name") or "").strip()
    pattern_id = str(canon.get("pattern_id") or "").strip()
    spoiler_extra = []
    if reveal:
        spoiler_extra.append(reveal)
        spoiler_extra.extend(pattern_id_variants(reveal.replace(" ", "_")))
    spoiler_extra.extend(pattern_id_variants(pattern_id))
    spoiler_terms = banned + [t for t in spoiler_extra if t]

    # Spoilers in pre-solve
    spoiler_hits: list[str] = []
    for slot in pre_solve:
        text = story.get(slot)
        if not isinstance(text, str):
            continue
        hits = find_banned(text, spoiler_terms)
        for h in hits:
            spoiler_hits.append(f"{slot}:{h}")
    if spoiler_hits:
        report.fail("spoilers_pre_solve", ", ".join(spoiler_hits))
    else:
        report.ok("spoilers_pre_solve", "no banned / reveal / pattern_id terms")

    # Fake I/O in pre-solve
    io_hits: list[str] = []
    for slot in pre_solve:
        text = story.get(slot)
        if not isinstance(text, str):
            continue
        for pat, label in FAKE_IO_PATTERNS:
            if pat.search(text):
                io_hits.append(f"{slot}:{label}")
    if io_hits:
        report.fail("no_fake_io", ", ".join(io_hits))
    else:
        report.ok("no_fake_io", "pre-solve clean")

    # Teaching / complexity in reflection_flavor
    flavor = story.get("reflection_flavor")
    flavor_hits: list[str] = []
    if isinstance(flavor, str):
        if COMPLEXITY_O_RE.search(flavor):
            flavor_hits.append("O(...) notation")
        flavor_hits.extend(find_banned(flavor, banned_complexity))
        # Also ban reveal name in flavor? Plan says teaching stays in canon;
        # complexity specifically. Allow pattern reveal name post-solve in flavor? 
        # Plan: "No teaching in flavor: reflection_flavor has no complexity notation"
        # So only complexity for this check.
    if flavor_hits:
        report.fail("no_teaching_in_flavor", ", ".join(flavor_hits))
    else:
        report.ok("no_teaching_in_flavor", "reflection_flavor clean")

    # Cast lock — invented NPCs only (not sentence-initial capitals)
    allowed_tokens = set(theme.get("character_name_tokens") or [])
    allowed_full_names: set[str] = set()
    for ch in theme.get("characters") or []:
        if isinstance(ch, dict) and ch.get("name"):
            full = str(ch["name"]).strip()
            allowed_full_names.add(full)
            for part in full.split():
                allowed_tokens.add(part)

    cast_hits: list[str] = []
    for slot in all_slots:
        text = story.get(slot)
        if not isinstance(text, str):
            continue
        for name in find_cast_violations(text, allowed_full_names, allowed_tokens):
            cast_hits.append(f"{slot}:{name}")
    if cast_hits:
        report.fail("cast_lock", f"unknown NPCs {cast_hits}")
    else:
        report.ok("cast_lock", "only theme cast")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("quest_yaml", type=Path, help="Path to quest YAML file")
    args = parser.parse_args(argv)

    quest_path = args.quest_yaml
    if not quest_path.is_file():
        print(f"FAIL  quest_file  not found: {quest_path}", file=sys.stderr)
        return 2

    report = Report()
    validate_quest(quest_path.resolve(), report)
    report.print()
    return 1 if report.failed else 0


if __name__ == "__main__":
    sys.exit(main())
