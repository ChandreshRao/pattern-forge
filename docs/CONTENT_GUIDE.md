# Content authoring guide

How to turn a `refer_problems/` stub into a PatternForge quest.

## Prerequisites

- Read `05_CONTENT_ENGINE.md` (schema)
- Read `STORY_BIBLE.md` (beats + continuity)
- Read `themes/detective_academy.md` (lexicon)
- Prefer skill: `.cursor/skills/author-quest/SKILL.md`

## Workflow

### 1. Pick the problem

From Blind-75 under `refer_problems/`. Phase 1a locked set:

1. `arrays/two_sum.py` → `q01_two_sum` / beat `B1`
2. `arrays/contains_duplicate.py` → `q02_contains_duplicate` / beat `B2`
3. `strings/valid_anagram.py` → `q03_valid_anagram` / beat `B3`

### 2. Freeze canon first

Copy educational truth before any story:

- Function signatures for Python, JS, TS
- Public examples (must match tests)
- Hidden tests (≥8 for 1a; aim 15–20 for 1b)
- `pattern_id` + `pattern_reveal_name`
- Recognition signals
- Hint ladder L1–L5 (facts only; no full solution at L1–L3)
- Reflection teaching: why, common mistakes, complexity
- Interview reference

**Do not** invent new algorithmic requirements that are not in the source problem.

### 3. Assign a story beat

Pick the next free beat in `STORY_BIBLE.md`. Continuity must advance the case — not reset to a random fable.

### 4. Fill story slots (theme only)

Using Detective Academy lexicon:

- `hook` — cold open
- `briefing` — what the academy needs
- `objective_in_world` — player-facing goal in world terms
- `success_line` — short win line
- `reflection_flavor` — atmospheric wrap (teaching stays in `canon.reflection`)

**Anti-hallucination:**

- Do not paraphrase fake I/O in story; UI shows `canon.examples`.
- Do not name the pattern/algorithm in pre-solve slots.
- Do not add edge cases in prose that are not in `canon.tests`.
- Metaphors must exist in the theme metaphor map.

### 5. Wire campaign order

Update `chapter.yaml` quest list / `order` fields. Unlock is sequential by `order` in Phase 1.

### 6. Validate mentally (script later)

- [ ] Canon tests ≥ phase minimum
- [ ] Examples ⊆ tests
- [ ] No spoiler terms in pre-solve story
- [ ] `beat_id` documented in story bible
- [ ] Starters compile as stubs in all three languages

## Hint ladder guidance

| Level | Intent |
|---|---|
| 1 | Clarify objective |
| 2 | Thinking direction |
| 3 | Suggest data structure family (still in-world if shown pre-solve; prefer careful wording) |
| 4 | Suggest algorithmic approach |
| 5 | Near pseudocode |

Never put the full answer in Level 1–2.

## Tests from stubs

`refer_problems` files often ship ~3–5 cases. Expand systematically:

- Happy path from problem statement
- Negatives / zeros
- Duplicates / empty where allowed
- Single-element / minimal constraints
- Large-ish arrays (still tiny for Judge0 latency)
- Order/index sensitivity
- Unicode/case for string problems when relevant

## Phase 1b batch

When expanding to 10 quests: extend bible beats B4–B10 first, then author canon, then story — same order every time.
