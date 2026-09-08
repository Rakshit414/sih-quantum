# ==============================================================================
# Q-SENTINEL: Multi-Stage Production Containerization
# Smart India Hackathon (SIH-26141) | Enterprise Deployment Specification
# ==============================================================================

FROM python:3.11-slim-bookworm AS base

# System optimization and security hardening
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install security updates
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create non-root application user
RUN useradd -m -u 1001 -s /bin/bash qsentinel && \
    mkdir -p /app/data && \
    chown -R qsentinel:qsentinel /app

# Copy application source code
COPY --chown=qsentinel:qsentinel . .

USER qsentinel

# Expose standard Streamlit web port
EXPOSE 8501

# Healthcheck probe for container orchestration
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

ENTRYPOINT ["python", "-m", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
