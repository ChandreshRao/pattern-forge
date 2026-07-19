# Judge0 CE (self-hosted)

PatternForge Phase 1a uses **Judge0 CE v1.13.1** for code execution. There is no local/fallback executor.

## Start

From this directory (or the repo root):

```bash
cd docker/judge0-v1.13.1
docker compose up -d db redis
# wait ~10s for Postgres/Redis
docker compose up -d
```

API docs: http://localhost:2358/docs

## Stop

```bash
cd docker/judge0-v1.13.1
docker compose down
```

## Notes

- Requires Docker with privileged containers (sandbox).
- Passwords for local demo live in `judge0.conf` (`REDIS_PASSWORD`, `POSTGRES_PASSWORD`).
- Backend expects `JUDGE0_BASE_URL=http://localhost:2358`.
- On Windows, keep `judge0.conf` as **LF** line endings (not CRLF). CRLF breaks Redis/Postgres host env vars inside the container.
- Official `judge0/judge0:1.13.1` needs **cgroups v1**. Docker Desktop (Windows/macOS) uses cgroups v2, so this compose uses `mrkushalsm/judge0:latest` (Judge0 CE API + isolate cgroup v2). On a cgroups-v1 Linux host you can switch the image back to `judge0/judge0:1.13.1`.
