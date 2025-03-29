import os
import sys
import fitz
import logging
# Importar el módulo compartido para el procesamiento de PDF
from .pdf_resize_algorithm import process_pdf, LETTER_WIDTH, LETTER_HEIGHT, LETTER_WIDTH_LANDSCAPE, LETTER_HEIGHT_LANDSCAPE

# Configurar logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

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
            # Verificar que el archivo existe
            if not os.path.exists(input_pdf):
                raise FileNotFoundError(f"El archivo PDF no existe: {input_pdf}")
            
            # Verificar que el archivo es un PDF válido
            if not input_pdf.lower().endswith('.pdf'):
                raise ValueError(f"El archivo no es un PDF: {input_pdf}")
            
            try:
                doc = fitz.open(input_pdf)
            except RuntimeError as e:
                raise ValueError(f"Error al abrir el PDF - el archivo podría estar corrupto o no ser un PDF válido: {str(e)}")
            
            # Verificar que el documento tiene páginas
            if len(doc) == 0:
                raise ValueError("El documento PDF está vacío (no tiene páginas)")
            
            # Utilizar el módulo compartido para procesar el PDF
            new_doc_final = process_pdf(doc, centrar, progress_callback)
            
            # Guardar el documento final con las páginas redimensionadas
            new_doc_final.save(output_pdf)
            logger.info(f"PDF redimensionado exitosamente a tamaño carta: {output_pdf}")
            return True
            
        except FileNotFoundError as e:
            logger.error(f"Error de archivo no encontrado: {e}")
            return False
        except ValueError as e:
            logger.error(f"Error de validación: {e}")
            return False
        except Exception as e:
            logger.error(f"Error inesperado procesando PDF: {str(e)}", exc_info=True)
            return False
        finally:
            # Cerrar los documentos si fueron abiertos
            if doc:
                try:
                    doc.close()
                except:
                    pass
            if new_doc_final:
                try:
                    new_doc_final.close()
                except:
                    pass