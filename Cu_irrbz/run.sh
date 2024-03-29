#!/bin/bash
set -e

PREFIX="Cu"

. ../environment_variables

if [ $GENERATE_REFERENCE == "true" ]; then
    echo "Regenerate reference data for $PREFIX"
    rm -rf reference/
    mkdir -p reference
    # SCF, NSCF
    $RUN_PARA_PREFIX $QE_REF/pw.x $RUN_PARA_SUFFIX_POOL -in scf.in > scf.out
    $RUN_PARA_PREFIX $QE_REF/pw.x $RUN_PARA_SUFFIX_POOL -in nscf.in > nscf.out
    $RUN_SERIAL_PREFIX $WANN -pp $PREFIX
    # pw2wannier90 with reference program
    $RUN_PARA_PREFIX $QE_REF/pw2wannier90.x $RUN_PARA_SUFFIX_NO_POOL -in pw2wan.in > reference/pw2wan.out
    time python -u $SYMWANNIER/symwannier/write_full_data.py $PREFIX
    cp $PREFIX* reference/
fi

for tag in amn mmn eig spn uHu uIu sHu sIu unkg iamn immn ieig; do
    rm -f $PREFIX*.$tag*
done

echo "Test $PREFIX without pools"
$RUN_PARA_PREFIX $QE_TEST/pw2wannier90.x $RUN_SUFFIX_NO_POOL -in pw2wan.in > pw2wan.out
time python -u $SYMWANNIER/symwannier/write_full_data.py $PREFIX
./test.py

for tag in amn mmn eig spn uHu uIu sHu sIu unkg iamn immn ieig; do
    rm -f $PREFIX*.$tag*
done

# echo "Test $PREFIX with pools"
# $RUN_PARA_PREFIX $QE_TEST/pw2wannier90.x $RUN_SUFFIX_POOL -in pw2wan.in > pw2wan.out
# time python -u $SYMWANNIER/symwannier/write_full_data.py $PREFIX
# ./test.py

# for tag in amn mmn eig spn uHu uIu sHu sIu unkg iamn immn ieig; do
#     rm -f $PREFIX*.$tag*
# done

if [ ! -z "$QE_TEST_SERIAL" ]; then
    for tag in amn mmn eig spn uHu uIu sHu sIu unkg iamn immn ieig; do
        rm -f $PREFIX*.$tag*
    done

    echo "Test $PREFIX with serial compilation"
    $RUN_SERIAL_PREFIX $QE_TEST_SERIAL/pw2wannier90.x -in pw2wan.in > pw2wan.out
    ./test.py
fi
