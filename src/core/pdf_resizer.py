import os
import sys
import fitz

class PDFResizer:
    # Definir constantes de tamaño
    LETTER_WIDTH = 8.5 * 72  # 612 puntos
    LETTER_HEIGHT = 11 * 72  # 792 puntos
    LETTER_WIDTH_LANDSCAPE = 11 * 72  # 792 puntos
    LETTER_HEIGHT_LANDSCAPE = 8.5 * 72  # 612 puntos
    
    def __init__(self):
        pass
    
    def resize_pdf(self, input_pdf, output_pdf, centrar=False):
        """Redimensionar PDF a tamaño carta"""
        try:
            doc = fitz.open(input_pdf)
            # Verificar que el documento tenga páginas
            if len(doc) == 0:
                print(f"Error: El archivo PDF '{input_pdf}' no contiene páginas")
                return False
        except Exception as e:
            print(f"Error abriendo archivo PDF: {e}")
            return False

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
                ancho_destino = self.LETTER_WIDTH_LANDSCAPE
                alto_destino = self.LETTER_HEIGHT_LANDSCAPE
            else:
                # Usar dimensiones de carta vertical
                ancho_destino = self.LETTER_WIDTH
                alto_destino = self.LETTER_HEIGHT
            
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
            return False
        finally:
            doc.close()
            new_doc_final.close()