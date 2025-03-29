"""
Configuración específica para la construcción segura del ejecutable.
"""

import os
from pathlib import Path

# Configuración de seguridad
SECURITY_CONFIG = {
    'certificate_name': 'PromiTierra Code Signing',
    'certificate_file': os.environ.get('CODE_SIGNING_CERT', ''),
    'timestamp_server': 'http://timestamp.digicert.com',
    'hash_algorithms': ['sha256', 'md5'],
    'min_signing_hash': 'sha256',
}

# Configuración de antivirus
AV_EXCLUSIONS = [
    'pyinstaller',
    'customtkinter',
    'PIL',
    'pandas',
    'numpy',
]

# Configuración de metadatos del ejecutable
METADATA = {
    'CompanyName': 'PromiTierra',
    'FileDescription': 'Herramientas PDF PromiTierra',
    'FileVersion': '0.3.0',
    'InternalName': 'herramientas_promitierra',
    'LegalCopyright': '© 2024 PromiTierra. Todos los derechos reservados.',
    'OriginalFilename': 'Herramientas.ProMiTIERRA.v0.3.0.exe',
    'ProductName': 'Herramientas PDF PromiTierra',
    'ProductVersion': '0.3.0',
}

# Configuración de empaquetado
PACKAGING_CONFIG = {
    'optimize': 2,  # Nivel máximo de optimización
    'strip': True,  # Eliminar símbolos de depuración
    'upx': False,  # No usar UPX para evitar falsos positivos de antivirus
    'clean': True,  # Limpiar archivos temporales
}

# Archivos a excluir del empaquetado
EXCLUDE_FILES = [
    '*.pyc',
    '*.pyo',
    '*.pyd',
    '__pycache__',
    '*.so',
    '*.dylib',
    'test*',
    'tests*',
]

# Configuración de verificación
VERIFICATION_CONFIG = {
    'generate_hashes': True,
    'verify_signature': True,
    'check_imports': True,
}

# URLs oficiales
OFFICIAL_URLS = {
    'website': 'https://promitierra.com',
    'repository': 'https://github.com/promitierra/tools-promitierra',
    'releases': 'https://github.com/promitierra/tools-promitierra/releases',
    'issues': 'https://github.com/promitierra/tools-promitierra/issues',
}

# Configuración de documentación
DOCS_CONFIG = {
    'include_docs': True,
    'docs_files': [
        'README.md',
        'TUTORIAL.md',
        'docs/SEGURIDAD.md',
        'CHANGELOG.md',
    ],
}

# Configuración de logging
LOG_CONFIG = {
    'log_level': 'INFO',
    'log_file': 'build.log',
    'include_timestamp': True,
} 