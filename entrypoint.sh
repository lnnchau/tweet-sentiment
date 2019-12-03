#!/bin/bash
mkdir data/
mkdir logs/

python3 download_script.py
gunicorn wsgi:app