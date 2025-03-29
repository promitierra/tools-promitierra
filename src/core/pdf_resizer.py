import os
import sys
import fitz
# Importar el módulo compartido para el procesamiento de PDF
from .pdf_resize_algorithm import process_pdf, LETTER_WIDTH, LETTER_HEIGHT, LETTER_WIDTH_LANDSCAPE, LETTER_HEIGHT_LANDSCAPE

class PDFResizer:
    # Usar las constantes importadas del módulo compartido
    
    def __init__(self):
        pass
    
    def resize_pdf(self, input_pdf, output_pdf, centrar=False, progress_callback=None):
        """
        Redimensionar PDF a tamaño carta, preservando la orientación.
        
        Args:
            input_pdf (str): Ruta al archivo PDF de entrada
            output_pdf (str): Ruta donde se guardará el PDF redimensionado
            centrar (bool): Si es True, centra el contenido en la página
            progress_callback (callable, optional): Función para reportar el progreso
                Debe aceptar dos parámetros: página actual y total de páginas
                
        Returns:
            bool: True si el proceso fue exitoso, False en caso contrario
        """
        doc = None
        new_doc_final = None
        try:
            doc = fitz.open(input_pdf)
            # Utilizar el módulo compartido para procesar el PDF
            # La función process_pdf ya verifica si el documento tiene páginas
            new_doc_final = process_pdf(doc, centrar, progress_callback)
            
            # Guardar el documento final con las páginas redimensionadas
            new_doc_final.save(output_pdf)
            print(f"PDF redimensionado exitosamente a tamaño carta (preservando orientación): {output_pdf}")
            return True
        except ValueError as e:
            print(f"Error: {e}")
            return False
        except Exception as e:
            print(f"Error procesando PDF: {e}")
            return False
        finally:
            # Cerrar los documentos si fueron abiertos
            if doc:
                doc.close()
            if new_doc_final:
                new_doc_final.close()