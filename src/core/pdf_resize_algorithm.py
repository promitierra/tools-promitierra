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
import hashlib
from typing import Dict, Tuple, Optional, List
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import multiprocessing
import queue

# Configurar el logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Definir constantes de tamaño (disponibles para importar)
LETTER_WIDTH = 8.5 * 72  # 612 puntos
LETTER_HEIGHT = 11 * 72  # 792 puntos
LETTER_WIDTH_LANDSCAPE = 11 * 72  # 792 puntos
LETTER_HEIGHT_LANDSCAPE = 8.5 * 72  # 612 puntos

# Caché de páginas procesadas
_page_cache: Dict[str, Tuple[fitz.Document, float]] = {}
_cache_hits = 0
_cache_misses = 0
_max_cache_size = 100  # Número máximo de páginas en caché
_cache_lock = threading.Lock()  # Lock para acceso al caché

# Cola para resultados ordenados
_result_queue = queue.PriorityQueue()

def _get_page_hash(page, centrar):
    """
    Genera un hash único para una página basado en su contenido y configuración.
    
    Args:
        page (fitz.Page): La página del PDF
        centrar (bool): Si el contenido debe centrarse
        
    Returns:
        str: Hash único que identifica la página y su configuración
    """
    try:
        # Obtener el contenido como diccionario y convertirlo a string
        content_dict = page.get_text("rawdict")
        content_str = str(content_dict)
        
        # Crear una cadena que combine el contenido y la configuración
        combined_content = f"{content_str}_{centrar}_{page.rect.width}_{page.rect.height}"
        
        # Generar y retornar el hash
        return hashlib.md5(combined_content.encode('utf-8')).hexdigest()
    except Exception as e:
        logger.warning(f"Error al generar hash de página: {str(e)}")
        # En caso de error, generar un hash basado en dimensiones y número de página
        fallback_content = f"page_{page.number}_{page.rect.width}_{page.rect.height}_{centrar}"
        return hashlib.md5(fallback_content.encode('utf-8')).hexdigest()

def _get_from_cache(page_hash: str) -> Optional[fitz.Document]:
    """
    Obtiene una página del caché si existe y no ha expirado.
    Thread-safe usando un lock.
    
    Args:
        page_hash (str): Hash de la página
        
    Returns:
        Optional[fitz.Document]: Documento en caché o None si no existe
    """
    global _cache_hits, _cache_misses
    
    with _cache_lock:
        if page_hash in _page_cache:
            doc, timestamp = _page_cache[page_hash]
            # Verificar si el caché ha expirado (30 minutos)
            if time.time() - timestamp <= 1800:
                _cache_hits += 1
                logger.debug(f"Cache hit! Hits: {_cache_hits}, Misses: {_cache_misses}")
                # Crear una nueva copia del documento
                new_doc = fitz.open()
                new_doc.insert_pdf(doc)
                return new_doc
        
        _cache_misses += 1
        logger.debug(f"Cache miss! Hits: {_cache_hits}, Misses: {_cache_misses}")
        return None

def _add_to_cache(page_hash: str, doc: fitz.Document):
    """
    Añade una página al caché, manteniendo el límite de tamaño.
    Thread-safe usando un lock.
    
    Args:
        page_hash (str): Hash de la página
        doc (fitz.Document): Documento a cachear
    """
    with _cache_lock:
        # Si el caché está lleno, eliminar la entrada más antigua
        if len(_page_cache) >= _max_cache_size:
            oldest_key = min(_page_cache.keys(), key=lambda k: _page_cache[k][1])
            old_doc, _ = _page_cache[oldest_key]
            old_doc.close()
            del _page_cache[oldest_key]
        
        # Crear una nueva copia del documento para el caché
        cached_doc = fitz.open()
        cached_doc.insert_pdf(doc)
        _page_cache[page_hash] = (cached_doc, time.time())

def _process_page_parallel(args: Tuple[fitz.Page, bool, int]) -> Tuple[int, fitz.Document]:
    """
    Procesa una página en paralelo.
    
    Args:
        args: Tupla con (página, centrar, índice)
        
    Returns:
        Tupla con (índice, documento procesado)
    """
    page, centrar, idx = args
    try:
        doc = resize_pdf_page(page, centrar)
        return idx, doc
    except Exception as e:
        logger.error(f"Error procesando página {idx + 1}: {str(e)}")
        raise

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
    
    # Intentar obtener del caché
    page_hash = _get_page_hash(page, centrar)
    cached_doc = _get_from_cache(page_hash)
    if cached_doc is not None:
        tiempo_cache = time.time() - inicio
        logger.info(f"Página {page.number + 1} recuperada del caché en {tiempo_cache:.2f} segundos")
        return cached_doc

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
    
    # Añadir al caché antes de retornar
    _add_to_cache(page_hash, temp_doc)
    
    # Crear una nueva copia para retornar
    result_doc = fitz.open()
    result_doc.insert_pdf(temp_doc)
    temp_doc.close()
    
    return result_doc

def process_pdf(doc, centrar=False, progress_callback=None, batch_size=10, max_workers=None):
    """
    Procesa un documento PDF completo, redimensionando todas sus páginas a tamaño carta.
    
    Esta función procesa cada página del documento PDF de entrada y crea un nuevo
    documento con todas las páginas redimensionadas a tamaño carta. Mantiene la
    orientación original de cada página y proporciona la opción de centrar el contenido.
    Para documentos grandes, procesa las páginas en lotes para optimizar el uso de memoria.
    
    Args:
        doc (fitz.Document): El documento PDF a procesar
        centrar (bool): Si es True, centra el contenido en cada página
        progress_callback (callable, optional): Función para reportar el progreso.
            La función debe aceptar dos parámetros:
            - página_actual (int): Número de página siendo procesada (1-indexed)
            - total_paginas (int): Número total de páginas en el documento
        batch_size (int): Número de páginas a procesar por lote. Por defecto es 10.
            Para documentos muy grandes, usar un valor menor puede ayudar con la memoria.
        max_workers (int, optional): Número máximo de workers para procesamiento paralelo.
            Si no se especifica, se usa min(32, os.cpu_count() + 4).
            
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
    
    # Determinar número óptimo de workers si no se especifica
    if max_workers is None:
        max_workers = min(32, multiprocessing.cpu_count() + 4)
    
    logger.info(f"Iniciando procesamiento de documento con {len(doc)} páginas")
    logger.info(f"Modo de centrado: {'activado' if centrar else 'desactivado'}")
    logger.info(f"Estado del caché - Hits: {_cache_hits}, Misses: {_cache_misses}, Tamaño: {len(_page_cache)}")
    logger.info(f"Configuración de paralelización - Workers: {max_workers}, Tamaño de lote: {batch_size}")
    
    # Crear un nuevo documento para almacenar las páginas redimensionadas
    new_doc_final = fitz.open()

    # Procesar páginas en lotes para optimizar memoria
    num_paginas = len(doc)
    tiempo_inicio_lote = time.time()
    paginas_procesadas = 0
    
    # Calcular número de lotes
    num_lotes = (num_paginas + batch_size - 1) // batch_size
    
    for lote in range(num_lotes):
        inicio_lote = lote * batch_size
        fin_lote = min(inicio_lote + batch_size, num_paginas)
        
        logger.info(f"Procesando lote {lote + 1}/{num_lotes} (páginas {inicio_lote + 1}-{fin_lote})")
        
        # Preparar argumentos para procesamiento paralelo
        paginas_lote = [(doc[i], centrar, i) for i in range(inicio_lote, fin_lote)]
        
        # Procesar páginas en paralelo
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Enviar trabajos
            futures = {
                executor.submit(_process_page_parallel, args): args[2]  # args[2] es el índice
                for args in paginas_lote
            }
            
            # Recolectar resultados ordenados
            resultados: List[Tuple[int, fitz.Document]] = []
            
            for future in as_completed(futures):
                idx = futures[future]
                try:
                    resultado = future.result()
                    resultados.append(resultado)
                    paginas_procesadas += 1
                    
                    # Reportar progreso
                    if progress_callback:
                        progress_callback(paginas_procesadas, num_paginas)
                    
                    # Calcular y mostrar estadísticas de tiempo
                    tiempo_actual = time.time()
                    tiempo_promedio = (tiempo_actual - inicio_total) / paginas_procesadas
                    tiempo_estimado = tiempo_promedio * (num_paginas - paginas_procesadas)
                    
                    logger.info(f"Progreso: {paginas_procesadas}/{num_paginas} páginas ({(paginas_procesadas/num_paginas)*100:.1f}%)")
                    logger.debug(f"Tiempo promedio: {tiempo_promedio:.2f}s, Estimado restante: {tiempo_estimado:.2f}s")
                    
                except Exception as e:
                    logger.error(f"Error procesando página {idx + 1}: {str(e)}")
                    raise
            
            # Ordenar resultados por índice
            resultados.sort(key=lambda x: x[0])
            
            # Añadir páginas al documento final en orden
            for _, temp_doc in resultados:
                new_doc_final.insert_pdf(temp_doc)
                temp_doc.close()
        
        # Forzar recolección de basura al final de cada lote
        import gc
        gc.collect()
        
        tiempo_inicio_lote = time.time()

    tiempo_total = time.time() - inicio_total
    logger.info(f"Procesamiento completado en {tiempo_total:.2f} segundos")
    logger.info(f"Tiempo promedio por página: {tiempo_total/num_paginas:.2f} segundos")
    logger.info(f"Estadísticas finales del caché - Hits: {_cache_hits}, Misses: {_cache_misses}, Ratio: {_cache_hits/(_cache_hits + _cache_misses):.2%}")
    
    return new_doc_final