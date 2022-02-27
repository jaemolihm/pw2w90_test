#!/bin/bash
set -e

# lib_diam is not tested by default.

if [ $# -eq 0 ]; then
  args="si si_scdm_erfc si_scdm_gaussian si_scdm_isolated benzene pt gaas gaas_nosoc col_fe_up col_fe_dn col_fe_paw_up col_fe_paw_dn fe mn3ir unk_si unk_gaas unk_col_fe"
elif [ $1 == "scdm" ]; then
  args="si_scdm_erfc si_scdm_gaussian si_scdm_isolated pt mn3ir"
elif [ $1 == "unk" ]; then
  args="unk_si unk_gaas unk_col_fe"
elif [ $1 == "lib" ]; then
  args="lib_diam"
else
  args="$@"
fi

for folder in $args; do
  cd $folder
  echo "RUNNING $folder test"
  ./run.sh
  cd -
  echo ""
done
