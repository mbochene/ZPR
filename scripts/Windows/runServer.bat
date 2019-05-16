SET currDir=%cd%
cd %~dp0
cd ../..
Call venv\Scripts\activate
py.test -v src/server/tests
%cd%\src\server\engine\tests\test.exe --log_level=test_suite
py -3 src/server/run.py
Call deactivate
cd %currDir%
