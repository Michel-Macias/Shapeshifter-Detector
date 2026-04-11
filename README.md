# 🛡️ Identify-Files (Shapeshifter-Detector)
## *Agente de Inteligencia Forense con Memoria y Detección de Amenazas Activa*

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Accuracy](https://img.shields.io/badge/Agent_Accuracy-100%25-brightgreen.svg)](#)
[![Security SAST](https://img.shields.io/badge/Security-Advanced_SAST-red.svg)](#)

**Identify-Files** es un agente forense avanzado diseñado para la detección de amenazas mediante el análisis de **firmas digitales binarias** (Magic Numbers) y **análisis estático profundo (SAST)**. A diferencia de las herramientas tradicionales, este agente posee **Memoria Persistente**, lo que le permite correlacionar Indicadores de Compromiso (IoCs) entre diferentes sesiones de análisis.

---

## ✨ Características de Élite

### 🧠 Memoria del Agente (Knowledge Base)
El agente no analiza en el vacío. Cada vez que encuentra una **IP, URL o Dominio**, lo registra en su base de conocimientos (`memory.json`). 
- **Correlación Cruzada:** Si una IP maliciosa aparece en dos archivos diferentes, el agente te alertará del vínculo.
- **Deduplicación:** Evita el re-análisis innecesario de archivos ya conocidos mediante hashing SHA256.

### 🛡️ Motor SAST de Grado Forense (Multi-Hilo)
Capaz de detectar patrones de ataque complejos a velocidades concurrentes:
- **Ransomware:** Borrado de Shadow Copies (`vssadmin`), cifrado masivo.
- **Troyanos & Persistencia:** Modificaciones en el registro de Windows (`RunKeys`), inyección de DLLs.
- **Spoofing de Extensión:** Detecta discrepancias entre el contenido binario real y su magia hexadecimal.
- **Heurística de Compilados:** Escaneo de cabeceras de SO (`pefile`) descubriendo secciones con alta entropía (Ofuscación/Packers).

### 🌐 Cyber Threat Intelligence (CTI)
- **VirusTotal Integrado:** Contrastación nativa de cualquier Hash sospechoso para certificar el veredicto en tiempo real con 100 puntos extra de "Paranoia".

### 📊 Observabilidad Total
- **CLI Hacker-Style:** Interfaz asíncrona enriquecida con `Rich`, barras en paralelo y mitigación de solapamiento gráfico.
- **Dashboard de Inteligencia:** Panel interactivo en `Streamlit` para visualizar correlaciones y dominios.
- **Dictámenes Periciales:** Exportación de evidencias ejecutivas usando la bandera `--pdf` para resúmenes a gerencia.

---

## 🚀 Guía de Arranque Rápido

### 1. Preparación del Entorno
```bash
# Clonar y acceder
git clone https://github.com/Michel-Macias/Shapeshifter-Detector.git
cd Shapeshifter-Detector

# Crear y activar entorno virtual (Recomendado para evitar PEP 668)
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Uso del Agente (CLI)
Analiza archivos individuales o directorios enteros. El motor paralelo asimilará cada escaneo a velocidades altas.

```bash
# Escanear un archivo base de prueba
python3 main.py ruta/al/archivo.exe

# Escaneo masivo con extracción de evidencias y dictamen PDF
python3 main.py /descargas --output reporte.json --pdf
```

### 3. Visualización de Inteligencia (Dashboard)
Lanza el panel gráfico para ver qué ha aprendido el agente.

```bash
streamlit run dashboard.py
```
*Carga el archivo `reports/mi_reporte.json` para ver las métricas y la pestaña de **"Inteligencia"**.*

### 4. Validación del Sistema
Verifica que el agente mantiene su **100% de precisión** con la suite de evaluación.

```bash
python3 evaluate_agent.py
```

---

## 📁 Estructura del "Cerebro"
- `src/core.py`: Motor de detección, firmas e IoCs.
- `src/memory.py`: Sistema de persistencia y correlación.
- `src/cli.py`: Interfaz de terminal y lógica de deduplicación.
- `reports/memory.json`: La base de conocimientos viva del agente.

---
*Desarrollado para la ciberseguridad avanzada y análisis forense proactivo.*
