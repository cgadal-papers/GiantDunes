import sphinx_gallery
import glob
from sphinx_gallery.sorting import FileNameSortKey, ExplicitOrder


# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('../'))


# -- Project information -----------------------------------------------------

project = 'Giant dunes feedback on wind'
copyright = '2021, Cyril Gadal'
author = 'Cyril Gadal'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',  # Core Sphinx library for auto html doc generation from docstrings
    'sphinx.ext.autosummary',  # Create neat summary tables for modules/classes/methods etc
    'sphinx.ext.intersphinx',  # Link to other project's documentation (see mapping below)
    'sphinx.ext.viewcode',  # Add a link to the Python source code for classes, functions etc.
    'sphinx_autodoc_typehints',  # Automatically document param types (less noise in class signature)
    # 'nbsphinx',  # Integrate Jupyter Notebooks and Sphinx
    'sphinx.ext.napoleon',
    'numpydoc',
    'sphinx.ext.doctest',
    'sphinx.ext.mathjax',
    'sphinx_gallery.gen_gallery',
    'sphinx.ext.coverage'
]

autosummary_generate = True  # Turn on sphinx.ext.autosummary
autoclass_content = "both"  # Add __init__ doc (ie. params) to class summaries
html_show_sourcelink = False  # Remove 'view source code' from top of page (for html, not python)
autodoc_inherit_docstrings = True  # If no docstring, inherit from base class
set_type_checking_flag = True  # Enable 'expensive' imports for sphinx_autodoc_typehints
nbsphinx_allow_errors = True  # Continue through Jupyter errors
# autodoc_typehints = "description" # Sphinx-native method. Not as good as sphinx_autodoc_typehints
add_module_names = False  # Remove namespaces from class/method signatures

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_template']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for Sphinx gallery ---------------------------------------------

intersphinx_mapping = {
    'python': ('https://docs.python.org/{.major}'.format(sys.version_info), None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'matplotlib': ('https://matplotlib.org/stable', None),
    'mayavi': ('http://docs.enthought.com/mayavi/mayavi', None),
    'sklearn': ('https://scikit-learn.org/stable', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master', None),
    'pandas': ('https://pandas.pydata.org/pandas-docs/stable/', None),
    'scipy': ('https://docs.scipy.org/doc/scipy/reference/', None)
}

examples_dirs = ['../Paper_figure', '../Processing']
gallery_dirs = ['Paper_figure', 'Processing']

sphinx_gallery_conf = {
    'examples_dirs': examples_dirs,   # path to your example scripts
    'gallery_dirs': gallery_dirs,  # path to where to save gallery generated output
    'backreferences_dir': 'gen_modules/backreferences',  # directory where function/class granular galleries are stored
    'doc_module': ('python_codes'),  # Modules for which function/class level galleries are created.
    'reference_url': {
                     # 'python_codes': None,  # The module you locally document uses None
                     'numpy': 'https://docs.scipy.org/doc/numpy/',
                     'scipy': 'https://docs.scipy.org/doc/scipy/reference/',
                     'matplotlib': 'https://matplotlib.org/stable'
                     },
    'matplotlib_animations': True,
    'plot_gallery': True,
    'ignore_pattern': '/_',
    'filename_pattern': '^(?!.*norun_)',
    'subsection_order': ExplicitOrder([
                                       '../Processing',
                                       '../Paper_figure/',
                                       '../Paper_figure/Supplementary_Figures/',
                                       ]),
    'within_subsection_order': FileNameSortKey,
     }

# -- Options for HTML output -------------------------------------------------


# Pydata theme
html_theme = "pydata_sphinx_theme"
html_theme_options = {"show_prev_next": False}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
# html_css_files = ['mne_style.css']
html_css_files = ['pydata-custom.css']
# html_css_files = ['numpy.css']


# If true, links to the reST sources are added to the pages.
html_show_sourcelink = False
html_copy_source = False
