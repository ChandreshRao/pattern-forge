# PatternForge

Story-driven learning platform for algorithmic **pattern recognition**. One Detective Academy chapter (10 quests), Monaco editor, Judge0 execution, hints, thin Codex, and email/password auth.

## Prerequisites

| Local | Publish (Render) |
|---|---|
| Node.js 20+ | GitHub repo |
| Python 3.11+ (`py` on Windows) | [Render](https://render.com) account |
| Docker Desktop (local Judge0) | [RapidAPI](https://rapidapi.com) Judge0 CE key (Basic plan is fine) |

---

## Local development

Three processes: Judge0 → API → Vite. Frontend calls `/api/...`; Vite proxies to the API.

### 1. Judge0 CE

```bash
cd docker/judge0-v1.13.1
docker compose up -d db redis
# wait ~10 seconds
docker compose up -d
```

Docs: http://localhost:2358/docs  
Details: [docker/README.md](docker/README.md)

> **Windows / Docker Desktop:** keep `judge0.conf` as **LF** line endings. Compose uses a cgroup v2–compatible Judge0 image.

### 2. Backend API

```bash
cd backend
py -m pip install -r requirements.txt
# copy .env.example → .env if you want overrides
py -m uvicorn app.main:app --reload --port 8000
```

Health: http://localhost:8000/api/health

Default env (see [backend/.env.example](backend/.env.example) or root [.env.example](.env.example)):

| Variable | Local default |
|---|---|
| `DATABASE_URL` | `sqlite:///./patternforge.db` |
| `JUDGE0_BASE_URL` | `http://localhost:2358` |
| `JUDGE0_RAPIDAPI_KEY` | empty (local Judge0) |
| `JWT_SECRET` | dev secret (change for any shared deploy) |
| `CORS_ORIGINS` | `["http://localhost:5173","http://127.0.0.1:5173"]` |

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

App: http://localhost:5173

### Demo loop

Landing → Case Board → quest story → Monaco (Python / JS / TS) → **Run** / **Submit** → reflection → unlock next quest.

Guests: progress is ephemeral. Register/login: progress persists in SQLite.

### Verify

```bash
# Judge0 + API running
py scripts/verify_phase1a.py
# optional: PF_API_BASE=http://127.0.0.1:8000/api

cd e2e
npm install
npx playwright install chromium
npm test
```

Details: [docs/TESTING.md](docs/TESTING.md).

---

## Publish on Render (public URL)

One Docker image serves the SPA and API. Code runs on **RapidAPI Judge0 CE**. Auth/progress use **Render Postgres**.

```text
Browser → Render (static FE + FastAPI /api)
              → Postgres
              → RapidAPI Judge0
```

### Step 1 — RapidAPI Judge0 key

1. Open [Judge0 CE on RapidAPI](https://rapidapi.com/judge0-official/api/judge0-ce).
2. Subscribe to the **Basic** (free) plan.
3. Copy your **X-RapidAPI-Key**.

### Step 2 — Push this repo to GitHub

Render builds from GitHub. Ensure the root [Dockerfile](Dockerfile) is on the branch you deploy.

### Step 3 — Deploy with Blueprint (simplest)

1. In Render: **New** → **Blueprint**.
2. Connect the GitHub repo; select [render.yaml](render.yaml).
3. When prompted for sync:false env vars, set:

| Variable | Value |
|---|---|
| `JUDGE0_RAPIDAPI_KEY` | your RapidAPI key |
| `CORS_ORIGINS` | `["https://YOUR-SERVICE.onrender.com"]` (use the URL Render assigns; you can update after first deploy) |

4. Apply. Wait for the web service and Postgres to become healthy.
5. Open `https://YOUR-SERVICE.onrender.com` → register → solve **Two Sum** (Python) to confirm Judge0.

Health check: `GET https://YOUR-SERVICE.onrender.com/api/health`

### Step 3 (alt) — Manual Web Service

1. **New** → **PostgreSQL** (free). Copy the **Internal Database URL**.
2. **New** → **Web Service** → this repo → **Docker**.
3. Dockerfile path: `./Dockerfile`. Instance: free (or starter if free is unavailable).
4. Environment:

| Variable | Value |
|---|---|
| `DATABASE_URL` | Internal Postgres URL from step 1 |
| `JWT_SECRET` | long random string |
| `JUDGE0_BASE_URL` | `https://judge0-ce.p.rapidapi.com` |
| `JUDGE0_RAPIDAPI_KEY` | your RapidAPI key |
| `JUDGE0_RAPIDAPI_HOST` | `judge0-ce.p.rapidapi.com` |
| `CONTENT_ROOT` | `/app/content` |
| `STATIC_ROOT` | `/app/static` |
| `CORS_ORIGINS` | `["https://YOUR-SERVICE.onrender.com"]` |

5. Deploy. Smoke: register → submit `q01_two_sum`.

> **Free tier notes:** Render may spin down idle free services (cold start). RapidAPI Basic has daily request limits — fine for demos, not heavy traffic.

### Optional: run the image locally

```bash
docker build -t patternforge .
docker run --rm -p 8000:8000 ^
  -e DATABASE_URL=sqlite:////tmp/patternforge.db ^
  -e JWT_SECRET=dev-local-docker ^
  -e JUDGE0_BASE_URL=http://host.docker.internal:2358 ^
  -e CORS_ORIGINS=["http://localhost:8000"] ^
  patternforge
```

(Use RapidAPI env instead of `host.docker.internal` if Judge0 is not on the host.)

---

## Later: self-hosted Judge0 on a VM

When you have a Docker VM (Oracle, Hetzner, etc.):

1. Run Judge0 from [docker/judge0-v1.13.1](docker/judge0-v1.13.1) on a **private** network (do not expose `:2358` publicly).
2. Point the app at it and **clear** the RapidAPI key:

```env
JUDGE0_BASE_URL=http://server:2358
JUDGE0_RAPIDAPI_KEY=
```

3. Use Postgres or SQLite on a persistent volume for `DATABASE_URL`.

No code change — same `Judge0Executor` and `/api` routes. See [docs/DEPLOY.md](docs/DEPLOY.md).

---

## Content

Quest YAML: `content/campaigns/detective_academy/`. Authoring: [docs/CONTENT_GUIDE.md](docs/CONTENT_GUIDE.md).

## Docs

Start at [docs/01_PRD.md](docs/01_PRD.md) → [docs/04_IMPLEMENTATION.md](docs/04_IMPLEMENTATION.md) → [docs/DEPLOY.md](docs/DEPLOY.md).
