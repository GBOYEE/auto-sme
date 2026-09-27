# AUTO-SME V1 engine
FROM python:3.12-slim

WORKDIR /app

# WeasyPrint system libs (Debian)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz-subset0 libjpeg-dev libopenjp2-7-dev libffi-dev gcc \
 && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
RUN pip install --no-cache-dir -e .

COPY templates/ templates/
COPY styles/ styles/
COPY src/ src/

ENTRYPOINT ["python", "-m", "auto_sme.cli"]
CMD ["--help"]
