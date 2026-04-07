FROM python:3.10-slim

# Force immediate log flushing
ENV PYTHONUNBUFFERED=1
WORKDIR /code

# 1. Install system tools
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# 2. Setup build environment (Crucial fix for wheel error)
RUN pip install --no-cache-dir --upgrade pip setuptools wheel hatchling

# 3. Install dependencies manually
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    huggingface_hub \
    python-multipart \
    "openenv-core>=0.2.0"

# 4. Copy project files
COPY . .

# 5. Install the project 
# We use --no-build-isolation to use the tools we just installed manually
RUN pip install --no-cache-dir --no-build-isolation .

# 6. Expose port
EXPOSE 7860

# 7. Run the entry point defined in pyproject.toml
CMD ["server"]
