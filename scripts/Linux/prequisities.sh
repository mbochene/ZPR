#!/bin/bash
sudo apt-get update
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
if ! [ -x "$(command -v pyenv)" ]; then
	curl https://pyenv.run | bash
	echo "" >> ~/.bashrc
	echo 'export PATH="~/.pyenv/bin:$PATH"' >> ~/.bashrc
	echo 'eval "$(pyenv init -)"' >> ~/.bashrc
	echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
	exec bash
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
