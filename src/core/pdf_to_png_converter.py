"""Módulo para convertir archivos PDF a imágenes PNG."""
import os
import fitz  # PyMuPDF
from PIL import Image
import io
import logging

class PDFToPNGConverter:
    """Clase para convertir archivos PDF a imágenes PNG."""
    
    def __init__(self):
        """Inicializa el conversor de PDF a PNG."""
        pass
    
    def convert_pdf_to_png(self, pdf_path):
        """Extrae imágenes incrustadas de un archivo PDF y las guarda como PNG.
        Procesa todas las páginas y extrae las imágenes en el orden en que aparecen en el documento.
        
        Args:
            pdf_path (str): Ruta al archivo PDF
            
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
                return False
            
            # Collect all images from all pages
            all_images = []
            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]
                # Extract images from the page
                page_images = page.get_images(full=True)
                # Add page number information to each image
                for img in page_images:
                    all_images.append((page_num, img))
            
            # If no images found in any page, fall back to converting the first page
            if not all_images:
                logging.info(f"No se encontraron imágenes incrustadas en {pdf_path}, recurriendo a la conversión de página")
                
                # Check if PNG already exists
                png_path = png_base_path + '.png'
                if os.path.exists(png_path):
                    logging.info(f"El archivo PNG ya existe: {png_path}")
                    return True
                    
                # Use a high resolution for better quality
                target_dpi = 300
                dpi_scale = target_dpi / 72
                matrix = fitz.Matrix(dpi_scale, dpi_scale)
                
                # Get the first page
                page = pdf_document[0]
                
                # Validación de resolución mínima
                if (page.rect.width * dpi_scale < 150) or (page.rect.height * dpi_scale < 150):
                    logging.error(f"Resolución insuficiente en {pdf_path}: {page.rect.width * dpi_scale:.0f}x{page.rect.height * dpi_scale:.0f}px")
                    return False
                    
                pixmap = page.get_pixmap(matrix=matrix)
                
                # Convert pixmap to PIL Image
                img_data = pixmap.samples
                img = Image.frombytes("RGB", [pixmap.width, pixmap.height], img_data)
                
                # Save the image as PNG
                img.save(png_path, "PNG", dpi=(target_dpi, target_dpi))
                
                # Verificación de integridad del archivo
                if os.path.getsize(png_path) == 0:
                    logging.error(f"Archivo PNG vacío: {png_path}")
                    os.remove(png_path)
                    return False
                    
                try:
                    with Image.open(png_path) as img_check:
                        img_check.verify()
                except Exception as e:
                    logging.error(f"PNG corrupto: {png_path} - {str(e)}")
                    os.remove(png_path)
                    return False
                    
                logging.info(f"Conversión de página exitosa: {pdf_path}")
                return True
            
            # Process each image found in the PDF
            successful = False
            for i, (page_num, img_info) in enumerate(all_images):
                # Get the XREF of the image
                xref = img_info[0]
                
                # Extract the image
                base_img = pdf_document.extract_image(xref)
                image_bytes = base_img["image"]
                image_ext = base_img["ext"]
                
                # Generate output filename
                if len(all_images) == 1:
                    # If there's only one image, use the original filename
                    png_path = png_base_path + '.png'
                elif len(all_images) <= 2:
                    # If there are exactly two images, still use the original filename with an index
                    png_path = f"{png_base_path}_{i+1}.png"
                else:
                    # If there are more than two images, add page number and index for proper sequencing
                    # Format: filename_pXX_imgYY.png (where XX is page number and YY is image index)
                    png_path = f"{png_base_path}_p{page_num+1}_img{i+1}.png"
                
                # Check if PNG already exists
                if os.path.exists(png_path):
                    logging.info(f"El archivo PNG ya existe: {png_path}")
                    successful = True
                    continue
                
                # Convert image bytes to PIL Image
                try:
                    img = Image.open(io.BytesIO(image_bytes))
                    
                    # Convert to RGB if needed
                    if img.mode != "RGB":
                        img = img.convert("RGB")
                    
                    # Save as PNG
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
                        
                    logging.info(f"Extracción de imagen exitosa: {png_path}")
                    successful = True
                except Exception as e:
                    logging.error(f"Error al procesar imagen {i+1} de {pdf_path}: {str(e)}")
                    continue
            
            return successful
        except Exception as e:
            logging.error(f"Error en conversión - {pdf_path}", exc_info=True)
            return False
        finally:
            if 'pdf_document' in locals():
                pdf_document.close()
    
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
    
    def convert_directory(self, directory_path):
        """Convierte todos los archivos PDF en un directorio a PNG.
        
        Args:
            directory_path (str): Ruta al directorio con archivos PDF
            
        Returns:
            tuple: (exitosos, fallidos) número de archivos convertidos exitosamente y fallidos
        """
        pdf_files = self.find_pdf_files(directory_path)
        successful = 0
        failed = 0
        
        for pdf_path in pdf_files:
            if self.convert_pdf_to_png(pdf_path):
                successful += 1
            else:
                failed += 1
        
        return successful, failed