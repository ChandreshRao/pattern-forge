# Testing

PatternForge has two verification layers. Neither generates curriculum — they exercise committed content under `content/`.

| Layer | What it covers | Needs |
|---|---|---|
| [`scripts/verify_phase1a.py`](../scripts/verify_phase1a.py) | API acceptance: health, auth, submit/run via Judge0, progress | Judge0 + API |
| Root [`e2e/`](../e2e/) Playwright | Browser UI: Case Board, Monaco, reflection, hints, Codex, auth durability | Judge0 + API + frontend |

## Prerequisites

Same stack as the root [README](../README.md):

1. Judge0 CE on `http://localhost:2358`
2. Backend API on `http://127.0.0.1:8000` (routes under `/api`)
3. Frontend on `http://127.0.0.1:5173` (Playwright can start this via `webServer`)

## API verify

```bash
# Judge0 + API already running
py scripts/verify_phase1a.py
# optional: PF_API_BASE=http://127.0.0.1:8000/api
```

Covers register/login, Python submits for q01–q03, JS re-submit of q01, guest ephemeral submit, progress totals.

## Playwright e2e (Phase 1b UI)

True browser tests live at the **repo root** in `e2e/` (not under `frontend/`). They hit the real Vite app, which proxies `/api` to the backend and Judge0.

```bash
# Judge0 + API already running
cd e2e
npm install
npx playwright install chromium
npm test
```

Useful scripts:

- `npm test` — headless Chromium
- `npm run test:ui` — Playwright UI mode
- `npm run install:browsers` — install Chromium only

`playwright.config.ts` starts `frontend` with `npm run dev` on `:5173` when nothing is already listening (`reuseExistingServer` outside CI).

Submit/Judge0 waits are long (up to ~120s per submit). Run with Judge0 warm.

### Spec map vs Phase 1b

| Spec | Asserts |
|---|---|
| `guest-loop.spec.ts` | Landing → story → Monaco Run/Submit → reflection → unlock; JS language path |
| `auth-progress.spec.ts` | Register, durable progress across reload, guest reset on sign-out, restore on login |
| `hints.spec.ts` | Hint ladder L1–L5 |
| `codex.spec.ts` | Empty Codex then Hash Map after q01 (guest + logged-in) |
| `locks.spec.ts` | Fresh guest: only q01 open; later quests sealed |

Representative quests only (not all ten through the UI). API script remains the bulk submit check.

## Deploy smoke

API-level post-deploy checks stay in [`DEPLOY.md`](DEPLOY.md). Optionally run Playwright locally against a staging URL by changing `baseURL` / skipping `webServer` — not wired for CI yet.
