#!/bin/bash
if ! [ -x "$(command -v pyenv)" ]; then
	echo 'Nie znaleziono polecenia pyenv'
	echo 'Aby zainstalowac potrzebne pakiety, najpierw zainstaluj pyenv wykonajac skrypt install_pyenv.sh, a nastepnie ponownie wykonaj skrypt prequisities.sh'
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
