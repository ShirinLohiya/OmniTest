# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# Include pytest for running unit tests
RUN pip install --no-cache-dir -r requirements.txt pytest

# Copy the rest of the application code
COPY . .

# Create a volume for results so they can be persisted
VOLUME /app/results

# By default, run the main.py script with the sample dataset
CMD ["python", "main.py", "data/sample_tests.json"]
