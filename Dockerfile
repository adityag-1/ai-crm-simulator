FROM python:3.10-slim

WORKDIR /code

# 1. Install system dependencies
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# 2. Upgrade pip and install the BUILD BACKEND tools
# This ensures hatchling is globally available before the project build starts
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir hatchling setuptools

# 3. Install core application dependencies
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    huggingface_hub \
    python-multipart \
    "openenv-core>=0.2.0"

# 4. Copy all project files
COPY . .

# 5. Install the project in editable mode
# Since we installed hatchling in Step 2, this will now succeed
RUN pip install --no-cache-dir -e .

# 6. Run the entry point defined in pyproject.toml
CMD ["server"]
