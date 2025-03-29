"""
Módulo principal para el redimensionamiento de archivos PDF a tamaño carta.

Este módulo implementa el algoritmo central para redimensionar páginas PDF a tamaño carta,
manteniendo la orientación original (vertical u horizontal) y proporcionando opciones
para centrar el contenido.

Constantes:
    LETTER_WIDTH (float): Ancho de página carta en puntos (612)
    LETTER_HEIGHT (float): Alto de página carta en puntos (792)
    LETTER_WIDTH_LANDSCAPE (float): Ancho de página carta horizontal (792)
    LETTER_HEIGHT_LANDSCAPE (float): Alto de página carta horizontal (612)

Funciones:
    resize_pdf_page: Redimensiona una página individual a tamaño carta
    process_pdf: Procesa un documento PDF completo, redimensionando todas sus páginas
"""

import fitz
import logging
from pathlib import Path
import time

# Configurar el logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Definir constantes de tamaño (disponibles para importar)
LETTER_WIDTH = 8.5 * 72  # 612 puntos
LETTER_HEIGHT = 11 * 72  # 792 puntos
LETTER_WIDTH_LANDSCAPE = 11 * 72  # 792 puntos
LETTER_HEIGHT_LANDSCAPE = 8.5 * 72  # 612 puntos

def resize_pdf_page(page, centrar=False):
    """
    Redimensiona una página de PDF a tamaño carta, preservando la orientación.
    
    Esta función toma una página de PDF y la redimensiona al tamaño carta estándar
    (8.5" x 11"), manteniendo su orientación original (vertical u horizontal).
    El contenido se escala proporcionalmente para ajustarse a las nuevas dimensiones.
    
    Args:
        page (fitz.Page): La página de PDF a redimensionar
        centrar (bool): Si es True, centra el contenido en la página. Si es False,
                       el contenido se alinea a la esquina superior izquierda.
        
    Returns:
        fitz.Document: Un documento temporal con la página redimensionada
        
    Raises:
        ValueError: Si la página está vacía o no se puede procesar
    """
    inicio = time.time()
    logger.info(f"Iniciando redimensionamiento de página {page.number + 1}")
    
    # Obtener dimensiones actuales
    rect = page.rect
    ancho_actual = rect.width
    alto_actual = rect.height

    # Determinar si la página es horizontal o vertical
    es_horizontal = ancho_actual > alto_actual
    orientacion = "horizontal" if es_horizontal else "vertical"
    logger.debug(f"Página {page.number + 1}: Orientación {orientacion}, dimensiones: {ancho_actual}x{alto_actual}")
    
    # Seleccionar dimensiones de carta según orientación
    if es_horizontal:
        # Usar dimensiones de carta horizontal
        ancho_destino = LETTER_WIDTH_LANDSCAPE
        alto_destino = LETTER_HEIGHT_LANDSCAPE
    else:
        # Usar dimensiones de carta vertical
        ancho_destino = LETTER_WIDTH
        alto_destino = LETTER_HEIGHT
    
    # Calcular factor de escala
    escala_ancho = ancho_destino / ancho_actual
    escala_alto = alto_destino / alto_actual
    escala = min(escala_ancho, escala_alto)
    logger.debug(f"Factor de escala calculado: {escala:.3f}")

    # Crear una página temporal con tamaño carta en la orientación correcta
    temp_doc = fitz.open()
    temp_page = temp_doc.new_page(width=ancho_destino, height=alto_destino)
    
    # Dibujar contenido escalado
    try:
        # Calcular el nuevo ancho y alto después de escalar
        nuevo_ancho = ancho_actual * escala
        nuevo_alto = alto_actual * escala
        
        # Si se solicita centrar, calcular desplazamientos para centrar el contenido
        if centrar:
            logger.debug("Aplicando centrado de contenido")
            # Calcular desplazamientos para centrar
            desplazamiento_x = (ancho_destino - (ancho_actual * escala)) / 2
            desplazamiento_y = (alto_destino - (alto_actual * escala)) / 2
            
            # Crear un rectángulo centrado para mostrar el contenido
            rect_destino = temp_page.rect
            
            # Crear una matriz de transformación que incluya tanto la escala como el desplazamiento
            matriz = fitz.Matrix(escala, escala).pretranslate(desplazamiento_x, desplazamiento_y)
            
            # Mostrar el contenido centrado usando la matriz de transformación
            temp_page.show_pdf_page(
                rect_destino,
                page.parent,  # Documento original
                page.number,  # Número de página
                matriz
            )
        else:
            logger.debug("Aplicando alineación a la esquina superior izquierda")
            # Mostrar el contenido sin centrar
            temp_page.show_pdf_page(
                temp_page.rect,
                page.parent,
                page.number,
                fitz.Matrix(escala, escala)
            )
    except ValueError as e:
        if "nothing to show - source page empty" in str(e):
            logger.warning(f"La página {page.number + 1} está vacía, se mantendrá en blanco")
        else:
            logger.error(f"Error al procesar la página {page.number + 1}: {str(e)}")
            raise
    
    tiempo_total = time.time() - inicio
    logger.info(f"Página {page.number + 1} redimensionada en {tiempo_total:.2f} segundos")
    return temp_doc

def process_pdf(doc, centrar=False, progress_callback=None):
    """
    Procesa un documento PDF completo, redimensionando todas sus páginas a tamaño carta.
    
    Esta función procesa cada página del documento PDF de entrada y crea un nuevo
    documento con todas las páginas redimensionadas a tamaño carta. Mantiene la
    orientación original de cada página y proporciona la opción de centrar el contenido.
    
    Args:
        doc (fitz.Document): El documento PDF a procesar
        centrar (bool): Si es True, centra el contenido en cada página
        progress_callback (callable, optional): Función para reportar el progreso.
            La función debe aceptar dos parámetros:
            - página_actual (int): Número de página siendo procesada (1-indexed)
            - total_paginas (int): Número total de páginas en el documento
            
    Returns:
        fitz.Document: Un nuevo documento con todas las páginas redimensionadas
        
    Raises:
        ValueError: Si el documento está vacío o no contiene páginas
    """
    inicio_total = time.time()
    
    # Verificar que el documento tenga páginas
    if len(doc) == 0:
        logger.error("El documento PDF no contiene páginas")
        raise ValueError("El documento PDF no contiene páginas")
    
    logger.info(f"Iniciando procesamiento de documento con {len(doc)} páginas")
    logger.info(f"Modo de centrado: {'activado' if centrar else 'desactivado'}")
    
    # Crear un nuevo documento para almacenar las páginas redimensionadas
    new_doc_final = fitz.open()

    # Procesar cada página del documento original
    num_paginas = len(doc)
    tiempo_inicio_pagina = time.time()
    
    for i in range(num_paginas):
        # Reportar progreso
        if progress_callback:
            progress_callback(i + 1, num_paginas)
            
        # Obtener la página actual
        pagina = doc[i]
        
        # Redimensionar la página
        temp_doc = resize_pdf_page(pagina, centrar)
        
        # Añadir la página redimensionada al documento final
        new_doc_final.insert_pdf(temp_doc)
        
        # Cerrar el documento temporal
        temp_doc.close()
        
        # Calcular y mostrar estadísticas de tiempo
        tiempo_pagina = time.time() - tiempo_inicio_pagina
        tiempo_promedio = (time.time() - inicio_total) / (i + 1)
        tiempo_estimado = tiempo_promedio * (num_paginas - (i + 1))
        
        logger.info(f"Progreso: {i + 1}/{num_paginas} páginas ({((i + 1)/num_paginas)*100:.1f}%)")
        logger.debug(f"Tiempo página actual: {tiempo_pagina:.2f}s, Promedio: {tiempo_promedio:.2f}s, Estimado restante: {tiempo_estimado:.2f}s")
        
        tiempo_inicio_pagina = time.time()

    tiempo_total = time.time() - inicio_total
    logger.info(f"Procesamiento completado en {tiempo_total:.2f} segundos")
    logger.info(f"Tiempo promedio por página: {tiempo_total/num_paginas:.2f} segundos")

    return new_doc_final