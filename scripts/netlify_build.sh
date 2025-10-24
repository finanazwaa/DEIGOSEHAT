#!/usr/bin/env bash
set -e
apt-get update
apt-get install -y gdal-bin libgdal-dev
# now install Python deps and continue your normal build steps
pip install -r requirements.txt
# (add any other build commands you need after here)