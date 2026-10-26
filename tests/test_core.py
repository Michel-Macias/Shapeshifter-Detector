import os
from src.core import calculate_entropy, identify_type, get_file_signature
from src.cli import check_mismatch

def test_entropy_computation(tmp_path):
    # Generar un archivo altamente predecible
    low_file = tmp_path / "low.bin"
    low_file.write_bytes(b"\x00" * 1000)
    assert calculate_entropy(str(low_file)) == 0.0
    
    # Generar un archivo pseudoaleatorio
    high_file = tmp_path / "high.bin"
    high_file.write_bytes(os.urandom(1000))
    assert calculate_entropy(str(high_file)) > 7.0

def test_identify_type(tmp_path):
    # Generar firma fake de un PE
    fake_exe = tmp_path / "fake.exe"
    fake_exe.write_bytes(b"MZ\x90\x00\x03\x00")
    hex_sig = get_file_signature(str(fake_exe))
    type_info = identify_type(hex_sig)
    is_mismatch = check_mismatch(str(fake_exe), type_info)
    assert type_info["type"] == "Ejecutable de Windows (EXE/DLL)"
    assert is_mismatch is False
