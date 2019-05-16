SET currDir=%cd%
cd %~dp0
cd ../..
Call venv\Scripts\activate
Call scons
cd %currDir%
Call deactivate