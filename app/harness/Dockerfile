FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3.12 \
    python3.12-venv \
    python3-pip \
    openjdk-21-jre-headless \
    gnucobol \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN python3.12 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY app/harness/requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN mkdir -p \
    /app/securatron/global/tools \
    /app/securatron/global/skills \
    /app/securatron/global/ledger \
    /app/securatron/global/charters \
    /app/securatron/sessions/.state \
    /app/securatron/inbox/new \
    /app/harness/atoms

WORKDIR /app/harness

COPY app/harness/ /app/harness/
COPY scripts/ /app/scripts/
COPY validation/ /app/validation/
COPY translations/ /app/translations/
COPY app/securatron/ /app/securatron/

RUN chmod +x /app/harness/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/harness/entrypoint.sh"]
