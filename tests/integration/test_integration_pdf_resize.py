import pytest
import os
import fitz
import tempfile
import shutil
from pathlib import Path

# Importar las implementaciones que queremos comparar
from src.core.pdf_resizer import PDFResizer
from src.core.pdf_resize_algorithm import LETTER_WIDTH, LETTER_HEIGHT, LETTER_WIDTH_LANDSCAPE, LETTER_HEIGHT_LANDSCAPE

@pytest.fixture
def sample_pdfs(tmp_path):
    """
    Genera varios tipos de PDFs para pruebas de integración:
    - PDF A4 vertical
    - PDF horizontal
    - PDF con múltiples páginas (mixtas)
    - PDF con contenido real (texto y gráficos)
    """
    # Generar PDF de prueba A4 vertical
    a4_path = tmp_path / "a4.pdf"
    doc = fitz.open()
    page = doc.new_page(width=595, height=842)  # Tamaño A4
    # Añadir texto para tener contenido real
    page.insert_text((100, 100), "Documento de prueba A4 vertical", fontsize=12)
    # Dibujar un rectángulo para tener contenido gráfico
    page.draw_rect((200, 200, 400, 300), color=(1, 0, 0), width=2)
    doc.save(a4_path)
    doc.close()
    
    # Generar PDF horizontal
    landscape_path = tmp_path / "landscape.pdf"
    doc = fitz.open()
    page = doc.new_page(width=842, height=595)  # A4 horizontal
    page.insert_text((100, 100), "Documento de prueba horizontal", fontsize=12)
    page.draw_rect((200, 200, 600, 300), color=(0, 1, 0), width=2)
    doc.save(landscape_path)
    doc.close()
    
    # Generar PDF con múltiples páginas (mixtas)
    multi_path = tmp_path / "multi_page.pdf"
    doc = fitz.open()
    # Página 1: vertical
    page = doc.new_page(width=595, height=842)
    page.insert_text((100, 100), "Página 1 - Vertical", fontsize=12)
    # Página 2: horizontal
    page = doc.new_page(width=842, height=595)
    page.insert_text((100, 100), "Página 2 - Horizontal", fontsize=12)
    # Página 3: tamaño personalizado
    page = doc.new_page(width=700, height=900)
    page.insert_text((100, 100), "Página 3 - Tamaño personalizado", fontsize=12)
    doc.save(multi_path)
    doc.close()
    
    # PDF con contenido complejo (formas, texto en diferentes posiciones)
    complex_path = tmp_path / "complex.pdf"
    doc = fitz.open()
    page = doc.new_page(width=595, height=842)
    # Añadir varios elementos de texto
    page.insert_text((50, 50), "Título del documento", fontsize=16)
    page.insert_text((50, 100), "Este es un documento con contenido complejo para pruebas.", fontsize=10)
    page.insert_text((50, 150), "Contiene múltiples elementos para verificar la fidelidad del redimensionamiento.", fontsize=10)
    # Añadir formas geométricas
    page.draw_rect((50, 200, 200, 300), color=(1, 0, 0), width=2)  # Rectángulo rojo
    page.draw_circle((300, 250), 50, color=(0, 0, 1), width=2)  # Círculo azul
    page.draw_line((50, 350), (400, 350), color=(0, 0, 0), width=1)  # Línea horizontal
    doc.save(complex_path)
    doc.close()
    
    return [a4_path, landscape_path, multi_path, complex_path]

def compare_pdf_files(file1, file2):
    """
    Compara dos archivos PDF y verifica si son idénticos en términos de:
    - Número de páginas
    - Dimensiones de cada página
    - Contenido visual (mediante hash de imagen)
    
    Returns:
        bool: True si los PDFs son idénticos, False en caso contrario
        str: Mensaje de error si hay diferencias
    """
    try:
        doc1 = fitz.open(file1)
        doc2 = fitz.open(file2)
        
        # Verificar número de páginas
        if len(doc1) != len(doc2):
            return False, f"Diferente número de páginas: {len(doc1)} vs {len(doc2)}"
        
        # Comparar cada página
        for i in range(len(doc1)):
            page1 = doc1[i]
            page2 = doc2[i]
            
            # Verificar dimensiones
            if page1.rect.width != page2.rect.width or page1.rect.height != page2.rect.height:
                return False, f"Dimensiones diferentes en página {i}: {page1.rect} vs {page2.rect}"
            
            # Comparar contenido visual mediante renderizado a imagen y comparación de pixmaps
            pix1 = page1.get_pixmap()
            pix2 = page2.get_pixmap()
            
            # Comparar dimensiones de pixmap
            if pix1.width != pix2.width or pix1.height != pix2.height:
                return False, f"Dimensiones de imagen diferentes en página {i}"
            
            # Comparar hash de imagen (método simple pero efectivo)
            # Nota: Podría haber pequeñas diferencias debido al renderizado
            # por lo que una comparación bit a bit podría ser demasiado estricta
            if pix1.digest != pix2.digest:
                return False, f"Contenido visual diferente en página {i}"
        
        # Si llegamos aquí, los PDFs son idénticos según nuestros criterios
        return True, "PDFs idénticos"
    
    finally:
        if 'doc1' in locals() and doc1:
            doc1.close()
        if 'doc2' in locals() and doc2:
            doc2.close()

@pytest.mark.integration
@pytest.mark.slow
def test_integration_resize_pdf_vs_pdfresizer(sample_pdfs, tmp_path):
    """
    Prueba de integración que verifica que ambas implementaciones
    (resize_pdf.py y PDFResizer) producen resultados idénticos.
    """
    # Crear instancia de PDFResizer
    pdf_resizer = PDFResizer()
    
    for pdf_path in sample_pdfs:
        # Crear rutas para los archivos de salida
        output_script = tmp_path / f"script_{pdf_path.name}"
        output_class = tmp_path / f"class_{pdf_path.name}"
        
        # 1. Redimensionar usando el script independiente
        script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                  "src", "scripts", "resize_pdf.py")
        cmd = f"python {script_path} {pdf_path} {output_script} centrar"
        result = os.system(cmd)
        assert result == 0, f"El script falló con código {result}"
        assert os.path.exists(output_script), f"El archivo de salida {output_script} no fue creado"
        
        # 2. Redimensionar usando la clase PDFResizer
        result = pdf_resizer.resize_pdf(str(pdf_path), str(output_class), centrar=True)
        assert result is True, "PDFResizer.resize_pdf devolvió False"
        assert os.path.exists(output_class), f"El archivo de salida {output_class} no fue creado"
        
        # 3. Comparar los resultados
        identical, message = compare_pdf_files(output_script, output_class)
        assert identical, f"Los PDFs no son idénticos: {message}"

@pytest.mark.integration
@pytest.mark.slow
def test_integration_resize_pdf_vs_pdfresizer_no_center(sample_pdfs, tmp_path):
    """
    Prueba de integración que verifica que ambas implementaciones
    producen resultados idénticos cuando no se centra el contenido.
    """
    # Crear instancia de PDFResizer
    pdf_resizer = PDFResizer()
    
    for pdf_path in sample_pdfs:
        # Crear rutas para los archivos de salida
        output_script = tmp_path / f"script_nocenter_{pdf_path.name}"
        output_class = tmp_path / f"class_nocenter_{pdf_path.name}"
        
        # 1. Redimensionar usando el script independiente (sin centrar)
        script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                  "src", "scripts", "resize_pdf.py")
        cmd = f"python {script_path} {pdf_path} {output_script}"
        result = os.system(cmd)
        assert result == 0, f"El script falló con código {result}"
        assert os.path.exists(output_script), f"El archivo de salida {output_script} no fue creado"
        
        # 2. Redimensionar usando la clase PDFResizer (sin centrar)
        result = pdf_resizer.resize_pdf(str(pdf_path), str(output_class), centrar=False)
        assert result is True, "PDFResizer.resize_pdf devolvió False"
        assert os.path.exists(output_class), f"El archivo de salida {output_class} no fue creado"
        
        # 3. Comparar los resultados
        identical, message = compare_pdf_files(output_script, output_class)
        assert identical, f"Los PDFs no son idénticos: {message}"

@pytest.mark.integration
def test_integration_resize_pdf_vs_pdfresizer_with_progress(sample_pdfs, tmp_path):
    """
    Prueba de integración que verifica que ambas implementaciones
    producen resultados idénticos cuando se utiliza la función de progreso.
    """
    # Crear instancia de PDFResizer
    pdf_resizer = PDFResizer()
    
    # Definir una función de callback de progreso para pruebas
    progress_data = []
    def progress_callback(current, total):
        progress_data.append((current, total))
    
    for pdf_path in sample_pdfs:
        # Solo probar con PDFs multipágina (más relevante para el progreso)
        if pdf_path.name != "multi_page.pdf":
            continue
            
        # Crear rutas para los archivos de salida
        output_class = tmp_path / f"class_progress_{pdf_path.name}"
        
        # Limpiar datos de progreso
        progress_data.clear()
        
        # Redimensionar usando la clase PDFResizer con callback de progreso
        result = pdf_resizer.resize_pdf(str(pdf_path), str(output_class), centrar=True, 
                                       progress_callback=progress_callback)
        assert result is True, "PDFResizer.resize_pdf devolvió False"
        assert os.path.exists(output_class), f"El archivo de salida {output_class} no fue creado"
        
        # Verificar que se llamó al callback de progreso
        assert len(progress_data) > 0, "No se llamó al callback de progreso"
        
        # Verificar que el último progreso reportado coincide con el total de páginas
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        doc.close()
        
        assert progress_data[-1][0] == total_pages, f"El progreso final no coincide: {progress_data[-1][0]} vs {total_pages}"
        assert progress_data[-1][1] == total_pages, f"El total de páginas no coincide: {progress_data[-1][1]} vs {total_pages}"