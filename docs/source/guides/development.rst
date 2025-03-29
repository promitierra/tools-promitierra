Guía de Desarrollo
================

Esta guía proporciona información detallada sobre el desarrollo y mantenimiento del proyecto Herramientas PromiTierra.

Estándares de Código
-----------------

1. **Estilo de Código**
   
   Seguimos estrictamente PEP 8 con algunas especificaciones adicionales:

   * Indentación: 4 espacios
   * Longitud máxima de línea: 88 caracteres (compatible con black)
   * Nombres en español
   * Docstrings en español

   Ejemplo:

   .. code-block:: python

       def procesar_documento(ruta_archivo: str, centrar: bool = False) -> bool:
           """
           Procesa un documento PDF y lo redimensiona a tamaño carta.

           Args:
               ruta_archivo: Ruta al archivo PDF a procesar
               centrar: Si True, centra el contenido en la página

           Returns:
               bool: True si el procesamiento fue exitoso
           """
           # Implementación...

2. **Convenciones de Nombres**

   * Clases: PascalCase
   * Funciones y variables: snake_case
   * Constantes: MAYÚSCULAS_CON_GUIONES
   * Archivos: snake_case.py

3. **Documentación**

   * Docstrings para todas las funciones y clases
   * Comentarios para lógica compleja
   * README actualizado para cada módulo
   * Ejemplos de uso incluidos

Control de Versiones
-----------------

1. **Estructura de Ramas**

   * `main`: Código en producción
   * `develop`: Desarrollo activo
   * `feature/*`: Nuevas características
   * `bugfix/*`: Correcciones de errores
   * `release/*`: Preparación de releases

2. **Commits**

   Formato de mensaje:

   .. code-block:: text

       tipo(alcance): descripción corta

       Descripción detallada si es necesaria.

       Referencia a issues: #123

   Tipos de commit:
   * feat: Nueva característica
   * fix: Corrección de error
   * docs: Documentación
   * style: Formato
   * refactor: Refactorización
   * test: Pruebas
   * chore: Mantenimiento

3. **Pull Requests**

   * Título descriptivo
   * Descripción detallada
   * Referencias a issues
   * Pruebas incluidas
   * Documentación actualizada

Pruebas
------

1. **Estructura**

   .. code-block:: text

       tests/
       ├── __init__.py
       ├── conftest.py
       ├── test_pdf_resizer.py
       ├── test_integration_pdf_resize.py
       └── test_performance_pdf_resize.py

2. **Tipos de Pruebas**

   * Unitarias: Funcionalidad individual
   * Integración: Interacción entre componentes
   * Rendimiento: Métricas y optimización
   * GUI: Interfaz de usuario

3. **Ejecución**

   .. code-block:: bash

       # Todas las pruebas
       pytest

       # Pruebas específicas
       pytest tests/test_pdf_resizer.py
       pytest -m "not slow"
       pytest -m performance

Integración Continua
-----------------

1. **GitHub Actions**

   Flujo de trabajo principal:

   .. code-block:: yaml

       name: Tests
       on: [push, pull_request]
       jobs:
         test:
           runs-on: windows-latest
           steps:
             - uses: actions/checkout@v3
             - name: Set up Python
               uses: actions/setup-python@v4
             - name: Run tests
               run: pytest

2. **Verificaciones Automáticas**

   * Pruebas unitarias
   * Cobertura de código
   * Análisis estático
   * Formato de código
   * Documentación

Gestión de Dependencias
--------------------

1. **Entorno Virtual**

   .. code-block:: bash

       python -m venv venv
       source venv/bin/activate  # Linux/Mac
       venv\Scripts\activate     # Windows

2. **Dependencias**

   Mantenemos dos archivos:

   * `requirements.txt`: Dependencias de producción
   * `requirements-dev.txt`: Dependencias de desarrollo

3. **Actualización**

   .. code-block:: bash

       uv pip install -r requirements.txt --upgrade
       uv pip freeze > requirements.txt

Despliegue
--------

1. **Preparación**

   * Actualizar versión en `setup.py`
   * Actualizar CHANGELOG.md
   * Ejecutar pruebas completas
   * Generar documentación

2. **Empaquetado**

   .. code-block:: bash

       python -m build
       twine check dist/*
       twine upload dist/*

3. **Distribución**

   * Generar ejecutable con PyInstaller
   * Firmar digitalmente
   * Publicar release en GitHub

Mantenimiento
-----------

1. **Monitoreo**

   * Logs de errores
   * Métricas de rendimiento
   * Retroalimentación de usuarios

2. **Actualizaciones**

   * Dependencias
   * Seguridad
   * Documentación

3. **Backups**

   * Código fuente
   * Base de datos
   * Configuraciones

Contribución
----------

1. **Proceso**

   * Fork del repositorio
   * Crear rama feature/bugfix
   * Desarrollar cambios
   * Pruebas y documentación
   * Pull request

2. **Revisión de Código**

   * Estilo y convenciones
   * Funcionalidad
   * Pruebas
   * Documentación

3. **Merge**

   * Squash commits
   * Mensaje descriptivo
   * Actualizar CHANGELOG 