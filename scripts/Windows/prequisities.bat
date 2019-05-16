pip3 install virtualenv
SET currDir=%cd%
cd %~dp0
cd ../..
virtualenv -p C:\Python37\python.exe venv
Call venv\Scripts\activate
pip3 install -U Flask
pip3 install flask-socketio
pip3 install eventlet
pip3 install pyd
pip3 install pytest
deactivate
cd %currDir