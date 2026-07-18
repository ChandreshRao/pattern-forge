# PatternForge — Agent Instructions

## Mission

Build a story-driven learning platform that teaches algorithmic **pattern recognition**, not problem memorization.

## Source of truth

Use **`docs/`** for all product and engineering decisions.

Start here: `docs/01_PRD.md` → `docs/04_IMPLEMENTATION.md` → `docs/03_AGENTS.md`.

## Core principles

- Keep demos focused on the active phase in `docs/04_IMPLEMENTATION.md`.
- Reuse before building.
- Prefer deterministic logic over AI.
- AI is optional; never required for the core loop.
- Never generate curriculum or stories at runtime — commit content under `content/`.
- Never implement future features unless listed in the active phase in `docs/04_IMPLEMENTATION.md`.

## Phase 1b (current)

- Email + password auth; guests ephemeral; logged-in progress durable
- One campaign, one chapter, **10** quests
- Monaco + Python / JS / TS
- Self-hosted Judge0 CE via backend adapter
- Reflection + XP + unlock; hint ladder L1–L5; thin Codex v1
- Deploy sketch in `docs/DEPLOY.md`

## Tech stack

- Frontend: React + Vite + TypeScript + Tailwind + shadcn/ui + Monaco
- Backend: FastAPI + SQLAlchemy + SQLite
- Judge: Judge0 CE (Docker)
- Content: YAML/JSON under `content/`

## Folders

`docs/` · `frontend/` · `backend/` · `content/` · `docker/` · `refer_problems/`

## Story & content

Follow `docs/STORY_BIBLE.md`, `docs/themes/*`, and `docs/CONTENT_GUIDE.md`. When authoring quests, use `.cursor/skills/author-quest/SKILL.md`.
