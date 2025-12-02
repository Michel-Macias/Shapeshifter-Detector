import binascii
from src.signatures import SIGNATURES

def get_file_signature(filepath, num_bytes=16):
    """
    Lee los primeros N bytes de un archivo y los devuelve como una cadena hexadecimal.
    """
    try:
        with open(filepath, 'rb') as f:
            chunk = f.read(num_bytes)
            # Convertir bytes a cadena hex (ej: b'\x89PNG' -> '89 50 4E 47')
            hex_str = binascii.hexlify(chunk).decode('utf-8').upper()
            # Formatear con espacios para legibilidad y coincidencia
            formatted_hex = ' '.join(hex_str[i:i+2] for i in range(0, len(hex_str), 2))
            return formatted_hex
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Error leyendo el archivo {filepath}: {e}")
        return None

def identify_type(hex_signature):
    """
    Compara la firma hexadecimal con la base de datos.
    Devuelve el tipo de archivo o 'Desconocido'.
    """
    if not hex_signature:
        return "Error: No se pudo leer la firma del archivo"

    # Iterar a través de las firmas para encontrar una coincidencia
    # Verificamos si la firma del archivo COMIENZA con la firma conocida
    for signature, file_type in SIGNATURES.items():
        if hex_signature.startswith(signature):
            return file_type
            
    return "Tipo de Archivo Desconocido"
