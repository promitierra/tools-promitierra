import os
from datetime import datetime
import time
from pathlib import Path
from typing import Optional

def agregar_detalle(text_widget, mensaje, tipo="info"):
    """Agregar mensaje al widget de detalles"""
    prefijos = {
        "info": "ℹ️",
        "error": "❌",
        "success": "✅",
        "warning": "⚠️"
    }
    prefijo = prefijos.get(tipo, "")
    timestamp = datetime.now().strftime("%H:%M:%S")
    text_widget.insert("end", f"[{timestamp}] {prefijo} {mensaje}\n")
    text_widget.see("end")

def actualizar_progreso(progressbar, valor):
    """Actualizar barra de progreso"""
    if hasattr(progressbar, 'set'):
        progressbar.set(valor)
    else:
        progressbar['value'] = valor * 100

def generar_nombre_zip():
    """Generar nombre para archivo ZIP"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    counter = getattr(generar_nombre_zip, '_counter', 0)
    generar_nombre_zip._counter = counter + 1
    return f"PDFs_{timestamp}_{counter}.zip"

def validar_directorio(directorio):
    """Validar que el directorio existe y tiene permisos"""
    if not os.path.exists(directorio):
        return False, "El directorio no existe"
    if not os.path.isdir(directorio):
        return False, "La ruta no es un directorio"
    if not os.access(directorio, os.R_OK | os.W_OK):
        return False, "No hay permisos suficientes en el directorio"
    return True, ""

def get_project_root() -> Path:
    """
    Obtiene la ruta raíz del proyecto.
    
    Returns:
        Path: Ruta absoluta al directorio raíz del proyecto
    """
    return Path(__file__).parent.parent.parent

def get_version() -> str:
    """
    Obtiene la versión actual del proyecto.
    
    Returns:
        str: Versión del proyecto (ej: '0.3.0')
    """
    return "0.3.0"

def get_app_name() -> str:
    """
    Obtiene el nombre de la aplicación.
    
    Returns:
        str: Nombre de la aplicación
    """
    return "Herramientas ProMiTIERRA"

def get_app_description() -> str:
    """
    Obtiene la descripción de la aplicación.
    
    Returns:
        str: Descripción de la aplicación
    """
    return "Herramientas para procesamiento de archivos y documentos"
