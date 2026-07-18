# Theme pack — Keepers of Patterns (future)

**Status:** Future / not authored. There is no `content/themes/keepers_of_patterns.yaml` yet. Detective Academy remains the active Phase 1 theme.

When this theme is authored, create the machine-oriented twin under `content/themes/` and bind quests via `theme_id` + new `story` slots. Canon stays identical.

## Identity

- **Theme id:** `keepers_of_patterns`
- **World:** Explorer-archaeology; rediscovering vaults left by an advanced civilization
- **Visual identity:** Warm earthy palette, ancient explorer aesthetic, painterly storybook busts (see `08_VISUAL_STYLE.md`)
- **Voice:** Mentoring, curious, lightly mythic — never campy

## Core premise

Thousands of years ago, an advanced civilization known as **The Keepers of Patterns** discovered that every great invention, mathematical breakthrough, and engineering marvel came from recognizing recurring patterns rather than memorizing isolated facts.

To preserve this philosophy, they built enormous vaults across the world. Each vault protects knowledge—not treasure—and can only be opened by demonstrating a particular way of thinking.

The civilization mysteriously vanished.

You are a young detective archaeologist who sets out to uncover what happened. Master Alaric, the last Keeper of the Codex, believes you may be the first explorer worthy of restoring the lost knowledge.

Long-term framing for players: they do not merely learn algorithms — they rediscover timeless patterns of reasoning.

## Cast

| Character | Role |
|---|---|
| **Master Alaric** | Wise mentor who teaches by asking questions |
| **Lira** | Archivist maintaining the Pattern Codex |
| **Rook** | Rival explorer representing brute-force thinking |
| **Professor Pemba** | Puzzle craftsman and comic relief |
| **Ancient Guardians** | Bosses protecting knowledge vaults |

Do not introduce major new named characters without updating this doc when the theme is authored.

## World regions (draft)

Progression is mastery-gated. Draft region chain (working titles — **must be renamed before authoring**; see spoiler compliance):

Temple of Arrays → Vault of Hash Maps → Forest of Two Pointers → Valley of Sliding Window → Tower of Trees → Graph Catacombs → DP Observatory

### Environments (reuse set)

Village, library, temple, forest, cave, ruins, observatory.

## UI naming (Keepers flavor)

Theme packs own screen naming. For this theme:

| App surface | Keepers label |
|---|---|
| Dashboard | Expedition Map |
| Sidebar / patterns | Pattern Codex |
| Achievements | Museum |
| Profile | Explorer Journal |

## Spoiler compliance

Region names that embed algorithm labels (e.g. "Vault of Hash Maps", "Forest of Two Pointers") **violate** the pre-solve spoiler rules used across themes (see `detective_academy.md` banned terms and `CONTENT_GUIDE.md`).

Before authoring:

1. Rename every region and location to non-spoiler world terms.
2. Keep pattern names out of pre-solve story slots (`hook`, `briefing`, `objective_in_world`, `success_line`).
3. Reveal pattern names only post-solve (reflection / Codex), from canon.

## Metaphor map

To be authored when the theme ships. Do not invent competing metaphors for the same pattern within a chapter. Curriculum (canon) remains identical to Detective Academy (and any other theme pack).

## Publishing rule

Stories and theme packs are **committed** under `content/`. No runtime generation on the player path. Optional AI slot-fill is offline + reviewed (`06_AI_STRATEGY.md`).
