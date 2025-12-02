# Database of file signatures (Magic Numbers)
# Format: 'HEX_SIGNATURE': 'FILE_TYPE'
# Signatures are stored as space-separated hex strings for readability.

SIGNATURES = {
    # Images
    '89 50 4E 47 0D 0A 1A 0A': 'PNG Image',
    'FF D8 FF': 'JPEG Image',
    '47 49 46 38 37 61': 'GIF Image (87a)',
    '47 49 46 38 39 61': 'GIF Image (89a)',
    '42 4D': 'BMP Image',
    
    # Documents
    '25 50 44 46': 'PDF Document',
    'D0 CF 11 E0 A1 B1 1A E1': 'Microsoft Office Document (Legacy)',
    '50 4B 03 04': 'ZIP Archive / Office Open XML',
    
    # Executables
    '4D 5A': 'Windows Executable (EXE/DLL)',
    '7F 45 4C 46': 'ELF Executable (Linux)',
    
    # Archives
    '1F 8B': 'GZIP Archive',
    '52 61 72 21 1A 07 00': 'RAR Archive',
    '37 7A BC AF 27 1C': '7z Archive',
    
    # Audio/Video
    '49 44 33': 'MP3 Audio (ID3v2)',
    'FF FB': 'MP3 Audio (MPEG-1 Layer 3)',
    '00 00 00 18 66 74 79 70 6D 70 34 32': 'MP4 Video',
    '1A 45 DF A3': 'Matroska Video (MKV/WebM)'
}
