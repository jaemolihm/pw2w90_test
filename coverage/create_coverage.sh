#!/bin/bash
set -e

. ../environment_variables

geninfo $QE_TEST/../PP/src/ -b $QE_TEST/../PP/src/ -o ./coverage.info
geninfo $QE_TEST_SERIAL/../PP/src/ -b $QE_TEST_SERIAL/../PP/src/ -o ./coverage_serial.info
geninfo $QE_REF/../PP/src/ -b $QE_REF/../PP/src/ -o ./coverage_ref.info

genhtml coverage.info -o output
genhtml coverage_serial.info -o output_serial
genhtml coverage_ref.info -o output_ref
