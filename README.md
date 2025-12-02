# 🛡️ Identify-Files: Detector de Amenazas por Firma Digital

**Proyecto de Ciberseguridad de Alto Impacto** 

## 💡 El Problema: La Mentira de las Extensiones
En el panorama actual de ciberseguridad, confiar en las extensiones de archivo es un error fatal. Los atacantes utilizan técnicas de **Extension Spoofing** (ej. renombrar `malware.exe` a `factura.pdf`) para evadir controles básicos y engañar a usuarios y analistas.

Las herramientas tradicionales o la inspección visual simple no son suficientes para detectar estas amenazas ocultas a simple vista.

## 🚀 La Solución: Identify-Files
**Identify-Files** es una herramienta de defensa activa y análisis forense diseñada para revelar la verdadera identidad de cualquier archivo. Utiliza **Magic Numbers** (firmas binarias) para ignorar la extensión declarada y analizar el contenido real del archivo.

Más que un simple identificador, es una suite forense que alerta sobre discrepancias, calcula indicadores de compromiso (IOCs) y detecta técnicas de ofuscación como el "packing".

## ✨ Características y Beneficios Clave
- 🛡️ **Detección de Spoofing:** Alerta roja inmediata si la extensión no coincide con la firma real.
- 🕵️ **Análisis Forense Profundo:** Cálculo automático de hashes (MD5, SHA256) y análisis de entropía para detectar cifrado/packing.
- 📝 **Inteligencia de Strings:** Extracción de cadenas legibles para hallar URLs de C2 o mensajes ocultos.
- 🎨 **Experiencia Profesional:**
    - **CLI Hacker-Style:** Interfaz de terminal con tablas y colores (Rich).
    - **Dashboard Web:** Panel gráfico interactivo (Streamlit) para reportes ejecutivos.
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
Ideal para análisis rápido o integración en scripts.

```bash
# Escaneo de un solo archivo
python3 main.py archivo_sospechoso.exe

# Escaneo masivo de directorio con reporte JSON
python3 main.py /ruta/descargas --output reporte_forense.json
```

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
│   ├── core.py         # Motor de análisis y lógica forense
│   ├── cli.py          # Interfaz de terminal (Rich)
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
