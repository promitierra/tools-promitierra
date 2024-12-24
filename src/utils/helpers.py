import os
from datetime import datetime
import time

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
