"""Módulo para convertir archivos PDF a imágenes PNG."""
import os
import fitz  # PyMuPDF
from PIL import Image
import io
import logging
from pathlib import Path

class PDFToPNGConverter:
    """Clase para convertir archivos PDF a imágenes PNG."""
    
    def __init__(self):
        """Inicializa el conversor de PDF a PNG."""
        self.cancelar = False
    
    def convert_pdf_to_png(self, pdf_path, callbacks=None):
        """Extrae imágenes incrustadas de un archivo PDF y las guarda como PNG.
        Procesa todas las páginas y extrae las imágenes en el orden en que aparecen en el documento.
        
        Args:
            pdf_path (str): Ruta al archivo PDF
            callbacks (object, optional): Objeto con métodos de callback para reportar progreso
            
        Returns:
            bool: True si la extracción fue exitosa, False en caso contrario
        """
        try:
            # Get the output path by replacing the extension
            png_base_path = os.path.splitext(pdf_path)[0]
            
            # Open the PDF file
            pdf_document = fitz.open(pdf_path)
            
            # Check if PDF has pages
            if pdf_document.page_count == 0:
                logging.error(f"El PDF no tiene páginas: {pdf_path}")
                if callbacks and hasattr(callbacks, 'on_file_error'):
                    callbacks.on_file_error(pdf_path, "El PDF no tiene páginas")
                return False
            
            # Reportar inicio de procesamiento
            if callbacks and hasattr(callbacks, 'on_processing_file'):
                callbacks.on_processing_file(Path(pdf_path).name)
            
            # Collect all images from all pages
            all_images = []
            for page_num in range(pdf_document.page_count):
                if self.cancelar:
                    return False
                
                page = pdf_document[page_num]
                # Extract images from the page
                page_images = page.get_images(full=True)
                # Add page number information to each image
                for img in page_images:
                    all_images.append((page_num, img))
            
            # Reportar imágenes encontradas
            if callbacks and hasattr(callbacks, 'on_images_found'):
                callbacks.on_images_found(len(all_images))
            
            if not all_images:
                # Si no hay imágenes, extraer la página completa como imagen
                logging.info(f"No se encontraron imágenes incrustadas en {pdf_path}, extrayendo páginas como imágenes")
                return self.extract_pages_as_images(pdf_path, pdf_document, callbacks)
            
            # Process each image
            successful = False
            for i, (page_num, img_info) in enumerate(all_images):
                if self.cancelar:
                    return False
                
                # Reportar progreso
                if callbacks and hasattr(callbacks, 'on_progress'):
                    progreso = (i + 1) / len(all_images)
                    callbacks.on_progress(progreso)
                
                try:
                    # Get the image reference
                    xref = img_info[0]
                    
                    # Determine image type (png, jpeg, etc.)
                    base_image = pdf_document.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    
                    # Skip very small images (likely icons or decorations)
                    if len(image_bytes) < 1000:  # Skip images < 1KB
                        continue
                    
                    # Generate a unique filename with page number and index
                    png_path = f"{png_base_path}_p{page_num+1}_img{i+1}.png"
                    
                    # Convert image bytes to PIL Image
                    try:
                        img = Image.open(io.BytesIO(image_bytes))
                        
                        # Convert to RGB if needed
                        if img.mode != "RGB":
                            img = img.convert("RGB")
                        
                        # Save as PNG with high quality
                        img.save(png_path, "PNG")
                        
                        # Verificación de integridad del archivo
                        if os.path.getsize(png_path) == 0:
                            logging.error(f"Archivo PNG vacío: {png_path}")
                            os.remove(png_path)
                            continue
                            
                        try:
                            with Image.open(png_path) as img_check:
                                img_check.verify()
                        except Exception as e:
                            logging.error(f"PNG corrupto: {png_path} - {str(e)}")
                            os.remove(png_path)
                            continue
                            
                        # Reportar imagen convertida
                        if callbacks and hasattr(callbacks, 'on_file_converted'):
                            callbacks.on_file_converted(os.path.basename(png_path))
                            
                        logging.info(f"Extracción de imagen exitosa: {png_path}")
                        successful = True
                    except Exception as e:
                        if callbacks and hasattr(callbacks, 'on_file_error'):
                            callbacks.on_file_error(f"Imagen {i+1}", str(e))
                        logging.error(f"Error al procesar imagen {i+1} de {pdf_path}: {str(e)}")
                        continue
                except Exception as e:
                    logging.error(f"Error extrayendo imagen {i+1} de {pdf_path}: {str(e)}")
                    continue
            
            return successful
        except Exception as e:
            if callbacks and hasattr(callbacks, 'on_file_error'):
                callbacks.on_file_error(pdf_path, str(e))
            logging.error(f"Error en conversión - {pdf_path}", exc_info=True)
            return False
        finally:
            if 'pdf_document' in locals():
                pdf_document.close()
    
    def extract_pages_as_images(self, pdf_path, pdf_document, callbacks=None):
        """Extrae cada página del PDF como una imagen PNG.
        
        Args:
            pdf_path (str): Ruta al archivo PDF
            pdf_document: Documento PDF abierto
            callbacks (object, optional): Objeto con métodos de callback para reportar progreso
            
        Returns:
            bool: True si la extracción fue exitosa, False en caso contrario
        """
        png_base_path = os.path.splitext(pdf_path)[0]
        successful = False
        
        for page_num in range(pdf_document.page_count):
            if self.cancelar:
                return False
                
            try:
                # Reportar progreso
                if callbacks and hasattr(callbacks, 'on_progress'):
                    progreso = (page_num + 1) / pdf_document.page_count
                    callbacks.on_progress(progreso)
                
                page = pdf_document[page_num]
                
                # Renderizar página a imagen con alta resolución
                pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))
                
                # Generar nombre único para la imagen
                png_path = f"{png_base_path}_page{page_num+1}.png"
                
                # Guardar imagen
                pix.save(png_path)
                
                # Reportar página convertida
                if callbacks and hasattr(callbacks, 'on_file_converted'):
                    callbacks.on_file_converted(os.path.basename(png_path))
                
                logging.info(f"Página extraída como imagen: {png_path}")
                successful = True
            except Exception as e:
                if callbacks and hasattr(callbacks, 'on_file_error'):
                    callbacks.on_file_error(f"Página {page_num+1}", str(e))
                logging.error(f"Error al extraer página {page_num+1} de {pdf_path}: {str(e)}")
        
        return successful
    
    def find_pdf_files(self, root_dir):
        """Encuentra todos los archivos PDF en el directorio dado y sus subdirectorios.
        
        Args:
            root_dir (str): Directorio raíz para buscar
            
        Returns:
            list: Lista de rutas a archivos PDF
        """
        pdf_files = []
        
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename.lower().endswith('.pdf'):
                    pdf_files.append(os.path.join(dirpath, filename))
        
        return pdf_files
    
    def convert_directory(self, directory_path, callbacks=None):
        """Convierte todos los archivos PDF en un directorio a PNG.
        
        Args:
            directory_path (str): Ruta al directorio con archivos PDF
            callbacks (object, optional): Objeto con métodos de callback para reportar progreso
            
        Returns:
            tuple: (exitosos, fallidos) número de archivos convertidos exitosamente y fallidos
        """
        self.cancelar = False
        pdf_files = self.find_pdf_files(directory_path)
        
        if callbacks and hasattr(callbacks, 'on_files_found'):
            callbacks.on_files_found(len(pdf_files))
        
        successful = 0
        failed = 0
        
        for i, pdf_path in enumerate(pdf_files):
            if self.cancelar:
                break
                
            # Reportar progreso global
            if callbacks and hasattr(callbacks, 'on_global_progress'):
                progreso_global = (i + 1) / len(pdf_files)
                callbacks.on_global_progress(progreso_global)
            
            if self.convert_pdf_to_png(pdf_path, callbacks):
                successful += 1
            else:
                failed += 1
        
        return successful, failed
    
    def cancelar_proceso(self):
        """Cancela el proceso actual de conversión"""
        self.cancelar = True