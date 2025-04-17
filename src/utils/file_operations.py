import os
import shutil
import logging
from pathlib import Path
from typing import Tuple, Optional, Callable

logger = logging.getLogger(__name__)

def rename_file(source_path: str, new_name: str, keep_extension: bool = True) -> Tuple[bool, str]:
    """
    Renombra un archivo manteniendo su ubicación original.
    
    Args:
        source_path: Ruta completa al archivo que se desea renombrar
        new_name: Nuevo nombre para el archivo (sin la ruta)
        keep_extension: Si es True, mantiene la extensión original del archivo
    
    Returns:
        Tupla (éxito, mensaje)
    """
    try:
        # Validar que el archivo existe
        if not os.path.exists(source_path):
            return False, f"El archivo no existe: {source_path}"
        
        # Validar que es un archivo y no un directorio
        if not os.path.isfile(source_path):
            return False, f"La ruta no corresponde a un archivo: {source_path}"
            
        # Obtener el directorio y la extensión
        source_dir = os.path.dirname(source_path)
        _, extension = os.path.splitext(source_path)
        
        # Construir el nuevo nombre completo
        if keep_extension:
            # Si el nuevo nombre ya incluye la extensión, no la añadimos
            if not new_name.endswith(extension):
                new_name = f"{new_name}{extension}"
        
        # Ruta completa del nuevo archivo
        new_path = os.path.join(source_dir, new_name)
        
        # Verificar si el archivo de destino ya existe
        if os.path.exists(new_path):
            return False, f"Ya existe un archivo con el nombre: {new_name}"
        
        # Renombrar el archivo
        shutil.move(source_path, new_path)
        
        return True, f"Archivo renombrado correctamente: {new_path}"
    
    except Exception as e:
        logger.error(f"Error al renombrar archivo: {str(e)}")
        return False, f"Error al renombrar archivo: {str(e)}"


def rename_file_with_callback(source_path: str, new_name: str, 
                             keep_extension: bool = True,
                             callbacks: Optional[object] = None) -> Tuple[bool, str]:
    """
    Renombra un archivo y notifica a través de callbacks.
    
    Args:
        source_path: Ruta completa al archivo que se desea renombrar
        new_name: Nuevo nombre para el archivo (sin la ruta)
        keep_extension: Si es True, mantiene la extensión original del archivo
        callbacks: Objeto con métodos de callback para notificaciones
    
    Returns:
        Tupla (éxito, mensaje)
    """
    try:
        success, message = rename_file(source_path, new_name, keep_extension)
        
        if success:
            if callbacks and hasattr(callbacks, 'on_file_renamed'):
                callbacks.on_file_renamed(os.path.basename(source_path), new_name)
        else:
            if callbacks and hasattr(callbacks, 'on_file_error'):
                callbacks.on_file_error(os.path.basename(source_path), message)
                
        return success, message
    
    except Exception as e:
        error_msg = f"Error en el proceso de renombrado: {str(e)}"
        logger.error(error_msg)
        
        if callbacks and hasattr(callbacks, 'on_file_error'):
            callbacks.on_file_error(os.path.basename(source_path), error_msg)
            
        return False, error_msg