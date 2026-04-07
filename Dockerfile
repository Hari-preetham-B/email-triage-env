# Dockerfile for Email Triage Environment - Dual Mode

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

# Expose ports
EXPOSE 7860
EXPOSE 8501

# Create a startup script to run both services
RUN echo '#!/bin/bash\n\
echo "Starting OpenEnv Server on port 7860..."\n\
openenv serve --host 0.0.0.0 --port 7860 &\n\
sleep 2\n\
echo "Starting Streamlit Dashboard on port 8501..."\n\
streamlit run dashboard.py --server.port=8501 --server.address=0.0.0.0 &\n\
wait\n\
' > /app/start.sh && chmod +x /app/start.sh

# Run the startup script
CMD ["/app/start.sh"]