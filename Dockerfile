FROM python:3.10-slim

# Force logs to stream immediately
ENV PYTHONUNBUFFERED=1
WORKDIR /code

# 1. Install system tools
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# 2. Upgrade pip and install build tools
RUN pip install --no-cache-dir --upgrade pip setuptools wheel hatchling

# 3. Install dependencies manually (including openai)
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    huggingface_hub \
    python-multipart \
    openai \
    "openenv-core>=0.2.0"

# 4. Copy project files
COPY . .

# 5. Install the project using the tools already in the environment
RUN pip install --no-cache-dir --no-build-isolation .

# 6. Expose port
EXPOSE 7860

# 7. Run the entry point defined in pyproject.toml
CMD ["server"]
