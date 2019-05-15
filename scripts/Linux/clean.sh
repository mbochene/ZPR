#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR/../..
scons --clean
rm src/server/*.pyc
rm -r src/server/__pycache__