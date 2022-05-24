# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("../../panim"))


# -- Project information -----------------------------------------------------

project = "panim"
copyright = "2022, Joschka Birk"
author = "Joschka Birk"

# The full version, including alpha/beta/rc tags
release = ""


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "myst_parser",
    "autoapi.extension",
    "sphinx_multiversion",
]

# Configuration of sphinx-autoapi extension
# https://sphinx-autoapi.readthedocs.io/en/latest/reference/config.html#
autoapi_type = "python"
autoapi_dirs = ["../../panim"]
autoapi_python_use_implicit_namespaces = True
autoapi_python_class_content = "both"

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]
html_sidebars = {
    "**": [
        "versioning.html",
    ],
}

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# settings for sphinx-multiversion
# define which releases are used in sphinx-multiversion
# smv_released_pattern = r"^tags/.*$" 
# define which tags are used in sphinx-multiversion
smv_tag_whitelist = r"^.*$"  
# define which branches are used in sphinx-multiversion
smv_branch_whitelist = r"^(master)"
# smv_branch_whitelist = None
# Whitelist pattern for remotes (set to None to use local branches only)
smv_remote_whitelist = r'^(origin/master)' 

# settings for version switcher
html_static_path = ['_static']
json_url = "https://jobirk.github.io/panim/master/_static/switcher.json"

default_role = "code"

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "pydata_sphinx_theme"
html_theme_options = {
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/jobirk/panim",
            "icon": "fab fa-github-square",
            "type": "fontawesome",
        },
    ],
    "switcher": {
        "json_url": json_url,
        "version_match": "latest",
    },
    "navbar_end": ["version-switcher", "navbar-icon-links"]
}
pygments_style = "friendly"