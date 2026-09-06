# Vibe 23 EnergyPlus Worker

A small authenticated HTTP worker for EnergyPlus 26.1 simulations. It is designed to run as a Docker web service on Render and serve the Streamlit Vibe 23 frontend.

The image downloads the official EnergyPlus 26.1 Ubuntu 24.04 x86-64 release, verifies its published SHA-256 checksum, and exposes a one-job-at-a-time FastAPI queue. Jobs run in separate directories and expire after 24 hours by default.

## Deploy on Render

1. Create a new GitHub repository and upload this repository's contents.
2. In Render, choose **New → Blueprint** and select the repository.
3. Render reads `render.yaml`, builds the Docker image, and generates `API_KEY`.
4. In the Render service, copy the generated `API_KEY` from **Environment**.
5. Set the same value in Streamlit Community Cloud secrets, together with the Render URL:

```toml
EPLUS_WORKER_URL = "https://your-render-service.onrender.com"
EPLUS_WORKER_API_KEY = "generated-render-api-key"
```

Choose a paid Render instance for dependable simulations. Free services can sleep, have ephemeral storage, and may not provide enough uninterrupted CPU time for a full 169-candidate campaign.

## API

Health does not require authentication:

```bash
curl https://your-render-service.onrender.com/healthz
```

Submit a simulation:

```bash
curl -X POST https://your-render-service.onrender.com/v1/jobs \
  -H "Authorization: Bearer $EPLUS_WORKER_API_KEY" \
  -F "idf=@model.idf" \
  -F "epw=@weather.epw" \
  -F "expand_objects=true"
```

Poll and download:

```bash
curl -H "Authorization: Bearer $EPLUS_WORKER_API_KEY" \
  https://your-render-service.onrender.com/v1/jobs/JOB_ID

curl -L -H "Authorization: Bearer $EPLUS_WORKER_API_KEY" \
  -o results.zip \
  https://your-render-service.onrender.com/v1/jobs/JOB_ID/results
```

Interactive API documentation is available at `/docs`.

## Local development

Build and run the same image Render will use:

```bash
docker build -t vibe23-energyplus-worker .
docker run --rm -p 8000:8000 -e API_KEY=local-secret vibe23-energyplus-worker
```

Then open <http://localhost:8000/docs>.

For fast Python-only checks without building EnergyPlus:

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt pytest ruff
pytest -q
ruff check app tests
```

## Operational behavior

- `API_KEY` is required as a bearer token for every job endpoint.
- `MAX_CONCURRENT_JOBS=1` avoids CPU contention on a small Render instance.
- `SIM_TIMEOUT_SECONDS=900` limits one EnergyPlus process to 15 minutes.
- `MAX_UPLOAD_MB=50` limits each uploaded file.
- `JOB_TTL_HOURS=24` removes old jobs when the service next receives a submission or starts.
- Output files are returned as a ZIP even when EnergyPlus reports a severe/fatal error, so the caller can inspect `eplusout.err`.
- Running jobs do not survive a service restart. Completed job files survive only as long as the instance filesystem. Add a Render persistent disk or object storage if results must survive deploys.

## Vibe 23 integration boundary

This repository runs one prepared IDF against one EPW. Vibe 23 still needs a small client module that:

1. prepares each candidate IDF;
2. submits jobs without blocking Streamlit;
3. polls their status;
4. downloads and parses the output;
5. constructs `ranking.json` and `twin_export.json`.

For 169 candidates, keep concurrency low initially and add a batch/campaign endpoint after measuring one-day simulation time and Render costs.

## License and provenance

Worker code is provided under the MIT License. EnergyPlus is downloaded from the official NatLabRockies release and retains its own license. This repository does not redistribute the EnergyPlus archive.

