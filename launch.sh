#!/bin/bash

source venv/bin/activate

PYTHON="venv/bin/python"
echo "venv ${PYTHON}"
echo ""

python web-ui.py $*

deactivate

