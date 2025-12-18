# ================================
# Stage 1: Builder
# ================================
FROM python:3.11-slim AS builder
WORKDIR /app

# Copy dependency file first for caching
COPY requirements.txt .
RUN python -m pip install --upgrade pip && \
    pip install --prefix=/install -r requirements.txt

# ================================
# Stage 2: Runtime
# ================================
FROM python:3.11-slim
ENV TZ=UTC
WORKDIR /app

# Install system dependencies for cron
RUN apt-get update && \
    apt-get install -y --no-install-recommends cron tzdata && \
    ln -sf /usr/share/zoneinfo/UTC /etc/localtime && \
    echo "UTC" > /etc/timezone && \
    rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from builder
COPY --from=builder /install /usr/local

# Copy app and key files
COPY . .

# Copy cron file and set permissions
RUN chmod 0644 Cron/2fa-cron && crontab Cron/2fa-cron

# Create required directories for persistence
RUN mkdir -p /data /cron && chmod 755 /data /cron

# Expose FastAPI port
EXPOSE 8080

# Start cron + FastAPI
CMD ["sh", "-c", "service cron start && uvicorn app:app --host 0.0.0.0 --port 8080"]
