"""
Script para construir el ejecutable de Herramientas PromiTierra.
"""

import os
import sys
import shutil
import subprocess
import hashlib
from pathlib import Path
from pyinstaller_config import (
    EXECUTABLE_CONFIG,
    INCLUDE_FILES,
    DATAS,
    HIDDEN_IMPORTS,
    EXCLUDES,
    ROOT_DIR
)

def limpiar_directorios():
    """Limpia los directorios de construcción anteriores."""
    print("Limpiando directorios de construcción...")
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        dir_path = ROOT_DIR / dir_name
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"- Eliminado {dir_name}/")

def verificar_dependencias():
    """Verifica que todas las dependencias estén instaladas."""
    print("Verificando dependencias...")
    requirements_file = ROOT_DIR / 'requirements.txt'
    try:
        subprocess.run(
            [sys.executable, '-m', 'pip', 'install', '-r', str(requirements_file)],
            check=True
        )
        print("- Todas las dependencias están instaladas")
    except subprocess.CalledProcessError as e:
        print(f"Error instalando dependencias: {e}")
        sys.exit(1)

def generar_hashes(archivo):
    """Genera hashes SHA-256 y MD5 para verificación."""
    sha256_hash = hashlib.sha256()
    md5_hash = hashlib.md5()
    
    with open(archivo, 'rb') as f:
        for byte_block in iter(lambda: f.read(4096), b''):
            sha256_hash.update(byte_block)
            md5_hash.update(byte_block)
    
    return {
        'sha256': sha256_hash.hexdigest(),
        'md5': md5_hash.hexdigest()
    }

def firmar_ejecutable(ejecutable_path):
    """Firma el ejecutable con un certificado digital."""
    try:
        # Verificar si signtool está disponible
        signtool_path = shutil.which('signtool')
        if not signtool_path:
            print("ADVERTENCIA: signtool no encontrado. El ejecutable no será firmado.")
            print("Se recomienda instalar Windows SDK y obtener un certificado de firma de código.")
            return False
        
        # Verificar certificado
        cert_path = os.environ.get('CODE_SIGNING_CERT')
        if not cert_path:
            print("ADVERTENCIA: No se encontró certificado de firma. Configure CODE_SIGNING_CERT.")
            return False
        
        # Firmar el ejecutable
        subprocess.run([
            signtool_path, 'sign',
            '/f', cert_path,
            '/tr', 'http://timestamp.digicert.com',
            '/td', 'sha256',
            '/fd', 'sha256',
            '/d', "Herramientas PromiTierra",
            '/du', "https://promitierra.com",
            ejecutable_path
        ], check=True)
        
        print("- Ejecutable firmado exitosamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error al firmar el ejecutable: {e}")
        return False

def generar_verificacion(dist_dir, hashes):
    """Genera archivos de verificación."""
    # Crear archivo de verificación
    verify_file = dist_dir / 'verificacion.txt'
    with open(verify_file, 'w', encoding='utf-8') as f:
        f.write("Herramientas PromiTierra - Información de Verificación\n")
        f.write("================================================\n\n")
        f.write("Para verificar la autenticidad de este software:\n")
        f.write("1. Verifique que descargó el archivo desde https://promitierra.com\n")
        f.write("2. Compare los siguientes hashes con el archivo descargado:\n\n")
        f.write(f"SHA-256: {hashes['sha256']}\n")
        f.write(f"MD5: {hashes['md5']}\n\n")
        f.write("3. En Windows, haga clic derecho en el ejecutable y verifique la firma digital\n")
    
    print("- Archivo de verificación generado")

def construir_ejecutable():
    """Construye el ejecutable usando PyInstaller."""
    print("Construyendo ejecutable...")
    
    # Preparar argumentos para PyInstaller
    pyinstaller_args = [
        'pyinstaller',
        '--noconfirm',
        '--clean',
        str(ROOT_DIR / 'main.py'),
    ]
    
    # Agregar configuración del ejecutable
    for key, value in EXECUTABLE_CONFIG.items():
        if isinstance(value, bool):
            if value:
                pyinstaller_args.append(f'--{key}')
        else:
            pyinstaller_args.extend([f'--{key}', str(value)])
    
    # Agregar archivos a incluir
    for src, dst in INCLUDE_FILES:
        pyinstaller_args.extend(['--add-data', f'{src}{os.pathsep}{dst}'])
    
    # Agregar datos adicionales
    for src, dst in DATAS:
        pyinstaller_args.extend(['--add-data', f'{src}{os.pathsep}{dst}'])
    
    # Agregar imports ocultos
    for imp in HIDDEN_IMPORTS:
        pyinstaller_args.extend(['--hidden-import', imp])
    
    # Agregar exclusiones
    for excl in EXCLUDES:
        pyinstaller_args.extend(['--exclude-module', excl])
    
    try:
        subprocess.run(pyinstaller_args, check=True)
        print("- Ejecutable construido exitosamente")
        
        # Obtener ruta del ejecutable generado
        dist_dir = ROOT_DIR / 'dist'
        exe_name = f"{EXECUTABLE_CONFIG['name']}.exe"
        exe_path = dist_dir / exe_name
        
        # Generar hashes
        hashes = generar_hashes(exe_path)
        
        # Firmar el ejecutable
        firmado = firmar_ejecutable(str(exe_path))
        
        # Generar archivo de verificación
        generar_verificacion(dist_dir, hashes)
        
        if not firmado:
            print("\nADVERTENCIA: El ejecutable no está firmado digitalmente.")
            print("Se recomienda obtener un certificado de firma de código para mayor seguridad.")
            print("Consulte la documentación para más información.")
        
    except subprocess.CalledProcessError as e:
        print(f"Error construyendo ejecutable: {e}")
        sys.exit(1)

def post_build():
    """Realiza tareas posteriores a la construcción."""
    print("Realizando tareas post-build...")
    
    # Copiar archivos adicionales
    dist_dir = ROOT_DIR / 'dist'
    if dist_dir.exists():
        # Copiar documentación
        for doc in ['README.md', 'TUTORIAL.md']:
            shutil.copy2(ROOT_DIR / doc, dist_dir / doc)
        print("- Documentación copiada")
        
        # Crear archivo version.txt
        with open(dist_dir / 'version.txt', 'w', encoding='utf-8') as f:
            f.write('1.0.0\n')
        print("- Archivo de versión creado")

def main():
    """Función principal de construcción."""
    print("=== Iniciando proceso de construcción ===")
    
    # Verificar que estamos en el entorno virtual
    if not hasattr(sys, 'real_prefix') and not sys.base_prefix != sys.prefix:
        print("ERROR: Este script debe ejecutarse dentro del entorno virtual")
        sys.exit(1)
    
    try:
        limpiar_directorios()
        verificar_dependencias()
        construir_ejecutable()
        post_build()
        print("\n=== Construcción completada exitosamente ===")
    except Exception as e:
        print(f"\nERROR: La construcción falló: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 