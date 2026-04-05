# Use an official Python image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /code

# Copy the requirements file first to cache the install step
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy all your project files into the container
COPY . .

# Tell the container to run your FastAPI server
# Port 7860 is the standard port for Hugging Face Spaces
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]