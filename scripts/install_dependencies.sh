#!/bin/bash
set -e

# Activate the virtual environment (if applicable)
# source /path/to/your/virtualenv/bin/activate
ls

cd deployment-root

ls

# Install the required Python packages
pip install -r requirements.txt