#!/bin/sh

python -m pip install --upgrade build

sudo rm -r build
sudo rm -r dist
sudo rm -r edx_oauth2_auth0_backend.egg-info

python3 -m build --sdist ./
python3 -m build --wheel ./

python3 -m pip install --upgrade twine
twine check dist/*

# PyPi test
twine upload --skip-existing --repository testpypi dist/*
