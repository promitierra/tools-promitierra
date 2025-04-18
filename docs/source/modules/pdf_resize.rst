Redimensionamiento de PDF
=======================

Este módulo proporciona funcionalidad para redimensionar documentos PDF a tamaño carta,
manteniendo la orientación original de cada página y permitiendo centrar el contenido.

Características
-------------

* Redimensionamiento automático a tamaño carta (8.5" x 11")
* Preservación de la orientación original (vertical/horizontal)
* Opción para centrar el contenido en la página
* Soporte para procesamiento por lotes
* Retroalimentación detallada del progreso
* Optimización de rendimiento

Uso Básico
---------

.. code-block:: python

    import fitz
    from src.core.pdf_resize_algorithm import process_pdf

    # Abrir documento PDF
    doc = fitz.open("input.pdf")

    # Procesar documento con centrado de contenido
    doc_procesado = process_pdf(doc, centrar=True)

    # Guardar resultado
    doc_procesado.save("output.pdf")

    # Cerrar documentos
    doc.close()
    doc_procesado.close()

Rendimiento
----------

El módulo está optimizado para manejar documentos grandes de manera eficiente:

* Procesamiento página por página para minimizar el uso de memoria
* Soporte para procesamiento concurrente
* Monitoreo detallado del rendimiento
* Límites de rendimiento establecidos:
    - Tiempo promedio por página: < 0.5 segundos
    - Uso de memoria: < 500MB por documento
    - Desviación estándar del tiempo de procesamiento: < 5.0 segundos

Métricas de Rendimiento
^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1

   * - Métrica
     - Valor Objetivo
     - Notas
   * - Tiempo por página
     - < 0.5s
     - Para páginas de tamaño estándar
   * - Memoria por documento
     - < 500MB
     - Para documentos de hasta 1000 páginas
   * - Consistencia
     - σ < 5.0s
     - Desviación estándar del tiempo total

API
---

.. automodule:: src.core.pdf_resize_algorithm
   :members:
   :undoc-members:
   :show-inheritance:

Ejemplos Avanzados
----------------

Procesamiento con Callback de Progreso
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    def mostrar_progreso(actual, total):
        porcentaje = (actual / total) * 100
        print(f"Progreso: {actual}/{total} páginas ({porcentaje:.1f}%)")

    doc_procesado = process_pdf(doc, centrar=True, progress_callback=mostrar_progreso)

Procesamiento en Lotes
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from concurrent.futures import ThreadPoolExecutor
    from pathlib import Path

    def procesar_archivo(ruta):
        doc = fitz.open(ruta)
        doc_procesado = process_pdf(doc, centrar=True)
        ruta_salida = Path(ruta).parent / f"carta_{Path(ruta).name}"
        doc_procesado.save(ruta_salida)
        doc.close()
        doc_procesado.close()
        return ruta_salida

    # Procesar múltiples archivos en paralelo
    with ThreadPoolExecutor(max_workers=3) as executor:
        rutas = ["doc1.pdf", "doc2.pdf", "doc3.pdf"]
        resultados = list(executor.map(procesar_archivo, rutas))

Consideraciones de Uso
--------------------

1. **Memoria**: El módulo está diseñado para procesar documentos página por página,
   minimizando el uso de memoria. Sin embargo, para documentos muy grandes,
   se recomienda monitorear el uso de recursos.

2. **Rendimiento**: El tiempo de procesamiento puede variar según:
   * Tamaño y complejidad de las páginas
   * Cantidad de contenido
   * Recursos del sistema disponibles

3. **Concurrencia**: Aunque el módulo soporta procesamiento concurrente,
   se recomienda limitar el número de trabajos paralelos según los recursos
   disponibles del sistema.

Solución de Problemas
-------------------

Problemas Comunes
^^^^^^^^^^^^^^^

1. **Uso excesivo de memoria**:
   * Procesar documentos más pequeños
   * Reducir el número de trabajos concurrentes
   * Verificar la liberación de recursos

2. **Rendimiento lento**:
   * Verificar el tamaño y complejidad del documento
   * Monitorear recursos del sistema
   * Considerar procesamiento por lotes más pequeños

3. **Errores de procesamiento**:
   * Verificar que el PDF de entrada sea válido
   * Comprobar permisos de archivo
   * Revisar logs para más detalles

Registro y Depuración
^^^^^^^^^^^^^^^^^^

El módulo utiliza el sistema de logging de Python para proporcionar información detallada:

.. code-block:: python

    import logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("src.core.pdf_resize_algorithm")

    # Los mensajes de debug ahora mostrarán información detallada
    doc_procesado = process_pdf(doc, centrar=True) 