# Content engine

Curriculum is data. The app loads packs; it does not hardcode DSA problems in UI code.

## Hierarchy

```
Curriculum (e.g. dsa)
 └── Campaign (e.g. detective_academy_ch01)
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

## Quest file layout (recommended)

```
content/
  themes/
    detective_academy.yaml          # machine-readable theme pack
  campaigns/
    detective_academy/
      campaign.yaml
      chapters/
        ch01/
          chapter.yaml
          quests/
            q01_two_sum.yaml        # canon + story keys in one file
            q02_contains_duplicate.yaml
            q03_valid_anagram.yaml
```

Single-file form (MVP-friendly):

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
  recognition_signals:
    - pair_lookup
    - complement
    - one_pass
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
  constraints_text: "..."   # shown as-is from canon
  examples:                 # public samples only; must match tests
    - input: { nums: [2, 7, 11, 15], target: 9 }
      output: [0, 1]
  tests:                    # server-only evaluation
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
    - level: 2
      text: "Think about remembering what you have already seen."
    - level: 3
      text: "A fast lookup structure helps."
    - level: 4
      text: "For each value, check if its complement was seen."
    - level: 5
      text: "Near-pseudocode: scan once; store value→index; probe target-value."
  reflection:
    why: "You looked up complements in constant time instead of checking every pair."
    common_mistakes:
      - "Using the same index twice"
      - "Returning values instead of indices"
    complexity:
      time: "O(n)"
      space: "O(n)"
  interview_reference: "LeetCode 1 — Two Sum"

story:
  hook: "..."
  briefing: "..."
  objective_in_world: "..."
  success_line: "..."
  reflection_flavor: "..."   # flavor only; teaching points stay in canon.reflection
```

## Judge harness contract

Backend wraps user code so Judge0 runs a fixed runner:

1. Load user source.
2. Call `function_name` with deserialized `input`.
3. Compare to `expected` (canonical JSON equality rules per type).
4. Aggregate pass/fail per test.

Language ids map inside `Judge0Executor` only.

### Test counts

| Phase | Target per quest |
|---|---|
| 1a | ≥8 |
| 1b | 15–20 |

## Phase 1a quest set

| Order | Quest id | Source | pattern_id |
|---|---|---|---|
| 1 | `q01_two_sum` | `arrays/two_sum.py` | `hash_map` |
| 2 | `q02_contains_duplicate` | `arrays/contains_duplicate.py` | `hash_set` |
| 3 | `q03_valid_anagram` | `strings/valid_anagram.py` | `frequency_count` |

## Phase 1b expansion (10 total)

Add seven more from Blind-75, still coherent with Chapter 1 case arc (see `STORY_BIBLE.md` beats B4–B10). Suggested pool (final pick at authoring time):

- `arrays/best_time_to_buy_and_sell_stock.py`
- `strings/valid_parentheses.py`
- `strings/group_anagrams.py`
- `arrays/product_of_array_except_self.py`
- `linked_lists/reverse_linked_list.py`
- `strings/longest_substring_without_repeating_characters.py`
- `arrays/maximum_subarray.py` or `arrays/3sum.py`

## Pattern metadata (global registry — later file)

`content/patterns/{pattern_id}.yaml` — description, recognition clues, variations, related patterns. Phase 1a may inline reveal name + why on reflection only.

## Theme packs

Human docs: `docs/themes/{theme}.md`  
Runtime: `content/themes/{theme}.yaml` (characters, metaphor_map, banned_spoiler_terms).

Same canon can later bind to another `theme_id` + new `story` slots (story packs).

## Validation (later script)

- Schema required fields present
- Every public example has a matching test
- Pre-solve story fields contain no `banned_spoiler_terms` / pattern reveal names
- `beat_id` exists in story bible for that campaign
