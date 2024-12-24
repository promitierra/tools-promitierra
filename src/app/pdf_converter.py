import os
import threading
from PIL import Image
import zipfile
from datetime import datetime
import tempfile
import shutil
import multiprocessing
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from ..utils.helpers import agregar_detalle, actualizar_progreso

class PDFConverter:
    # Extensiones de imagen soportadas
    EXTENSIONES_SOPORTADAS = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp', '.gif', '.heic', '.heif'}
    
    def __init__(self):
        self.procesando = False
        self.directorio_salida = None
        self.cancelar = False
        # Usar el número de CPUs disponibles o un máximo de 4
        self.max_workers = min(multiprocessing.cpu_count(), 4)
        
    def es_imagen_valida(self, ruta):
        """Verifica si un archivo es una imagen válida basado en su extensión"""
        return Path(ruta).suffix.lower() in self.EXTENSIONES_SOPORTADAS
    
    def encontrar_imagenes(self, directorio, patron="*"):
        """
        Encuentra todas las imágenes en el directorio y subdirectorios usando pathlib.
        
        Args:
            directorio (str): Ruta al directorio a buscar
            patron (str): Patrón para filtrar archivos (por defecto "*")
            
        Returns:
            list: Lista de rutas de imágenes encontradas
        """
        ruta = Path(directorio)
        imagenes = set()  # Usar set para evitar duplicados
        
        # Buscar todos los archivos recursivamente
        for archivo in ruta.rglob("*"):
            if archivo.is_file() and archivo.suffix.lower() in self.EXTENSIONES_SOPORTADAS:
                imagenes.add(archivo)
        
        # Convertir a lista y ordenar
        imagenes = sorted(imagenes)
        
        # Filtrar por patrón personalizado si es necesario
        if patron and patron != "*":
            from fnmatch import fnmatch
            imagenes = [
                img for img in imagenes 
                if fnmatch(img.name.lower(), patron.lower())
            ]
        
        return imagenes
    
    def convertir_imagen(self, ruta_imagen, directorio_destino):
        """Convierte una imagen a PDF"""
        try:
            nombre_archivo = Path(ruta_imagen).name
            nombre_base = Path(ruta_imagen).stem
            ruta_pdf = Path(directorio_destino) / f"{nombre_base}.pdf"
            
            # Crear directorios intermedios si no existen
            ruta_pdf.parent.mkdir(parents=True, exist_ok=True)
            
            # Abrir y convertir imagen
            with Image.open(ruta_imagen) as img:
                # Optimizar memoria para imágenes grandes
                if img.size[0] > 2000 or img.size[1] > 2000:
                    img.thumbnail((2000, 2000), Image.Resampling.LANCZOS)
                
                # Convertir a RGB si es necesario
                if img.mode in ('RGBA', 'LA', 'P', 'PA'):
                    img = img.convert('RGB')
                elif img.mode not in ('RGB', 'L'):
                    img = img.convert('RGB')
                
                # Guardar como PDF con compresión optimizada
                img.save(str(ruta_pdf), 'PDF', resolution=100.0, optimize=True)
            return True, nombre_archivo, None
        except Exception as e:
            return False, nombre_archivo, str(e)
    
    def procesar_carpeta(self, directorio, modo_comprimido, callbacks, patron="*"):
        """Procesa todas las imágenes en la carpeta usando un thread pool"""
        temp_dir = None
        try:
            self.procesando = True
            self.cancelar = False
            callbacks.on_start()
            
            # Crear directorio temporal si es modo comprimido
            if modo_comprimido:
                temp_dir = tempfile.mkdtemp()
            
            # Encontrar todas las imágenes usando pathlib
            imagenes = self.encontrar_imagenes(directorio, patron)
            
            if not imagenes:
                callbacks.on_no_images()
                return
            
            total_imagenes = len(imagenes)
            callbacks.on_images_found(total_imagenes)
            convertidas = 0
            errores = 0
            
            # Directorio de destino para PDFs
            directorio_destino = temp_dir if modo_comprimido else directorio
            
            # Procesar imágenes en paralelo
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                # Crear futuras para cada imagen
                futuros = {
                    executor.submit(self.convertir_imagen, str(img), directorio_destino): img 
                    for img in imagenes
                }
                
                # Procesar resultados conforme se completan
                for futuro in as_completed(futuros):
                    if self.cancelar:
                        break
                        
                    ruta_imagen = futuros[futuro]
                    try:
                        exito, nombre, error = futuro.result()
                        if exito:
                            convertidas += 1
                            callbacks.on_file_converted(nombre)
                        else:
                            errores += 1
                            callbacks.on_file_error(nombre, error)
                        
                        # Actualizar progreso
                        progreso = (convertidas + errores) / total_imagenes
                        callbacks.on_progress(progreso)
                        
                    except Exception as e:
                        errores += 1
                        nombre = Path(ruta_imagen).name
                        callbacks.on_file_error(nombre, str(e))
            
            # Si se canceló, limpiar y salir
            if self.cancelar:
                if temp_dir and os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
                return
            
            # Crear ZIP si es necesario
            if modo_comprimido and temp_dir:
                callbacks.on_creating_zip()
                zip_path = self.directorio_salida or Path(directorio) / f"PDFs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
                
                with zipfile.ZipFile(str(zip_path), 'w', zipfile.ZIP_DEFLATED) as zipf:
                    temp_path = Path(temp_dir)
                    for pdf in temp_path.rglob('*.pdf'):
                        arcname = pdf.relative_to(temp_path)
                        zipf.write(pdf, arcname)
                
                callbacks.on_zip_created(str(zip_path))
                
                # Limpiar directorio temporal
                shutil.rmtree(temp_dir)
            
            callbacks.on_complete(convertidas, total_imagenes, errores, modo_comprimido)
            
        except Exception as e:
            callbacks.on_error(str(e))
        finally:
            self.procesando = False
            callbacks.on_finish()
    
    def cancelar_proceso(self):
        """Cancela el proceso actual"""
        self.cancelar = True
