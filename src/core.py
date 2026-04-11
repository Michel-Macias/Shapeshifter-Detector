import os
import math
import hashlib
import binascii
import json
import re
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

def identify_iocs(strings):
    """
    Analiza una lista de strings en busca de Indicadores de Compromiso (IoCs).
    Retorna un diccionario clasificado por tipo (IPs, URLs, Dominios).
    """
    iocs = {
        "ips": set(),
        "urls": set(),
        "domains": set()
    }
    
    # Regex para IPv4
    ip_pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
    # Regex para URLs (http/https/ftp)
    url_pattern = r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/\w\.-]*"
    # Regex para dominios (muy simplificado para evitar falsos positivos)
    domain_pattern = r"\b[a-zA-Z0-9.-]+\.(?:com|net|org|io|gov|edu|xyz|top|pw|sh|bin)\b"

    for s in strings:
        # Buscar IPs
        ips = re.findall(ip_pattern, s)
        for ip in ips:
            # Validación básica de octetos (0-255)
            try:
                if all(0 <= int(part) <= 255 for part in ip.split('.')):
                    iocs["ips"].add(ip)
            except ValueError:
                continue
        
        # Buscar URLs
        urls = re.findall(url_pattern, s)
        for url in urls:
            iocs["urls"].add(url)
            
        # Buscar Dominios (solo si no es ya una URL o IP)
        if not urls and not ips:
            domains = re.findall(domain_pattern, s)
            for domain in domains:
                iocs["domains"].add(domain)

    # Convertir sets a listas para serialización JSON
    return {k: list(v) for k, v in iocs.items() if v}

try:
    import yara
    YARA_AVAILABLE = True
except ImportError:
    YARA_AVAILABLE = False

# Ruta al directorio de reglas YARA
YARA_RULES_DIR = os.path.join(os.path.dirname(__file__), '..', 'rules')

def analyze_vulnerabilities(filepath):
    """
    Realiza un análisis estático del archivo buscando patrones de vulnerabilidades
    o indicadores de compromiso (IoC) comunes.
    
    Combina reglas basadas en Regex con escaneo YARA si está disponible.
    """
    
    # Excluir archivos de definición de tipos de Python
    if filepath.endswith('.pyi'):
        return []
    
    findings = []
    
    # --- ANÁLISIS YARA (Si está disponible) ---
    if YARA_AVAILABLE and os.path.exists(YARA_RULES_DIR):
        try:
            # Compilar todas las reglas en el directorio
            rule_files = {f: os.path.join(YARA_RULES_DIR, f) for f in os.listdir(YARA_RULES_DIR) if f.endswith('.yar')}
            if rule_files:
                rules = yara.compile(filepaths=rule_files)
                matches = rules.match(filepath)
                for match in matches:
                    findings.append({
                        "rule": f"YARA: {match.rule}",
                        "severity": match.meta.get("severity", "Alta"),
                        "line": "N/A",
                        "content": match.meta.get("description", "Coincidencia de regla YARA")
                    })
        except Exception as e:
            logger.error(f"Error en escaneo YARA para [cyan]{filepath}[/cyan]: {e}")

    # --- ANÁLISIS REGEX (Fallback/Complementario) ---
    # Patrones de riesgo comunes (Regex)
    RULES = [
        # --- CÓDIGO DINÁMICO Y OFUSCACIÓN ---
        {"name": "Ejecución de Código Dinámico", "pattern": r"(eval\(|exec\(|os\.system\(|subprocess\.Popen\()", "severity": "Alta"},
        {"name": "Posible Web Shell / Ofuscación", "pattern": r"(base64_decode|eval\(gzinflate|eval\(base64_decode)", "severity": "Crítica"},
        {"name": "Hardcoded Secret/Token", "pattern": r"(API_KEY|SECRET|PASSWORD|TOKEN)\s*=\s*['\"][a-zA-Z0-9\-_]{16,}['\"]", "severity": "Media"},
        
        # --- RANSOMWARE & DESTRUCCIÓN ---
        {"name": "Borrado de Copias de Seguridad (Shadow Copies)", "pattern": r"(vssadmin\.exe\s+delete\s+shadows|wmic\s+shadowcopy\s+delete)", "severity": "Crítica"},
        {"name": "Cifrado Masivo (Posible Ransomware)", "pattern": r"(AES\.new\(|Fernet\.generate_key\(|RSA\.import_key\()", "severity": "Alta"},
        {"name": "Modificación de Arranque (BCD)", "pattern": r"(bcdedit\s+/set\s+{default}\s+recoveryenabled\s+no)", "severity": "Crítica"},
        
        # --- TROYANOS & PERSISTENCIA ---
        {"name": "Persistencia en Registro (Run Keys)", "pattern": r"(RegSetValue|RegCreateKey|CurrentVersion\\Run|HKEY_LOCAL_MACHINE\\Software|Software\\Microsoft\\Windows\\CurrentVersion)", "severity": "Alta"},
        {"name": "Inyección de DLL / Hooking", "pattern": r"(SetWindowsHookEx|CreateRemoteThread|VirtualAllocEx|WriteProcessMemory)", "severity": "Crítica"},
        {"name": "Descarga de Payloads Externos", "pattern": r"(powershell.*IEX.*DownloadString|curl\s+-O\s+http|wget\s+http)", "severity": "Alta"},
        
        # --- RED & EXFILTRACIÓN ---
        {"name": "Conexión a Red Sospechosa", "pattern": r"(socket\.socket|requests\.get|urllib\.request|nc\s+-e)", "severity": "Media"},
        {"name": "Bypass de Seguridad (uac/amsi)", "pattern": r"(AmsiScanBuffer|FodHelper|CmpRegistryTransaction)", "severity": "Crítica"}
    ]

    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            # Leer línea a línea para ser eficiente con la memoria
            for line_num, line in enumerate(f, 1):
                for rule in RULES:
                    if re.search(rule["pattern"], line, re.IGNORECASE):
                        findings.append({
                            "rule": rule["name"],
                            "severity": rule["severity"],
                            "line": line_num,
                            "content": line.strip()[:50] + "..."
                        })
        return findings
    except Exception as e:
        logger.error(f"Error analizando vulnerabilidades en [cyan]{filepath}[/cyan]: {e}")
        return []

# Hash map para búsqueda de firmas optimizada
_SIGNATURE_CACHE = None

def identify_type(hex_signature, signatures_db=None):
    """
    Compara la firma hexadecimal con la base de datos de forma optimizada.
    Utiliza un sistema de caché indexada para evitar búsquedas lineales O(N).
    """
    global _SIGNATURE_CACHE
    
    if not hex_signature:
        return None

    # Cargar y pre-procesar firmas si no están en caché
    if _SIGNATURE_CACHE is None:
        if signatures_db is None:
            signatures_db = load_signatures()
        
        # Indexar por el primer byte para reducir drásticamente el espacio de búsqueda
        _SIGNATURE_CACHE = {}
        for entry in signatures_db:
            first_byte = entry['hex'].split(' ')[0]
            if first_byte not in _SIGNATURE_CACHE:
                _SIGNATURE_CACHE[first_byte] = []
            _SIGNATURE_CACHE[first_byte].append(entry)

    # Obtener el primer byte de la firma que estamos analizando
    first_byte_target = hex_signature.split(' ')[0]
    
    # Buscar solo en el subconjunto de firmas que empiezan por ese byte
    possible_matches = _SIGNATURE_CACHE.get(first_byte_target, [])
    for signature_entry in possible_matches:
        signature_hex = signature_entry['hex']
        if hex_signature.startswith(signature_hex):
            return signature_entry
            
    return None

try:
    import pefile
    PEFILE_AVAILABLE = True
except ImportError:
    PEFILE_AVAILABLE = False

def analyze_pe_headers(filepath):
    """
    Analiza cabeceras PE (Portable Executable) buscando anomalías estructurales
    típicas de malware ofuscado (packers, secciones anómalas).
    """
    if not PEFILE_AVAILABLE:
        return []
        
    findings = []
    try:
        # Cargar PE (solo funcionará en ejecutables y DLLs de Windows)
        pe = pefile.PE(filepath, fast_load=True)
        pe.parse_data_directories()
        
        # 1. Comprobar entropía por secciones (Típico de Packers como UPX)
        for section in pe.sections:
            section_name = section.Name.decode('utf-8', errors='ignore').strip('\x00')
            entropy = section.get_entropy()
            if entropy > 7.5:
                findings.append({
                    "rule": f"Sección Empaquetada ({section_name}) - Entropía: {entropy:.2f}",
                    "severity": "Alta",
                    "line": "Header",
                    "content": "Posible ofuscación o packer detectado en el binario."
                })
                
        # 2. Importaciones de riesgo (Malware clásico)
        if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
            suspicious_apis = ['VirtualAllocEx', 'CreateRemoteThread', 'WriteProcessMemory', 'SetWindowsHookEx']
            for entry in pe.DIRECTORY_ENTRY_IMPORT:
                dll_name = entry.dll.decode('utf-8', errors='ignore').lower()
                for imp in entry.imports:
                    if imp.name:
                        api_name = imp.name.decode('utf-8', errors='ignore')
                        if api_name in suspicious_apis:
                            findings.append({
                                "rule": f"Importación Sospechosa ({api_name})",
                                "severity": "Crítica",
                                "line": f"IAT ({dll_name})",
                                "content": "API frecuentemente usada para inyección/hooking."
                            })
                            
    except pefile.PEFormatError:
        pass # No es un ejecutable válido
    except Exception as e:
        logger.error(f"Error evaluando PE en [cyan]{filepath}[/cyan]: {e}")
        
    return findings

