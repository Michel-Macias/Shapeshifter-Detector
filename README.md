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
- **Detección de anomalías:** Identifica cuando la extensión no coincide con el contenido real.

## 🕵️ Modo Forense (Análisis de Malware)

¡Transforma la herramienta en una navaja suiza para el análisis preliminar de malware!

Nuevas Capacidades:
-   **#️⃣ Hashes (MD5/SHA256):** Genera identificadores únicos del archivo para su rápida identificación y comparación con bases de datos de amenazas.
-   **🎲 Entropía:** Calcula la entropía del archivo, un indicador clave para detectar si el contenido está "empaquetado" o cifrado, característica común en malware avanzado.
-   **📝 Strings:** Extrae cadenas de texto legibles del binario, revelando posibles URLs, nombres de archivos, mensajes incrustados o funciones API que podrían indicar su comportamiento.

## 🛠️ Instalación y Uso

### Requisitos
- Python 3.x

### Uso Básico
Ejecuta la herramienta desde la terminal pasando la ruta del archivo o carpeta que quieres analizar:

```bash
python3 main.py /ruta/al/archivo_o_carpeta
```

### Uso del Modo Forense

Para activar el modo forense y obtener un análisis profundo de un archivo, usa el siguiente comando:

```bash
python3 main.py --forense /ruta/al/archivo_sospechoso
```

### Ejemplo de Salida (Modo Forense)

```text
Archivo: malware_sample.exe
Firma: 4D 5A 90 00
Tipo Detectado: Executable (Windows)

--- Análisis Forense ---
MD5: d41d8cd98f00b204e9800998ecf8427e
SHA256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
Entropía: 7.98 (Alto, posible empaquetado/cifrado)
Strings (fragmento):
  - "This program cannot be run in DOS mode."
  - "kernel32.dll"
  - "http://malicious.example.com/payload.bin"
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
