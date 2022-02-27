#!/bin/bash
set -e

PREFIX="diam"

. ../environment_variables

if [ $GENERATE_REFERENCE == "true" ]; then
    echo "Regenerate reference data for $PREFIX"
    mkdir -p reference
    # SCF, NSCF
    $RUN_PARA_PREFIX $QE_REF/pw.x $RUN_PARA_SUFFIX_POOL -in scf.in > scf.out
    $RUN_PARA_PREFIX $QE_REF/pw.x $RUN_PARA_SUFFIX_POOL -in nscf.in > nscf.out

    # pw2wannier90 with reference program
    $RUN_SERIAL_PREFIX $QE_REF/pw2wannier90.x $RUN_SERIAL_SUFFIX -in pw2wan.in > pw2wan.out
    mv pw2wan.out reference/
    w90chk2chk.x -u2f $PREFIX
    cp $PREFIX.* reference/
fi

rm diam.chk diam.chk.fmt

echo "Test $PREFIX library mode in serial"
$RUN_SERIAL_PREFIX $QE_TEST/pw2wannier90.x $RUN_SERIAL_SUFFIX -in pw2wan.in > pw2wan.out
w90chk2chk.x -u2f diam
./test.py

if [ ! -z "$QE_TEST_SERIAL" ]; then
    echo "Test $PREFIX library mode with serial compilation"
    $RUN_SERIAL_PREFIX $QE_TEST_SERIAL/pw2wannier90.x $RUN_SERIAL_SUFFIX -in pw2wan.in > pw2wan.out
    ./test.py
fi

