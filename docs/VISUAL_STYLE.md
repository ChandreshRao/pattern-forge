# Visual style guide

**Status:** Theme-agnostic product art and UI motion direction. Theme packs own palette, lexicon, and screen naming (e.g. Detective Academy in `themes/detective_academy.md`).

## Guiding principle

PatternForge should feel like **a living storybook that occasionally asks the player to write code** — not a traditional action game and not a bare coding challenge site.

Focus: discovery, mystery, story, coding, pattern recognition.

## Inspirations

- Professor Layton
- Ace Attorney
- Monument Valley
- Dorfromantik
- Classic Pokémon

**Avoid:** Limbo (too dark), Mario/platformers, AAA realism.

## UI philosophy

**The application is the game.** Surfaces should feel like places in the world, not admin chrome.

| Neutral surface | Example theme labels |
|---|---|
| Dashboard | Expedition Map / Case Board |
| Pattern notebook | Pattern Codex / Case Files |
| Achievements | Museum / Commendations |
| Profile | Explorer Journal / Recruit Dossier |

Detective Academy visual direction (cool night desk lamps, paper files, cork boards) lives in its theme doc — not here.

## Character style

Use **2D illustrated bust portraits**.

- Waist-up portraits
- Painterly / storybook style
- Palette and costume follow the active theme

## Animation

Do **not** use GIFs.

Prefer: WebP / PNG stills, Framer Motion, CSS transitions, Lottie (optional).

Effect vocabulary: fade in, blink, gentle breathing, floating, dialogue typing.

## Environments

Reuse a **small** set per theme. Prefer variation through lighting and props over many unique backgrounds.

## NPC and asset pipeline

Generate once and reuse forever.

1. Character profile (personality, role, relationships)
2. Portrait (2–4 candidates; pick one)
3. Expressions (5–8)
4. Dialogue templates with placeholders
5. Commit assets to Git under the theme’s asset path

**Runtime:** React loads static committed assets. No AI during gameplay. See [CONTENT.md](CONTENT.md) (AI boundaries).

## Recommended frontend motion stack

- React, Tailwind, Framer Motion, shadcn/ui (core)
- Optional later: Lottie, PixiJS, Rive

Stack choices: [ARCHITECTURE.md](ARCHITECTURE.md).
