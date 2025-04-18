import os
from pathlib import Path
import sys
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Agregar el directorio raíz del proyecto al path
sys.path.append(str(Path(__file__).parent.parent))

from src.utils.file_operations import FileRenamer
from src.utils.callbacks import RenameCallbacks

def patron_renombrado_entrega(nombre_archivo: str) -> str:
    """
    Convierte el nombre del archivo al formato ID_ENTREGA_IPPTA
    """
    # Si ya tiene el formato correcto, lo dejamos igual
    if "_ENTREGA_IPPTA." in nombre_archivo:
        return nombre_archivo
        
    # Extraer el ID del nombre actual
    partes = nombre_archivo.split('_')
    if not partes[0].isdigit():
        return nombre_archivo
        
    # Obtener la extensión original
    extension = Path(nombre_archivo).suffix
    
    # Crear el nuevo nombre
    return f"{partes[0]}_ENTREGA_IPPTA{extension}"

def main():
    # Crear instancias necesarias
    renamer = FileRenamer()
    callbacks = RenameCallbacks()
    
    # Obtener la ruta del directorio desde los argumentos
    if len(sys.argv) < 2:
        logger.error("Debe especificar la ruta del directorio")
        sys.exit(1)
        
    directorio = sys.argv[1]
    
    # Verificar que el directorio existe
    if not os.path.exists(directorio):
        logger.error(f"El directorio {directorio} no existe")
        sys.exit(1)
    
    # Mostrar vista previa de los cambios
    logger.info("Vista previa de los cambios:")
    cambios = renamer.preview_changes(directorio, patron_renombrado_entrega)
    for original, nuevo in cambios:
        logger.info(f"{os.path.basename(original)} -> {os.path.basename(nuevo)}")
    
    # Confirmar con el usuario
    respuesta = input("\n¿Desea proceder con los cambios? (s/n): ")
    if respuesta.lower() != 's':
        logger.info("Operación cancelada")
        return
    
    # Realizar el renombrado
    callbacks.on_start_batch(len(cambios))
    resultados = renamer.rename_files_batch(
        directorio,
        patron_renombrado_entrega,
        recursive=False,
        keep_extension=True,
        callbacks=callbacks,
        validation_pattern='entrega_ippta'
    )
    
    # Mostrar resumen
    callbacks.on_batch_complete()
    summary = callbacks.get_summary()
    logger.info(f"\nResumen: {summary}")
    
    # Verificar si hubo errores
    if callbacks.errors:
        logger.warning("\nErrores encontrados:")
        for archivo, error in callbacks.errors:
            logger.warning(f"{archivo}: {error}")

if __name__ == "__main__":
    main() 