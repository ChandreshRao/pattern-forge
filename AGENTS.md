# PatternForge — Agent Instructions

## Mission

Build a story-driven learning platform that teaches algorithmic **pattern recognition**, not problem memorization.

## Source of truth

Use **`docs/`** for all product and engineering decisions.

Start here: `docs/PRODUCT.md` → `docs/ARCHITECTURE.md` → `docs/CONTENT.md`.

## Core principles

- Keep demos focused on **shipped** scope in `docs/PRODUCT.md` (Phases 1a–1c). Do not build future roadmap items unless explicitly scoped.
- Reuse before building.
- Prefer deterministic logic over AI.
- AI is optional; never required for the core loop.
- Never generate curriculum or stories at runtime — commit content under `content/`.
- Never implement future-phase features from the PRODUCT roadmap unless the user asks.

## Current product (1b / 1c)

- Email + password auth; guests ephemeral; logged-in progress durable
- One campaign, one chapter, **10** quests
- Monaco + Python / JS / TS
- Judge0 CE via backend adapter (local Docker or RapidAPI)
- Reflection + XP + unlock; hint ladder L1–L5; thin Codex v1
- Deploy: Render (Docker FE+API) + Postgres + RapidAPI Judge0 — root `README.md`

## Tech stack

- Frontend: React + Vite + TypeScript + Tailwind + shadcn/ui + Monaco
- Backend: FastAPI + SQLAlchemy + SQLite (Postgres on Render)
- Judge: Judge0 CE via `CodeExecutor` adapter
- Content: YAML/JSON under `content/`

## Folders

`docs/` · `frontend/` · `backend/` · `content/` · `docker/` · `refer_problems/` · `e2e/`

## Story & content

Follow `docs/STORY_BIBLE.md`, `docs/themes/*`, and `docs/CONTENT.md`. When authoring quests, use `.cursor/skills/author-quest/SKILL.md`.
