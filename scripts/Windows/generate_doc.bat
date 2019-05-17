SET currDir=%cd%
cd %~dp0
cd ../../docs
Call doxygen Doxyfile
cd %currDir%