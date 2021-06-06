#!/bin/bash
set -e

. ../environment_variables

geninfo $QE_TEST/../PP/src/ -b $QE_TEST/../PP/src/ -o ./coverage.info

genhtml coverage.info -o output