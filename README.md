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

### 🛡️ Motor SAST de Grado Forense
Capaz de detectar patrones de ataque complejos en tiempo real:
- **Ransomware:** Borrado de Shadow Copies (`vssadmin`), cifrado masivo.
- **Troyanos & Persistencia:** Modificaciones en el registro de Windows (`RunKeys`), inyección de DLLs.
- **Spoofing de Extensión:** Detecta discrepancias entre el contenido binario real y la extensión del archivo.

### 📊 Observabilidad Total
- **CLI Hacker-Style:** Interfaz enriquecida con `Rich`, alertas visuales y barras de progreso.
- **Dashboard de Inteligencia:** Panel interactivo en `Streamlit` para visualizar la red de correlaciones y métricas globales.

---

## 🚀 Guía de Arranque Rápido

### 1. Preparación del Entorno
```bash
# Clonar y acceder
git clone https://github.com/Michel-Macias/Shapeshifter-Detector.git
cd Identify-files

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Uso del Agente (CLI)
Analiza archivos individuales o directorios enteros. El agente aprenderá de cada escaneo.

```bash
# Escanear un archivo (ej: detectar spoofing o malware)
python3 main.py ruta/al/archivo.exe

# Escaneo masivo de un directorio con generación de reporte
python3 main.py /descargas --output mi_reporte.json
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
