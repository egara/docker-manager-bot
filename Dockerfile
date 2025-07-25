# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code
COPY src/ /app/src/

# Set PYTHONPATH to include the /app directory for module imports
ENV PYTHONPATH=/app

# Run main.py when the container launches
CMD ["python3", "src/main.py"]
