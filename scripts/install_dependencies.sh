#!/bin/bash
set -e

# Activate the virtual environment (if applicable)
# source /path/to/your/virtualenv/bin/activate
cd /var/www/html/

# Install the required Python packages
pip install -r requirements.txt