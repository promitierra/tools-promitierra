Guía de Instalación
==================

Esta guía te ayudará a instalar y configurar Herramientas PromiTierra en tu sistema.

Requisitos del Sistema
-------------------

* Python 3.9 o superior
* Windows 10 o superior
* 4GB de RAM mínimo (8GB recomendado)
* 500MB de espacio en disco

Dependencias Principales
---------------------

* CustomTkinter - Para la interfaz gráfica moderna
* PyMuPDF (fitz) - Para procesamiento de PDFs
* Pillow - Para procesamiento de imágenes
* pandas/openpyxl - Para procesamiento de archivos Excel

Instalación
----------

1. Preparación del Entorno
^^^^^^^^^^^^^^^^^^^^^^^^

Primero, asegúrate de tener Python instalado:

.. code-block:: bash

    python --version

Si no tienes Python instalado, descárgalo de https://python.org

2. Crear Entorno Virtual
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # Crear el entorno virtual
    python -m venv venv

    # Activar el entorno virtual
    # En Windows:
    venv\Scripts\activate
    # En Linux/Mac:
    source venv/bin/activate

3. Instalar Dependencias
^^^^^^^^^^^^^^^^^^^^^

Usamos `uv` como gestor de paquetes para una instalación más rápida y confiable:

.. code-block:: bash

    # Instalar uv
    pip install uv

    # Instalar dependencias del proyecto
    uv pip install -r requirements.txt

4. Verificar la Instalación
^^^^^^^^^^^^^^^^^^^^^^^^

Ejecuta las pruebas para verificar que todo está correctamente instalado:

.. code-block:: bash

    pytest tests/

Instalación para Desarrollo
------------------------

Si planeas contribuir al proyecto, necesitarás algunas dependencias adicionales:

.. code-block:: bash

    uv pip install -r requirements-dev.txt

Esto instalará:

* pytest - Para pruebas unitarias
* sphinx - Para documentación
* black - Para formateo de código
* flake8 - Para análisis estático
* mypy - Para verificación de tipos

Configuración del IDE
------------------

Recomendamos usar Visual Studio Code con las siguientes extensiones:

* Python
* Pylance
* Python Test Explorer
* Python Docstring Generator
* Git Graph

Configuración de VS Code:

.. code-block:: json

    {
        "python.linting.enabled": true,
        "python.linting.flake8Enabled": true,
        "python.formatting.provider": "black",
        "editor.formatOnSave": true,
        "python.testing.pytestEnabled": true
    }

Solución de Problemas
------------------

Error: ImportError: DLL load failed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Este error suele ocurrir en Windows cuando faltan las bibliotecas de Visual C++:

1. Descarga e instala "Microsoft Visual C++ Redistributable"
2. Reinicia tu sistema
3. Intenta la instalación nuevamente

Error: No module named 'tkinter'
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

En sistemas Linux, necesitas instalar tkinter:

.. code-block:: bash

    # Ubuntu/Debian
    sudo apt-get install python3-tk

    # Fedora
    sudo dnf install python3-tkinter

Actualización
-----------

Para actualizar a la última versión:

.. code-block:: bash

    # Activar entorno virtual
    venv\Scripts\activate

    # Actualizar dependencias
    uv pip install -r requirements.txt --upgrade

Desinstalación
------------

Para desinstalar:

1. Desactiva el entorno virtual:

   .. code-block:: bash

       deactivate

2. Elimina el directorio del proyecto y el entorno virtual:

   .. code-block:: bash

       # Windows
       rmdir /s /q venv
       # Linux/Mac
       rm -rf venv 