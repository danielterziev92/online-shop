FROM python:3.13-alpine AS builder

# Set working directory for builder stage
WORKDIR /build

# Install build-time dependencies
RUN apk add --no-cache \
    postgresql-dev \
    build-base

# Copy only requirements file first for better caching
COPY requirements.txt .

# Build wheels for faster installation in final stage
RUN pip wheel --no-cache-dir --wheel-dir /build/wheels -r requirements.txt

# Second stage: final image
FROM python:3.13-alpine

# Set build arguments and environment variables
ARG APP_HOME=/app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_HOME=$APP_HOME \
    SCRIPTS_PATH="./scripts"

# Create non-privileged user
RUN adduser -D appuser

# Install system dependencies
RUN apk update && apk add --no-cache \
   build-base \
   python3-dev \
   postgresql-dev \
   libffi-dev \
   linux-headers \
   musl-dev \
   netcat-openbsd \
   curl

# Set working directory
WORKDIR $APP_HOME

# Copy wheels from builder stage
COPY --from=builder /build/wheels /wheels

# Install packages from pre-compiled wheels
RUN pip install --no-cache-dir /wheels/*

# Copy project files
COPY --chown=appuser:appuser . .

# Create and configure scripts directory
RUN chmod +x $SCRIPTS_PATH/*.sh && \
    mkdir -p /logs /staticfiles /mediafiles && \
    chown -R appuser:appuser $APP_HOME /logs /staticfiles /mediafiles


# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/api/health/ || exit 1

## Switch to non-root user
#USER appuser

# Set entrypoint and CMD
ENTRYPOINT ["sh", "-c", "mkdir -p ${APP_HOME}/staticfiles && chown -R appuser:appuser ${APP_HOME}/staticfiles && su -c \"${SCRIPTS_PATH}/entrypoint.sh\" appuser"]