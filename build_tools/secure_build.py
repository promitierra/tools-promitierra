#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para construir ejecutables seguros de la aplicación ProMiTIERRA.
Soporta compilación para Windows, Linux y macOS.
"""

import os
import sys
import shutil
import logging
import platform
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
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SecureBuildError(Exception):
    """Excepción personalizada para errores de construcción segura."""
    pass

def verificar_entorno():
    """Verificar que el entorno de construcción está correctamente configurado."""
    logger.info("Verificando entorno de construcción...")
    return True

def obtener_sistema_destino():
    """Preguntar al usuario para qué sistema operativo quiere construir el ejecutable."""
    sistemas = {
        '1': 'windows',
        # Comentamos las opciones para Linux y macOS
        # '2': 'linux',
        # '3': 'macos'
    }
    
    print("\n=== Generador de Ejecutables Multiplataforma ===")
    print("Seleccione el sistema operativo de destino:")
    print("1) Windows (EXE)")
    # Comentamos las opciones para Linux y macOS
    # print("2) Linux (AppImage)")
    # print("3) macOS (APP)")
    
    while True:
        opcion = input("\nElija una opción (1): ")
        if opcion in sistemas:
            return sistemas[opcion]
        print("Opción no válida. Intente de nuevo.")

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

def construir_ejecutable(sistema_destino):
    """Construir el ejecutable usando PyInstaller para el sistema operativo especificado."""
    try:
        # Verificar que el ícono existe
        icon_path = None
        if sistema_destino == 'windows':
            icon_path = Path('build_tools/assets/icon.ico').absolute()
        # Comentamos el código para Linux y macOS
        # elif sistema_destino == 'linux' or sistema_destino == 'macos':
        #     icon_path = Path('build_tools/assets/icon.png').absolute()
        #     # Si no existe el icono PNG, convertir el ICO a PNG
        #     if not icon_path.exists() and Path('build_tools/assets/icon.ico').exists():
        #         try:
        #             from PIL import Image
        #             ico_path = Path('build_tools/assets/icon.ico').absolute()
        #             img = Image.open(ico_path)
        #             img.save(icon_path)
        #             logger.info(f"Icono convertido: {icon_path}")
        #         except Exception as e:
        #             logger.warning(f"No se pudo convertir el icono: {str(e)}")
        #             # Usar una ruta relativa si no se pudo convertir
        #             icon_path = Path('build_tools/assets/icon.ico').absolute()
        
        if icon_path and not icon_path.exists():
            logger.warning(f"No se encontró el ícono en {icon_path}")
            icon_path = None
        elif icon_path:
            logger.info(f"Usando ícono: {icon_path}")

        # Limpiar solo directorios específicos para el sistema operativo seleccionado
        # Siempre limpiar 'build'
        if os.path.exists('build'):
            logger.info("Limpiando directorio 'build'")
            shutil.rmtree('build')
            
        # Para 'dist', solo eliminar los archivos del sistema operativo seleccionado
        if os.path.exists('dist'):
            if sistema_destino == 'windows':
                # Eliminar solo archivos .exe
                for archivo in Path('dist').glob('*.exe'):
                    logger.info(f"Eliminando ejecutable anterior de Windows: {archivo}")
                    os.remove(archivo)
            # Comentamos el código para Linux y macOS
            # elif sistema_destino == 'linux':
            #     # En Linux, el problema es que no podemos usar una simple expresión glob
            #     # ya que los ejecutables no tienen una extensión específica
            #     for archivo in Path('dist').iterdir():
            #         # Verificar si el archivo corresponde a un ejecutable de Linux
            #         # (no tiene extensión y es un archivo, no un directorio)
            #         if archivo.is_file() and not archivo.suffix and 'Herramientas' in archivo.name:
            #             logger.info(f"Eliminando ejecutable anterior de Linux: {archivo}")
            #             os.remove(archivo)
            # elif sistema_destino == 'macos':
            #     # Eliminar solo los paquetes .app de macOS
            #     for archivo in Path('dist').glob('*.app'):
            #         logger.info(f"Eliminando ejecutable anterior de macOS: {archivo}")
            #         shutil.rmtree(archivo)
        else:
            # Si no existe el directorio 'dist', crearlo
            os.makedirs('dist', exist_ok=True)
            logger.info("Creado directorio 'dist'")

        # Crear archivo README si no existe
        readme_file = Path('README.txt')
        if not readme_file.exists():
            with open(readme_file, 'w', encoding='utf-8') as f:
                f.write(f"{METADATA['ProductName']} v{METADATA['ProductVersion']}\n")
                f.write(f"{METADATA['FileDescription']}\n\n")
                f.write(f"© {METADATA['LegalCopyright']}\n")
                f.write(f"Sitio web oficial: {OFFICIAL_URLS['website']}\n")

        # Configuración base para todos los sistemas
        comando = [
            "pyinstaller",
            # Nombre específico para Windows (comentamos la parte condicional)
            f"--name=Herramientas.ProMiTIERRA.v0.3.0", # if sistema_destino == 'windows' else f"--name=Herramientas_ProMiTIERRA",
            "--onefile",
            "--clean",
            "--noconfirm",
            "--noupx",  # Evitar compresión UPX (reduce falsos positivos)
            # Usar formato Windows para las rutas (comentamos la parte condicional)
            "--add-data=src;src", # if sistema_destino == 'windows' else "--add-data=src:src",
            "--add-data=LICENSE;.", # if sistema_destino == 'windows' else "--add-data=LICENSE:.",
            "--add-data=README.txt;.", # if sistema_destino == 'windows' else "--add-data=README.txt:.",
            "--hidden-import=src.app.gui",
            "--hidden-import=src.app.components",
            "--hidden-import=src.core",
            "--hidden-import=src.utils",
            "--collect-all=src",
            "--paths=.",
            "src/main.py"
        ]
        
        # Agregar opciones específicas para Windows
        # (comentamos la parte condicional y el código para Linux y macOS)
        # if sistema_destino == 'windows':
        comando.insert(3, "--windowed")
        if icon_path:
            comando.insert(4, f"--icon={icon_path}")
            comando.append(f"--add-binary={icon_path};.")
        # elif sistema_destino == 'linux':
        #     # Forzar un nombre de archivo sin extensión para Linux
        #     if icon_path:
        #         comando.insert(3, f"--icon={icon_path}")
        # elif sistema_destino == 'macos':
        #     comando.insert(3, "--windowed")
        #     if icon_path:
        #         comando.insert(4, f"--icon={icon_path}")
        #     # Agregar opciones específicas para macOS
        #     comando.append("--osx-bundle-identifier=org.promitierra.herramientas")

        # Ejecutar PyInstaller
        logger.info("Ejecutando PyInstaller con los siguientes argumentos:")
        logger.info(" ".join(comando))
        
        resultado = subprocess.run(comando, capture_output=True, text=True)
            
        if resultado.returncode != 0:
            logger.error("Error al construir el ejecutable:")
            logger.error(resultado.stderr)
            return False
        
        logger.info(resultado.stdout)
        logger.info("\nConstrucción completada exitosamente")
        
        # Verificar que el ejecutable se creó correctamente
        ejecutable_path = None
        if sistema_destino == 'windows':
            ejecutable_path = Path('dist/Herramientas.ProMiTIERRA.v0.3.0.exe')
        # Comentamos el código para Linux y macOS
        # elif sistema_destino == 'linux':
        #     ejecutable_path = Path('dist/Herramientas_ProMiTIERRA')
        # elif sistema_destino == 'macos':
        #     ejecutable_path = Path('dist/Herramientas_ProMiTIERRA.app')
        
        if ejecutable_path and not ejecutable_path.exists():
            # Comentamos el código para sistemas Unix
            # En sistemas Unix comprobar con separadores de ruta adecuados
            # alt_path = None
            # if sistema_destino == 'linux':
            #     alt_path = Path('dist/Herramientas_ProMiTIERRA')
            # 
            # if alt_path and alt_path.exists():
            #     ejecutable_path = alt_path
            #     logger.info(f"Ejecutable encontrado en ruta alternativa: {ejecutable_path}")
            # else:
            # Listar archivos en el directorio dist para diagnóstico
            try:
                dist_files = list(Path('dist').glob('*'))
                if dist_files:
                    logger.info(f"Archivos encontrados en dist: {[str(f) for f in dist_files]}")
                    # Si hay un archivo ejecutable, usar ese
                    # for file in dist_files:
                    #     if sistema_destino == 'linux' and not file.is_dir():
                    #         ejecutable_path = file
                    #         logger.info(f"Usando ejecutable encontrado: {ejecutable_path}")
                    #         break
            except Exception as e:
                logger.error(f"Error al listar archivos en dist: {str(e)}")
            
            if not ejecutable_path or not ejecutable_path.exists():
                logger.error(f"No se encontró el ejecutable en la ruta esperada: {ejecutable_path}")
                return False
            
        logger.info(f"Ejecutable creado correctamente en: {ejecutable_path}")
        return True
        
    except Exception as e:
        logger.error(f"Error durante la construcción: {str(e)}", exc_info=True)
        return False

def main():
    """Función principal."""
    # Verificar entorno
    verificar_entorno()
    
    # Establecemos directamente Windows como sistema destino
    # Comentamos la línea que pregunta al usuario
    # sistema_destino = obtener_sistema_destino()
    sistema_destino = 'windows'
    
    # Mostrar qué sistema se va a construir
    logger.info(f"Iniciando construcción para {sistema_destino.upper()}...")
    
    # Construir ejecutable
    if construir_ejecutable(sistema_destino):
        logger.info(f"Construcción completada exitosamente para {sistema_destino.upper()}")
    else:
        logger.error(f"Error durante la construcción para {sistema_destino.upper()}")
        sys.exit(1)

if __name__ == "__main__":
    main() 