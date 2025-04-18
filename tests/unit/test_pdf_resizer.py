import pytest
import os
import fitz
import tempfile
from pathlib import Path

# Importar la clase que vamos a probar
from src.core.pdf_resizer import PDFResizer
from src.core.pdf_resize_algorithm import LETTER_WIDTH, LETTER_HEIGHT, LETTER_WIDTH_LANDSCAPE, LETTER_HEIGHT_LANDSCAPE

@pytest.fixture
def pdf_resizer():
    """Fixture que proporciona una instancia de PDFResizer para las pruebas."""
    return PDFResizer()

@pytest.fixture
def sample_pdfs(tmp_path):
    """Genera varios tipos de PDFs para pruebas unitarias:
    - PDF A4 vertical
    - PDF horizontal
    - PDF con múltiples páginas (mixtas)
    - PDF con contenido real (texto y gráficos)
    - PDF vacío para probar manejo de errores
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
    
    # Crear un PDF con una página en blanco para probar manejo de errores
    empty_path = tmp_path / "empty.pdf"
    doc = fitz.open()
    doc.new_page()  # Añadir una página en blanco
    doc.save(empty_path)
    doc.close()
    
    # Crear un archivo que no es PDF para probar manejo de errores
    not_pdf_path = tmp_path / "not_pdf.txt"
    with open(not_pdf_path, "w") as f:
        f.write("Este no es un archivo PDF")
    
    return {
        "a4": a4_path,
        "landscape": landscape_path,
        "multi": multi_path,
        "complex": complex_path,
        "empty": empty_path,
        "not_pdf": not_pdf_path
    }

# Pruebas para el método resize_pdf
def test_resize_pdf_success(pdf_resizer, sample_pdfs, tmp_path):
    """Prueba que el método resize_pdf funcione correctamente con un PDF válido."""
    # Probar con un PDF A4 vertical
    input_pdf = sample_pdfs["a4"]
    output_pdf = tmp_path / "a4_resized.pdf"
    
    # Ejecutar el método
    result = pdf_resizer.resize_pdf(input_pdf, output_pdf)
    
    # Verificar que el resultado sea exitoso
    assert result is True
    assert os.path.exists(output_pdf)
    
    # Verificar que el PDF resultante tenga el tamaño carta
    doc = fitz.open(output_pdf)
    assert len(doc) == 1  # Debe tener una página
    page = doc[0]
    assert page.rect.width == LETTER_WIDTH
    assert page.rect.height == LETTER_HEIGHT
    doc.close()

def test_resize_pdf_landscape(pdf_resizer, sample_pdfs, tmp_path):
    """Prueba que el método resize_pdf preserve la orientación horizontal."""
    # Probar con un PDF horizontal
    input_pdf = sample_pdfs["landscape"]
    output_pdf = tmp_path / "landscape_resized.pdf"
    
    # Ejecutar el método
    result = pdf_resizer.resize_pdf(input_pdf, output_pdf)
    
    # Verificar que el resultado sea exitoso
    assert result is True
    assert os.path.exists(output_pdf)
    
    # Verificar que el PDF resultante tenga el tamaño carta horizontal
    doc = fitz.open(output_pdf)
    assert len(doc) == 1  # Debe tener una página
    page = doc[0]
    assert page.rect.width == LETTER_WIDTH_LANDSCAPE
    assert page.rect.height == LETTER_HEIGHT_LANDSCAPE
    doc.close()

def test_resize_pdf_multi_page(pdf_resizer, sample_pdfs, tmp_path):
    """Prueba que el método resize_pdf funcione correctamente con un PDF de múltiples páginas."""
    # Probar con un PDF de múltiples páginas
    input_pdf = sample_pdfs["multi"]
    output_pdf = tmp_path / "multi_resized.pdf"
    
    # Ejecutar el método
    result = pdf_resizer.resize_pdf(input_pdf, output_pdf)
    
    # Verificar que el resultado sea exitoso
    assert result is True
    assert os.path.exists(output_pdf)
    
    # Verificar que el PDF resultante tenga el número correcto de páginas
    doc_original = fitz.open(input_pdf)
    doc_resized = fitz.open(output_pdf)
    assert len(doc_resized) == len(doc_original)
    
    # Verificar que cada página tenga el tamaño correcto según su orientación
    for i in range(len(doc_original)):
        pagina_original = doc_original[i]
        pagina_resized = doc_resized[i]
        
        # Determinar si la página original es horizontal o vertical
        es_horizontal = pagina_original.rect.width > pagina_original.rect.height
        
        # Verificar que se mantuvo la orientación
        if es_horizontal:
            assert pagina_resized.rect.width == LETTER_WIDTH_LANDSCAPE
            assert pagina_resized.rect.height == LETTER_HEIGHT_LANDSCAPE
        else:
            assert pagina_resized.rect.width == LETTER_WIDTH
            assert pagina_resized.rect.height == LETTER_HEIGHT
    
    doc_original.close()
    doc_resized.close()

def test_resize_pdf_with_centering(pdf_resizer, sample_pdfs, tmp_path):
    """Prueba que el método resize_pdf funcione correctamente con la opción de centrado."""
    # Probar con un PDF A4 vertical
    input_pdf = sample_pdfs["a4"]
    output_pdf = tmp_path / "a4_centered.pdf"
    
    # Ejecutar el método con centrado
    result = pdf_resizer.resize_pdf(input_pdf, output_pdf, centrar=True)
    
    # Verificar que el resultado sea exitoso
    assert result is True
    assert os.path.exists(output_pdf)
    
    # Verificar que el PDF resultante tenga el tamaño carta
    doc = fitz.open(output_pdf)
    assert len(doc) == 1  # Debe tener una página
    page = doc[0]
    assert page.rect.width == LETTER_WIDTH
    assert page.rect.height == LETTER_HEIGHT
    doc.close()

def test_resize_pdf_with_progress_callback(pdf_resizer, sample_pdfs, tmp_path):
    """Prueba que el método resize_pdf llame correctamente a la función de progreso."""
    # Probar con un PDF de múltiples páginas
    input_pdf = sample_pdfs["multi"]
    output_pdf = tmp_path / "multi_progress.pdf"
    
    # Crear una función de progreso de prueba
    progress_calls = []
    def progress_callback(current, total):
        progress_calls.append((current, total))
    
    # Ejecutar el método con la función de progreso
    result = pdf_resizer.resize_pdf(input_pdf, output_pdf, progress_callback=progress_callback)
    
    # Verificar que el resultado sea exitoso
    assert result is True
    assert os.path.exists(output_pdf)
    
    # Verificar que la función de progreso fue llamada correctamente
    doc = fitz.open(input_pdf)
    total_pages = len(doc)
    doc.close()
    
    # Debe haber al menos una llamada por página
    assert len(progress_calls) >= total_pages
    
    # La última llamada debe tener el total correcto
    assert progress_calls[-1][1] == total_pages
    
    # La última llamada debe indicar que se procesó la última página
    assert progress_calls[-1][0] == total_pages

def test_resize_pdf_empty_pdf(pdf_resizer, sample_pdfs, tmp_path):
    """Prueba que el método resize_pdf maneje correctamente un PDF vacío."""
    # Probar con un PDF vacío
    input_pdf = sample_pdfs["empty"]
    output_pdf = tmp_path / "empty_resized.pdf"
    
    # Crear un PDF vacío con al menos una página en blanco para evitar el error
    # "ValueError: cannot save with zero pages"
    doc = fitz.open()
    doc.new_page()  # Añadir una página en blanco
    doc.save(input_pdf)
    doc.close()
    
    # Ejecutar el método
    result = pdf_resizer.resize_pdf(input_pdf, output_pdf)
    
    # Verificar que el resultado sea exitoso (no debería fallar con un PDF con página en blanco)
    assert result is True
    assert os.path.exists(output_pdf)
    
    # Verificar que el PDF resultante tenga una página en blanco
    doc = fitz.open(output_pdf)
    assert len(doc) == 1  # Debe tener una página en blanco
    doc.close()

def test_resize_pdf_invalid_input(pdf_resizer, sample_pdfs, tmp_path):
    """Prueba que el método resize_pdf maneje correctamente un archivo de entrada inválido."""
    # Probar con un archivo que no es PDF
    input_pdf = sample_pdfs["not_pdf"]
    output_pdf = tmp_path / "not_pdf_resized.pdf"
    
    # Ejecutar el método
    result = pdf_resizer.resize_pdf(input_pdf, output_pdf)
    
    # Verificar que el resultado sea fallido
    assert result is False
    # El archivo de salida no debería existir o debería estar vacío
    assert not os.path.exists(output_pdf) or os.path.getsize(output_pdf) == 0

def test_resize_pdf_nonexistent_input(pdf_resizer, tmp_path):
    """Prueba que el método resize_pdf maneje correctamente un archivo de entrada inexistente."""
    # Ruta a un archivo que no existe
    input_pdf = tmp_path / "nonexistent.pdf"
    output_pdf = tmp_path / "nonexistent_resized.pdf"
    
    # Ejecutar el método
    result = pdf_resizer.resize_pdf(input_pdf, output_pdf)
    
    # Verificar que el resultado sea fallido
    assert result is False
    # El archivo de salida no debería existir
    assert not os.path.exists(output_pdf)

def test_resize_pdf_invalid_output_path(pdf_resizer, sample_pdfs, tmp_path):
    """Prueba que el método resize_pdf maneje correctamente una ruta de salida inválida."""
    # Probar con un PDF válido pero una ruta de salida inválida
    input_pdf = sample_pdfs["a4"]
    # Crear una ruta de salida inválida (directorio inexistente)
    output_pdf = tmp_path / "nonexistent_dir" / "output.pdf"
    
    # Ejecutar el método
    result = pdf_resizer.resize_pdf(input_pdf, output_pdf)
    
    # Verificar que el resultado sea fallido
    assert result is False
    # El archivo de salida no debería existir
    assert not os.path.exists(output_pdf)