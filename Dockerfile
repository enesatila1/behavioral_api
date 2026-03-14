FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Note: .env is git-ignored. Either:
# 1. Copy .env if present: docker build --build-context=extra=.env
# 2. Or pass env vars at runtime: docker run -e FIREBASE_CREDENTIALS="..."
# 3. Or use docker-compose with env_file: .env

EXPOSE 8000

ENV PYTHONPATH=/app

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]