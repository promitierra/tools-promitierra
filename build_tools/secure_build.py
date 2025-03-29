"""
Script para la construcción segura del ejecutable de Herramientas PromiTierra.
"""

import os
import sys
import shutil
import logging
import subprocess
import hashlib
import time
from pathlib import Path
from typing import Dict, List, Optional
from secure_build_config import (
    SECURITY_CONFIG,
    AV_EXCLUSIONS,
    METADATA,
    PACKAGING_CONFIG,
    EXCLUDE_FILES,
    VERIFICATION_CONFIG,
    OFFICIAL_URLS,
    DOCS_CONFIG,
    LOG_CONFIG
)

# Configurar logging
logging.basicConfig(
    level=getattr(logging, LOG_CONFIG['log_level']),
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_CONFIG['log_file']),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SecureBuildError(Exception):
    """Excepción personalizada para errores de construcción segura."""
    pass

def verificar_entorno() -> None:
    """Verifica que el entorno de construcción sea seguro."""
    logger.info("Verificando entorno de construcción...")
    
    # Verificar Python
    if sys.version_info < (3, 8):
        raise SecureBuildError("Se requiere Python 3.8 o superior")
    
    # Verificar entorno virtual
    if not (hasattr(sys, 'real_prefix') or sys.base_prefix != sys.prefix):
        raise SecureBuildError("Este script debe ejecutarse en un entorno virtual")
    
    # Verificar Windows SDK y certificado (opcional por ahora)
    tiene_firma_digital = False
    if shutil.which('signtool') and SECURITY_CONFIG['certificate_file']:
        tiene_firma_digital = True
    else:
        logger.warning("No se encontró signtool o certificado. El ejecutable se construirá sin firma digital.")
    
    return tiene_firma_digital

def limpiar_directorio(path: Path) -> None:
    """Limpia un directorio de forma segura."""
    if path.exists():
        logger.info(f"Limpiando directorio: {path}")
        try:
            shutil.rmtree(path)
        except Exception as e:
            raise SecureBuildError(f"Error al limpiar {path}: {e}")

def generar_hashes(archivo: Path) -> Dict[str, str]:
    """Genera hashes de verificación para un archivo."""
    hashes = {}
    for algoritmo in SECURITY_CONFIG['hash_algorithms']:
        hasher = hashlib.new(algoritmo)
        with open(archivo, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hasher.update(chunk)
        hashes[algoritmo] = hasher.hexdigest()
    return hashes

def firmar_ejecutable(ejecutable: Path) -> None:
    """Firma el ejecutable con el certificado digital."""
    logger.info("Firmando ejecutable...")
    try:
        subprocess.run([
            'signtool', 'sign',
            '/f', SECURITY_CONFIG['certificate_file'],
            '/tr', SECURITY_CONFIG['timestamp_server'],
            '/td', SECURITY_CONFIG['min_signing_hash'],
            '/fd', SECURITY_CONFIG['min_signing_hash'],
            '/d', METADATA['FileDescription'],
            '/du', OFFICIAL_URLS['website'],
            str(ejecutable)
        ], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        raise SecureBuildError(f"Error al firmar el ejecutable: {e.stdout}\n{e.stderr}")

def generar_verificacion(dist_dir: Path, hashes: Dict[str, str]) -> None:
    """Genera el archivo de verificación."""
    verify_file = dist_dir / 'verificacion.txt'
    with open(verify_file, 'w', encoding='utf-8') as f:
        f.write(f"{METADATA['ProductName']} - Información de Verificación\n")
        f.write("=" * 50 + "\n\n")
        f.write("Para verificar la autenticidad de este software:\n\n")
        f.write(f"1. Descargue el software ÚNICAMENTE de: {OFFICIAL_URLS['releases']}\n\n")
        f.write("2. Verifique los siguientes hashes:\n\n")
        for algoritmo, hash_value in hashes.items():
            f.write(f"{algoritmo.upper()}: {hash_value}\n")
        f.write("\n3. Verifique la firma digital (clic derecho > Propiedades > Firmas digitales)\n")
        f.write(f"\nCertificado emitido a: {SECURITY_CONFIG['certificate_name']}\n")

def copiar_documentacion(dist_dir: Path) -> None:
    """Copia la documentación al directorio de distribución."""
    if DOCS_CONFIG['include_docs']:
        logger.info("Copiando documentación...")
        for doc in DOCS_CONFIG['docs_files']:
            src = Path(doc)
            if src.exists():
                shutil.copy2(src, dist_dir / src.name)
            else:
                logger.warning(f"Archivo de documentación no encontrado: {doc}")

def verificar_estructura() -> None:
    """Verifica y crea la estructura de directorios necesaria."""
    logger.info("Verificando estructura de directorios...")
    
    directorios = [
        Path('src/assets'),
        Path('src/config'),
        Path('build_tools/assets'),
        Path('dist'),
        Path('build')
    ]
    
    for directorio in directorios:
        if not directorio.exists():
            logger.info(f"Creando directorio: {directorio}")
            directorio.mkdir(parents=True, exist_ok=True)
    
    # Verificar icono
    icono = Path('build_tools/assets/icon.ico')
    if not icono.exists():
        logger.warning(f"Falta el icono en {icono}")
        logger.info("Se usará un icono por defecto")
        # TODO: Generar o copiar un icono por defecto

def construir_ejecutable():
    """Construir el ejecutable usando PyInstaller."""
    try:
        # Verificar que el ícono existe
        icon_path = Path('build_tools/assets/icon.ico').absolute()
        if not icon_path.exists():
            logging.error(f"No se encontró el ícono en {icon_path}")
            return False
        
        logging.info(f"Usando ícono: {icon_path}")

        # Limpiar directorios anteriores
        for dir_name in ['build', 'dist']:
            if os.path.exists(dir_name):
                shutil.rmtree(dir_name)

        # Construir usando subprocess para mayor control
        cmd = [
            sys.executable,
            '-m', 'PyInstaller',
            '--name=Herramientas.ProMiTIERRA.v0.3.0',
            '--windowed',
            '--clean',
            '--noconfirm',
            f'--icon={icon_path}',
            '--add-binary', f'{icon_path};.',
            '--add-data=src;src',
            '--hidden-import=src.app.gui',
            '--hidden-import=src.app.components',
            '--hidden-import=src.core',
            '--hidden-import=src.utils',
            '--collect-all=src',
            '--paths=.',
            '--log-level=DEBUG',
            'src/main.py'
        ]
        
        logging.info("Ejecutando PyInstaller con los siguientes argumentos:")
        logging.info(" ".join(str(arg) for arg in cmd))
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            logging.error(f"Error en PyInstaller: {result.stderr}")
            return False
        else:
            logging.info(result.stdout)
            
        # Verificar que el ícono se copió correctamente
        exe_path = Path('dist/Herramientas.ProMiTIERRA.v0.3.0/Herramientas.ProMiTIERRA.v0.3.0.exe')
        if not exe_path.exists():
            logging.error("No se encontró el ejecutable generado")
            return False
            
        return True
    except Exception as e:
        logging.error(f"Error durante la construcción: {str(e)}")
        return False

def main():
    """Función principal."""
    # Verificar entorno
    logging.info("Verificando entorno de construcción...")
    
    # Construir ejecutable
    logging.info("Iniciando construcción del ejecutable...")
    if construir_ejecutable():
        logging.info("Construcción completada exitosamente")
    else:
        logging.error("Error durante la construcción")
        sys.exit(1)

if __name__ == "__main__":
    main() 