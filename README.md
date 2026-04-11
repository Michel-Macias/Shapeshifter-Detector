# 🛡️ SHAPESHIFTER-DETECTOR: ENTERPRISE FORENSIC ENGINE
> **Asynchronous Static Analysis & Correlation Intelligence Platform**

[![Engine](https://img.shields.io/badge/Engine-Asynchronous_Multithread-00f2fe.svg)](#)
[![Security](https://img.shields.io/badge/Posture-Paranoia_Max-red.svg)](#)
[![Infrastructure](https://img.shields.io/badge/Infra-Docker_&_CI--CD-brightgreen.svg)](#)
[![CTI](https://img.shields.io/badge/Intel-VirusTotal_v3-blue.svg)](#)

**Shapeshifter-Detector** es un ecosistema de alta fidelidad diseñado para la **contrainteligencia forense**. A diferencia de los scanners tradicionales basados en firmas estáticas de terceros, nuestro motor opera mediante el análisis profundo del **DNA binario**, la reconstrucción heurística de cabeceras y la correlación atómica de IoCs en una base de conocimientos persistente.

---

## 💎 Valor Operativo (Hacked-Mindset)

### 🚀 Motor de Ejecución Asíncrona
Diseñado para el triage de incidentes masivos. Utiliza una arquitectura de **Hilos Concurrentes (ThreadPool)** que permite procesar repositorios enteros de malware en segundos, sin bloqueos y con mitigación de solapamiento gráfico en consola.

### 🧬 Análisis Heurístico de DNA Binario
- **Desmitificación de Spoofing:** Validación cruzada de *Magic Numbers* contra extensiones lógicas. Si miente, el motor lo encadena.
- **Deep PE dissection:** Análisis estructural de binarios Windows (`pefile`). Detecta **Entropía Crítica (>7.5)** típica de Ransomware y expone importaciones sospechosas de bajo nivel (*Hooking/Injection*).

### 🧠 Memoria Correlacional (Persistent Knowledge)
No es un escáner efímero. Cada análisis alimenta un **Knowledge Base transaccional (SQLite/ACID)**. 
- El sistema detecta cuando una IP maliciosa o un dominio visto en un incidente previo reaparece en una nueva muestra.
- **Visualización 3D de Amenazas:** Genera grafos interactivos de correlación para mapear la infraestructura del atacante.

### 🌐 Vigilancia CTI (VirusTotal v3)
Enriquecimiento de evidencias mediante integración nativa con redes de inteligencia externa. Valida el veredicto heurístico con la autoridad global de VirusTotal de forma automatizada.

---

## 🏗️ Infraestructura de Grado Producción

- **Sandboxing Nativo:** Implementación de `Dockerfile` para la detonación y análisis en entornos aislados, protegiendo la integridad del Host.
- **Ciclo de Vida CI/CD:** Pipeline automatizado en GitHub Actions. Cada línea de código es auditada mediante pruebas de regresión y validación de seguridad (`pytest`).
- **Dictámenes Ejecutivos:** Generación automatizada de reportes **PDF Forenses** mediante la bandera `--pdf`, listos para ser presentados como evidencias periciales o reportes a gerencia.

---

## ⚡ Guía de Despliegue Táctico

### A. Auditoría Rápida con Docker (Test de Humo)
Para verificar que el motor funciona, lánzalo contra tu directorio actual. Analizará los archivos del repositorio y generará un reporte PDF instantáneo:

```bash
# 1. Construir el motor
docker build -t shapeshifter-engine .

# 2. Analizar el directorio actual (donde estás ahora)
docker run --rm \
  -v $(pwd):/app/target \
  -v $(pwd)/reports:/app/reports \
  shapeshifter-engine /app/target --pdf
```
*Esto mapea tu ubicación actual al motor. Verás la barra de progreso y se creará un Dictamen PDF en `./reports/`.*

---

## 🛠️ Uso Forense Avanzado (Sysadmin)
Si necesitas auditar una ruta específica del servidor sin mover archivos:

```bash
docker run --rm \
  -v /RUTA/DEL/INCIDENTE:/app/target \
  -v $(pwd)/reports:/app/reports \
  shapeshifter-engine /app/target --pdf
```

---

## 🧭 Flujo de Trabajo Operativo

1.  **Ingesta de Muestras:** Introduce los archivos sospechosos en la carpeta `./muestras`.
2.  **Detonación SAST:** Ejecuta el motor (vía Docker o nativo). El agente diseccionará el binario y consultará CTI (VirusTotal) enriqueciendo su base de datos corporativa.
3.  **Extracción de Evidencias:**
    *   Revisa la carpeta `reports/`. Encontrarás el **Dictamen Pericial PDF** y el log transaccional de la sesión.
    *   El motor habrá actualizado `memory.db` (SQLite) con los nuevos IoCs.

---

## 📊 Dashboard de Inteligencia

Para visualizar los hallazgos persistidos en SQLite:

### Opción 1: Docker (Recomendado)
Levanta el dashboard sin instalar dependencias locales:
```bash
docker run --rm -it \
  -p 8501:8501 \
  -v $(pwd)/reports:/app/reports \
  --entrypoint streamlit \
  shapeshifter-engine run dashboard.py --server.address 0.0.0.0
```
> Accede en: `http://localhost:8501`

### Opción 2: Local (Host)
```bash
# Asegúrate de activar tu entorno virtual
source venv/bin/activate
streamlit run dashboard.py
```

---

## 🛠️ Solución de Problemas (FAQ)

### 1. Error: `externally-managed-environment`
**Solución:** Estás en un sistema Linux moderno. Usa la **Opción 1 (Docker)** o crea un entorno virtual (`python3 -m venv venv && source venv/bin/activate`).

### 2. Error: `no such column: cti_hits`
**Solución:** Reconstruye la imagen (`docker build -t shapeshifter-engine .`). El motor reparará la base de datos automáticamente en su próximo arranque.

---

> **PROYECTO AUDITADO POR NEX-OS**  
> *"En la guerra por la información, el anonimato es el arma, pero la heurística es el escudo."*
