FROM python:3.10-slim

WORKDIR /code

# 1. Install system tools
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# 2. Upgrade pip and install build tools
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir hatchling setuptools

# 3. Install dependencies manually first to ensure they exist
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    huggingface_hub \
    python-multipart \
    "openenv-core>=0.2.0"

# 4. Copy project files
COPY . .

# 5. Install the project (NO '-e' flag)
# This installs the code as a standard library in site-packages
RUN pip install --no-cache-dir .

# 6. Expose port
EXPOSE 7860

# 7. Run the entry point defined in pyproject.toml
CMD ["server"]
