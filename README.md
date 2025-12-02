# Identify-files

Una herramienta de ciberseguridad en Python para identificar tipos de archivos reales utilizando sus "números mágicos" (firmas de archivo).

## 🧐 El Problema: ¿Por qué necesitamos esto?

En el mundo digital, solemos confiar en las extensiones de archivo (como `.jpg`, `.pdf`, `.exe`) para saber qué tipo de contenido estamos manejando. Sin embargo, **las extensiones mienten**.

Cualquiera puede renombrar un archivo malicioso `virus.exe` a `foto_vacaciones.jpg`. Si intentas abrirlo, el sistema operativo podría confundirse o, peor aún, un analista de seguridad podría pasarlo por alto si solo mira el nombre.

### ¿Qué son los Números Mágicos?
Los archivos tienen una "huella digital" interna: los primeros bytes de su contenido binario. Estos bytes son únicos para cada formato y se conocen como **Números Mágicos** o *File Signatures*.

Por ejemplo:
- Un archivo **PNG** siempre empieza con: `89 50 4E 47`
- Un **PDF** siempre empieza con: `25 50 44 46`

Esta herramienta ignora la extensión del nombre y mira directamente estos bytes para decirte qué es realmente el archivo.

## 🚀 Funcionalidades
- **Base de datos de firmas:** Reconoce formatos comunes (Imágenes, Documentos, Ejecutables, Archivos comprimidos).
- **Escaneo inteligente:** Analiza archivos individuales o directorios completos recursivamente.
- **Detección de anomalías:** Identifica cuando la extensión no coincide con el contenido real (Próximamente).

## 🛠️ Instalación y Uso

### Requisitos
- Python 3.x

### Uso Básico
Ejecuta la herramienta desde la terminal pasando la ruta del archivo o carpeta que quieres analizar:

```bash
python3 main.py /ruta/al/archivo_o_carpeta
```

### Ejemplo de Salida
```text
Archivo: documento_sospechoso.jpg
Firma: 25 50 44 46
Tipo Detectado: PDF Document
```
*¡Alerta! Un archivo con extensión .jpg que en realidad es un PDF.*

## 📂 Estructura del Proyecto
- `src/`: Código fuente de la herramienta.
  - `core.py`: Lógica principal de lectura e identificación.
  - `signatures.py`: Base de datos de firmas hexadecimales.
  - `cli.py`: Interfaz de línea de comandos.
- `tests/`: Pruebas unitarias para asegurar que todo funciona correctamente.
