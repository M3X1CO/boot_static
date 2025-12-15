#!/bin/bash

# Generate the static site (with default basepath "/")
python3 src/main.py

# Start the web server
cd docs && python3 -m http.server 8888
