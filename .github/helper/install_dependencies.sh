#!/bin/bash

# Check for merge conflicts before proceeding
python -m compileall -f $GITHUB_WORKSPACE
if grep -lr --exclude-dir=node_modules "^<<<<<<< " $GITHUB_WORKSPACE
    then echo "Found merge conflicts"
    exit 1
fi

sudo apt update -y && sudo apt install redis-server mariadb-client -y
