#!/bin/bash

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment and install requirements
source venv/bin/activate
pip install -r requirements.txt

echo ""
echo "Requirements installed successfully."

# Deactivate virtual environment
deactivate
