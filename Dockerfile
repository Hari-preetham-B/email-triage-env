FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server/ ./server/
COPY models.py environment.py tasks.py random_agent.py ./
COPY emails_*.json ./

ENV PYTHONPATH=/app

EXPOSE 7860

CMD ["python", "-m", "server.app"]