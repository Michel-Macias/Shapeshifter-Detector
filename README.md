# 🛡️ Shapeshifter-Detector Enterprise
**Plataforma de Inteligencia Forense y Análisis Estático de Amenazas (SAST)**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Sandboxed-2496ED.svg)](#)
[![Security](https://img.shields.io/badge/Paranoia-Max-red.svg)](#)
[![Status](https://img.shields.io/badge/Status-Production_Ready-brightgreen.svg)](#)

**Shapeshifter-Detector** no es solo un simple script de escaneo; es una **plataforma forense asíncrona de alto rendimiento** diseñada para equipos de SOC (Security Operations Center) y Sysadmins puristas. 

Su motor escudriña el ADN binario de grandes volúmenes de archivos para desmantelar ataques de *Spoofing* (camuflaje de extensiones), detectar troyanos empaquetados e identificar Indicadores de Compromiso (IoCs cruzados) entre múltiples incidentes, todo sin depender en primera instancia de bases de datos de antivirus comerciales, sino del crudo análisis heurístico.

---

## ⚡ Capacidades Core

### 🧬 Motor Heurístico Híbrido
- **Inspección de Firmas Binarias:** Destruye cualquier intento de camuflaje cruzando las extensiones lógicas contra los verdaderos *Magic Numbers* hexadecimales del archivo.
- **Análisis de Cabeceras PE Profundo:** Utiliza la librería `pefile` para destripar la estructura de binarios Windows, detectando anomalías, funciones importadas sospechosas (*VirtualAllocEx*, *CreateRemoteThread*) y midiendo la **Entropía de secciones** (>7.5) para exponer tácticas de *Ransomware* y código empaquetado/ofuscado.
- **Escaneo Concurrente:** Procesamiento asíncrono con `ThreadPoolExecutor`, destruyendo cientos de binarios en apenas segundos. 

### 🌐 Cyber Threat Intelligence Automatizada
- Integración nativa con **VirusTotal (API v3)**. Una vez destripado el binario lógicamente, contrastamos sus hashes SHA-256 en tiempo real. 
- Castigos heurísticos: Operamos en "Paranoia Máxima". Cualquier formato desconocido o discrepancia lanza las alarmas a nivel crítico. Todo positivo en redes CTI suma 100 puntos inmediatos al puntaje de amenaza.

### 🧠 Inteligencia Forense Viva (Memoria ACID)
- **Base de Datos SQLite Tolerante a Fallos:** Despídete de los archivos huérfanos. La memoria histórica del agente (conocimiento acumulativo de escaneos) reside en un motor transaccional en `C` altamente escalable.
- **Correlación de Redes (Grafos 3D):** Identifica cuando un actor malicioso usa la misma IP en tres binarios diferentes, construyendo modelos matemáticos para predecir tácticas.

### 📊 Visibilidad Ejecutiva
- **Consola Hacker-Style:** Monitorización limpia CLI mediante librerías `Rich`.
- **Informes PDF Automatizados:** Si lanzas el comando con la flag `--pdf`, el motor vomita el dictamen sumariado en un formato formal e imprimible.
- **Centro de Control Streamlit:** Dashboard web robusto con visualizaciones *Dark-Cyber* interactivas, animaciones reactivas y mapeos de Grafos interactivos de las amenazas.

---

## 🛠️ Arquitectura y Despliegue CI/CD

Integramos filosofía Zero-Trust. El proyecto es auditado por `GitHub Actions` disparando la suite `pytest` (`tests/test_core.py`) en cada Pull Request para asegurar que el core de validación entrópica nunca sea alterado.

Contamos con una base `Dockerfile` oficial para aislar el escáner del sistema de archivos *Host*, evitando riesgos severos al detonar entornos de malware activo.

---

## 🚀 Guía Rápida de Despliegue

### 1. Instalación Standard (Entorno Nativo)

```bash
git clone https://github.com/Michel-Macias/Shapeshifter-Detector.git
cd Shapeshifter-Detector

# Aislar dependencias (Evitar PEP-668 del OS base)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# (Opcional) Renombra el .env.example a .env y añade tus claves de Cyber-Inteligencia.
```

### 2. Sandbox Mode (Docker)
Altamente recomendado si vas a escanear carpetas reales extraídas de incidentes corporativos:
```bash
docker build -t shapeshifter-engine .
docker run --rm -v /ruta/archivos/infectados:/target shapeshifter-engine /target
```

---

## 💻 Control Operativo

### A. Escáner de Terminal (CLI)
Escanea de forma salvaje y genera directamente el PDF pericial.

```bash
# Analiza todo tu entorno de Descargas de un plumazo
python3 main.py /home/user/Downloads --output mi_reporte.json --pdf
```

### B. Módulo Gráfico SOC (Dashboard)
Arranca el radar web y conecta tu inteligencia visual. Sube tu `.json` autogenerado y observa los mapas de relaciones en formato Grafo 3D.

```bash
streamlit run dashboard.py
```

---

*Prototipado por Nex-OS | Diseñado para la investigación forense agresiva y proactiva.*
