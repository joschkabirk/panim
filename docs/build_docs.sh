#!/bin/bash

pip install .

# install requirements for sphinx
pip install -r docs/requirements.txt

# build the documentation
cd docs
rm -rf _build _static _templates
# sphinx-build -b html source _build/html
# mkdir -p _build/html
# cp source/_static/versions.json _build/html
sphinx-multiversion source _build/html
# copy the index.html that redirects to the master folder
cp source/redirect_index.html _build/html/index.html

# we have to create an empty .nojekyll file in order to make the html theme work
touch _build/html/.nojekyll