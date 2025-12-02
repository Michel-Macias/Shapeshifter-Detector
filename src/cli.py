import argparse
import os
import json
from src.core import get_file_signature, identify_type

def check_mismatch(filepath, detected_type_info):
    """
    Verifica si la extensión del archivo coincide con las extensiones esperadas para el tipo detectado.
    Devuelve True si hay una discrepancia (posible spoofing), False si todo está bien.
    """
    if not detected_type_info:
        return False
        
    _, ext = os.path.splitext(filepath)
    ext = ext.lower()
    
    expected_extensions = detected_type_info.get('extensions', [])
    
    # Si la extensión actual NO está en la lista de esperadas, es una discrepancia
    if ext not in expected_extensions:
        return True
    return False

def scan_file(filepath, report_list=None):
    """
    Escanea un archivo individual, imprime el resultado y lo añade al reporte si se solicita.
    """
    signature = get_file_signature(filepath)
    type_info = identify_type(signature)
    
    file_type = type_info['type'] if type_info else "Desconocido"
    is_mismatch = check_mismatch(filepath, type_info)
    
    # Salida por consola
    print(f"Archivo: {filepath}")
    print(f"Firma: {signature}")
    print(f"Tipo Detectado: {file_type}")
    
    if is_mismatch:
        print("\033[91m[!] ALERTA: La extensión del archivo no coincide con el tipo detectado (Posible Spoofing)\033[0m")
    
    print("-" * 40)
    
    # Añadir al reporte
    if report_list is not None:
        report_entry = {
            "path": filepath,
            "signature": signature,
            "detected_type": file_type,
            "extension_mismatch": is_mismatch
        }
        report_list.append(report_entry)

def main():
    parser = argparse.ArgumentParser(description="Identifica tipos de archivos usando números mágicos y detecta spoofing.")
    parser.add_argument("path", help="Ruta al archivo o directorio a escanear")
    parser.add_argument("--output", help="Ruta para guardar el reporte en formato JSON", default=None)
    
    args = parser.parse_args()
    
    report_data = [] if args.output else None
    
    if os.path.isfile(args.path):
        scan_file(args.path, report_data)
    elif os.path.isdir(args.path):
        print(f"Escaneando directorio: {args.path}\n")
        for root, _, files in os.walk(args.path):
            for file in files:
                filepath = os.path.join(root, file)
                scan_file(filepath, report_data)
    else:
        print(f"Error: La ruta '{args.path}' no existe.")

    # Guardar reporte si se solicitó
    if args.output and report_data is not None:
        try:
            with open(args.output, 'w') as f:
                json.dump(report_data, f, indent=4)
            print(f"Reporte guardado exitosamente en: {args.output}")
        except Exception as e:
            print(f"Error al guardar el reporte: {e}")

if __name__ == "__main__":
    main()
