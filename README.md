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

### A. Ejecución en Sandbox (Recomendado)
Para realizar análisis en entornos aislados, utiliza el montaje de volúmenes. Debes montar tanto la carpeta de **muestras** como la de **reportes** para persistir las evidencias y la inteligencia acumulada.

```bash
# 1. Construir la imagen
docker build -t shapeshifter-engine .

# 2. Ejecutar análisis persistiendo resultados
docker run --rm \
  -v $(pwd)/muestras:/app/target \
  -v $(pwd)/reports:/app/reports \
  shapeshifter-engine /app/target --pdf --output analisis_actual.json
```

---

## 🧭 Flujo de Trabajo Operativo

1.  **Ingesta de Muestras:** Introduce los archivos sospechosos en la carpeta `./muestras`.
2.  **Detonación SAST:** Ejecuta el motor (vía Docker o nativo). El agente diseccionará el binario y consultará CTI (VirusTotal) enriqueciendo su base de datos corporativa.
3.  **Extracción de Evidencias:**
    *   Revisa la carpeta `reports/`. Encontrarás el **Dictamen Pericial PDF** y el log transaccional de la sesión.
    *   El motor habrá actualizado `memory.db` (SQLite) con los nuevos IoCs.
4.  **Inteligencia Visual:**
    *   Lanza el Dashboard: `streamlit run dashboard.py`.
    *   Explora el **Grafo de Conocimiento** para identificar si esta muestra está vinculada a ataques previos.

### B. Instalación Manual
```bash
# Clonar y blindar entorno
git clone https://github.com/Michel-Macias/Shapeshifter-Detector.git && cd Shapeshifter-Detector
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

---

## 🕹️ Control de Misión

| Comando | Descripción |
| :--- | :--- |
| `python3 main.py <ruta>` | Inicia el escaneo asíncrono profundo. |
| `python3 main.py <ruta> --pdf` | Escanea y genera Dictamen Pericial en PDF. |
| `streamlit run dashboard.py` | Lanza el Centro de Control Visual (Correlaciones & Grafos). |
| `pytest tests/` | Ejecuta la auditoría de integridad del motor. |

---

> **PROYECTO AUDITADO POR NEX-OS**  
> *"En la guerra por la información, el anonimato es el arma, pero la heurística es el escudo."*
