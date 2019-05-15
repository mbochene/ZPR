#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR/../..
source venv/bin/activate
cd src/server
py.test -v tests
cd ../../scripts/Linux
./test --log_level=test_suite >&2
cd ../../src/server
./run.py
