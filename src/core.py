import binascii
from src.signatures import SIGNATURES

def get_file_signature(filepath, num_bytes=16):
    """
    Reads the first N bytes of a file and returns them as a hex string.
    """
    try:
        with open(filepath, 'rb') as f:
            chunk = f.read(num_bytes)
            # Convert bytes to hex string (e.g., b'\x89PNG' -> '89 50 4E 47')
            hex_str = binascii.hexlify(chunk).decode('utf-8').upper()
            # Format with spaces for readability and matching
            formatted_hex = ' '.join(hex_str[i:i+2] for i in range(0, len(hex_str), 2))
            return formatted_hex
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return None

def identify_type(hex_signature):
    """
    Matches the hex signature against the database.
    Returns the file type or 'Unknown'.
    """
    if not hex_signature:
        return "Error: Could not read file signature"

    # Iterate through signatures to find a match
    # We check if the file's signature STARTS with the known signature
    for signature, file_type in SIGNATURES.items():
        if hex_signature.startswith(signature):
            return file_type
            
    return "Unknown File Type"
