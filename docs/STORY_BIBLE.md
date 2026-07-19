# Story bible — Detective Academy, Chapter 1

Progressive narrative for the first DSA campaign. Story **dresses** canon; it never replaces it.

## Campaign premise

You are a recruit at **Detective Academy**. A string of small inconsistencies in the city’s case files threatens to bury a larger conspiracy. Each quest is a **case desk assignment**. Solving it advances the investigation. Patterns are techniques you *discover* under pressure — named only after the case closes.

## Tone

Curious, procedural, lightly noir. Clever, not campy. Story motivates; never blocks understanding of the coding objective.

## Cast

| Character | Role |
|---|---|
| **Captain Mora** | Briefs recruits; sets stakes |
| **Archivist Quin** | Guards the records room; hints at filing systems (metaphor fuel) |
| **The Recruiter (player)** | Silent protagonist |

Do not introduce major new named characters in Chapter 1 without updating this bible.

## Continuity rules

1. Each quest has a `beat_id` (`B1`…`B10`) that advances the case.
2. Later briefs may reference earlier discoveries **without** naming algorithms until post-solve.
3. Do not reset the world between quests (no unrelated fairy-tale one-shots).
4. Pre-solve copy: **no** pattern names, complexity classes as “the trick”, or textbook algorithm labels.
5. Exact I/O lives in canon/UI examples — story states the goal in world terms only.
6. No edge cases in prose that are not covered by tests.

## Anti-hallucination checklist

- [ ] Pattern reveal only in post-solve reflection / Codex
- [ ] Metaphors from `themes/detective_academy.md` only
- [ ] `objective_in_world` aligns with canon function behavior
- [ ] Beat advances stakes or information
- [ ] Teaching facts only in `canon.reflection`, not invented in `reflection_flavor`

## Chapter 1 beats

### Phase 1a (playable)

#### B1 — Paired receipts (`q01_two_sum`)

- **Location:** Night desk, intake counter  
- **Stakes:** Two evidence tag numbers must sum to a sealed case code; wrong pair wastes a warrant window.  
- **Player knows after:** A fast “what complements what” lookup works under time pressure.  
- **Reveal (post-solve):** Hash Map  
- **Handoff to B2:** Mora notices duplicate tags flooding the same drawer.

#### B2 — Double tags (`q02_contains_duplicate`)

- **Location:** Evidence locker intake  
- **Stakes:** If any tag number appears twice, the chain of custody is compromised.  
- **Player knows after:** Detecting repeats needs memory of what was already seen.  
- **Reveal (post-solve):** Hash Set  
- **Handoff to B3:** Quin finds two witness statements that should be rearrangements of the same tip.

#### B3 — Scrambled tip (`q03_valid_anagram`)

- **Location:** Records room  
- **Stakes:** Confirm whether two tips are the same message with letters rearranged (coded courier habit).  
- **Player knows after:** Counting symbol frequency proves equivalence.  
- **Reveal (post-solve):** Frequency counting  
- **Chapter 1a close:** The conspiracy uses coded rearrangements and forged duplicates — academy promotes you to field cases (1b).

### Phase 1b (documented; author when expanding)

| Beat | Working title | Intent (world) | Likely pattern family |
|---|---|---|---|
| B4 | Ledger peaks | Spot best single profit window in price chalk marks | One-pass / running min |
| B5 | Bracketed seal | Validate sealed note delimiters | Stack |
| B6 | Alias bundles | Group tips that are rearrangements | Frequency + grouping |
| B7 | Blind multipliers | Reconstruct product clues without self-factor | Prefix/suffix products |
| B8 | Reverse trail | Reverse a linked trail of informants | Linked list reverse |
| B9 | Unique stretch | Longest stretch of nights without repeating signal | Sliding window (reveal after) |
| B10 | Strongest streak | Strongest contiguous streak of leads | Kadane / subarray |

Exact `refer_problems` binding for B4–B10 is chosen at authoring time per [CONTENT.md](CONTENT.md).

## Story slot templates

```text
hook: 1–3 sentences cold open at the location
briefing: Captain Mora assigns the task; stakes clear
objective_in_world: One sentence the player could paraphrase as the coding goal
success_line: One line on case closed
reflection_flavor: 1–2 sentences atmosphere; do NOT teach complexity here
```

## Publishing rule

Stories are **committed** under `content/`. No runtime generation on the player path. Optional AI slot-fill is offline + reviewed ([CONTENT.md](CONTENT.md) — AI boundaries).
