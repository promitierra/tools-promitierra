try:
    import fitz
    from reportlab.lib.pagesizes import letter
    import sys
    import os
except ImportError:
    print("Por favor instale los paquetes requeridos: pip install pymupdf reportlab")
    import sys
    sys.exit(1)

# Definir constantes de tamaño (disponibles para importar)
LETTER_WIDTH = 8.5 * 72  # 612 puntos
LETTER_HEIGHT = 11 * 72  # 792 puntos
LETTER_WIDTH_LANDSCAPE = 11 * 72  # 792 puntos
LETTER_HEIGHT_LANDSCAPE = 8.5 * 72  # 612 puntos

# Función principal para redimensionar PDF
def resize_pdf(input_pdf, output_pdf, centrar=False):
    try:
        doc = fitz.open(input_pdf)
        # Verificar que el documento tenga páginas
        if len(doc) == 0:
            print(f"Error: El archivo PDF '{input_pdf}' no contiene páginas")
            sys.exit(1)
    except Exception as e:
        print(f"Error abriendo archivo PDF: {e}")
        sys.exit(1)  # Aseguramos que se lance SystemExit

    # Crear un nuevo documento para almacenar las páginas redimensionadas
    new_doc_final = fitz.open()

    # Procesar cada página del documento original
    num_paginas = len(doc)
    for i in range(num_paginas):
        # Siempre trabajamos con la primera página porque vamos eliminando páginas
        pagina = doc[0]
        rect = pagina.rect
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
                matriz = fitz.Matrix(escala, escala).postTranslate(desplazamiento_x, desplazamiento_y)
                
                # Mostrar el contenido centrado usando la matriz de transformación
                temp_page.show_pdf_page(
                    rect_destino,
                    doc,
                    0,  # Siempre usamos la página 0
                    matriz
                )
            else:
                # Mostrar el contenido sin centrar (alineado a la esquina superior izquierda)
                temp_page.show_pdf_page(
                    temp_page.rect,
                    doc,
                    0,  # Siempre usamos la página 0
                    fitz.Matrix(escala, escala)
                )
        except ValueError as e:
            # Manejar el caso de páginas vacías
            if "nothing to show - source page empty" in str(e):
                # Para páginas vacías, simplemente continuamos con la página en blanco
                print(f"Advertencia: Página {i} está vacía, se mantendrá en blanco")
            else:
                # Si es otro tipo de error, lo propagamos
                raise
        
        # Añadir la página redimensionada al documento final
        new_doc_final.insert_pdf(temp_doc)
        
        # Eliminar la página original después de procesarla
        doc.delete_page(0)
        
        # Cerrar el documento temporal
        temp_doc.close()

    try:
        # Guardar el documento final con las páginas redimensionadas
        new_doc_final.save(output_pdf)
        print(f"PDF redimensionado exitosamente a tamaño carta (preservando orientación): {output_pdf}")
        return True
    except Exception as e:
        print(f"Error guardando PDF: {e}")
        doc.close()
        new_doc_final.close()
        sys.exit(1)  # Lanzar SystemExit en caso de error
    finally:
        doc.close()
        new_doc_final.close()

# Función para listar archivos PDF en el directorio actual
def listar_pdfs_disponibles():
    # Obtener la lista de archivos en el directorio actual
    archivos = os.listdir()
    # Filtrar solo los archivos PDF
    pdfs = [archivo for archivo in archivos if archivo.lower().endswith('.pdf')]
    
    if not pdfs:
        print("No se encontraron archivos PDF en el directorio actual.")
        sys.exit(1)
    
    return pdfs

# Función para mostrar menú de selección
def mostrar_menu_seleccion(pdfs):
    print("\nArchivos PDF disponibles:")
    for i, pdf in enumerate(pdfs, 1):
        print(f"{i}. {pdf}")
    
    while True:
        try:
            seleccion = int(input("\nSeleccione el número del archivo PDF a redimensionar (0 para salir): "))
            if seleccion == 0:
                print("Operación cancelada.")
                sys.exit(0)
            elif 1 <= seleccion <= len(pdfs):
                return pdfs[seleccion-1]
            else:
                print(f"Por favor, ingrese un número entre 1 y {len(pdfs)}.")
        except ValueError:
            print("Por favor, ingrese un número válido.")

# Ejecutar el script solo cuando se llama directamente
if __name__ == "__main__":
    # Verificar si se proporcionaron argumentos de línea de comandos
    if len(sys.argv) >= 3:
        input_pdf = sys.argv[1]
        output_pdf = sys.argv[2]
        
        # Verificar si hay un tercer argumento para centrar
        centrar = False
        if len(sys.argv) > 3 and sys.argv[3].lower() in ['centrar', 'c', 'center', 'true', 's', 'si', 'sí']:
            centrar = True
        
        # Verificar si el archivo de entrada existe
        if not os.path.exists(input_pdf):
            print(f"Error: El archivo de entrada '{input_pdf}' no existe")
            sys.exit(1)
    else:
        # Mostrar archivos PDF disponibles y permitir selección
        pdfs_disponibles = listar_pdfs_disponibles()
        input_pdf = mostrar_menu_seleccion(pdfs_disponibles)
        
        # Solicitar nombre del archivo de salida
        nombre_base = os.path.splitext(input_pdf)[0]
        output_pdf_default = f"{nombre_base}_letter.pdf"
        output_pdf_input = input(f"\nNombre del archivo de salida [{output_pdf_default}]: ").strip()
        output_pdf = output_pdf_input if output_pdf_input else output_pdf_default
        
        # Preguntar si desea centrar el contenido
        centrar_input = input("\n¿Desea centrar el contenido en la página? (s/n) [n]: ").strip().lower()
        centrar = centrar_input == 's' or centrar_input == 'si' or centrar_input == 'sí'
        
        print(f"\nProcesando: {input_pdf} -> {output_pdf} (Centrado: {'Sí' if centrar else 'No'})")
    
    # Llamar a la función principal
    resize_pdf(input_pdf, output_pdf, centrar)