# Plan de Acción: Integrar Generación de PDF Horizontal en la GUI

Este documento detalla los pasos para agregar la funcionalidad de crear un archivo PDF horizontal a partir de todas las imágenes apaisadas contenidas en una carpeta seleccionada por el usuario.

**Contexto:** Se asume que la lógica principal para esta conversión ya existe dentro de `src/core/`.

**Estado Actual: COMPLETADO ✅**

## Pasos:

1.  **Verificar/Adaptar Lógica Core:** ✅
    *   **Ubicación:** ✅ Identificada en `src/scripts/generar_pdf_imagenes.py`. La función `generar_pdf_con_imagenes` contiene la lógica necesaria.
    *   **Interfaz:** ✅ Ajustada para incluir un parámetro de callback que permite reportar el progreso durante la generación.
    *   **Progreso:** ✅ Implementado sistema de callback para reportar el progreso de conversión imagen por imagen.

2.  **Crear Nuevo Componente GUI:** ✅
    *   **Implementación:** En lugar de crear un nuevo archivo, se ha integrado directamente en la pestaña existente "Imágenes a PDFs" en `src/app/gui.py`.
    *   **Posición:** Añadido debajo de los controles existentes, separado visualmente mediante un divisor horizontal.
    *   **Widgets:** 
        *   ✅ Título descriptivo separado ("Generar PDF Consolidado Horizontal").
        *   ✅ Botón "Seleccionar Carpeta (Consolidado)" para elegir el directorio.
        *   ✅ Label para mostrar la ruta de carpeta seleccionada (usando StringVar).
        *   ✅ Campo para editar el nombre del archivo PDF de salida.
        *   ✅ Botón "Generar PDF Consolidado" para iniciar el proceso.
        *   ✅ Barra de progreso dedicada para esta función.
        *   ✅ Label para mostrar el estado del proceso.

3.  **Implementar Lógica del Componente GUI:** ✅
    *   **Selección de Carpeta:** ✅ Implementado método `seleccionar_carpeta_consolidado` que actualiza `self.ruta_carpeta_consolidado`.
    *   **Generación de PDF:** ✅
        *   Implementado método `iniciar_generacion_consolidado` que valida la entrada, configura la interfaz y lanza un hilo.
        *   Implementado método `_ejecutar_generacion_consolidado` que llama a la función de generación en un hilo separado.
        *   ✅ Implementado callback `_callback_progreso_gui` que actualiza la barra de progreso y el estado desde el hilo.
        *   ✅ Los botones se deshabilitan durante el procesamiento y se rehabilitan al completar.
        *   ✅ Se muestra un mensaje de éxito o error al finalizar.

4.  **Integrar en la GUI Principal:** ✅
    *   **Pestaña:** Integrado en la pestaña existente "Imágenes a PDFs" en lugar de crear una nueva, siguiendo la solicitud del usuario.
    *   **Plantilla de Nombre:** Implementada como campo editable con un valor predeterminado según la especificación "P - MUNICIPIO - CONSOLIDADO FORMATO ENTREGA - PRODUCTO - EXTENSIONISTA.pdf".

5.  **Pruebas:** ✅
    *   La funcionalidad ha sido probada y funciona según lo esperado.
    *   La interfaz de usuario es intuitiva y consistente con el resto de la aplicación.
    *   El sistema de progreso ofrece retroalimentación en tiempo real durante la generación.

6.  **Documentación y Estilo:** ✅
    *   Añadidos docstrings en español a todos los nuevos métodos.
    *   El código sigue las convenciones de estilo del proyecto existente.
    *   Implementado un manejo de errores consistente con el resto de la aplicación.

7.  **Refinamientos:** ✅
    *   Implementada la plantilla para nombrar el PDF según el formato solicitado.
    *   La barra de progreso muestra el avance en tiempo real gracias al sistema de callbacks. 