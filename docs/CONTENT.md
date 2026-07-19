# PatternForge — Content

Curriculum is data. The app loads packs; it does not hardcode DSA problems in UI code.

Skills: `.cursor/skills/author-quest/SKILL.md` (canon) · `.cursor/skills/write-quest-story/SKILL.md` (story).

---

## Hierarchy

```
Curriculum (e.g. dsa)
 └── Campaign (e.g. detective_academy)
      └── Chapter
            └── Quest
                  ├── canon   (immutable learning)
                  └── story   (theme presentation)
```

## Separation rules

| Layer | Owns | Must not |
|---|---|---|
| `canon` | pattern, signals, signatures, tests, hint facts, reflection teaching, interview ref | Theme lore, spoilers in pre-solve UI |
| `story` | hook, briefing, objective_in_world, success_line, reflection_flavor, beat_id | Change tests, invent I/O, name algorithm pre-solve |
| `theme` | lexicon, characters, metaphor map | Override pattern ids or complexity |

## Quest file layout

```
content/
  themes/
    detective_academy.yaml
  campaigns/
    detective_academy/
      campaign.yaml
      chapters/
        ch01/
          chapter.yaml
          quests/
            q01_two_sum.yaml
            ...
```

Single-file form (MVP):

```yaml
id: q01_two_sum
chapter_id: ch01
order: 1
beat_id: B1
theme_id: detective_academy
refer_problem: refer_problems/arrays/two_sum.py

canon:
  title: "Paired Receipts"
  pattern_id: hash_map
  pattern_reveal_name: "Hash Map"
  recognition_signals: [pair_lookup, complement, one_pass]
  difficulty_rank: explorer
  languages:
    python:
      function_name: two_sum
      starter: |
        from typing import List
        def two_sum(nums: List[int], target: int) -> List[int]:
            pass
    javascript:
      function_name: twoSum
      starter: |
        function twoSum(nums, target) {
        }
    typescript:
      function_name: twoSum
      starter: |
        function twoSum(nums: number[], target: number): number[] {
        }
  constraints_text: "..."
  examples:
    - input: { nums: [2, 7, 11, 15], target: 9 }
      output: [0, 1]
  tests:
    - id: t1
      input: { nums: [2, 7, 11, 15], target: 9 }
      expected: [0, 1]
      hidden: false
    - id: t2
      input: { nums: [3, 2, 4], target: 6 }
      expected: [1, 2]
      hidden: true
  hints:
    - level: 1
      text: "Clarify what two values must satisfy."
    # ... levels 2–5
  reflection:
    why: "You looked up complements in constant time instead of checking every pair."
    common_mistakes:
      - "Using the same index twice"
    complexity:
      time: "O(n)"
      space: "O(n)"
  interview_reference: "LeetCode 1 — Two Sum"

story:
  hook: "..."
  briefing: "..."
  objective_in_world: "..."
  success_line: "..."
  reflection_flavor: "..."   # flavor only; teaching stays in canon.reflection
```

## Judge harness

Backend wraps user code so Judge0:

1. Loads user source.
2. Calls `function_name` with deserialized `input`.
3. Compares to `expected` (canonical JSON equality).
4. Aggregates pass/fail per test.

Language ids map inside `Judge0Executor` only. Target: **15–20 tests** per quest (Chapter 1).

## Chapter 1 quest set

| Order | Quest id | Source | pattern_id |
|---|---|---|---|
| 1 | `q01_two_sum` | `arrays/two_sum.py` | `hash_map` |
| 2 | `q02_contains_duplicate` | `arrays/contains_duplicate.py` | `hash_set` |
| 3 | `q03_valid_anagram` | `strings/valid_anagram.py` | `frequency_count` |
| 4–10 | see [STORY_BIBLE.md](STORY_BIBLE.md) beats B4–B10 | Blind-75 pool | chapter-coherent |

## Authoring workflow

### 1. Pick the problem

From Blind-75 under `refer_problems/`. Do not invent new algorithmic requirements absent from the source.

### 2. Freeze canon first

- Signatures for Python, JS, TS
- Public examples (must match tests) + hidden tests
- `pattern_id` + `pattern_reveal_name`, recognition signals
- Hint ladder L1–L5 (no full solution at L1–L2)
- Reflection teaching: why, common mistakes, complexity
- Interview reference

### 3. Assign a story beat

Next free beat in [STORY_BIBLE.md](STORY_BIBLE.md). Continuity must advance the case.

### 4. Fill story slots

Use `.cursor/skills/write-quest-story/SKILL.md` and theme lexicon (`content/themes/detective_academy.yaml`):

- `hook`, `briefing`, `objective_in_world`, `success_line`, `reflection_flavor`

**Anti-hallucination:** no fake I/O in prose; no pattern names pre-solve; no edge cases absent from tests; metaphors from the theme map only.

### 5. Wire campaign order

Update `chapter.yaml` / `order`. Unlock is sequential by `order`.

### 6. Validate

```bash
python scripts/validate_story.py path/to/quest.yaml
```

Must exit 0. Also: examples ⊆ tests; test count; beat in bible; starters are stubs in all three languages.

### Hint ladder

| Level | Intent |
|---|---|
| 1 | Clarify objective |
| 2 | Thinking direction |
| 3 | Data structure family (careful pre-solve wording) |
| 4 | Algorithmic approach |
| 5 | Near pseudocode |

### Expanding tests from stubs

`refer_problems` often ship ~3–5 cases. Add: happy path, negatives/zeros, duplicates/empty, minimal constraints, large-ish arrays (still Judge0-friendly), index/order sensitivity, unicode/case when relevant.

## Theme packs

Human docs: `docs/themes/{theme}.md`  
Runtime: `content/themes/{theme}.yaml`

Same canon can later bind to another `theme_id` + new `story` slots.

## Pattern registry (later)

`content/patterns/{pattern_id}.yaml` — full Codex pages. Current thin Codex uses reveal name + progress.

## AI boundaries

AI is an **enhancement**, never the curriculum.

| May | Must not |
|---|---|
| Explain, mentor, encourage, ask questions (future BYO key) | Reveal full solutions on demand |
| Fill approved story slots **offline** → human review → commit | Generate curriculum/tests/patterns at runtime |
| | Decide unlocks or replace Judge0 |

**Levels:** 0 none (default) → 1 static hints (shipped) → 2+ BYO mentoring later.

**Spoiler boundary:** Pre-solve surfaces never name patterns or “use a hash map.” Post-solve teaching comes from **canon**, not free-form model invention.

**Art:** Generate portraits/environments **once offline**, commit permanently. No runtime art generation. See [VISUAL_STYLE.md](VISUAL_STYLE.md).

If asked to “just have the model make problems,” refuse and use this guide + `refer_problems/`.

## Validation details

`scripts/validate_story.py` checks (theme-driven):

- All story slots present; `beat_id` / `theme_id` set
- `beat_id` exists in `STORY_BIBLE.md`
- Pre-solve: no banned spoilers, no fake I/O phrasing
- `reflection_flavor`: no complexity teaching
- Cast lock + slot budgets

Fixtures: `scripts/fixtures/q01_two_sum_clean.yaml` (PASS), `q01_two_sum_bad.yaml` (FAIL).
