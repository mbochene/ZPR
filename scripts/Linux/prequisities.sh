#!/bin/bash
if ! [ -x "$(command -v pyenv)" ]; then
	echo 'Nie znaleziono polecenia pyenv (Instalacja: ./install_pyenv.sh)'
	exit
fi
pyenv install 2.7.16
echo "2.7.16" > ~/.pyenv/version
sudo apt-get install libboost-all-dev
sudo apt-get install scons
sudo apt install python-pip
pip install -U Flask
pip install flask-socketio
pip install eventlet
pip install pytest
#sudo apt install python-pytest
