FROM python:3.10

WORKDIR /code

# Copy requirements first
COPY ./requirements.txt /code/requirements.txt

# Install dependencies from the list
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy everything else
COPY . .

# IMPORTANT: No "pip install ." here to avoid build errors
# Just start the server directly
CMD ["python", "main.py"]
