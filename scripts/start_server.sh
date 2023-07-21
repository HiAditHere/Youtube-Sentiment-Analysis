#!/bin/bash
set -e

# Activate the virtual environment (if applicable)
# source /path/to/your/virtualenv/bin/activate
cd /var/www/html/

# Start the Flask server
python app.py