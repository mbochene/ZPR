#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR/../..
sudo apt-get install python3.5
sudo apt-get install libboost-all-dev
sudo apt-get install scons
sudo apt install python-pip
pip install --user virtualenv
virtualenv venv
virtualenv -p /usr/bin/python3.5m venv
source venv/bin/activate
pip install -U Flask
pip install flask-socketio
pip install eventlet
pip install pytest
