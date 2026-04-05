FROM python:3.10-slim

WORKDIR /code

# Install ONLY the necessary libraries via pip
RUN pip install --no-cache-dir fastapi uvicorn huggingface_hub python-multipart "openenv-core>=0.2.0"

# Copy your code
COPY . .

# Start the server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
