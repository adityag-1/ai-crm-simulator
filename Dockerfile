# Use Python 3.10 as the base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /code

# 1. Copy requirements and pyproject.toml first to leverage Docker cache
COPY ./requirements.txt /code/requirements.txt
COPY ./pyproject.toml /code/pyproject.toml

# 2. Install dependencies
# We install '.' to recognize the project as a package (fixes multi-mode error)
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip install --no-cache-dir .

# 3. Copy the rest of the application code
COPY . .

# 4. Expose the port Hugging Face expects
EXPOSE 7860

# 5. Start the FastAPI server
# We use 0.0.0.0 to allow external traffic to reach the container
CMD ["python", "main.py"]
