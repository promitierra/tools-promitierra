import os
from pathlib import Path
import sys
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Agregar el directorio raíz del proyecto al path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from src.utils.file_operations import FileRenamer
from src.utils.callbacks import RenameCallbacks

def patron_renombrado_planeador(nombre_archivo: str) -> str:
    """
    Convierte el nombre del archivo al formato ID_ENTREGA_PLANEADOR
    """
    # Si ya tiene el formato correcto, lo dejamos igual
    if "_ENTREGA_PLANEADOR." in nombre_archivo:
        return nombre_archivo
        
    # Extraer el ID del nombre actual
    nombre_base = Path(nombre_archivo).stem
    extension = Path(nombre_archivo).suffix
    
    # Si el archivo ya tiene _PLANEADOR, extraemos el ID
    if "_PLANEADOR" in nombre_base:
        id_numero = nombre_base.split('_')[0]
        if id_numero.isdigit():
            return f"{id_numero}_ENTREGA_PLANEADOR{extension}"
    
    return nombre_archivo

def main():
    # Crear instancias necesarias
    renamer = FileRenamer()
    callbacks = RenameCallbacks()
    
    # Ruta del directorio
    directorio = r"C:\Users\mmluf\Fundación ProMITIERRA\TERRITORIAL EPSEA AMDELCA-Territorial Zona Sur - Documentos\2_OPERACION\CONSOLIDADO ENGREGA IPPTA´s & PLANEADORES\CONSOLIDADO FORMATO ENTREGA PLANEADOR - CURILLO - YENNY PAOLA MOLANO"
    
    # Verificar que el directorio existe
    if not os.path.exists(directorio):
        logger.error(f"El directorio {directorio} no existe")
        sys.exit(1)
    
    # Agregar el patrón de validación para planeadores
    renamer.add_validation_pattern('entrega_planeador', r'^\d+_ENTREGA_PLANEADOR(?:\.[^.]+)?$')
    
    # Mostrar vista previa de los cambios
    logger.info("Vista previa de los cambios:")
    cambios = renamer.preview_changes(directorio, patron_renombrado_planeador)
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
        patron_renombrado_planeador,
        recursive=False,
        keep_extension=True,
        callbacks=callbacks,
        validation_pattern='entrega_planeador'
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