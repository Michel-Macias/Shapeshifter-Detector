import os
import math
import hashlib
import binascii
import json
from src.logger import logger

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
        logger.error(f"No se encontró el archivo de firmas en [bold red]{SIGNATURES_FILE}[/bold red]")
        return []
    except json.JSONDecodeError:
        logger.error(f"El archivo de firmas [bold red]{SIGNATURES_FILE}[/bold red] no es un JSON válido")
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
        logger.error(f"Error leyendo el archivo [cyan]{filepath}[/cyan]: {e}")
        return None


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
        logger.error(f"Error calculando hashes para [cyan]{filepath}[/cyan]: {e}")
        return None

def calculate_entropy(filepath):
    """
    Calcula la entropía de Shannon del archivo de forma eficiente por bloques.
    Valores cercanos a 8 indican alta aleatoriedad (posible cifrado/compresión).
    """
    try:
        if not os.path.exists(filepath):
            return 0.0

        filesize = os.path.getsize(filepath)
        if filesize == 0:
            return 0.0

        byte_counts = [0] * 256
        
        with open(filepath, "rb") as f:
            while True:
                chunk = f.read(4096)
                if not chunk:
                    break
                for byte in chunk:
                    byte_counts[byte] += 1
            
        entropy = 0
        for count in byte_counts:
            if count > 0:
                p_i = float(count) / filesize
                entropy -= p_i * math.log(p_i, 2)
        
        return entropy
    except Exception as e:
        logger.error(f"Error calculando entropía para [cyan]{filepath}[/cyan]: {e}")
        return 0.0


def extract_strings(filepath, min_length=4):
    """
    Extrae cadenas de texto ASCII legibles del archivo de forma eficiente por bloques.
    Mantiene el estado entre bloques para no romper cadenas en los límites de lectura.
    """
    strings = []
    current_string = ""
    
    try:
        with open(filepath, "rb") as f:
            while True:
                chunk = f.read(4096)
                if not chunk:
                    break
                
                for byte in chunk:
                    # Caracteres ASCII imprimibles (32-126)
                    if 32 <= byte <= 126:
                        current_string += chr(byte)
                    else:
                        if len(current_string) >= min_length:
                            strings.append(current_string)
                        current_string = ""
        
        # Añadir la última cadena si quedó algo al final del archivo
        if len(current_string) >= min_length:
            strings.append(current_string)
            
        return strings
    except Exception as e:
        logger.error(f"Error extrayendo strings para [cyan]{filepath}[/cyan]: {e}")
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

