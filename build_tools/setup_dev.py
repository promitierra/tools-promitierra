"""
Script para configurar el entorno de desarrollo rápidamente.
"""

import os
import sys
import venv
import subprocess
from pathlib import Path

def crear_entorno_virtual():
    """Crea un nuevo entorno virtual si no existe."""
    venv_dir = Path('venv')
    if not venv_dir.exists():
        print("Creando entorno virtual...")
        venv.create(venv_dir, with_pip=True)
        print("- Entorno virtual creado")
    else:
        print("El entorno virtual ya existe")

def instalar_dependencias():
    """Instala todas las dependencias necesarias."""
    print("Instalando dependencias...")
    
    # Determinar el ejecutable de pip
    if sys.platform == 'win32':
        pip = 'venv/Scripts/pip.exe'
    else:
        pip = 'venv/bin/pip'
    
    try:
        # Actualizar pip
        subprocess.run([pip, 'install', '--upgrade', 'pip'], check=True)
        
        # Instalar uv
        subprocess.run([pip, 'install', 'uv'], check=True)
        
        # Usar uv para instalar dependencias
        if sys.platform == 'win32':
            uv = 'venv/Scripts/uv.exe'
        else:
            uv = 'venv/bin/uv'
        
        subprocess.run([
            uv, 'pip', 'install', 
            '-r', 'requirements.txt',
            '--no-cache'
        ], check=True)
        
        print("- Dependencias instaladas correctamente")
    except subprocess.CalledProcessError as e:
        print(f"Error instalando dependencias: {e}")
        sys.exit(1)

def configurar_git_hooks():
    """Configura los hooks de git para pre-commit."""
    print("Configurando git hooks...")
    hooks_dir = Path('.git/hooks')
    if not hooks_dir.exists():
        print("- No se encontró directorio .git")
        return
    
    # Crear pre-commit hook
    pre_commit = hooks_dir / 'pre-commit'
    with open(pre_commit, 'w', encoding='utf-8') as f:
        f.write('''#!/bin/sh
# Ejecutar formateo de código
venv/bin/black . || exit 1
# Ejecutar verificación de tipos
venv/bin/mypy src/ || exit 1
# Ejecutar linter
venv/bin/flake8 src/ || exit 1
''')
    
    # Hacer ejecutable el hook en sistemas Unix
    if sys.platform != 'win32':
        os.chmod(pre_commit, 0o755)
    
    print("- Hooks de git configurados")

def main():
    """Función principal de configuración."""
    print("=== Configurando entorno de desarrollo ===")
    
    try:
        crear_entorno_virtual()
        instalar_dependencias()
        configurar_git_hooks()
        print("\n=== Configuración completada exitosamente ===")
        print("\nPara activar el entorno virtual:")
        if sys.platform == 'win32':
            print("    .\\venv\\Scripts\\activate")
        else:
            print("    source venv/bin/activate")
    except Exception as e:
        print(f"\nERROR: La configuración falló: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 