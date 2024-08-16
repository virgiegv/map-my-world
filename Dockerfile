# Use the official Python image from the Docker Hub
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN python -m ensurepip --upgrade
RUN python -m pip install --upgrade setuptools
RUN python -m pip install --no-cache-dir -r requirements.txt
RUN python -m pip install "fastapi[standard]"

# Copy the rest of the application code into the container
COPY . .

RUN apt-get update && apt-get install -y ca-certificates && rm -rf /var/lib/apt/lists/*

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]