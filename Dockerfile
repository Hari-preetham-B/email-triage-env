FROM python:3.10-slim

WORKDIR /app

# Install only essential system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Copy only requirements first (better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy only necessary files for API server
COPY server.py models.py environment.py tasks.py openenv.yaml ./

# Copy email data files
COPY emails_*.json ./

EXPOSE 7860

CMD ["python", "server.py", "--port", "7860"]