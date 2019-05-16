#cd do katalogu głównego
py.test -v src/server/tests
src/server/engine/tests/test.exe --log_level=test_suite
py -3 src/server/run.py
