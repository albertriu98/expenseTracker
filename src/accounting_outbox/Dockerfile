FROM python:3.12-slim

# Prevent python buffering
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first (better layer caching)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Run worker
CMD ["python", "-m", "src.main"]