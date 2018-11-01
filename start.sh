#!/bin/bash

os=`uname`
if [[ "$os" == 'Darwin' ]]; then
    PYTHONPATH=~/git/insight-core FLASK_APP=run.py FLASK_DEBUG=1 python3 -m flask run --host=0.0.0.0 --port=5002
else
    PYTHONPATH=~/git/insight-core FLASK_APP=run.py FLASK_DEBUG=1 python3 -m flask run --host=0.0.0.0 --port=5002 > dt.log 2>&1 &
fi
