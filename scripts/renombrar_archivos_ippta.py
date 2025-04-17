import os
import sys
import re
import logging
from pathlib import Path

# Agregar el directorio raíz del proyecto al path para poder importar los módulos
sys.path.append(str(Path(__file__).parent.parent))

from src.utils.file_operations import FileRenamer
from src.utils.callbacks import RenameCallbacks

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def patron_renombrado(nombre_archivo: str) -> str:
    """
    Función que define el patrón de renombrado para archivos IPPTA.
    
    Args:
        nombre_archivo: Nombre del archivo a procesar
        
    Returns:
        Nuevo nombre para el archivo
    """
    # Ignorar archivos que no son relevantes
    if nombre_archivo.startswith('.'):
        return nombre_archivo
    
    # Extraer el número de identificación si existe
    match = re.search(r'(\d+)', nombre_archivo)
    if match:
        numero_id = match.group(1)
        
        # Verificar si ya tiene el sufijo _IPPTA
        if "_IPPTA" in nombre_archivo:
            # Si ya tiene el formato correcto, no lo cambiamos
            return nombre_archivo
        else:
            # Normalizar el nombre con el formato: ID_IPPTA
            return f"{numero_id}_IPPTA"
    else:
        # Si no tiene un número de ID, mantener el nombre original
        return nombre_archivo


def main():
    # Ruta a la carpeta que contiene los archivos a renombrar
    carpeta_ippta = input("Ingrese la ruta completa de la carpeta 'CONSOLIDADO FORMATO ENTREGA IPPTA - CURILLO - YENNY PAOLA MOLANO': ")
    
    if not os.path.exists(carpeta_ippta):
        logger.error(f"La carpeta {carpeta_ippta} no existe.")
        return
    
    if not os.path.isdir(carpeta_ippta):
        logger.error(f"La ruta {carpeta_ippta} no es una carpeta.")
        return
    
    # Crear instancia del renombrador y callbacks
    renamer = FileRenamer(logger)
    callbacks = RenameCallbacks(logger)
    
    # Agregar patrón de validación específico para archivos IPPTA
    renamer.add_validation_pattern('ippta', r'^\d+_IPPTA$')
    
    # Mostrar vista previa de los cambios
    logger.info("Generando vista previa de cambios...")
    changes = renamer.preview_changes(carpeta_ippta, patron_renombrado)
    
    if not changes:
        logger.info("No se encontraron archivos para renombrar.")
        return
    
    logger.info("Vista previa de cambios:")
    for old_path, new_path in changes:
        logger.info(f"  {os.path.basename(old_path)} -> {os.path.basename(new_path)}")
    
    # Solicitar confirmación
    confirmacion = input("\n¿Desea proceder con el renombrado? (s/n): ").lower()
    if confirmacion != 's':
        logger.info("Operación cancelada por el usuario.")
        return
    
    # Iniciar el proceso de renombrado
    total_files = len(changes)
    callbacks.on_start_batch(total_files)
    
    results = renamer.rename_files_batch(
        carpeta_ippta,
        patron_renombrado,
        recursive=True,
        keep_extension=True,
        callbacks=callbacks,
        validation_pattern='ippta'
    )
    
    # Mostrar resumen
    callbacks.on_batch_complete()
    summary = callbacks.get_summary()
    
    logger.info(f"\nResumen del proceso:")
    logger.info(f"- Total de archivos procesados: {summary['processed_files']}")
    logger.info(f"- Archivos renombrados exitosamente: {summary['renamed_files']}")
    logger.info(f"- Errores encontrados: {summary['errors']}")
    logger.info(f"- Tasa de éxito: {summary['success_rate']:.2f}%")
    
    if summary['errors'] > 0:
        logger.error("\nErrores encontrados:")
        for file_name, error in callbacks.errors:
            logger.error(f"  {file_name}: {error}")


if __name__ == "__main__":
    main()