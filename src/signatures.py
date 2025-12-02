# Base de datos de firmas de archivo (Números Mágicos)
# Formato: 'FIRMA_HEX': 'TIPO_DE_ARCHIVO'
# Las firmas se almacenan como cadenas hexadecimales separadas por espacios para mayor legibilidad.

SIGNATURES = {
    # Imágenes
    '89 50 4E 47 0D 0A 1A 0A': 'Imagen PNG',
    'FF D8 FF': 'Imagen JPEG',
    '47 49 46 38 37 61': 'Imagen GIF (87a)',
    '47 49 46 38 39 61': 'Imagen GIF (89a)',
    '42 4D': 'Imagen BMP',
    
    # Documentos
    '25 50 44 46': 'Documento PDF',
    'D0 CF 11 E0 A1 B1 1A E1': 'Documento Microsoft Office (Legacy)',
    '50 4B 03 04': 'Archivo ZIP / Office Open XML',
    
    # Ejecutables
    '4D 5A': 'Ejecutable de Windows (EXE/DLL)',
    '7F 45 4C 46': 'Ejecutable ELF (Linux)',
    
    # Archivos Comprimidos
    '1F 8B': 'Archivo GZIP',
    '52 61 72 21 1A 07 00': 'Archivo RAR',
    '37 7A BC AF 27 1C': 'Archivo 7z',
    
    # Audio/Video
    '49 44 33': 'Audio MP3 (ID3v2)',
    'FF FB': 'Audio MP3 (MPEG-1 Layer 3)',
    '00 00 00 18 66 74 79 70 6D 70 34 32': 'Video MP4',
    '1A 45 DF A3': 'Video Matroska (MKV/WebM)'
}
