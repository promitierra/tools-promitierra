"""
Pruebas de rendimiento para el módulo de redimensionamiento de PDF.
"""

import pytest
import fitz
import time
import tempfile
from pathlib import Path
from statistics import mean, stdev

from src.core.pdf_resize_algorithm import process_pdf, resize_pdf_page
from src.core.pdf_resizer import PDFResizer

@pytest.fixture
def large_pdf(tmp_path):
    """
    Genera un PDF grande para pruebas de rendimiento.
    """
    pdf_path = tmp_path / "large.pdf"
    doc = fitz.open()
    
    # Crear 50 páginas con contenido variado
    for i in range(50):
        # Alternar entre vertical y horizontal
        if i % 2 == 0:
            page = doc.new_page(width=595, height=842)  # A4 vertical
        else:
            page = doc.new_page(width=842, height=595)  # A4 horizontal
            
        # Añadir contenido variado
        page.insert_text((50, 50), f"Página de prueba {i+1}", fontsize=12)
        page.draw_rect((100, 100, 400, 200), color=(1, 0, 0), width=2)
        page.draw_circle((300, 300), 50, color=(0, 0, 1), width=2)
        
        # Añadir más texto para simular contenido real
        for j in range(10):
            y_pos = 250 + (j * 30)
            page.insert_text((50, y_pos), f"Línea de texto {j+1} con contenido de prueba", fontsize=10)
    
    doc.save(pdf_path)
    doc.close()
    return pdf_path

@pytest.mark.performance
def test_pdf_resize_performance(large_pdf, tmp_path):
    """
    Prueba el rendimiento del redimensionamiento de PDF.
    Mide:
    - Tiempo total de procesamiento
    - Tiempo promedio por página
    - Uso de memoria
    - Consistencia de rendimiento
    """
    num_iteraciones = 3
    tiempos_totales = []
    tiempos_por_pagina = []
    
    for i in range(num_iteraciones):
        output_path = tmp_path / f"output_{i}.pdf"
        
        # Medir tiempo de procesamiento
        inicio = time.time()
        
        # Abrir y procesar el documento
        doc = fitz.open(large_pdf)
        doc_procesado = process_pdf(doc, centrar=True)
        doc_procesado.save(output_path)
        
        # Cerrar documentos
        doc.close()
        doc_procesado.close()
        
        tiempo_total = time.time() - inicio
        tiempos_totales.append(tiempo_total)
        
        # Calcular tiempo por página
        doc = fitz.open(large_pdf)
        tiempo_por_pagina = tiempo_total / len(doc)
        tiempos_por_pagina.append(tiempo_por_pagina)
        doc.close()
    
    # Calcular estadísticas
    tiempo_promedio = mean(tiempos_totales)
    desviacion_std = stdev(tiempos_totales)
    tiempo_por_pagina_promedio = mean(tiempos_por_pagina)
    
    # Verificar rendimiento
    assert tiempo_promedio < 30.0, f"Tiempo promedio ({tiempo_promedio:.2f}s) excede el límite de 30 segundos"
    assert desviacion_std < 5.0, f"Desviación estándar ({desviacion_std:.2f}s) indica inconsistencia en el rendimiento"
    assert tiempo_por_pagina_promedio < 0.5, f"Tiempo promedio por página ({tiempo_por_pagina_promedio:.2f}s) excede el límite de 0.5 segundos"

@pytest.mark.performance
def test_memory_usage(large_pdf, tmp_path):
    """
    Prueba el uso de memoria durante el procesamiento de PDF.
    """
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    memoria_inicial = process.memory_info().rss / 1024 / 1024  # MB
    
    # Procesar documento grande
    doc = fitz.open(large_pdf)
    doc_procesado = process_pdf(doc, centrar=True)
    doc_procesado.save(tmp_path / "output_memory.pdf")
    
    # Medir uso de memoria después del procesamiento
    memoria_final = process.memory_info().rss / 1024 / 1024  # MB
    uso_memoria = memoria_final - memoria_inicial
    
    # Cerrar documentos
    doc.close()
    doc_procesado.close()
    
    # Verificar uso de memoria
    assert uso_memoria < 500, f"Uso de memoria ({uso_memoria:.2f}MB) excede el límite de 500MB"

@pytest.mark.performance
def test_concurrent_processing(large_pdf, tmp_path):
    """
    Prueba el rendimiento con procesamiento concurrente.
    """
    from concurrent.futures import ThreadPoolExecutor
    import threading
    
    num_threads = 3
    resultados = []
    lock = threading.Lock()
    
    def procesar_documento(i):
        output_path = tmp_path / f"output_concurrent_{i}.pdf"
        doc = fitz.open(large_pdf)
        doc_procesado = process_pdf(doc, centrar=True)
        doc_procesado.save(output_path)
        doc.close()
        doc_procesado.close()
        
        with lock:
            resultados.append(output_path)
    
    # Procesar en paralelo
    inicio = time.time()
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        executor.map(procesar_documento, range(num_threads))
    tiempo_total = time.time() - inicio
    
    # Verificar resultados
    assert len(resultados) == num_threads, "No todos los hilos completaron el procesamiento"
    for output_path in resultados:
        assert output_path.exists(), f"No se creó el archivo {output_path}"
    
    # Verificar que el tiempo total es razonable para procesamiento paralelo
    tiempo_por_documento = tiempo_total / num_threads
    assert tiempo_por_documento < 20.0, f"Tiempo promedio por documento ({tiempo_por_documento:.2f}s) excede el límite" 