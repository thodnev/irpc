# encoding: utf-8
#
# Copyright (C) 2020 Tymofii Khodniev <thodnev@xinity.dev>
#
# This file is part of IRPC.
#
# IRPC is free software: you can redistribute it and/or modify it under the terms of the
# GNU Lesser General Public License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# IRPC is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along with IRPC.
# If not, see <https://www.gnu.org/licenses/>.


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
curdir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(curdir, '..')))
import irpc     # noqa: E402

# is_rtd is whether we are on readthedocs, this line of code grabbed from docs.readthedocs.org
is_rtd = os.environ.get('READTHEDOCS', '0').lower() in {'true', '1', 'y', 'yes'}


# -- Project information -----------------------------------------------------

project = 'IRPC'
copyright = '2020, thodnev'
author = 'thodnev'
version = irpc.__version__
release = version


# -- General configuration ---------------------------------------------------
# The document name of the “master” document, that is, the document that contains
# the root toctree directive
master_doc = 'index'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon'
]

# Napoleon-related config
#
# use Google style only
napoleon_google_docstring = True
napoleon_numpy_docstring = False
# Set to list __init___ docstrings separately from the class docstring
napoleon_include_init_with_doc = False
# Set to include private members (like _membername) with docstrings in the documentation
napoleon_include_private_with_doc = False
# Set to include special members (like __membername__) with docstrings in the documentation
napoleon_include_special_with_doc = True
# Set True to use the .. admonition:: directive. False to use the .. rubric:: directive instead
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
# Set True to use the :ivar: role for instance variables. False to use .. attribute:: directive
napoleon_use_ivar = False
# True to use a :param: role for each function parameter.
# False to use a single :parameters: role for all the parameters
napoleon_use_param = True
# True to use a :keyword: role for each function keyword argument.
# False to use a single :keyword arguments: role for all the keywords
napoleon_use_keyword = True
# True to use the :rtype: role for the return type.
# False to output the return type inline with the description
napoleon_use_rtype = True


# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#

# only import and set the theme if we're building docs locally
# otherwise, readthedocs.org uses their theme by default, so no need to specify it
if not is_rtd:
    import sphinx_theme
    html_theme = 'neo_rtd_theme'
    html_theme_path = [sphinx_theme.get_html_theme_path(html_theme)]


# Get rid of theme customized notice at the bottom of page
html_show_sphinx = False

# Don't show "View page source" link
html_show_sourcelink = False

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']
