FROM python:3.10-slim

# Metadatos
LABEL maintainer="SysAdmin"
LABEL description="Shapeshifter-Detector Docker Sandbox"

WORKDIR /app

# Instalar dependencias del SO si fuese necesario
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el código
COPY . .

# Por defecto, ejecuta la versión de consola imprimiendo ayuda
ENTRYPOINT ["python3", "main.py"]
CMD ["--help"]
