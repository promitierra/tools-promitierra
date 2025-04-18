"""
Configuración para la construcción del ejecutable con PyInstaller.
"""

import sys
from pathlib import Path

# Obtener el directorio raíz del proyecto
ROOT_DIR = Path(__file__).parent.parent.absolute()

# Configuración del ejecutable
EXECUTABLE_CONFIG = {
    'name': 'Herramientas PromiTierra',
    'icon': str(ROOT_DIR / 'build_tools' / 'assets' / 'icon.ico'),
    'console': False,  # False para aplicación GUI
    'onefile': True,  # True para generar un solo archivo ejecutable
    'windowed': True,  # True para aplicaciones con GUI
    'clean': True,
    'strip': False,  # False para mantener información de depuración
    'noupx': True,  # True para evitar compresión UPX
    'uac_admin': True,  # True para solicitar privilegios de administrador
}

# Archivos y directorios a incluir
INCLUDE_FILES = [
    (str(ROOT_DIR / 'src'), 'src'),
    (str(ROOT_DIR / 'README.md'), '.'),
    (str(ROOT_DIR / 'TUTORIAL.md'), '.'),
]

# Datos adicionales a incluir
DATAS = [
    (str(ROOT_DIR / 'build_tools' / 'assets'), 'assets'),
]

# Imports ocultos que PyInstaller podría no detectar
HIDDEN_IMPORTS = [
    'customtkinter',
    'PIL',
    'fitz',
    'pandas',
    'openpyxl',
]

# Excluir módulos innecesarios para reducir tamaño
EXCLUDES = [
    'matplotlib',
    'scipy',
    'numpy',
    'tkinter.test',
    'unittest',
    'pdb',
    'doctest',
    'pydoc',
]

# Configuración específica para Windows
if sys.platform.startswith('win'):
    EXECUTABLE_CONFIG.update({
        'version_file': str(ROOT_DIR / 'build_tools' / 'version_info.txt'),
        'manifest': str(ROOT_DIR / 'build_tools' / 'manifest.xml'),
    }) 