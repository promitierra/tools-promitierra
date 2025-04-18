import pytest
import fitz
import os
from resize_pdf import LETTER_WIDTH, LETTER_HEIGHT, LETTER_WIDTH_LANDSCAPE, LETTER_HEIGHT_LANDSCAPE

@pytest.fixture
def sample_pdfs(tmp_path):
    # Generar PDF de prueba A4 vertical
    a4_path = tmp_path / "a4.pdf"
    doc = fitz.open()
    page = doc.new_page(width=595, height=842)  # Tamaño A4
    doc.save(a4_path)
    doc.close()
    
    # Generar PDF horizontal
    landscape_path = tmp_path / "landscape.pdf"
    doc = fitz.open()
    page = doc.new_page(width=842, height=595)
    doc.save(landscape_path)
    doc.close()
    
    # Generar PDF con múltiples páginas
    multi_path = tmp_path / "multi_page.pdf"
    doc = fitz.open()
    doc.new_page(width=595, height=842)  # A4
    doc.new_page(width=842, height=595)  # Horizontal
    doc.save(multi_path)
    doc.close()
    
    return [a4_path, landscape_path, multi_path]

def test_resize_dimensions(sample_pdfs):
    for pdf_path in sample_pdfs:
        output_path = pdf_path.parent / "resized.pdf"
        
        # Ejecutar el script de redimensionado
        result = os.system(f"python resize_pdf.py {pdf_path} {output_path}")
        assert result == 0, "El script falló al ejecutarse"
        
        # Verificar que el archivo de salida existe
        assert os.path.exists(output_path), f"El archivo de salida {output_path} no fue creado"
        
        # Verificar resultado
        doc_original = fitz.open(pdf_path)
        doc_resized = fitz.open(output_path)
        
        assert len(doc_original) == len(doc_resized), "El número de páginas debe ser igual"
        
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
        
def test_centered_content(tmp_path):
    # Crear PDF de prueba con contenido en esquina superior izquierda
    test_path = tmp_path / "test_centrado.pdf"
    doc = fitz.open()
    page = doc.new_page(width=595, height=842)
    
    # Dibujar un rectángulo pequeño en la esquina superior izquierda
    rect = fitz.Rect(0, 0, 100, 100)
    page.draw_rect(rect, color=(1, 0, 0), width=2)
    doc.save(test_path)
    doc.close()
    
    # Redimensionar con centrado
    output_path = tmp_path / "centrado_output.pdf"
    result = os.system(f"python resize_pdf.py {test_path} {output_path} centrar")
    assert result == 0, "Error al ejecutar con opción de centrado"
    
    # Verificar posición del contenido
    doc_resized = fitz.open(output_path)
    page_resized = doc_resized[0]
    
    # El rectángulo debería estar centrado
    scale = min(LETTER_WIDTH/595, LETTER_HEIGHT/842)
    page_width_scaled = 595 * scale
    page_height_scaled = 842 * scale
    
    # Calcular desplazamiento para centrar la página escalada
    expected_x = (LETTER_WIDTH - page_width_scaled) / 2
    expected_y = (LETTER_HEIGHT - page_height_scaled) / 2
    
    # Calcular dimensiones del contenido escalado
    expected_width = 100 * scale
    expected_height = 100 * scale
    
    # Verificar que el contenido se movió desde la esquina
    for annot in page_resized.get_drawings():
        expected_rect = fitz.Rect(expected_x, expected_y, expected_x + expected_width, expected_y + expected_height)
        if not annot['rect'].intersects(expected_rect):
            assert False, f"El contenido no se centró. Esperado: {expected_rect}, Obtenido: {annot['rect']}"
    
    doc_resized.close()

def test_centered_content_landscape(tmp_path):
    # Crear PDF de prueba horizontal con contenido en esquina superior izquierda
    test_path = tmp_path / "test_centrado_horizontal.pdf"
    doc = fitz.open()
    page = doc.new_page(width=842, height=595)  # A4 horizontal
    
    # Dibujar un rectángulo pequeño en la esquina superior izquierda
    rect = fitz.Rect(0, 0, 100, 100)
    page.draw_rect(rect, color=(0, 0, 1), width=2)
    doc.save(test_path)
    doc.close()
    
    # Redimensionar con centrado
    output_path = tmp_path / "centrado_horizontal_output.pdf"
    result = os.system(f"python resize_pdf.py {test_path} {output_path} centrar")
    assert result == 0, "Error al ejecutar con opción de centrado en documento horizontal"
    
    # Verificar posición del contenido
    doc_resized = fitz.open(output_path)
    page_resized = doc_resized[0]
    
    # Verificar que la página resultante tiene orientación horizontal
    assert page_resized.rect.width == LETTER_WIDTH_LANDSCAPE
    assert page_resized.rect.height == LETTER_HEIGHT_LANDSCAPE
    
    # El rectángulo debería estar centrado
    scale = min(LETTER_WIDTH_LANDSCAPE/842, LETTER_HEIGHT_LANDSCAPE/595)
    page_width_scaled = 842 * scale
    page_height_scaled = 595 * scale
    
    # Calcular desplazamiento para centrar la página escalada
    expected_x = (LETTER_WIDTH_LANDSCAPE - page_width_scaled) / 2
    expected_y = (LETTER_HEIGHT_LANDSCAPE - page_height_scaled) / 2
    
    # Calcular dimensiones del contenido escalado
    expected_width = 100 * scale
    expected_height = 100 * scale
    
    # Verificar que el contenido se movió desde la esquina
    for annot in page_resized.get_drawings():
        expected_rect = fitz.Rect(expected_x, expected_y, expected_x + expected_width, expected_y + expected_height)
        if not annot['rect'].intersects(expected_rect):
            assert False, f"El contenido no se centró en documento horizontal. Esperado: {expected_rect}, Obtenido: {annot['rect']}"
    
    doc_resized.close()

def test_multi_page_centering(tmp_path):
    # Crear PDF de prueba con múltiples páginas y diferentes orientaciones
    test_path = tmp_path / "test_multi_centrado.pdf"
    doc = fitz.open()
    
    # Página 1: vertical con rectángulo en esquina superior izquierda
    page1 = doc.new_page(width=595, height=842)  # A4 vertical
    rect1 = fitz.Rect(0, 0, 100, 100)
    page1.draw_rect(rect1, color=(1, 0, 0), width=2)
    
    # Página 2: horizontal con rectángulo en esquina inferior derecha
    page2 = doc.new_page(width=842, height=595)  # A4 horizontal
    rect2 = fitz.Rect(742, 495, 842, 595)
    page2.draw_rect(rect2, color=(0, 1, 0), width=2)
    
    doc.save(test_path)
    doc.close()
    
    # Redimensionar con centrado
    output_path = tmp_path / "multi_centrado_output.pdf"
    result = os.system(f"python resize_pdf.py {test_path} {output_path} centrar")
    assert result == 0, "Error al ejecutar con opción de centrado en documento multipágina"
    
    # Verificar que el archivo de salida existe
    assert os.path.exists(output_path), f"El archivo de salida {output_path} no fue creado"
    
    # Verificar resultado
    doc_resized = fitz.open(output_path)
    
    # Verificar que se mantiene el número de páginas
    assert len(doc_resized) == 2, "El número de páginas debe ser igual al original"
    
    # Verificar página 1 (vertical)
    page1_resized = doc_resized[0]
    assert page1_resized.rect.width == LETTER_WIDTH
    assert page1_resized.rect.height == LETTER_HEIGHT
    
    # Verificar página 2 (horizontal)
    page2_resized = doc_resized[1]
    assert page2_resized.rect.width == LETTER_WIDTH_LANDSCAPE
    assert page2_resized.rect.height == LETTER_HEIGHT_LANDSCAPE
    
    doc_resized.close()

def test_error_handling(tmp_path):
    # Archivo corrupto
    corrupt_path = tmp_path / "corrupt.pdf"
    with open(corrupt_path, "w") as f:
        f.write("esto no es un PDF")
    
    # Ejecutar y verificar código de salida
    result = os.system(f"python resize_pdf.py {corrupt_path} output.pdf")
    assert result != 0, "Se esperaba un código de error para archivo corrupto"
    
    # Archivo inexistente
    result = os.system("python resize_pdf.py no_existo.pdf output.pdf")
    assert result != 0, "Se esperaba un código de error para archivo inexistente"