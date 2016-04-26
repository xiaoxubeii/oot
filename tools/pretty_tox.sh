#!/usr/bin/env bash

set -o pipefail

TESTRARGS=$1

if [[ "$TESTARGS" =~ "until-failure" ]]; then
    python setup.py testr --slowest --testr-args="$TESTRARGS"
else
    python setup.py testr --slowest --testr-args="--subunit $TESTRARGS" | subunit-trace -f
fi
