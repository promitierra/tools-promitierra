\
.. _guide-generar-pdf-imagenes:

Script: Generación de PDFs a partir de Imágenes
===============================================

Descripción General
-------------------

El script :code:`generar_pdf_imagenes.py` es una herramienta versátil diseñada para convertir un conjunto de imágenes en un documento PDF formateado profesionalmente. Garantiza márgenes precisos, mantiene las proporciones de las imágenes, las centra adecuadamente y permite configurar opciones como la numeración de páginas y la orientación.

Características Principales
---------------------------

*   **Orientación Configurable**: Por defecto, todas las imágenes se presentan en formato horizontal, rotando automáticamente las que están en vertical.
*   **Márgenes Exactos**: Garantiza márgenes de 1 cm en todos los lados (superior, inferior, izquierdo y derecho).
*   **Centrado Automático**: Posiciona las imágenes perfectamente centradas en cada página.
*   **Preservación de Proporciones**: Mantiene la relación de aspecto original de las imágenes.
*   **Numeración de Páginas Opcional**: Permite activar o desactivar la numeración en la esquina externa de cada página.
*   **Verificación de Integridad**: Verifica que el PDF generado sea válido y legible.
*   **Manejo de Nombres Largos**: Gestiona automáticamente nombres de archivo largos y caracteres especiales.

Uso del Script
--------------

El script se puede ejecutar desde la línea de comandos de la siguiente manera:

.. code-block:: bash

    python src/scripts/generar_pdf_imagenes.py "ruta/al/directorio/de/imagenes" [opciones]

Parámetros
~~~~~~~~~~

*   :code:`ruta/al/directorio/de/imagenes`: Directorio que contiene las imágenes a procesar.

Opciones
~~~~~~~~

*   :code:`-o, --output`: Ruta de salida personalizada para el PDF (opcional). Si no se especifica, se guarda en el directorio de entrada con el nombre "CONSOLIDADO_[nombre_directorio].pdf".
*   :code:`-d, --debug`: Activa el modo de depuración para información detallada del proceso.
*   :code:`--no-page-numbers`: Desactiva la numeración de páginas en el documento.

Ejemplos de Uso
~~~~~~~~~~~~~~~

1.  Uso básico (con numeración de páginas):

    .. code-block:: bash

        python src/scripts/generar_pdf_imagenes.py "C:/Usuarios/ejemplo/Imagenes"

2.  Generación sin números de página:

    .. code-block:: bash

        python src/scripts/generar_pdf_imagenes.py "C:/Usuarios/ejemplo/Imagenes" --no-page-numbers

3.  Especificando ruta de salida:

    .. code-block:: bash

        python src/scripts/generar_pdf_imagenes.py "C:/Usuarios/ejemplo/Imagenes" -o "C:/Salida/documento.pdf"

4.  Modo debug con numeración desactivada:

    .. code-block:: bash

        python src/scripts/generar_pdf_imagenes.py "C:/Usuarios/ejemplo/Imagenes" -d --no-page-numbers

Detalles Técnicos
-----------------

Flujo de Procesamiento
~~~~~~~~~~~~~~~~~~~~~~

1.  **Lectura del Directorio**: El script lee todas las imágenes (PNG, JPG, JPEG) del directorio especificado.
2.  **Ordenamiento**: Las imágenes se ordenan alfabéticamente por nombre de archivo.
3.  **Procesamiento Individual**:
    *   Conversión a formato RGB si es necesario
    *   Rotación a horizontal si la imagen está en vertical
    *   Redimensionamiento para ajustarse a los márgenes mientras se mantiene la proporción
    *   Centrado en la página
    *   Aplicación opcional de numeración de página
4.  **Generación del PDF**: Se crea un PDF con todas las imágenes procesadas, una por página.
5.  **Verificación**: Se comprueba que el PDF generado sea válido y legible.

Formatos de Imagen Soportados
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*   PNG
*   JPG
*   JPEG

Requisitos Técnicos
~~~~~~~~~~~~~~~~~~

El script utiliza las siguientes bibliotecas:

*   Pillow (PIL): Para procesamiento de imágenes
*   ReportLab: Para generación de PDFs
*   pathlib: Para manejo de rutas
*   logging: Para registro de operaciones

Casos de Uso Recomendados
-------------------------

*   Consolidación de documentos escaneados (IPPTA, planeadores, formatos, etc.)
*   Creación de documentos PDF a partir de colecciones de imágenes
*   Estandarización de documentos para impresión con márgenes consistentes
*   Generación de documentos para presentación profesional
*   Consolidación de archivos con y sin numeración de página según necesidad

Resolución de Problemas
-----------------------

Errores Comunes
~~~~~~~~~~~~~~~

1.  **Error de Permisos**: Asegúrese de tener permisos de escritura en el directorio de salida.
2.  **Imágenes Corruptas**: El script detecta y reporta imágenes dañadas que no se pueden procesar.
3.  **Rutas no Encontradas**: Verifique que la ruta al directorio de imágenes exista.
4.  **Caracteres Especiales**: El script maneja automáticamente rutas con espacios y caracteres especiales.

Mensajes de Log
~~~~~~~~~~~~~~~

El script genera mensajes de log detallados que ayudan a identificar el progreso y posibles problemas:

*   :code:`INFO`: Información sobre el proceso (imágenes procesadas, progreso, resultado final)
*   :code:`ERROR`: Errores durante el procesamiento (imágenes corruptas, problemas de escritura)

Notas Adicionales
-----------------

*   El script está optimizado para mantener la calidad visual mientras genera archivos PDF de tamaño razonable.
*   Las imágenes muy grandes se redimensionan manteniendo su proporción original.
*   Si una imagen necesita rotación, se rota automáticamente a la orientación horizontal.
*   La numeración de página (cuando está activada) aparece en la esquina externa inferior. (Nota: Hay una tarea pendiente para mejorar esta ubicación).
*   El script maneja automáticamente la creación de nombres de archivo únicos cuando ya existe un archivo con el mismo nombre.

Ejemplos de Resultados
----------------------

El script genera PDFs con estas características:

*   Tamaño de página: Carta (8.5\" x 11\")
*   Orientación: Horizontal (apaisado)
*   Márgenes: 1 cm en todos los lados
*   Imágenes: Centradas, con la proporción original preservada
*   Numeración: Opcional, en esquina externa inferior cuando está activada 