py.test -v ../../src/server/tests
./test --log_level=test_suite >&2
./../../src/server/run.py
