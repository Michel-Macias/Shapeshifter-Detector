import binascii
import json
import os

# Ruta al archivo JSON de firmas
SIGNATURES_FILE = os.path.join(os.path.dirname(__file__), 'signatures.json')

def load_signatures():
    """
    Carga las firmas desde el archivo JSON.
    """
    try:
        with open(SIGNATURES_FILE, 'r') as f:
            data = json.load(f)
            return data.get('signatures', [])
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo de firmas en {SIGNATURES_FILE}")
        return []
    except json.JSONDecodeError:
        print(f"Error: El archivo de firmas {SIGNATURES_FILE} no es un JSON válido")
        return []

def get_file_signature(filepath, num_bytes=32):
    """
    Lee los primeros N bytes de un archivo y los devuelve como una cadena hexadecimal.
    Aumentamos num_bytes a 32 para cubrir firmas más largas.
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

def identify_type(hex_signature, signatures_db=None):
    """
    Compara la firma hexadecimal con la base de datos.
    Devuelve un diccionario con la información del tipo de archivo o None si no se encuentra.
    """
    if not hex_signature:
        return None

    if signatures_db is None:
        signatures_db = load_signatures()

    # Iterar a través de las firmas para encontrar una coincidencia
    for signature_entry in signatures_db:
        signature_hex = signature_entry['hex']
        if hex_signature.startswith(signature_hex):
            return signature_entry
            
    return None
