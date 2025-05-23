#!/bin/bash

if [ -z "$CHECK_RUN_BUILT" ]; then
    export CHECK_RUN_BUILT=1
    vite build --config=./check_run/public/js/vite.config.js
    bench build --app check_run
else
    echo "Build already executed (CHECK_RUN_BUILT is set). Skipping."
fi
