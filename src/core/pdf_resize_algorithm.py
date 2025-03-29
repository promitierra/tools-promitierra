import fitz

# Definir constantes de tamaño (disponibles para importar)
LETTER_WIDTH = 8.5 * 72  # 612 puntos
LETTER_HEIGHT = 11 * 72  # 792 puntos
LETTER_WIDTH_LANDSCAPE = 11 * 72  # 792 puntos
LETTER_HEIGHT_LANDSCAPE = 8.5 * 72  # 612 puntos

def resize_pdf_page(page, centrar=False):
    """
    Redimensiona una página de PDF a tamaño carta, preservando la orientación.
    
    Args:
        page (fitz.Page): La página de PDF a redimensionar
        centrar (bool): Si es True, centra el contenido en la página
        
    Returns:
        fitz.Document: Un documento temporal con la página redimensionada
    """
    # Obtener dimensiones actuales
    rect = page.rect
    ancho_actual = rect.width
    alto_actual = rect.height

    # Determinar si la página es horizontal o vertical
    es_horizontal = ancho_actual > alto_actual
    
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
            # Calcular desplazamientos para centrar
            desplazamiento_x = (ancho_destino - (ancho_actual * escala)) / 2
            desplazamiento_y = (alto_destino - (alto_actual * escala)) / 2
            
            # Crear un rectángulo centrado para mostrar el contenido
            # Usamos el rectángulo completo de la página destino
            rect_destino = temp_page.rect
            
            # Crear una matriz de transformación que incluya tanto la escala como el desplazamiento
            # para centrar el contenido como un objeto completo
            matriz = fitz.Matrix(escala, escala).pretranslate(desplazamiento_x, desplazamiento_y)
            
            # Mostrar el contenido centrado usando la matriz de transformación
            temp_page.show_pdf_page(
                rect_destino,
                page.parent,  # Documento original
                page.number,  # Número de página
                matriz
            )
        else:
            # Mostrar el contenido sin centrar (alineado a la esquina superior izquierda)
            temp_page.show_pdf_page(
                temp_page.rect,
                page.parent,  # Documento original
                page.number,  # Número de página
                fitz.Matrix(escala, escala)
            )
    except ValueError as e:
        # Manejar el caso de páginas vacías
        if "nothing to show - source page empty" in str(e):
            # Para páginas vacías, simplemente continuamos con la página en blanco
            print(f"Advertencia: La página está vacía, se mantendrá en blanco")
        else:
            # Si es otro tipo de error, lo propagamos
            raise
    
    return temp_doc

def process_pdf(doc, centrar=False, progress_callback=None):
    """
    Procesa un documento PDF completo, redimensionando todas sus páginas a tamaño carta.
    
    Args:
        doc (fitz.Document): El documento PDF a procesar
        centrar (bool): Si es True, centra el contenido en cada página
        progress_callback (callable, optional): Función para reportar el progreso
            Debe aceptar dos parámetros: página actual y total de páginas
            
    Returns:
        fitz.Document: Un nuevo documento con todas las páginas redimensionadas
    """
    # Verificar que el documento tenga páginas
    if len(doc) == 0:
        raise ValueError("El documento PDF no contiene páginas")
        
    # Crear un nuevo documento para almacenar las páginas redimensionadas
    new_doc_final = fitz.open()

    # Procesar cada página del documento original
    num_paginas = len(doc)
    for i in range(num_paginas):
        # Reportar progreso si se proporcionó una función de callback
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

    return new_doc_final