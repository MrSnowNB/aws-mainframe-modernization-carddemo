FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3.12 \
    python3.12-venv \
    python3-pip \
    openjdk-21-jre-headless \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN python3.12 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN mkdir -p \
    /app/securatron/global/tools \
    /app/securatron/global/skills \
    /app/securatron/sessions/.state \
    /app/harness/atoms

WORKDIR /app/harness

COPY app/harness/ /app/harness/
COPY scripts/ /app/scripts/
COPY validation/ /app/validation/

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
