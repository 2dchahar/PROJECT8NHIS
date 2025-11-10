# Use a lightweight official Python image as a base
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code (app.py, engine.py)
# Note: The data file will be handled by Docker Compose (Step 4)
COPY app.py .
COPY engine.py .

# Expose the port the Flask app runs on
EXPOSE 5000

# Define the command to run your application
CMD ["python", "app.py"]