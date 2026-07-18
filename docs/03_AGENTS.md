# Agent & contributor instructions (detailed)

Companion to root `AGENTS.md`. Read `docs/01_PRD.md` and `docs/04_IMPLEMENTATION.md` before implementing features.

## Mission

Build a story-driven curriculum engine that teaches algorithmic **pattern recognition**, not problem memorization.

## Hard rules

1. Keep the MVP small and demoable (Phase 1a cut in PRD).
2. Reuse before building.
3. Every change should leave the app runnable (once scaffolding exists).
4. Prefer deterministic logic over AI.
5. AI is optional and BYO API key in future — never required for core loop.
6. **Never generate educational curriculum or stories at runtime.** Author into committed `content/` only.
7. Never implement future-phase features unless the current phase in `04_IMPLEMENTATION.md` lists them.
8. When writing story copy, follow `STORY_BIBLE.md` + `themes/*`; do not invent tests, patterns, or I/O.

## Source of truth

| Topic | Doc |
|---|---|
| Vision | `00_VISION.md` |
| Scope / acceptance | `01_PRD.md` |
| Architecture | `02_ARCHITECTURE.md` |
| Build phases / tasks | `04_IMPLEMENTATION.md` |
| Quest schema | `05_CONTENT_ENGINE.md` |
| AI boundaries | `06_AI_STRATEGY.md` |
| Roadmap | `07_ROADMAP.md` |
| Authoring steps | `CONTENT_GUIDE.md` |
| Narrative continuity | `STORY_BIBLE.md` |

## Content authoring

Use project skill `.cursor/skills/author-quest/SKILL.md` when adding quests.

Pipeline: `refer_problems/` → canon YAML → story bible beat → theme lexicon → story slots → validate.

## Stack reminder

Frontend: React + Vite + TypeScript + Tailwind + shadcn/ui + Monaco  
Backend: FastAPI + SQLAlchemy + SQLite  
Judge: Judge0 CE (Docker) via `CodeExecutor` adapter  
Languages: Python, JavaScript, TypeScript
