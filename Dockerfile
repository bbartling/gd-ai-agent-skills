FROM ubuntu:24.04

ARG DEBIAN_FRONTEND=noninteractive
ARG ENERGYPLUS_VERSION=26.1.0
ARG ENERGYPLUS_SHA=6f2e40d102
ARG ENERGYPLUS_RELEASE_SHA256=b651f4197bfc147a0f66dc92c58895d1748bdadb7a0288145fa9d50375edfbca

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    ENERGYPLUS_VERSION=${ENERGYPLUS_VERSION} \
    ENERGYPLUS_ROOT=/opt/EnergyPlus-26-1-0 \
    ENERGYPLUS_EXE=/opt/EnergyPlus-26-1-0/energyplus \
    JOB_ROOT=/var/lib/eplus-worker/jobs \
    PORT=8000

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       ca-certificates curl libexpat1 libgomp1 libx11-6 python3 python3-pip python3-venv \
    && rm -rf /var/lib/apt/lists/*

RUN set -eux; \
    archive="EnergyPlus-${ENERGYPLUS_VERSION}-${ENERGYPLUS_SHA}-Linux-Ubuntu24.04-x86_64.tar.gz"; \
    url="https://github.com/NatLabRockies/EnergyPlus/releases/download/v${ENERGYPLUS_VERSION}/${archive}"; \
    curl --fail --location --retry 4 --output "/tmp/${archive}" "${url}"; \
    echo "${ENERGYPLUS_RELEASE_SHA256}  /tmp/${archive}" | sha256sum --check -; \
    mkdir -p /opt; \
    tar -xzf "/tmp/${archive}" -C /opt; \
    mv "/opt/EnergyPlus-${ENERGYPLUS_VERSION}-${ENERGYPLUS_SHA}-Linux-Ubuntu24.04-x86_64" "${ENERGYPLUS_ROOT}"; \
    chmod +x "${ENERGYPLUS_EXE}" "${ENERGYPLUS_ROOT}/ExpandObjects"; \
    rm "/tmp/${archive}"; \
    "${ENERGYPLUS_EXE}" --version

WORKDIR /app
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:${ENERGYPLUS_ROOT}:${PATH}"
COPY requirements.txt .
RUN pip install --no-cache-dir --requirement requirements.txt
COPY app ./app
RUN useradd --create-home --uid 10001 worker \
    && mkdir -p "${JOB_ROOT}" \
    && chown -R worker:worker /app /var/lib/eplus-worker
USER worker

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:' + __import__('os').environ.get('PORT','8000') + '/healthz', timeout=3)" || exit 1

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT} --workers 1"]

