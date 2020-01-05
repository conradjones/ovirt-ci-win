#!/usr/bin/env bash

# /opt/libivrt-executor/prepare.sh

currentDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
python3 ${currentDir}/prepare.py
