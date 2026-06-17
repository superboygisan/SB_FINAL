FROM python:3.11-slim

WORKDIR /app

# Install system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    curl \
    ffmpeg \
    git \
    zip \
    gcc \
    g++ \
    musl-dev \
    build-essential \
    python3-dev \
    libffi-dev \
    libssl-dev \
    pkg-config \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app/

# Upgrade pip and install uv
RUN pip install --no-cache-dir --upgrade pip uv

# IMPORTANT:
# Remove old pyrogram if exists
RUN pip uninstall -y pyrogram || true

# Install dependencies from pyproject.toml
RUN uv sync

# Force latest kurigram for styled buttons
RUN pip install --no-cache-dir -U kurigram

# Proper venv path
ENV PATH="/app/.venv/bin:$PATH"

# Prevent buffered logs
ENV PYTHONUNBUFFERED=1

CMD ["bash", "start"]