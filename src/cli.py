import argparse
import os
from src.core import get_file_signature, identify_type

def scan_file(filepath):
    """
    Escanea un archivo individual e imprime el resultado.
    """
    signature = get_file_signature(filepath)
    file_type = identify_type(signature)
    print(f"Archivo: {filepath}")
    print(f"Firma: {signature}")
    print(f"Tipo Detectado: {file_type}")
    print("-" * 40)

def main():
    parser = argparse.ArgumentParser(description="Identifica tipos de archivos usando números mágicos.")
    parser.add_argument("path", help="Ruta al archivo o directorio a escanear")
    
    args = parser.parse_args()
    
    if os.path.isfile(args.path):
        scan_file(args.path)
    elif os.path.isdir(args.path):
        print(f"Escaneando directorio: {args.path}\n")
        for root, _, files in os.walk(args.path):
            for file in files:
                filepath = os.path.join(root, file)
                scan_file(filepath)
    else:
        print(f"Error: La ruta '{args.path}' no existe.")

if __name__ == "__main__":
    main()
