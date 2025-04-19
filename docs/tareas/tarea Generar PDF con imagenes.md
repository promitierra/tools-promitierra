# Plan de Acción: Integrar Generación de PDF Horizontal en la GUI

Este documento detalla los pasos para agregar la funcionalidad de crear un archivo PDF horizontal a partir de todas las imágenes apaisadas contenidas en una carpeta seleccionada por el usuario.

**Contexto:** Se asume que la lógica principal para esta conversión ya existe dentro de `src/core/`.

**Pasos:**

1.  **Verificar/Adaptar Lógica Core:**
    *   **Ubicación:** Identificar la clase/módulo exacto en `src/core/` responsable de la conversión (posiblemente parte de `PDFConverter` o una nueva clase).
    *   **Interfaz:** Asegurar que la función/método acepte la ruta de la carpeta de entrada (como `pathlib.Path`) y devuelva el estado de la operación y la ruta del PDF generado.
    *   **Progreso:** Si es una operación larga, verificar si implementa callbacks o un mecanismo para reportar el progreso, necesario para la GUI. De no ser así, adaptarla.

2.  **Crear Nuevo Componente GUI (`HorizontalPdfFrame`):**
    *   **Archivo:** Crear un nuevo archivo, por ejemplo, `src/gui/horizontal_pdf_frame.py`.
    *   **Clase:** Definir una clase `HorizontalPdfFrame` que herede de `customtkinter.CTkFrame`.
    *   **Widgets:**
        *   `CTkLabel`: Título descriptivo ("Generar PDF Horizontal desde Carpeta").
        *   `CTkButton`: Botón "Seleccionar Carpeta" para elegir el directorio de imágenes.
        *   `CTkEntry` (o `CTkLabel`): Para mostrar la ruta de la carpeta seleccionada (deshabilitado para edición).
        *   `CTkButton`: Botón "Generar PDF" para iniciar el proceso.
        *   (Opcional) `CTkProgressBar`: Para mostrar el progreso de la conversión.
        *   (Opcional) `CTkLabel`: Para mostrar mensajes de estado (ej. "Procesando...", "Completado", "Error").
    *   **Estilo:** Seguir las convenciones de estilo de `CustomTkinter` y del proyecto.

3.  **Implementar Lógica del Componente GUI:**
    *   **Selección de Carpeta:** En `HorizontalPdfFrame`, implementar el método asociado al botón "Seleccionar Carpeta". Usar `customtkinter.filedialog.askdirectory()` para obtener la ruta. Actualizar el `CTkEntry`/`CTkLabel` correspondiente. Usar `pathlib.Path` para manejar la ruta.
    *   **Generación de PDF:**
        *   Implementar el método asociado al botón "Generar PDF".
        *   Obtener la ruta de la carpeta desde el `CTkEntry`/`CTkLabel`.
        *   Realizar validaciones básicas (¿se seleccionó una carpeta?).
        *   **Ejecución Asíncrona:** Utilizar `concurrent.futures.ThreadPoolExecutor` para llamar a la función del *core* en un hilo separado, evitando bloquear la GUI.
        *   Deshabilitar botones mientras el proceso está en ejecución y mostrar un indicador de "trabajando".
        *   **Feedback:** Conectar los callbacks de progreso (si existen en el core) o usar polling para actualizar la `CTkProgressBar` y/o el `CTkLabel` de estado.
        *   **Resultado:** Al finalizar el hilo, mostrar un mensaje de éxito (con la ruta del PDF) o error usando `tkinter.messagebox`. Habilitar los botones nuevamente.

4.  **Integrar en la GUI Principal:**
    *   **Archivo:** Modificar el archivo de la ventana principal (probablemente `src/app/imagen_a_pdf_gui.py` o similar).
    *   **Pestaña/Sección:** Si la GUI principal usa `CTkTabview`, añadir una nueva pestaña ("PDF Horizontal").
    *   **Instanciación:** Importar `HorizontalPdfFrame` desde `src.gui.horizontal_pdf_frame`.
    *   **Añadir:** Crear una instancia de `HorizontalPdfFrame` y añadirla como contenido de la nueva pestaña o sección correspondiente en la ventana principal.

5.  **Pruebas:**
    *   Probar la selección de diferentes carpetas.
    *   Verificar la correcta generación del PDF con imágenes apaisadas.
    *   Probar con carpetas que contengan subcarpetas, imágenes no apaisadas u otros tipos de archivos (verificar manejo de errores/filtrado).
    *   Probar con carpetas vacías.
    *   Confirmar que la GUI permanezca responsiva durante el proceso.
    *   Verificar que los mensajes de estado, progreso y finalización sean claros.

6.  **Documentación y Estilo:**
    *   Añadir `docstrings` en español a la nueva clase `HorizontalPdfFrame` y sus métodos principales.
    *   Asegurar que todo el código nuevo siga las convenciones PEP 8 y las reglas del proyecto (nombres `snake_case`, comentarios en español, etc.).
    *   Actualizar `requirements.txt` si se añade alguna dependencia (poco probable para este caso).

7.  **(Opcional) Refinamientos:**
    *   Permitir al usuario especificar el nombre del archivo PDF de salida.
    *   Añadir opción para abrir el PDF generado automáticamente al finalizar. 