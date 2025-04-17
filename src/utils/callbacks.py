from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)

class RenameCallbacks:
    """
    Clase para manejar callbacks durante operaciones de renombrado de archivos.
    Proporciona notificaciones sobre el progreso y errores.
    """
    
    def __init__(self, logger=None):
        """
        Inicializa el objeto de callbacks.
        
        Args:
            logger: Logger personalizado (opcional)
        """
        self.logger = logger or logging.getLogger(__name__)
        self.renamed_files: List[Tuple[str, str]] = []
        self.errors: List[Tuple[str, str]] = []
        self.preview_changes: List[Tuple[str, str]] = []
        self.total_files = 0
        self.processed_files = 0
    
    def on_file_renamed(self, old_name: str, new_name: str):
        """
        Notifica cuando un archivo es renombrado exitosamente.
        
        Args:
            old_name: Nombre original del archivo
            new_name: Nuevo nombre del archivo
        """
        self.renamed_files.append((old_name, new_name))
        self.processed_files += 1
        self.logger.info(f"Archivo renombrado: {old_name} -> {new_name}")
    
    def on_file_error(self, file_name: str, error: str):
        """
        Notifica cuando ocurre un error al renombrar un archivo.
        
        Args:
            file_name: Nombre del archivo que causó el error
            error: Descripción del error
        """
        self.errors.append((file_name, error))
        self.processed_files += 1
        self.logger.error(f"Error al renombrar {file_name}: {error}")
    
    def on_preview_change(self, old_name: str, new_name: str):
        """
        Notifica un cambio potencial en modo vista previa.
        
        Args:
            old_name: Nombre original del archivo
            new_name: Nuevo nombre propuesto
        """
        self.preview_changes.append((old_name, new_name))
        self.logger.info(f"Vista previa: {old_name} -> {new_name}")
    
    def on_start_batch(self, total_files: int):
        """
        Notifica el inicio de un proceso por lotes.
        
        Args:
            total_files: Número total de archivos a procesar
        """
        self.total_files = total_files
        self.processed_files = 0
        self.renamed_files.clear()
        self.errors.clear()
        self.preview_changes.clear()
        self.logger.info(f"Iniciando proceso de renombrado para {total_files} archivos")
    
    def on_batch_complete(self):
        """
        Notifica la finalización de un proceso por lotes.
        """
        self.logger.info(f"Proceso completado: {len(self.renamed_files)} archivos renombrados, "
                        f"{len(self.errors)} errores")
    
    def get_progress(self) -> Tuple[int, int]:
        """
        Obtiene el progreso actual del proceso.
        
        Returns:
            Tupla (archivos_procesados, total_archivos)
        """
        return self.processed_files, self.total_files
    
    def get_summary(self) -> dict:
        """
        Obtiene un resumen de la operación.
        
        Returns:
            Diccionario con el resumen de la operación
        """
        return {
            'total_files': self.total_files,
            'processed_files': self.processed_files,
            'renamed_files': len(self.renamed_files),
            'errors': len(self.errors),
            'preview_changes': len(self.preview_changes),
            'success_rate': (len(self.renamed_files) / self.total_files * 100) if self.total_files > 0 else 0
        } 