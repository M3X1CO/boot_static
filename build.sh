#!/bin/bash

# Build the static site for GitHub Pages production deployment
# This uses the repository name as the basepath
python3 src/main.py "/boot_static/"
