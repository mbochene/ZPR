#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR/../..
source venv/bin/activate
#py.test -v src/server/tests
./src/server/engine/tests/test --log_level=test_suite >&2
./src/server/run.py
