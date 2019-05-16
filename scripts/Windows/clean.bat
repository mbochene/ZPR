SET currDir=%cd%
cd %~dp0
cd ../..
Call scons --clean
del %cd%\src\server\*.pyc >NUL 2>&1
rmdir /s /q %cd%\src\server\__pycache__ %cd%\src\server\tests\__pycache__ >NUL 2>&1
cd %currDir%