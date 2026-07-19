---
name: author-quest
description: >-
  Author a PatternForge quest from refer_problems into canon + story YAML.
  Use when adding or editing quests, campaign content, story beats, or theme copy.
---

# Author a PatternForge quest

## When to use

Adding/editing files under `content/`, expanding Chapter 1, or rewriting Detective Academy story slots.

## Steps

### 1. Pick source

- Choose a file under `refer_problems/`.
- Chapter 1 first three: `two_sum`, `contains_duplicate`, `valid_anagram` (see `docs/CONTENT.md`).
- Note `refer_problem` path on the quest.

### 2. Write canon first

In the quest YAML `canon` key (schema: `docs/CONTENT.md`):

- `pattern_id`, `pattern_reveal_name`, `recognition_signals`
- Starters for `python`, `javascript`, `typescript`
- `examples` (public) and `tests` (hidden + public); Phase 1a ≥8 tests, 1b → 15–20
- Hint ladder levels 1–5 (no full solution in 1–2)
- `reflection.why`, `common_mistakes`, `complexity`
- `interview_reference`

Do not invent requirements absent from the source problem.

### 3. Assign beat

- Read `docs/STORY_BIBLE.md`.
- Set `beat_id` (B1–B3 for 1a; B4–B10 for 1b).
- Ensure the beat advances the case; update the bible if you introduce new continuity.

### 4. Fill story slots

Delegate to `.cursor/skills/write-quest-story/SKILL.md` (brief → slots → `scripts/validate_story.py`).

Do not invent story here if that skill is available — keep this skill focused on canon + campaign wiring.

### 5. Wire campaign

- Set `order`, `chapter_id`, `theme_id: detective_academy`
- Register quest in chapter manifest when that file exists

### 6. Validate

- [ ] Examples ⊆ tests
- [ ] Test count meets phase minimum
- [ ] `python scripts/validate_story.py <quest.yaml>` exits 0
- [ ] Beat exists in story bible
- [ ] Starters are stubs in all three languages

## References

- `docs/CONTENT.md`
- `docs/STORY_BIBLE.md`
- `docs/themes/detective_academy.md`
- `content/themes/detective_academy.yaml`
- `.cursor/skills/write-quest-story/SKILL.md`
- `scripts/validate_story.py`
