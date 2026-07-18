# Theme pack — Detective Academy

Machine-oriented twin will live at `content/themes/detective_academy.yaml` when content is scaffolded.

## Identity

- **Theme id:** `detective_academy`
- **World:** Modern city police/detective training academy with a records-driven mystery
- **Visual direction (later UI):** Cool night desk lamps, paper files, cork boards — not purple sci-fi default
- **Voice:** Procedural, concise, respectful of the learner’s intelligence

## Characters

See `STORY_BIBLE.md` cast. Theme pack owns *how they speak*:

- **Captain Mora:** Direct, short sentences, stakes-first
- **Archivist Quin:** Dry, metaphor-friendly, never spoils the algorithm name

## Metaphor map (allowed)

Use these when story needs a concrete image. Do not invent competing metaphors for the same pattern in Chapter 1.

| Pattern family / idea | Allowed metaphor |
|---|---|
| Hash map (key → value) | Case filing cabinet / tag → drawer index |
| Hash set (seen?) | Evidence stamp log (“already logged?”) |
| Frequency count | Letter tally on a courier slip |
| Stack | Sealed evidence brackets / nesting seals |
| Sliding window | Moving surveillance window along a street |
| Two pointers | Two officers walking a line from opposite ends |
| Linked list | Informant chain / paperclip trail |
| Running minimum | Lowest chalk price seen so far on the board |

## Banned spoiler terms (pre-solve story slots)

Do not use in `hook`, `briefing`, `objective_in_world`, or `success_line`:

- Algorithm/pattern names: `hash map`, `hashmap`, `hash set`, `sliding window`, `two pointers`, `kadane`, `dynamic programming`, `BFS`, `DFS`, `trie`, etc.
- Complexity flex: `O(n)`, `O(1)`, `linear time`, `constant time lookup` as the “answer”
- Interview branding: `LeetCode`, `Blind 75` (ok in post-solve interview_reference UI, not in story)

Post-solve reflection **may** use the official `pattern_reveal_name` from canon.

## Variables for templates (future AI fill)

| Variable | Example |
|---|---|
| `{{location}}` | Night desk |
| `{{captain}}` | Captain Mora |
| `{{stakes}}` | warrant window closes at dawn |
| `{{object}}` | evidence tags |
| `{{beat_handoff}}` | duplicate tags in the same drawer |

AI fill (later) may only substitute these and polish dialogue — never edit canon.

## Reuse

The same DSA canon quests can later ship under another theme (e.g. Lost Kingdom) by writing new `story` slots + a new theme pack. Canon stays identical.
