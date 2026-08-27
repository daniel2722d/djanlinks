# Dockerfile del backend Django — usado por docker-compose.yml
# Construye la imagen Python con todas las dependencias de requirements.txt

FROM python:3.12-slim

WORKDIR /app

# Dependencias del sistema para PostgreSQL
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Gunicorn para producción (docker-compose usa runserver en desarrollo)
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000", "--chdir", "backend"]
