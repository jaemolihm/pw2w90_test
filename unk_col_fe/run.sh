#!/bin/bash
set -e

PREFIX="collinear_Fe"

. ../environment_variables

if [ $GENERATE_REFERENCE == "true" ]; then
    echo "Regenerate reference data for $PREFIX"
    mkdir -p reference
    # SCF, NSCF
    $RUN_PARA_PREFIX $QE_REF/pw.x $RUN_PARA_SUFFIX_POOL -in scf.in > scf.out
    $RUN_PARA_PREFIX $QE_REF/pw.x $RUN_PARA_SUFFIX_POOL -in nscf.in > nscf.out
    $RUN_SERIAL_PREFIX $WANN -pp $PREFIX
    # pw2wannier90 with reference program
    for imode in 1 2; do
        $RUN_PARA_PREFIX $QE_REF/pw2wannier90.x $RUN_PARA_SUFFIX_NO_POOL -in pw2wan.$imode.in > reference/pw2wan.$imode.out
        mkdir -p reference/unk_$imode
        mv UNK* reference/unk_$imode/
    done
fi

rm -rf unk_*
echo "Test $PREFIX without pools"
for imode in 1 2; do
    $RUN_PREFIX $QE_TEST/pw2wannier90.x $RUN_SUFFIX_NO_POOL -in pw2wan.$imode.in > pw2wan.$imode.out
    mkdir -p unk_$imode
    mv UNK* unk_$imode/
done
./test.py

rm -rf unk_*
echo "Test $PREFIX with pools"
for imode in 1 2; do
    $RUN_PREFIX $QE_TEST/pw2wannier90.x $RUN_SUFFIX_POOL -in pw2wan.$imode.in > pw2wan.$imode.pool.out
    mkdir -p unk_$imode
    mv UNK* unk_$imode/
done
./test.py

if [ ! -z "$QE_TEST_SERIAL" ]; then
    rm -rf unk_*
    echo "Test $PREFIX with pools"
    for imode in 1 2; do
        $RUN_SERIAL_PREFIX $QE_TEST_SERIAL/pw2wannier90.x $RUN_SERIAL_SUFFIX -in pw2wan.$imode.in > pw2wan.$imode.pool.out
        mkdir -p unk_$imode
        mv UNK* unk_$imode/
    done
    ./test.py
fi
