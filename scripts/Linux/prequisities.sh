#!/bin/bash
if ! [ -x "$(command -v pyenv)" ]; then
	echo 'Nie znaleziono polecenia pyenv (Instalacja: ./install_pyenv.sh)'
	exit
fi
pyenv install 2.7.15
echo "2.7.15" > ~/.pyenv/version
sudo apt-get install libboost-all-dev
sudo apt-get install scons
sudo apt install python-pip
pip install -U Flask
pip install flask-socketio
pip install eventlet
sudo apt install python-pytest
