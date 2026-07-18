# PatternForge

Story-driven learning platform for algorithmic **pattern recognition**. Phase 1a demo: guest play through 3 Detective Academy quests with Monaco + Judge0.

## Prerequisites

- Node.js 20+
- Python 3.11+ (`py` launcher on Windows)
- Docker Desktop (Judge0 CE requires privileged containers)

## Run order

### 1. Judge0 CE

```bash
cd docker/judge0-v1.13.1
docker compose up -d db redis
# wait ~10 seconds
docker compose up -d
```

Docs: http://localhost:2358/docs  
Details: [docker/README.md](docker/README.md)

> **Windows / Docker Desktop:** compose uses a Judge0 CE-compatible image with cgroup v2 support. Keep `judge0.conf` as LF line endings.

### 2. Backend API

```bash
cd backend
py -m pip install -r requirements.txt
# from backend/, so `app` is importable
py -m uvicorn app.main:app --reload --port 8000
```

Health: http://localhost:8000/health

Optional env (defaults work for local demo):

- `JUDGE0_BASE_URL=http://localhost:2358`
- `CONTENT_ROOT` — absolute path to repo `content/` (default: sibling of `backend/`)
- `DATABASE_URL=sqlite:///./patternforge.db`

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

App: http://localhost:5173

## Demo loop

Landing → Case Board → quest story → Monaco (Python / JS / TS) → **Run** (public tests) / **Submit** (all tests) → reflection (XP + pattern) → unlock next quest.

Progress is stored in `localStorage` and synced to the API via `guest_id`.

## Content

Quest YAML lives under `content/campaigns/detective_academy/`. Authoring guide: `docs/CONTENT_GUIDE.md`.

## Docs

Start at `docs/01_PRD.md` and `docs/04_IMPLEMENTATION.md`.
