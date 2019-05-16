#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR/../..
scons --clean
rm src/server/*.pyc src/server/tests/pytest.pycache 2> /dev/null
rm -r src/server/__pycache__ src/server/tests/__pycache__ src/server/.pytest_cache 2> /dev/null
