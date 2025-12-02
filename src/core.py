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

import hashlib
import math

def calculate_hashes(filepath):
    """
    Calcula los hashes MD5 y SHA256 del archivo.
    """
    md5_hash = hashlib.md5()
    sha256_hash = hashlib.sha256()
    
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                md5_hash.update(byte_block)
                sha256_hash.update(byte_block)
        return {
            "md5": md5_hash.hexdigest(),
            "sha256": sha256_hash.hexdigest()
        }
    except Exception as e:
        print(f"Error calculando hashes para {filepath}: {e}")
        return None

def calculate_entropy(filepath):
    """
    Calcula la entropía de Shannon del archivo.
    Valores cercanos a 8 indican alta aleatoriedad (posible cifrado/compresión).
    """
    try:
        with open(filepath, "rb") as f:
            data = f.read()
            
        if not data:
            return 0.0
            
        entropy = 0
        for x in range(256):
            p_x = float(data.count(bytes([x]))) / len(data)
            if p_x > 0:
                entropy += - p_x * math.log(p_x, 2)
        
        return entropy
    except Exception as e:
        print(f"Error calculando entropía para {filepath}: {e}")
        return 0.0

def extract_strings(filepath, min_length=4):
    """
    Extrae cadenas de texto ASCII y Unicode legibles del archivo.
    Útil para encontrar URLs, IPs o mensajes ocultos.
    """
    strings = []
    try:
        with open(filepath, "rb") as f:
            data = f.read()
            
        # Buscar secuencias de caracteres imprimibles
        current_string = ""
        for byte in data:
            # Caracteres ASCII imprimibles (32-126)
            if 32 <= byte <= 126:
                current_string += chr(byte)
            else:
                if len(current_string) >= min_length:
                    strings.append(current_string)
                current_string = ""
        
        # Añadir la última cadena si cumple la longitud
        if len(current_string) >= min_length:
            strings.append(current_string)
            
        return strings
    except Exception as e:
        print(f"Error extrayendo strings para {filepath}: {e}")
        return []

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

