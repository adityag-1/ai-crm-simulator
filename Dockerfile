FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Copy configuration first
COPY pyproject.toml .
RUN touch uv.lock

# Pre-install core libs to speed up build and ensure they exist
RUN pip install --no-cache-dir fastapi uvicorn openai openenv-core

# Copy source code
COPY inference.py .
COPY server/ ./server/

# Install the project as a package
RUN pip install --no-cache-dir -e .

EXPOSE 7860

# Execute the entry point defined in toml
CMD ["server"]
