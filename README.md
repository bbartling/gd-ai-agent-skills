# Vibe 23 EnergyPlus Worker

Authenticated FastAPI worker that runs **EnergyPlus 26.1** simulations in Docker. It backs the [Vibe 23 Residential DSM Studio](https://github.com/bbartling/py-bacnet-stacks-playground/tree/develop/vibe_code_apps_23) (Streamlit) with a one-job-at-a-time queue.

| | |
|---|---|
| **Live service** | [https://vibe23-energyplus-worker.onrender.com/](https://vibe23-energyplus-worker.onrender.com/) |
| **OpenAPI / Swagger** | [https://vibe23-energyplus-worker.onrender.com/docs](https://vibe23-energyplus-worker.onrender.com/docs) |
| **Health** | [https://vibe23-energyplus-worker.onrender.com/healthz](https://vibe23-energyplus-worker.onrender.com/healthz) |
| **Source** | [github.com/bbartling/vibe23-energyplus-worker](https://github.com/bbartling/vibe23-energyplus-worker) |
| **Frontend (Vibe 23)** | [`vibe_code_apps_23`](https://github.com/bbartling/py-bacnet-stacks-playground/tree/develop/vibe_code_apps_23) in [py-bacnet-stacks-playground](https://github.com/bbartling/py-bacnet-stacks-playground) |

The image downloads the official EnergyPlus 26.1 Ubuntu 24.04 x86-64 release, verifies its published SHA-256 checksum, and runs each job in a separate directory. Job artifacts expire after 24 hours by default.

> **Free-tier note:** The public deploy uses Render’s free web service tier. Idle instances **sleep** and need a wake (first `/healthz` or Studio **Wake worker**, typically 30–90s). Prefer a paid always-on instance for long campaigns (e.g. full 169-cell searches).

## Deploy on Render

1. Push this repository to GitHub (`develop` or `main`).
2. In Render: **New → Blueprint** and select the repo so [`render.yaml`](render.yaml) applies.
3. Confirm Environment includes `API_KEY` (Blueprint may use `generateValue: true`).
4. If `/healthz` shows `"api_key_configured": false`, set `API_KEY` manually:

**Dashboard** — Render → `vibe23-energyplus-worker` → **Environment** → `API_KEY` = a long random secret → Save → Manual Deploy.

**Script** (needs a Render *account* API key `rnd_…`, not the worker bearer key):

```powershell
$env:RENDER_API_KEY = "rnd_..."
.\scripts\configure_render.ps1
```

Writes gitignored `.env.render.local` for local Streamlit.

5. Point Studio / Streamlit Community Cloud secrets at the live service:

```toml
EPLUS_BACKEND = "worker"
EPLUS_WORKER_URL = "https://vibe23-energyplus-worker.onrender.com"
EPLUS_WORKER_API_KEY = "same-as-render-service-API_KEY"
```

Verify:

```bash
curl https://vibe23-energyplus-worker.onrender.com/healthz
# expect ok=true and api_key_configured=true
```

## API

Interactive docs: [https://vibe23-energyplus-worker.onrender.com/docs](https://vibe23-energyplus-worker.onrender.com/docs)

Health (no auth):

```bash
curl https://vibe23-energyplus-worker.onrender.com/healthz
```

Submit a simulation:

```bash
curl -X POST https://vibe23-energyplus-worker.onrender.com/v1/jobs \
  -H "Authorization: Bearer $EPLUS_WORKER_API_KEY" \
  -F "idf=@model.idf" \
  -F "epw=@weather.epw" \
  -F "expand_objects=true"
```

Poll and download:

```bash
curl -H "Authorization: Bearer $EPLUS_WORKER_API_KEY" \
  https://vibe23-energyplus-worker.onrender.com/v1/jobs/JOB_ID

curl -L -H "Authorization: Bearer $EPLUS_WORKER_API_KEY" \
  -o results.zip \
  https://vibe23-energyplus-worker.onrender.com/v1/jobs/JOB_ID/results
```

## Local development

```bash
docker build -t vibe23-energyplus-worker .
docker run --rm -p 8000:8000 -e API_KEY=local-secret vibe23-energyplus-worker
```

Open [http://localhost:8000/docs](http://localhost:8000/docs).

Python-only checks (no EnergyPlus binary build):

```bash
python -m venv .venv
. .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt pytest ruff
pytest -q
ruff check app tests
```

## Operational behavior

- `API_KEY` bearer token required for every job endpoint.
- `MAX_CONCURRENT_JOBS=1` avoids CPU contention on a small instance.
- `SIM_TIMEOUT_SECONDS=900` caps one EnergyPlus process at 15 minutes.
- `MAX_UPLOAD_MB=50` per uploaded file.
- `JOB_TTL_HOURS=24` cleans old jobs on later activity.
- Results ZIP is returned even on severe/fatal EnergyPlus errors so callers can read `eplusout.err`.
- Running jobs do not survive a restart; completed files live only on the instance filesystem unless you add a persistent disk or object storage.

## Vibe 23 integration

This service runs **one prepared IDF + one EPW** per job. The Studio client in [`vibe_code_apps_23`](https://github.com/bbartling/py-bacnet-stacks-playground/tree/develop/vibe_code_apps_23) prepares candidate IDFs, submits/polls jobs, and builds `ranking.json` / `twin_export.json`.

For large catalogs (up to 169 cells), keep concurrency low and watch free-tier sleep + CPU limits.

## License and provenance

Worker code is MIT. EnergyPlus is downloaded from the official NatLabRockies release and retains its own license. This repository does not redistribute the EnergyPlus archive.
