FROM python:3.10-slim

WORKDIR /code

# 1. Install system tools
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# 2. Install BUILD BACKEND and dependencies first
# This is the CRITICAL step to fix BackendUnavailable
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir hatchling setuptools

# 3. Install core dependencies
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    huggingface_hub \
    python-multipart \
    "openenv-core>=0.2.0"

# 4. Copy everything from your GitHub/Root
COPY . .

# 5. Install the project in editable mode
# Hatchling is now available to handle this
RUN pip install --no-cache-dir -e .

# 6. Run the entry point defined in pyproject.toml
CMD ["server"]
