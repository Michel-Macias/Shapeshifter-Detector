# 🛡️ Identify-Files: Detector de Amenazas por Firma Digital
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![TDD Certified](https://img.shields.io/badge/Methodology-TDD-green.svg)](https://en.wikipedia.org/wiki/Test-driven_development)
[![Security Scan](https://img.shields.io/badge/Security-SAST%20Enabled-red.svg)](#)

**Identify-Files** (nombre en GitHub: *Shapeshifter-Detector*) es una herramienta de defensa activa y análisis forense diseñada para revelar la verdadera identidad de cualquier archivo. Ignora la extensión declarada y analiza el **contenido binario real** (Magic Numbers).

> **¿Sabías que...?** Los atacantes suelen renombrar `.exe` a `.jpg` para evadir controles. Con esta herramienta, ese engaño es detectado en milisegundos.

---

## 🎯 ¿Por qué Identify-Files?
En ciberseguridad, la confianza ciega en las extensiones de archivo es un vector de compromiso crítico. 

- **Forense Real**: Basado en números mágicos, no en metadatos editables.
- **Detección de Spoofing**: Alerta sobre discrepancias entre extensión y contenido.
- **Análisis de Vulnerabilidades (SAST)**: Busca patrones de backdoors, shellshells y secretos expuestos dentro de los archivos.
- **Optimizado para Gigabytes**: Motor de procesamiento por bloques que cuida tu memoria RAM.

## 🎥 Video de Demostración
Mira la herramienta en acción:

[![Video de Demostración](https://img.youtube.com/vi/By_SXV3f808/maxresdefault.jpg)](https://youtu.be/By_SXV3f808?si=FdgXz23D_SfSd8dD)

*Haz clic en la imagen para ver el análisis forense completo: detección de tipos, cálculo de hashes, análisis de entropía y visualización en el dashboard.*

## ✨ Características y Beneficios Clave
- 🛡️ **Detección de Spoofing:** Alerta roja inmediata si la extensión no coincide con la firma real.
- 🕵️ **Análisis Forense Escalable:** Procesamiento por bloques (Chunking) para archivos de gran tamaño.
- 🔍 **Motor de Vulnerabilidades (SAST):** Análisis estático en busca de IoCs, backdoors, inyecciones de código (eval/os.system) y secretos hardcodeados.
- 📊 **Métricas Avanzadas:** Cálculo de hashes (MD5, SHA256) y entropía de Shannon.
- 📝 **Inteligencia de Strings:** Extracción incremental de cadenas legibles (URLs, IPs, metadatos).
- 🎨 **Experiencia Profesional:**
    - **CLI Hacker-Style:** Interfaz enriquecida con `Rich`, barras de progreso y logging profesional.
    - **Dashboard Web:** Panel gráfico interactivo (Streamlit) para análisis masivo.
- 💾 **Base de Datos Extensible:** Firmas gestionadas en JSON externo, soportando cientos de formatos y vectores de ataque.

## 🚀 Primeros Pasos

### 1. Clonar el repositorio
```bash
git clone https://github.com/Michel-Macias/Shapeshifter-Detector.git
cd Shapeshifter-Detector
```

### 2. Instalar dependencias
Se recomienda usar un entorno virtual.
```bash
pip install -r requirements.txt
```

## 🎯 Uso Detallado

### Modo Terminal (CLI)
Ideal para análisis rápido o integración en scripts. El análisis forense y el escaneo de vulnerabilidades se ejecutan de forma **autónoma** en cada archivo.

```bash
# Escaneo de un solo archivo (Muestra firmas, hashes, entropía y vulnerabilidades)
python3 main.py archivo_sospechoso.exe

# Escaneo masivo de directorio con reporte JSON completo
python3 main.py /ruta/descargas --output reporte_forense.json
```

**Interpretación de Alertas:**
- 🔴 **ALERTA CRÍTICA (Spoofing)**: El archivo miente sobre su extensión.
- 🟡 **ADVERTENCIA (Entropía)**: El archivo podría estar cifrado o empaquetado (común en malware).
- 🚩 **Hallazgos de Seguridad (SAST)**: Lista de líneas sospechosas (ej. sockets, exec, eval) detectadas en el código.

### Modo Gráfico (Dashboard)
Ideal para visualizar hallazgos y presentar reportes.

```bash
streamlit run dashboard.py
```
*Sube el archivo `reporte_forense.json` generado anteriormente para ver las métricas.*

## 📁 Estructura del Proyecto
```
Identify-Files/
├── README.md           # Este archivo
├── .gitignore          # Archivos ignorados
├── requirements.txt    # Dependencias del proyecto
├── main.py             # Punto de entrada CLI
├── dashboard.py        # Interfaz web (Streamlit)
├── src/                # Código fuente principal
│   ├── core.py         # Motor de análisis (Optimizado para memoria)
│   ├── cli.py          # Interfaz de terminal (Rich e integración de logs)
│   ├── logger.py       # Sistema de eventos centralizado
│   └── signatures.json # Base de datos de firmas
└── tests/              # Tests unitarios
```

## 🛠️ Tecnologías Utilizadas
- **[Python 3.x](https://www.python.org/):** Lenguaje base.
- **[Rich](https://github.com/Textualize/rich):** Para una CLI moderna y visual.
- **[Streamlit](https://streamlit.io/):** Para el dashboard de análisis de datos.
- **[Pandas](https://pandas.pydata.org/):** Procesamiento de datos de reportes.
- **[Hashlib & Math](https://docs.python.org/3/library/):** Cálculos criptográficos y matemáticos.

## 🔐 Seguridad
- Esta herramienta es de **solo lectura**: no modifica los archivos analizados.
- Se recomienda ejecutarla en un entorno aislado (Sandbox) al analizar malware real.

## 🧪 Testing
El proyecto cuenta con una suite de pruebas unitarias para asegurar la fiabilidad de la detección.

```bash
python3 -m unittest discover tests
```

## 👤 Autor
**Michel Macias**
- GitHub: [@MaciasIT](https://github.com/MaciasIT)

---
*Desarrollado como parte del portafolio de ciberseguridad avanzada.*
