---
name: write-quest-story
description: >-
  Fill PatternForge quest story slots from frozen canon + story bible.
  Use when writing hook/briefing/objective_in_world/success_line/reflection_flavor,
  or when authoring story for an additional problem/beat.
---

# Write quest story (slot fill)

Authoring-time only. Never generate story at runtime for players.
Canon stays untouched — use `author-quest` first if canon is incomplete.

## When to use

- Quest YAML already has frozen `canon` and needs `story` slots
- Expanding Chapter 1 with a new beat (B4+)
- Rewriting Detective Academy dialogue without changing tests

## Hard rules

1. **Never edit `canon`.** Story only fills approved slots.
2. **Refuse to write** until `canon` has: `pattern_id`, `pattern_reveal_name`, signatures/starters, examples, tests, hints, `reflection`.
3. **You may only claim completion if** `python scripts/validate_story.py <quest>` exits **0**. A mental checklist without validator stdout is **not** completion.
4. Pre-solve slots must not name patterns, invent I/O, or invent NPCs.

## Inputs gate

Before prose, confirm the quest file has:

- `id`, `beat_id`, `theme_id`, `order`
- Complete `canon` (see above)

If anything is missing: stop and point the user to `.cursor/skills/author-quest/SKILL.md`.

## Step 1 — Build a story brief (no creativity)

Paste this block **verbatim** in your response, filled from sources (do not invent):

```text
STORY BRIEF
-----------
quest_id:        <from quest YAML>
beat_id:         <from quest YAML>
theme_id:        <from quest YAML>
pattern_id:      <canon.pattern_id>          # NEVER put this word in pre-solve prose
reveal_name:     <canon.pattern_reveal_name> # post-solve only

FROM docs/STORY_BIBLE.md (quote the beat section):
  location:      <Location line>
  stakes:        <Stakes line>
  player_knows:  <Player knows after line>
  handoff_from_prev: <previous beat's "Handoff to B…" line, or "N/A" for B1>
  handoff_to_next:   <this beat's Handoff line if present>

FROM content/themes/<theme_id>.yaml:
  allowed_metaphor: <metaphor_map[pattern_id]>
  cast:             <character names only>
  banned_terms:     <do not use in pre-solve>

OBJECTIVE SOURCE (paraphrase in world terms only; do not copy examples):
  function / behavior: <one line from canon title or constraints — no arrays>
```

If `beat_id` is new (not in the bible): **update `docs/STORY_BIBLE.md` in the same change** before writing slots.

## Step 2 — Fill slots one at a time

Write only these keys under `story:`:

| Slot | Role | Budget (theme defaults) |
|------|------|-------------------------|
| `hook` | Cold open at location | 1–3 sentences, ≤80 words |
| `briefing` | Captain Mora assigns task; stakes clear | 1–4 sentences, ≤100 words |
| `objective_in_world` | Player-facing coding goal in world terms | **1** sentence, ≤40 words |
| `success_line` | Case closed | **1** sentence, ≤30 words |
| `reflection_flavor` | Atmosphere only | 1–2 sentences, ≤50 words; **no** teaching / O(...) |

Per-slot rules:

- Use theme lexicon + allowed metaphor only (as image, not as algorithm name).
- No banned spoiler terms; no `pattern_reveal_name` / `pattern_id` wording in pre-solve.
- No fake I/O: no `[2, 7, ...]`, no `->` / `=>`, no `input:` / `returns:`.
- No new named characters (cast lock: Captain Mora, Archivist Quin).
- Teaching facts stay in `canon.reflection` — not in `reflection_flavor`.

### Worked example (B1 / two_sum) — BAD then GOOD

**BAD** (annotated — do not ship):

```yaml
story:
  hook: "Detective Lex opens a hash map of tags [2,7,11] -> target 9."
  # ❌ invented NPC "Lex"  ❌ spoiler "hash map"  ❌ fake I/O array
  briefing: "Mora says use O(n) constant time lookup like LeetCode 1."
  # ❌ complexity as the answer  ❌ interview branding
  objective_in_world: "Return indices where nums[i]+nums[j]==target."
  # ❌ textbook wording / fake I/O vibe — prefer world terms
  success_line: "Hash Map unlocked."
  # ❌ pattern name pre-solve (and success_line is pre-solve)
  reflection_flavor: "You achieved O(n) time and O(n) space."
  # ❌ teaching belongs in canon.reflection
```

**GOOD**:

```yaml
story:
  hook: >
    Rain ticks the night-desk lamp. Two evidence tag numbers sit in the
    intake tray, waiting to match a sealed case code before the warrant window dies.
  briefing: >
    Captain Mora does not raise her voice. Find the pair of tags that add up to
    the sealed code — wrong pair wastes the window. Archivist Quin leaves the
    filing cabinet unlocked; speed matters more than a full drawer search.
  objective_in_world: >
    Identify which two tag indices sum to the sealed case code.
  success_line: >
    The warrant window holds; the paired tags clear intake.
  reflection_flavor: >
    Quin closes the cabinet. Somewhere in the same drawer, duplicate stamps
    are already stacking up.
```

## Step 3 — Continuity stitch

Before finishing:

1. Quote the previous beat's **Handoff** line from the bible (or `N/A` for B1).
2. Quote the sentence in your new `hook` or `briefing` that picks it up.
3. If this beat introduces new continuity (new location chain, new stake), update `STORY_BIBLE.md` in the same change.

Example for B2:

```text
PREV HANDOFF: "Mora notices duplicate tags flooding the same drawer."
STITCH: briefing opens with duplicate tags at the evidence locker intake.
```

## Step 4 — Run the harness (mandatory)

```bash
python scripts/validate_story.py path/to/quest.yaml
```

- Paste the **full** stdout in your response.
- Exit code must be **0**.
- On FAIL: fix the failing slots (or bible/theme), re-run. Never claim done on a failed report.

## References

- `docs/STORY_BIBLE.md`
- `docs/themes/detective_academy.md`
- `content/themes/detective_academy.yaml`
- `docs/CONTENT.md`
- `scripts/validate_story.py`
- `.cursor/skills/author-quest/SKILL.md` (canon first)
