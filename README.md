# Identify-files 🛡️

**Herramienta de Ciberseguridad de Alto Impacto** para la identificación de archivos mediante análisis de firmas binarias (Magic Numbers) y análisis forense.

## 🧐 El Problema: ¿Por qué necesitamos esto?

En el mundo digital, solemos confiar en las extensiones de archivo (como `.jpg`, `.pdf`, `.exe`) para saber qué tipo de contenido estamos manejando. Sin embargo, **las extensiones mienten**.

Cualquiera puede renombrar un archivo malicioso `virus.exe` a `foto_vacaciones.jpg`. Si intentas abrirlo, el sistema operativo podría confundirse o, peor aún, un analista de seguridad podría pasarlo por alto si solo mira el nombre.

Esta herramienta ignora la extensión del nombre y mira directamente los **Números Mágicos** (los primeros bytes del archivo) para decirte qué es realmente.

## 🚀 Funcionalidades Clave

### 🛡️ Seguridad Defensiva
*   **Detección de Spoofing:** Alerta roja inmediata si la extensión del archivo no coincide con su firma real (ej. un `.pdf` que es realmente un `.exe`).
*   **Base de Datos Externa:** Soporte para cientos de formatos, incluyendo vectores de ataque críticos como scripts de PowerShell, instaladores MSI y documentos con macros.

### 🕵️ Análisis Forense Avanzado
*   **IOCs Automáticos:** Calcula hashes **MD5** y **SHA256** para cada archivo, listos para buscar en VirusTotal.
*   **Análisis de Entropía:** Detecta archivos **empaquetados (packed)** o cifrados midiendo la aleatoriedad de sus bytes.
*   **Extracción de Strings:** Muestra cadenas de texto legibles ocultas en el binario (URLs, IPs, mensajes).

### 🎨 Experiencia de Usuario (UX/UI)
*   **CLI Profesional:** Interfaz de terminal estilo "hacker" con tablas, colores y barras de progreso (gracias a `rich`).
*   **Dashboard Web:** Panel de control gráfico con `Streamlit` para visualizar reportes, métricas y gráficos de distribución.
*   **Reportes JSON:** Exporta los resultados para integrarlos con otras herramientas SIEM o de análisis.

## 🛠️ Instalación

1.  Clona el repositorio:
    ```bash
    git clone https://github.com/Michel-Macias/Shapeshifter-Detector.git
    cd Shapeshifter-Detector
    ```

2.  Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

## 💻 Uso

### 1. Escaneo en Terminal (CLI)
Escanea un archivo o un directorio completo. La herramienta detectará automáticamente el tipo, calculará hashes y buscará anomalías.

```bash
# Escaneo básico
python3 main.py /ruta/al/archivo_o_carpeta

# Escaneo generando un reporte JSON
python3 main.py . --output reporte_seguridad.json
```

### 2. Dashboard Web
Visualiza los resultados de forma gráfica e interactiva.

1.  Genera primero un reporte JSON (ver comando anterior).
2.  Inicia el dashboard:
    ```bash
    streamlit run dashboard.py
    ```
3.  Sube el archivo `reporte_seguridad.json` en la interfaz web que se abrirá en tu navegador.

## 📂 Estructura del Proyecto

*   `src/`: Código fuente.
    *   `core.py`: Motor de análisis forense y detección.
    *   `cli.py`: Interfaz de línea de comandos profesional.
    *   `signatures.json`: Base de datos de firmas (fácilmente editable).
*   `dashboard.py`: Aplicación web para visualización de datos.
*   `tests/`: Suite de pruebas unitarias.
*   `main.py`: Punto de entrada de la aplicación.

---
Desarrollado con fines educativos y profesionales para el análisis de malware y defensa de redes.
