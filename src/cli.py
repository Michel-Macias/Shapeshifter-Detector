import argparse
import os
from src.core import get_file_signature, identify_type

def scan_file(filepath):
    """
    Scans a single file and prints the result.
    """
    signature = get_file_signature(filepath)
    file_type = identify_type(signature)
    print(f"File: {filepath}")
    print(f"Signature: {signature}")
    print(f"Type: {file_type}")
    print("-" * 40)

def main():
    parser = argparse.ArgumentParser(description="Identify file types using magic numbers.")
    parser.add_argument("path", help="Path to file or directory to scan")
    
    args = parser.parse_args()
    
    if os.path.isfile(args.path):
        scan_file(args.path)
    elif os.path.isdir(args.path):
        print(f"Scanning directory: {args.path}\n")
        for root, _, files in os.walk(args.path):
            for file in files:
                filepath = os.path.join(root, file)
                scan_file(filepath)
    else:
        print(f"Error: Path '{args.path}' not found.")

if __name__ == "__main__":
    main()
