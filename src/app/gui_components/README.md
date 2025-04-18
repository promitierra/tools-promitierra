# Componentes de GUI

Esta carpeta contiene componentes reutilizables de la interfaz gráfica para la aplicación Herramientas ProMITIERRA.

## Componentes disponibles

- `components.py`: Componentes básicos de UI como títulos, selectores de archivos y barras de progreso
- `main_window.py`: Implementación de la ventana principal y sus componentes
- `progress_dialog.py`: Diálogo modal para mostrar progreso de operaciones

## Convenciones de código

- Todos los componentes deben seguir el patrón de diseño de CustomTkinter
- Nombres de clases en PascalCase (ej. `ProgressDialog`)
- Métodos y variables en snake_case (ej. `mostrar_progreso`)
- Incluir docstrings para todas las clases y métodos 