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
- Phase 1a locked: `two_sum`, `contains_duplicate`, `valid_anagram` (see `docs/01_PRD.md`).
- Note `refer_problem` path on the quest.

### 2. Write canon first

In the quest YAML `canon` key (schema: `docs/05_CONTENT_ENGINE.md`):

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

Using `docs/themes/detective_academy.md` lexicon only:

- `hook`, `briefing`, `objective_in_world`, `success_line`, `reflection_flavor`

Checks:

- No banned spoiler terms / pattern names in pre-solve slots
- No fake I/O in prose
- No new edge cases not in `canon.tests`
- Teaching stays in `canon.reflection`; flavor stays atmospheric

### 5. Wire campaign

- Set `order`, `chapter_id`, `theme_id: detective_academy`
- Register quest in chapter manifest when that file exists

### 6. Validate

- [ ] Examples ⊆ tests
- [ ] Test count meets phase minimum
- [ ] Pre-solve story passes spoiler check against theme banned list
- [ ] Beat exists in story bible
- [ ] Starters are stubs in all three languages

## References

- `docs/CONTENT_GUIDE.md`
- `docs/05_CONTENT_ENGINE.md`
- `docs/STORY_BIBLE.md`
- `docs/themes/detective_academy.md`
- `docs/06_AI_STRATEGY.md`
