SET currDir=%cd%
cd %~dp0
cd ../..
rmdir /s /q %cd%\venv >NUL 2>&1
cd %currDir%