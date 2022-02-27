#!/bin/bash
set -e

PREFIX="o2"

. ../environment_variables

if [ $GENERATE_REFERENCE == "true" ]; then
    echo "Regenerate reference data for $PREFIX"
    mkdir -p reference
    # SCF, NSCF
    $RUN_PARA_PREFIX $QE_REF/pw.x $RUN_PARA_SUFFIX_POOL -in scf.in > scf.out
    $RUN_PARA_PREFIX $QE_REF/pw.x $RUN_PARA_SUFFIX_POOL -in nscf.in > nscf.out
    $RUN_SERIAL_PREFIX $WANN -pp $PREFIX
    # pw2wannier90 with reference program
    for spin in up dn; do
        $RUN_PARA_PREFIX $QE_REF/pw2wannier90.x $RUN_PARA_SUFFIX_NO_POOL -in pw2wan.$spin.in > reference/pw2wan.$spin.out
        for tag in amn mmn eig unkg; do
            mv $PREFIX.$tag reference/$PREFIX.$spin.$tag
        done
    done
fi

for tag in amn mmn eig spn uHu uIu sHu sIu unkg; do
    rm -f $PREFIX*.$tag*
done

echo "Test $PREFIX without pools"
for spin in up dn; do
    $RUN_PREFIX $QE_TEST/pw2wannier90.x $RUN_SUFFIX_NO_POOL -in pw2wan.$spin.in > pw2wan.$spin.out
    for tag in amn mmn eig unkg; do
        mv $PREFIX.$tag $PREFIX.$spin.$tag
    done
done
./test.py

for tag in amn mmn eig spn uHu uIu sHu sIu unkg; do
    rm -f $PREFIX*.$tag*
done

if [ ! -z "$QE_TEST_SERIAL" ]; then
    echo "Test $PREFIX with serial compilation"
    for spin in up dn; do
        $RUN_SERIAL_PREFIX $QE_TEST_SERIAL/pw2wannier90.x $RUN_SERIAL_SUFFIX -in pw2wan.$spin.in > pw2wan.$spin.out
        for tag in amn mmn eig unkg; do
            mv $PREFIX.$tag $PREFIX.$spin.$tag
        done
    done
    ./test.py
fi

# Gamma only case, so pools cannot be used.
