FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=5000

# Actualizar paquetes del SO y herramientas base de Python antes de instalar dependencias
RUN apt-get update \
    && apt-get install -y --no-install-recommends --only-upgrade libzstd1 \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir --upgrade pip setuptools wheel

# Instalar dependencias
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiar codigo de la aplicacion
COPY app ./app
COPY run.py .

# Preparar directorio para SQLite
RUN useradd --create-home --uid 10001 appuser \
    && mkdir -p /app/instance \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 5000

# Iniciar aplicacion Flask mediante Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--access-logfile", "-", "--error-logfile", "-", "run:app"]