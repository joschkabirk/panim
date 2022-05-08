#!/bin/bash

# install requirements and panim
pip install .

# install requirements for sphinx
pip install -r docs/requirements.txt

# render placeholders with §§§ syntax
wget -O replace_placeholders_in_md.py https://gitlab.cern.ch/atlas-flavor-tagging-tools/algorithms/umami/-/raw/master/.gitlab/workflow/replace_placeholders_in_md.py
python replace_placeholders_in_md.py -i "docs/**/*.md" --no_backup
doxec docs/source/examples.md
mkdir examples_output
python examples_for_ci.py

# build the documentation
cd docs
rm -rf _build _static _templates
sphinx-apidoc -f -o . ../panim
make html

# we have to create an empty .nojekyll file in order to make the html theme work
touch _build/html/.nojekyll