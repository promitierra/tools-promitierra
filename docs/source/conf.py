"""
Archivo de configuración de Sphinx para la documentación de Herramientas PromiTierra.
"""

import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

# -- Información del proyecto -----------------------------------------------------
project = 'Herramientas PromiTierra'
copyright = '2024, PromiTierra'
author = 'PromiTierra'
release = '1.0.0'

# -- Configuración general ------------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx.ext.coverage',
    'sphinx_rtd_theme',
]

templates_path = ['_templates']
exclude_patterns = []
language = 'es'

# -- Opciones para la salida HTML ----------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# -- Opciones de Napoleon ----------------------------------------------------
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = True
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = True
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_type_aliases = None

# -- Opciones de intersphinx -------------------------------------------------
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'fitz': ('https://pymupdf.readthedocs.io/en/latest/', None),
} 