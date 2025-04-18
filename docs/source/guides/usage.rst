Guía de Uso
==========

Esta guía proporciona instrucciones detalladas sobre cómo usar las diferentes funcionalidades de Herramientas PromiTierra.

Interfaz Gráfica
--------------

La aplicación principal proporciona una interfaz gráfica moderna y fácil de usar:

1. **Inicio**
   
   * Ejecute el archivo `main.py` o el ejecutable distribuido
   * La interfaz mostrará las diferentes herramientas disponibles en pestañas

2. **Navegación**
   
   * Use las pestañas para cambiar entre herramientas
   * Cada herramienta tiene su propia interfaz optimizada
   * Los ajustes comunes están disponibles en el menú de configuración

Redimensionamiento de PDF
----------------------

1. **Uso Básico**
   
   a. Seleccione la pestaña "Redimensionar PDF"
   b. Haga clic en "Seleccionar Archivo" o arrastre y suelte el PDF
   c. Elija si desea centrar el contenido
   d. Haga clic en "Procesar"

   .. image:: _static/resize_pdf_basic.png
      :alt: Interfaz básica de redimensionamiento
      :width: 600px

2. **Opciones Avanzadas**
   
   * **Centrado**: Centra el contenido en la página
   * **Orientación**: Mantiene la orientación original
   * **Procesamiento por Lotes**: Procesa múltiples archivos
   * **Vista Previa**: Muestra el resultado antes de guardar

3. **Procesamiento por Lotes**
   
   a. Haga clic en "Modo Lote"
   b. Seleccione una carpeta con PDFs
   c. Configure las opciones deseadas
   d. Haga clic en "Procesar Lote"

   .. code-block:: text

       Estructura de carpetas recomendada:
       input/
       ├── doc1.pdf
       ├── doc2.pdf
       └── doc3.pdf
       
       output/
       ├── carta_doc1.pdf
       ├── carta_doc2.pdf
       └── carta_doc3.pdf

Conversión de Imágenes a PDF
-------------------------

1. **Conversión Individual**
   
   a. Seleccione la pestaña "Imágenes a PDF"
   b. Seleccione una o más imágenes
   c. Configure opciones de página
   d. Haga clic en "Convertir"

2. **Conversión por Lotes**
   
   * Seleccione una carpeta con imágenes
   * Las imágenes se procesarán en orden alfabético
   * Se mantendrá la estructura de carpetas

3. **Formatos Soportados**
   
   * PNG
   * JPEG/JPG
   * TIFF
   * BMP
   * GIF (primera imagen)

Conversión de PDF a PNG
--------------------

1. **Extracción de Páginas**
   
   a. Seleccione la pestaña "PDF a PNG"
   b. Elija el PDF de origen
   c. Seleccione páginas específicas o todas
   d. Configure la calidad de salida

2. **Opciones de Calidad**
   
   * **Baja**: 72 DPI
   * **Media**: 150 DPI
   * **Alta**: 300 DPI
   * **Personalizada**: DPI configurable

Creación de Estructura de Carpetas
------------------------------

1. **Desde Excel**
   
   a. Prepare el archivo Excel con la estructura deseada
   b. Seleccione la pestaña "Crear Carpetas"
   c. Cargue el archivo Excel
   d. Verifique la estructura
   e. Haga clic en "Crear"

2. **Formato de Excel**
   
   .. list-table::
      :header-rows: 1

      * - Nivel 1
        - Nivel 2
        - Nivel 3
      * - Carpeta1
        - Subcarpeta1
        - SubSubcarpeta1
      * - Carpeta1
        - Subcarpeta2
        - 
      * - Carpeta2
        - 
        - 

Configuración
-----------

1. **Preferencias Generales**
   
   * Idioma de la interfaz
   * Tema visual (claro/oscuro)
   * Directorio de trabajo predeterminado
   * Formato de nombres de archivo

2. **Rendimiento**
   
   * Número máximo de trabajos paralelos
   * Uso máximo de memoria
   * Calidad predeterminada

3. **Guardado Automático**
   
   * Habilitar/deshabilitar
   * Intervalo de guardado
   * Ubicación de respaldo

Solución de Problemas
------------------

1. **Problemas Comunes**
   
   * **Error al abrir archivo**: Verifique permisos y si está en uso
   * **Memoria insuficiente**: Reduzca el tamaño de lote
   * **Archivo corrupto**: Verifique integridad del PDF

2. **Mensajes de Error**
   
   * Los mensajes incluyen códigos de error
   * Consulte el registro para más detalles
   * Use la ayuda contextual

3. **Registro de Actividad**
   
   * Ubicación: `logs/app.log`
   * Nivel de detalle configurable
   * Útil para diagnóstico

Atajos de Teclado
---------------

.. list-table::
   :header-rows: 1

   * - Atajo
     - Acción
   * - Ctrl+O
     - Abrir archivo
   * - Ctrl+S
     - Guardar
   * - Ctrl+B
     - Modo lote
   * - F1
     - Ayuda
   * - Ctrl+Q
     - Salir

Mejores Prácticas
--------------

1. **Organización**
   
   * Use nombres descriptivos
   * Mantenga una estructura de carpetas clara
   * Haga respaldos regulares

2. **Rendimiento**
   
   * Procese lotes de tamaño razonable
   * Monitoree el uso de recursos
   * Cierre archivos después de usarlos

3. **Calidad**
   
   * Verifique los resultados
   * Use la vista previa
   * Ajuste la configuración según necesidad

Recursos Adicionales
-----------------

1. **Tutoriales**
   
   * Videos demostrativos
   * Ejemplos paso a paso
   * Casos de uso comunes

2. **Documentación**
   
   * Manual completo
   * Referencia de API
   * Notas de versión

3. **Soporte**
   
   * Foro de usuarios
   * Base de conocimientos
   * Contacto de soporte 