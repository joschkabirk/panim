#!/bin/bash

# install requirements and panim
pip install .

# install requirements for sphinx
pip install -r docs/requirements.txt

# build the documentation
cd docs
rm -rf _build _static _templates
sphinx-apidoc -f -o . ../panim
make html

# we have to create an empty .nojekyll file in order to make the html theme work
touch _build/html/.nojekyll