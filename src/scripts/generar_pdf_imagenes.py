"""
Script para generar PDFs a partir de imágenes con características específicas.

Este script toma un directorio de imágenes y genera un PDF con todas ellas,
asegurando que estén en orientación horizontal, con márgenes exactos de 1 cm
en todos los lados, centradas correctamente y con numeración de página opcional.

Creado para Fundación ProMITIERRA - Herramientas de procesamiento documental.

Uso:
    python generar_pdf_imagenes.py [directorio] [--output RUTA] [--debug] [--no-page-numbers]

Argumentos:
    directorio:          Ruta al directorio con las imágenes a procesar
    --output, -o:        Ruta de salida del PDF (opcional)
    --debug, -d:         Muestra información adicional durante la ejecución
    --no-page-numbers:   No incluir números de página en el documento

Ejemplos:
    python generar_pdf_imagenes.py "C:/Directorio/Imagenes"
    python generar_pdf_imagenes.py "C:/Directorio/Imagenes" --no-page-numbers
    python generar_pdf_imagenes.py "C:/Directorio/Imagenes" -o "C:/Salida/resultado.pdf"
"""

import os
from pathlib import Path
import sys
import logging
from typing import Optional, Callable, Tuple
from PIL import Image
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import argparse

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Agregar el directorio raíz del proyecto al path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

# Configuraciones predefinidas de calidad
CONFIGURACIONES_CALIDAD = {
    "baja": {"dpi": 150, "calidad": 60, "formato_temp": "JPEG"},
    "media": {"dpi": 300, "calidad": 85, "formato_temp": "JPEG"},
    "maxima": {"dpi": 600, "calidad": 100, "formato_temp": "PNG"}
}

def estimar_tamano_pdf(directorio_imagenes: str, nivel_calidad: str) -> Tuple[float, str]:
    """
    Estima el tamaño aproximado del PDF resultante basado en las imágenes y nivel de calidad.
    
    Args:
        directorio_imagenes (str): Ruta al directorio con las imágenes
        nivel_calidad (str): Nivel de calidad (baja, media, maxima)
        
    Returns:
        Tuple[float, str]: Tamaño estimado (en MB) y unidad
    """
    config = CONFIGURACIONES_CALIDAD[nivel_calidad]
    
    # Obtener lista de imágenes
    imagenes = []
    for ext in ['.png', '.jpg', '.jpeg', '.tif', '.tiff', '.bmp']:
        imagenes.extend(Path(directorio_imagenes).glob(f'*{ext}'))
    
    # Si no hay imágenes, devolver 0
    if not imagenes:
        return 0.0, "MB"
    
    # Calcular tamaño total de las imágenes originales
    tamano_total = sum(img.stat().st_size for img in imagenes)
    
    # Factores de estimación según calidad
    factores = {
        "baja": 0.15,   # Estimado: 15% del tamaño original
        "media": 0.4,   # Estimado: 40% del tamaño original
        "maxima": 0.8,  # Estimado: 80% del tamaño original
    }
    
    # Estimar tamaño del PDF
    factor = factores[nivel_calidad]
    tamano_estimado = tamano_total * factor / (1024 * 1024)  # Convertir a MB
    
    # Elegir la unidad adecuada
    if tamano_estimado < 1:
        return tamano_estimado * 1024, "KB"
    elif tamano_estimado > 1024:
        return tamano_estimado / 1024, "GB"
    else:
        return tamano_estimado, "MB"

def generar_pdf_con_imagenes(
    directorio_imagenes: str,
    ruta_salida: str,
    debug: bool = False,
    incluir_numeros_pagina: bool = True,
    callback_progreso: Optional[Callable[[int, int], None]] = None,
    nivel_calidad: str = "media"
):
    """
    Genera un PDF con todas las imágenes del directorio, garantizando:
    - Orientación siempre horizontal (landscape)
    - Márgenes exactos de 1cm en todos los lados
    - Imágenes ajustadas al máximo tamaño posible respetando márgenes
    - Número de página en la esquina externa inferior (opcional)
    - Calidad de imagen según el nivel seleccionado
    
    Args:
        directorio_imagenes (str): Ruta al directorio que contiene las imágenes
        ruta_salida (str): Ruta donde se guardará el PDF generado
        debug (bool, opcional): Activa el modo debug para información adicional
        incluir_numeros_pagina (bool, opcional): Indica si se deben incluir números de página
        callback_progreso (Callable, opcional): Función a llamar para reportar progreso
        nivel_calidad (str): Nivel de calidad (baja, media, maxima)
    
    Returns:
        None: El PDF se guarda en la ruta especificada
    
    Raises:
        Exception: Si hay errores al procesar imágenes o generar el PDF
    """
    if nivel_calidad not in CONFIGURACIONES_CALIDAD:
        raise ValueError(f"Nivel de calidad no válido: {nivel_calidad}")
    
    # Obtener configuración según el nivel seleccionado
    config = CONFIGURACIONES_CALIDAD[nivel_calidad]
    dpi = config["dpi"]
    calidad_imagen = config["calidad"]
    formato_temp = config["formato_temp"]
    
    # Mostrar configuración utilizada
    if debug:
        logger.info(f"Configuración utilizada: {config}")
        
    # Configurar tamaño de página y márgenes
    margen = 1 * cm  # 1 centímetro exacto
    ancho_pagina, alto_pagina = landscape(letter)  # Forzar orientación horizontal
    
    # Calcular área disponible para la imagen
    ancho_disponible = ancho_pagina - (2 * margen)
    alto_disponible = alto_pagina - (2 * margen)
    
    # Crear el PDF con configuración de calidad mejorada
    c = canvas.Canvas(ruta_salida, pagesize=landscape(letter))
    
    # Obtener lista de imágenes y ordenarlas
    imagenes = []
    for ext in ['.png', '.jpg', '.jpeg', '.tif', '.tiff', '.bmp']:
        imagenes.extend(Path(directorio_imagenes).glob(f'*{ext}'))
    imagenes = sorted(imagenes, key=lambda x: x.name)
    
    total_imagenes = len(imagenes)
    
    # Crear directorio temporal si no existe
    temp_dir = Path('temp_images')
    temp_dir.mkdir(exist_ok=True)
    
    # Procesar cada imagen
    for num_pagina, ruta_imagen in enumerate(imagenes, 1):
        try:
            # Abrir y procesar la imagen
            with Image.open(ruta_imagen) as img:
                # Convertir a RGB si es necesario pero preservando canal alfa si existe
                if img.mode == 'RGBA' and formato_temp == "PNG":
                    # Mantener el canal alfa para mejor calidad en PNG
                    pass
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Obtener dimensiones originales
                ancho_orig, alto_orig = img.size
                
                # Rotar la imagen si está en vertical
                if alto_orig > ancho_orig:
                    img = img.rotate(
                        -90, 
                        expand=True, 
                        resample=Image.Resampling.BICUBIC
                    )
                    ancho_orig, alto_orig = img.size
                
                # Calcular el factor de escala para ajustar la imagen
                escala_ancho = ancho_disponible / ancho_orig
                escala_alto = alto_disponible / alto_orig
                escala = min(escala_ancho, escala_alto)
                
                # Calcular nuevas dimensiones
                nuevo_ancho = int(ancho_orig * escala)
                nuevo_alto = int(alto_orig * escala)
                
                # En calidad máxima, solo redimensionar si es necesario
                if nivel_calidad == "maxima" and escala < 1:
                    img = img.resize(
                        (nuevo_ancho, nuevo_alto), 
                        Image.Resampling.LANCZOS
                    )
                elif nivel_calidad != "maxima" or escala < 1:
                    # En calidad baja o media, siempre redimensionar
                    img = img.resize(
                        (nuevo_ancho, nuevo_alto), 
                        Image.Resampling.LANCZOS if nivel_calidad != "baja" 
                        else Image.Resampling.BICUBIC
                    )
                else:
                    # Si no es necesario reducir con calidad máxima
                    nuevo_ancho, nuevo_alto = ancho_orig, alto_orig
                
                # Calcular posición para centrado exacto
                x = margen + (ancho_disponible - nuevo_ancho) / 2
                y = margen + (alto_disponible - nuevo_alto) / 2
                
                # Guardar la imagen temporalmente con calidad configurada
                temp_img_path = temp_dir / f"temp_img_{num_pagina}.{formato_temp.lower()}"
                
                # Guardar con el formato y calidad configurada
                if formato_temp == "PNG":
                    img.save(temp_img_path, format=formato_temp, dpi=(dpi, dpi))
                else:
                    img.save(
                        temp_img_path, 
                        format=formato_temp,
                        quality=calidad_imagen,
                        dpi=(dpi, dpi)
                    )
                
                # Dibujar la imagen con calidad optimizada
                c.drawImage(
                    str(temp_img_path), 
                    x, y, 
                    width=nuevo_ancho, 
                    height=nuevo_alto,
                    preserveAspectRatio=True, 
                    mask='auto'
                )
                
                # Agregar número de página si está habilitado
                if incluir_numeros_pagina:
                    c.setFont("Helvetica", 10)
                    c.drawString(
                        ancho_pagina - margen - 20, 
                        margen - 15, 
                        str(num_pagina)
                    )
                
                # Nueva página
                c.showPage()
                
                # Llamar al callback de progreso si existe
                if callback_progreso:
                    callback_progreso(num_pagina, total_imagenes)
                
                logger.info(
                    f"Procesada imagen {num_pagina} de {total_imagenes}: {ruta_imagen.name}"
                )
                
        except Exception as e:
            logger.error(f"Error procesando {ruta_imagen.name}: {str(e)}")
            raise
    
    # Guardar el PDF con configuración de calidad
    try:
        c.save()
        logger.info(f"PDF generado exitosamente: {ruta_salida}")
    except Exception as e:
        logger.error(f"Error al guardar el PDF: {str(e)}")
        raise
    
    # Limpiar archivos temporales
    try:
        for temp_file in temp_dir.glob(f"temp_img_*.*"):
            temp_file.unlink()
        temp_dir.rmdir()
    except Exception as e:
        logger.warning(f"Error al limpiar archivos temporales: {str(e)}")

def main():
    """
    Función principal que procesa los argumentos de línea de comandos
    y llama a la función de generación de PDF.
    
    Args:
        None: Los argumentos se toman de sys.argv
        
    Returns:
        None
    """
    # Configurar el parser de argumentos
    parser = argparse.ArgumentParser(
        description='Genera un PDF a partir de imágenes en un directorio.'
    )
    parser.add_argument('directorio', help='Directorio que contiene las imágenes')
    parser.add_argument(
        '--output', '-o', 
        help='Ruta de salida del PDF (opcional)'
    )
    parser.add_argument(
        '--debug', '-d', 
        action='store_true', 
        help='Activa el modo debug'
    )
    parser.add_argument(
        '--no-page-numbers', 
        action='store_true', 
        help='No incluir números de página en el documento'
    )
    parser.add_argument(
        '--calidad', 
        choices=['baja', 'media', 'maxima'],
        default='media',
        help='Nivel de calidad del PDF (baja, media, maxima)'
    )
    parser.add_argument(
        '--solo-estimar', 
        action='store_true',
        help='Solo estimar el tamaño del PDF sin generarlo'
    )
    
    args = parser.parse_args()
    
    # Verificar que el directorio existe
    if not os.path.isdir(args.directorio):
        logger.error(f"El directorio {args.directorio} no existe")
        sys.exit(1)
        
    # Estimar el tamaño del PDF resultante
    tamano_estimado, unidad = estimar_tamano_pdf(args.directorio, args.calidad)
    logger.info(
        f"Tamaño estimado del PDF con calidad {args.calidad}: "
        f"{tamano_estimado:.2f} {unidad}"
    )
    
    # Si solo se quiere estimar, terminar aquí
    if args.solo_estimar:
        logger.info("Estimación completada. Terminando.")
        return
    
    # Si no se especifica una ruta de salida, usar el nombre del directorio
    if args.output:
        ruta_salida_base = args.output
    else:
        nombre_directorio = os.path.basename(os.path.normpath(args.directorio))
        ruta_salida_base = os.path.join(
            args.directorio, 
            f"CONSOLIDADO_{nombre_directorio}"
        )

    # Asegurar que el nombre base no tenga extensión .pdf para el chequeo
    if ruta_salida_base.lower().endswith(".pdf"):
        ruta_salida_sin_ext = ruta_salida_base[:-4]
    else:
        ruta_salida_sin_ext = ruta_salida_base
        
    ruta_salida = f"{ruta_salida_sin_ext}.pdf"
    contador = 1
    while os.path.exists(ruta_salida):
        ruta_salida = f"{ruta_salida_sin_ext} ({contador}).pdf"
        contador += 1
    
    # Generar el PDF
    generar_pdf_con_imagenes(
        args.directorio,
        ruta_salida,
        debug=args.debug,
        incluir_numeros_pagina=not args.no_page_numbers,
        nivel_calidad=args.calidad
    )
    
    # Mostrar tamaño real del archivo generado
    tamano_real = os.path.getsize(ruta_salida) / (1024 * 1024)  # MB
    if tamano_real < 1:
        tamano_real_formateado = f"{tamano_real * 1024:.2f} KB"
    elif tamano_real > 1024:
        tamano_real_formateado = f"{tamano_real / 1024:.2f} GB"
    else:
        tamano_real_formateado = f"{tamano_real:.2f} MB"
    
    logger.info(f"Tamaño real del PDF generado: {tamano_real_formateado}")
    
    # Triple verificación final
    logger.info("Realizando verificación final...")
    try:
        with open(ruta_salida, 'rb') as f:
            assert f.readable(), "El PDF no se puede leer"
            contenido = f.read()
            assert len(contenido) > 0, "El PDF está vacío"
            logger.info("Verificación final completada: PDF generado correctamente")
    except Exception as e:
        logger.error(f"Error en la verificación final: {str(e)}")
        raise

if __name__ == "__main__":
    main() 