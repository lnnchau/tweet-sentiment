#!/bin/bash
pip install -r requirements.txt

mkdir data/
mkdir logs/

FILE=/usr/local/bin/chromedriver_linux64
if test -f "$FILE"; then
    wget https://chromedriver.storage.googleapis.com/77.0.3865.40/chromedriver_linux64.zip
    unzip -d /usr/local/bin $PWD/chromedriver_linux64.zip
    rm $PWD/chromedriver_linux64.zip
fi

python3 download_script.py
gunicorn --bind 0.0.0.0:5000 wsgi:app