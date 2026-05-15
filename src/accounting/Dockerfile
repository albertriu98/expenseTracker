# Build from project root so the full src/ tree is available:
#   docker build -f src/accounting/Dockerfile -t albertriu/accounting-api:0.0.1 .

FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq-dev \
        gcc \
    && rm -rf /var/lib/apt/lists/*

COPY src/accounting/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

EXPOSE 8000

CMD ["uvicorn", "src.accounting.main:app", "--host", "0.0.0.0", "--port", "8000"]
