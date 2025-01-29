# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
# Initialiser Django
import django
django.setup()


sys.path.insert(0, os.path.abspath('../apis'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'base'  # Utilise base.py dans la racine
project = 'Events'
copyright = '2025, Elvis brown'
author = 'Elvis brown'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
  'sphinx.ext.autodoc',        # Pour documenter les docstrings
    'sphinx.ext.napoleon',       # Pour les docstrings en style Google/NumPy
    'sphinx.ext.viewcode',       # Pour afficher le code source dans la documentation
    'sphinx.ext.intersphinx',    # Pour lier la documentation avec d'autres projets
]
templates_path = ['_templates']
exclude_patterns = []

language = 'english'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
