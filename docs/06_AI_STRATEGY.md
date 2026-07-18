# AI strategy

## Philosophy

AI is an **enhancement**, never the curriculum.

**AI may:** explain, mentor, encourage, ask questions, review code (within policy).

**AI must not:** reveal full solutions on demand, generate curriculum at runtime, decide progression/unlocks, invent tests or pattern metadata.

## Levels

| Level | Capability | Phase |
|---|---|---|
| 0 | No AI | Default MVP |
| 1 | Static hints from content | 1b UI |
| 2 | Bring Your Own API Key mentoring | 2+ |
| 3 | Platform-sponsored limited hints | Later |
| 4 | Personalized mentoring | Later |
| 5 | Community-authored AI experiences | Later |

If no key exists, the core loop still works. Only personalized mentoring is disabled.

## Providers (future)

Gemini, OpenAI, Anthropic, Grok — behind an **AI abstraction layer** + provider adapters. New providers = new adapters only.

```
Frontend → Backend → AI abstraction → Provider adapter → Vendor API
```

## Story generation policy

**Never generate educational content live in the player path.**

Authoring pipeline (offline / pre-publish only):

```
Canonical problem → Pattern metadata → Story template + variables
  → (optional) AI fills dialogue slots → Human review → Published quest
```

- Algorithm, tests, and pattern ids **never** change via AI.
- AI may only fill approved story slots (`hook`, `briefing`, NPC lines) using theme lexicon + beat variables.
- Human (or explicit author approval) required before merge to `content/`.

Phase 1a/1b: **human or agent-authored committed YAML** — no AI fill step required.

## Mentoring policy (when enabled)

- Prefer questions over answers.
- Respect hint ladder; do not jump to Level 5 pseudocode immediately.
- Never paste a full passing solution unless a future “reveal” product mode is explicitly designed and gated.
- Mentoring must not bypass Judge0 or unlock quests.

## Spoiler boundary

Pre-solve surfaces (story, objective, editor chrome): no pattern names, no “use a hash map”, no complexity targets beyond what canon exposes as constraints.

Post-solve (reflection, Codex): pattern reveal and teaching points from **canon**, not free-form model invention.

## Art and NPC asset policy

Generate portraits, expression sheets, environments, relics, and icons **once offline**. Commit them permanently. Never regenerate artwork or biographies at runtime.

Use dialogue templates with placeholders (e.g. `{player_name}`, `{vault_name}`) instead of free-form generation during play. Optional AI may only fill approved story dialogue slots offline, then requires human review before merge.

Pipeline and motion guidance: `08_VISUAL_STYLE.md`.
