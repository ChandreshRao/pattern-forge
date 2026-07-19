# Detective Academy art assets

Committed static portraits and environments. Never generate artwork at runtime
(see `docs/VISUAL_STYLE.md` and `docs/CONTENT.md` — AI boundaries).

## Drop-in generated art

1. Export WebP (or PNG) busts at ~512–768px wide, same crop/eye line.
2. Replace the SVG placeholders in `characters/{mora|quin}/` using the same
   basenames: `neutral`, `stern`, `pleased`, `concerned`, `thinking`.
3. Replace `environments/{night_desk|evidence_locker|records_room}.*` similarly.
4. Update imports in `frontend/src/content/npcs.ts` if you change extensions
   (e.g. `.svg` → `.webp`).

## Free generation tools

Bing Image Creator, Google Gemini, Ideogram Character — generate offline once,
then commit. Record the tool + date below for license hygiene.

| Asset set | Tool | Date | Notes |
|---|---|---|---|
| SVG placeholders | hand-authored | 2026-07-18 | Temporary stand-ins |
| | | | |

## Cast

- **mora** — Captain Mora
- **quin** — Archivist Quin
