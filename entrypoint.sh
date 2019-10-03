#!/bin/bash
pip install -r requirements.txt

mkdir data/
mkdir logs/

FILE=/usr/local/bin/chromedriver
if ! test -f "$FILE"; then
    if [[ "$OSTYPE" == "linux-gnu" ]]; then
        LINK=https://chromedriver.storage.googleapis.com/77.0.3865.40/chromedriver_linux64.zip
        FILE_NAME=chromedriver_linux64.zip
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        LINK=https://chromedriver.storage.googleapis.com/77.0.3865.40/chromedriver_mac64.zip
        FILE_NAME=chromedriver_mac64.zip
    fi
    wget $LINK
    unzip -d /usr/local/bin $PWD/$FILE_NAME
    rm $PWD/$FILE_NAME
fi

python3 download_script.py
gunicorn --bind 0.0.0.0:5000 wsgi:app