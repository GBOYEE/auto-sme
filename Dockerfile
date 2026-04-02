# AutoSME Backend
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY pyproject.toml .
RUN pip install --no-cache-dir -e .[dev]

# Copy source
COPY . .

ENV AUTOSME_ENV=production
ENV AUTOSME_PORT=8000

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "src.auto_sme.main:app", "--host", "0.0.0.0", "--port", "8000"]
