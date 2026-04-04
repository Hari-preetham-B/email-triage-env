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

# Expose the port for Streamlit
EXPOSE 7860

# Run Streamlit dashboard directly
CMD ["streamlit", "run", "dashboard.py", "--server.port=7860", "--server.address=0.0.0.0"]