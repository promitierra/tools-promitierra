import os
from pathlib import Path
import sys
import logging
from PIL import Image
import piexif
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from skimage.metrics import structural_similarity as ssim
import cv2
import shutil

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Agregar el directorio raíz del proyecto al path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

def calcular_similitud(img1_path: Path, img2_path: Path) -> float:
    """
    Calcula la similitud estructural (SSIM) entre dos imágenes.
    Retorna un valor entre 0 y 1, donde 1 significa imágenes idénticas.
    """
    # Leer imágenes con OpenCV
    img1 = cv2.imread(str(img1_path))
    img2 = cv2.imread(str(img2_path))
    
    # Convertir a escala de grises
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    
    # Calcular SSIM
    score = ssim(gray1, gray2)
    return score

def probar_optimizacion(ruta_imagen: Path, calidad: int = 85) -> tuple[bool, float, float]:
    """
    Prueba la optimización en una imagen y retorna métricas de calidad.
    
    Returns:
        tuple: (éxito, porcentaje_reducción, similitud)
    """
    try:
        # Crear directorio temporal para la prueba
        temp_dir = ruta_imagen.parent / "temp_test"
        temp_dir.mkdir(exist_ok=True)
        
        # Copiar imagen original al directorio temporal
        img_test = temp_dir / ruta_imagen.name
        shutil.copy2(ruta_imagen, img_test)
        
        # Optimizar la imagen de prueba
        with Image.open(img_test) as img:
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # Guardar versión optimizada
            output_test = temp_dir / f"{img_test.stem}_opt.jpg"
            img.save(output_test, 'JPEG', quality=calidad, optimize=True)
        
        # Calcular métricas
        tamaño_original = img_test.stat().st_size
        tamaño_optimizado = output_test.stat().st_size
        porcentaje_reduccion = ((tamaño_original - tamaño_optimizado) / tamaño_original) * 100
        
        # Calcular similitud estructural
        similitud = calcular_similitud(img_test, output_test)
        
        # Limpiar archivos temporales
        shutil.rmtree(temp_dir)
        
        return True, porcentaje_reduccion, similitud
        
    except Exception as e:
        logger.error(f"Error en prueba de optimización para {ruta_imagen.name}: {str(e)}")
        return False, 0.0, 0.0

def optimizar_imagen(ruta_imagen: Path, calidad: int = 85) -> bool:
    """
    Optimiza una imagen manteniendo buena calidad pero reduciendo su tamaño.
    
    Args:
        ruta_imagen: Ruta de la imagen a optimizar
        calidad: Nivel de calidad JPEG (1-100)
    
    Returns:
        bool: True si la optimización fue exitosa, False en caso contrario
    """
    try:
        # Abrir la imagen
        with Image.open(ruta_imagen) as img:
            # Conservar la metadata EXIF si existe
            exif_data = None
            if "exif" in img.info:
                exif_data = img.info["exif"]
            
            # Convertir a RGB si es necesario
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # Preparar el nombre del archivo optimizado
            nombre_base = ruta_imagen.stem
            ruta_salida = ruta_imagen.parent / f"{nombre_base}_opt.jpg"
            
            # Guardar la imagen optimizada
            if exif_data:
                img.save(ruta_salida, 'JPEG', quality=calidad, optimize=True, exif=exif_data)
            else:
                img.save(ruta_salida, 'JPEG', quality=calidad, optimize=True)
            
            # Verificar si el archivo optimizado es más pequeño
            if ruta_salida.stat().st_size < ruta_imagen.stat().st_size:
                # Crear backup antes de reemplazar
                backup_path = ruta_imagen.parent / f"{nombre_base}_backup{ruta_imagen.suffix}"
                shutil.copy2(ruta_imagen, backup_path)
                
                # Reemplazar el archivo original con el optimizado
                ruta_salida.replace(ruta_imagen)
                logger.info(f"Imagen optimizada: {ruta_imagen.name}")
                return True
            else:
                # Si no hay mejora, eliminar el archivo optimizado
                ruta_salida.unlink()
                logger.info(f"No se logró optimizar más: {ruta_imagen.name}")
                return False
                
    except Exception as e:
        logger.error(f"Error al procesar {ruta_imagen.name}: {str(e)}")
        return False

def procesar_directorio(directorio: str, modo_prueba: bool = False):
    """
    Procesa todas las imágenes en un directorio.
    """
    ruta = Path(directorio)
    if not ruta.exists():
        logger.error(f"El directorio {directorio} no existe")
        return
    
    # Obtener todas las imágenes
    extensiones = ('.jpg', '.jpeg', '.png')
    imagenes = [f for f in ruta.glob('*') if f.suffix.lower() in extensiones]
    
    if not imagenes:
        logger.warning(f"No se encontraron imágenes en {directorio}")
        return
    
    if modo_prueba:
        # Seleccionar una muestra representativa (máximo 3 imágenes)
        muestra = imagenes[:3] if len(imagenes) > 3 else imagenes
        logger.info(f"\nRealizando pruebas de optimización en {len(muestra)} imágenes de muestra...")
        
        resultados_prueba = []
        for img in muestra:
            exito, reduccion, similitud = probar_optimizacion(img)
            if exito:
                resultados_prueba.append((reduccion, similitud))
                logger.info(f"\nResultados para {img.name}:")
                logger.info(f"Reducción de tamaño: {reduccion:.2f}%")
                logger.info(f"Similitud estructural: {similitud:.4f}")
        
        if resultados_prueba:
            reduccion_promedio = np.mean([r[0] for r in resultados_prueba])
            similitud_promedio = np.mean([r[1] for r in resultados_prueba])
            
            logger.info("\nResultados promedio de las pruebas:")
            logger.info(f"Reducción promedio: {reduccion_promedio:.2f}%")
            logger.info(f"Similitud promedio: {similitud_promedio:.4f}")
            
            if similitud_promedio < 0.95:
                logger.warning("¡ADVERTENCIA! La calidad de la optimización podría ser demasiado baja.")
                return False
            
            logger.info("\nLas pruebas indican que la optimización es segura.")
            return True
    else:
        logger.info(f"Procesando {len(imagenes)} imágenes en {directorio}")
        
        # Procesar imágenes en paralelo
        with ThreadPoolExecutor() as executor:
            resultados = list(executor.map(optimizar_imagen, imagenes))
        
        # Mostrar resumen
        optimizadas = sum(1 for r in resultados if r)
        logger.info(f"Resumen: {optimizadas} de {len(imagenes)} imágenes optimizadas")

def main():
    # Directorios a procesar
    directorios = [
        r"C:\Users\mmluf\Fundación ProMITIERRA\TERRITORIAL EPSEA AMDELCA-Territorial Zona Sur - Documentos\2_OPERACION\CONSOLIDADO ENGREGA IPPTA´s & PLANEADORES\CONSOLIDADO FORMATO ENTREGA IPPTA - CURILLO - YENNY PAOLA MOLANO",
        r"C:\Users\mmluf\Fundación ProMITIERRA\TERRITORIAL EPSEA AMDELCA-Territorial Zona Sur - Documentos\2_OPERACION\CONSOLIDADO ENGREGA IPPTA´s & PLANEADORES\CONSOLIDADO FORMATO ENTREGA PLANEADOR - CURILLO - YENNY PAOLA MOLANO"
    ]
    
    # Primero ejecutar pruebas
    logger.info("Iniciando pruebas de optimización...")
    for directorio in directorios:
        logger.info(f"\nProbando optimización en: {Path(directorio).name}")
        if not procesar_directorio(directorio, modo_prueba=True):
            logger.error("Las pruebas no pasaron los criterios de calidad. Abortando proceso.")
            return
    
    # Preguntar al usuario si desea continuar
    respuesta = input("\n¿Los resultados de las pruebas son satisfactorios? ¿Desea continuar con la optimización? (s/n): ")
    if respuesta.lower() != 's':
        logger.info("Proceso cancelado por el usuario.")
        return
    
    # Procesar todos los directorios
    logger.info("\nIniciando proceso de optimización...")
    for directorio in directorios:
        logger.info(f"\nProcesando directorio: {Path(directorio).name}")
        procesar_directorio(directorio)
        
    logger.info("\nProceso completado. Se han creado copias de respaldo con el sufijo '_backup' para todas las imágenes optimizadas.")

if __name__ == "__main__":
    main() 