FROM python:3.10-slim

# Metadatos
LABEL maintainer="SysAdmin"
LABEL description="Shapeshifter-Detector Docker Sandbox"

WORKDIR /app

# Instalar dependencias del SO necesarias para compilar paquetes C
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario no-root para seguridad
RUN groupadd -r app && useradd -r -g app app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --no-cache-dir -r requirements.txt

# Copiar el código y establecer pertenencia al usuario no-root
COPY --chown=app:app . .

# Ejecutar como usuario no-root
USER app

# Por defecto, ejecuta la versión de consola imprimiendo ayuda
ENTRYPOINT ["python3", "main.py"]
CMD ["--help"]