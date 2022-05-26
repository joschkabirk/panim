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
import panim
from subprocess import run

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
    "sphinx.ext.napoleon",
    "autoapi.extension",
]

# -- sphinx-autoapi extension -----------------------------------------------
# https://sphinx-autoapi.readthedocs.io/en/latest/reference/config.html#
autoapi_type = "python"
autoapi_dirs = ["../../panim"]
autoapi_python_use_implicit_namespaces = True
autoapi_python_class_content = "both"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

default_role = "code"

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# settings for version switcher
html_static_path = ["_static"]
json_url = "https://jobirk.github.io/panim/master/_static/switcher.json"
release = panim.__version__

# get currently active branch
command = "git rev-parse --abbrev-ref HEAD".split()
git_branch = (
    run(command, capture_output=True, check=True).stdout.strip().decode("utf-8")
)

if "dev" in release:
    version_match = "master"
else:
    version_match = f"v{release}"

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
        "version_match": version_match,
    },
    "navbar_end": ["version-switcher", "navbar-icon-links"],
}

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "friendly"
