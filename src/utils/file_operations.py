import os
import re
import shutil
import logging
from pathlib import Path
from typing import Tuple, Optional, Callable, List, Dict, Pattern

logger = logging.getLogger(__name__)

class FileRenamer:
    """
    Clase principal para el manejo de renombrado de archivos.
    Incluye validación, vista previa y registro de operaciones.
    """
    
    # Patrones de validación predefinidos
    PATRONES_VALIDACION = {
        'alfanumerico': r'^[\w\-. ]+$',  # Letras, números, guiones, puntos y espacios
        'sin_espacios': r'^[\w\-.]+$',   # Sin espacios
        'solo_letras': r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\-. ]+$',  # Solo letras (incluyendo acentos)
        'fecha_prefijo': r'^\d{4}-\d{2}-\d{2}_.*$',  # Formato YYYY-MM-DD_resto
        'ippta': r'^\d+_IPPTA(?:\.[^.]+)?$',  # Formato ID_IPPTA con extensión opcional
        'entrega_ippta': r'^\d+_ENTREGA_IPPTA(?:\.[^.]+)?$',  # Formato ID_ENTREGA_IPPTA con extensión opcional
        'entrega_planeador': r'^\d+_ENTREGA_PLANEADOR(?:\.[^.]+)?$'  # Formato ID_ENTREGA_PLANEADOR con extensión opcional
    }
    
    def __init__(self, logger=None):
        """
        Inicializa el renombrador de archivos.
        
        Args:
            logger: Logger personalizado (opcional)
        """
        self.logger = logger or logging.getLogger(__name__)
        self.preview_mode = False
        self.changes_history = []
        self.last_operation_files = []
    
    def validate_filename(self, filename: str, pattern_key: str = 'alfanumerico') -> Tuple[bool, str]:
        """
        Valida que el nombre del archivo cumpla con el patrón especificado.
        
        Args:
            filename: Nombre del archivo a validar
            pattern_key: Clave del patrón de validación a utilizar
            
        Returns:
            Tupla (es_valido, mensaje)
        """
        if pattern_key not in self.PATRONES_VALIDACION:
            return False, f"Patrón de validación '{pattern_key}' no encontrado"
            
        patron = self.PATRONES_VALIDACION[pattern_key]
        if not re.match(patron, filename):
            return False, f"El nombre '{filename}' no cumple con el patrón {pattern_key}"
            
        return True, "Nombre válido"
    
    def add_validation_pattern(self, name: str, pattern: str) -> bool:
        """
        Agrega un nuevo patrón de validación personalizado.
        
        Args:
            name: Nombre del patrón
            pattern: Expresión regular del patrón
            
        Returns:
            True si se agregó correctamente, False si ya existía
        """
        if name in self.PATRONES_VALIDACION:
            return False
            
        try:
            re.compile(pattern)  # Validar que el patrón sea válido
            self.PATRONES_VALIDACION[name] = pattern
            return True
        except re.error:
            self.logger.error(f"Patrón de validación inválido: {pattern}")
            return False
    
    def preview_changes(self, folder_path: str, pattern_func: Callable,
                       recursive: bool = True) -> List[Tuple[str, str]]:
        """
        Muestra una vista previa de los cambios sin aplicarlos.
        
        Args:
            folder_path: Ruta de la carpeta a procesar
            pattern_func: Función que genera el nuevo nombre
            recursive: Si debe procesar subcarpetas
            
        Returns:
            Lista de tuplas (nombre_original, nuevo_nombre)
        """
        changes = []
        
        def process_folder(path: str):
            for entry in os.scandir(path):
                if entry.is_file():
                    new_name = pattern_func(entry.name)
                    if new_name != entry.name:
                        changes.append((entry.path, os.path.join(os.path.dirname(entry.path), new_name)))
                elif entry.is_dir() and recursive:
                    process_folder(entry.path)
        
        try:
            process_folder(folder_path)
            return changes
        except Exception as e:
            self.logger.error(f"Error al generar vista previa: {str(e)}")
            return []
    
    def rename_file(self, source_path: str, new_name: str, 
                   keep_extension: bool = True) -> Tuple[bool, str]:
        """
        Renombra un archivo individual.
        
        Args:
            source_path: Ruta completa del archivo
            new_name: Nuevo nombre para el archivo
            keep_extension: Si debe mantener la extensión original
            
        Returns:
            Tupla (éxito, mensaje)
        """
        try:
            if not os.path.exists(source_path):
                return False, f"El archivo no existe: {source_path}"
            
            if not os.path.isfile(source_path):
                return False, f"La ruta no corresponde a un archivo: {source_path}"
                
            source_dir = os.path.dirname(source_path)
            _, extension = os.path.splitext(source_path)
            
            if keep_extension and not new_name.endswith(extension):
                new_name = f"{new_name}{extension}"
            
            new_path = os.path.join(source_dir, new_name)
            
            if os.path.exists(new_path):
                return False, f"Ya existe un archivo con el nombre: {new_name}"
            
            # Validar el nuevo nombre
            is_valid, message = self.validate_filename(new_name)
            if not is_valid:
                return False, message
            
            shutil.move(source_path, new_path)
            self.last_operation_files.append((new_path, source_path))
            
            return True, f"Archivo renombrado correctamente: {new_path}"
        
        except Exception as e:
            self.logger.error(f"Error al renombrar archivo: {str(e)}")
            return False, f"Error al renombrar archivo: {str(e)}"
    
    def rename_files_batch(self, folder_path: str, pattern_func: Callable[[str], str],
                          recursive: bool = True, keep_extension: bool = True,
                          callbacks: Optional[object] = None, skip_existing: bool = True,
                          validation_pattern: str = 'alfanumerico',
                          dry_run: bool = False) -> Dict[str, List[Tuple[bool, str]]]:
        """
        Renombra archivos en lote aplicando un patrón específico.
        
        Args:
            folder_path: Ruta de la carpeta a procesar
            pattern_func: Función que genera el nuevo nombre
            recursive: Si debe procesar subcarpetas
            keep_extension: Si debe mantener la extensión original
            callbacks: Objeto con métodos de callback para notificaciones
            skip_existing: Si debe omitir archivos que ya tienen el nombre correcto
            validation_pattern: Patrón de validación a utilizar
            dry_run: Si es True, solo muestra los cambios sin aplicarlos
            
        Returns:
            Diccionario con los resultados por carpeta
        """
        results = {}
        self.last_operation_files = []
        
        def process_folder(path: str):
            folder_results = []
            results[path] = folder_results
            
            try:
                for entry in os.scandir(path):
                    if entry.is_file():
                        new_name = pattern_func(entry.name)
                        
                        # Verificar si el archivo ya tiene el nombre correcto
                        if new_name == entry.name and skip_existing:
                            continue
                        
                        # Validar el nuevo nombre
                        is_valid, message = self.validate_filename(new_name, validation_pattern)
                        if not is_valid:
                            if callbacks and hasattr(callbacks, 'on_file_error'):
                                callbacks.on_file_error(entry.name, message)
                            folder_results.append((False, message))
                            continue
                        
                        if dry_run:
                            if callbacks and hasattr(callbacks, 'on_preview_change'):
                                callbacks.on_preview_change(entry.name, new_name)
                            folder_results.append((True, f"Se renombraría: {entry.name} -> {new_name}"))
                            continue
                        
                        success, message = self.rename_file(entry.path, new_name, keep_extension)
                        
                        if success and callbacks and hasattr(callbacks, 'on_file_renamed'):
                            callbacks.on_file_renamed(entry.name, new_name)
                        elif not success and callbacks and hasattr(callbacks, 'on_file_error'):
                            callbacks.on_file_error(entry.name, message)
                        
                        folder_results.append((success, message))
                    
                    elif entry.is_dir() and recursive:
                        process_folder(entry.path)
            
            except Exception as e:
                error_msg = f"Error al procesar carpeta {path}: {str(e)}"
                self.logger.error(error_msg)
                folder_results.append((False, error_msg))
        
        try:
            if not os.path.exists(folder_path):
                return {folder_path: [(False, f"La carpeta no existe: {folder_path}")]}
            
            if not os.path.isdir(folder_path):
                return {folder_path: [(False, f"La ruta no corresponde a una carpeta: {folder_path}")]}
            
            process_folder(folder_path)
            return results
        
        except Exception as e:
            error_msg = f"Error en el proceso de renombrado por lotes: {str(e)}"
            self.logger.error(error_msg)
            return {folder_path: [(False, error_msg)]}
    
    def undo_last_operation(self) -> Tuple[bool, str]:
        """
        Deshace la última operación de renombrado.
        
        Returns:
            Tupla (éxito, mensaje)
        """
        if not self.last_operation_files:
            return False, "No hay operaciones para deshacer"
        
        success = True
        errors = []
        
        for new_path, original_path in reversed(self.last_operation_files):
            try:
                if os.path.exists(new_path):
                    shutil.move(new_path, original_path)
                else:
                    errors.append(f"No se encuentra el archivo: {new_path}")
            except Exception as e:
                errors.append(f"Error al deshacer {new_path}: {str(e)}")
                success = False
        
        self.last_operation_files = []
        
        if errors:
            return False, "Errores al deshacer cambios: " + "; ".join(errors)
        
        return True, "Operación deshecha correctamente"