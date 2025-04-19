"""
Utilidades comunes para todas las herramientas.

Este módulo contiene funciones de utilidad generales que son utilizadas
por diferentes componentes de la aplicación.
"""

from .file_operations import FileRenamer
from .helpers import (
    get_project_root,
    get_version,
    get_app_name,
    get_app_description,
    agregar_detalle,
    actualizar_progreso,
    validar_directorio
)

from .config_manager import ConfigManager

# Crear una instancia global de configuración
config = ConfigManager()

__all__ = [
    'FileRenamer',
    'get_project_root',
    'get_version',
    'get_app_name',
    'get_app_description',
    'agregar_detalle',
    'actualizar_progreso',
    'validar_directorio',
    'ConfigManager',
    'config'
]