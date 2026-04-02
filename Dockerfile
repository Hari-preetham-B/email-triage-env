# Dockerfile for Email Triage Environment

FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port for the environment server
EXPOSE 7860

# Command to run the environment server
CMD ["openenv", "serve", "--host", "0.0.0.0", "--port", "7860"]