#!/usr/bin/env python3
import sys
import numpy as np
from termcolor import colored

sys.path.append("/group2/jmlim/dipole/test_pw2wan")
from mod_test_pw2wan import *

def read_chk_fmt(filename):
    f = open(filename)
    header = f.readline()
    num_bands = read_ints(f)[0]
    num_exclude_bands = read_ints(f)[0]
    exclude_bands = []
    for i in range(num_exclude_bands):
        exclude_bands += read_ints(f)

    real_lattice = read_floats(f)
    recip_lattice = read_floats(f)
    num_kpts = read_ints(f)[0]
    mp_grid = read_ints(f)
    kpt_latt = []
    for i in range(num_kpts):
        kpt_latt += [read_floats(f)]
    nntot = read_ints(f)[0]
    num_wann = read_ints(f)[0]
    checkpoint = f.readline().strip()
    idum = read_ints(f)[0]
    have_disentangled = idum == 1

    if have_disentangled:
        raise NotImplementedError("have_disentangled not implemented")

    u_matrix = np.zeros((num_wann, num_wann, num_kpts), dtype=complex)
    for ik in range(num_kpts):
        for j in range(num_wann):
            for i in range(num_wann):
                data = read_floats(f)
                u_matrix[i, j, ik] = data[0] + 1j * data[1]

    m_matrix = np.zeros((num_wann, num_wann, nntot, num_kpts), dtype=complex)
    for ik in range(num_kpts):
        for ib in range(nntot):
            for j in range(num_wann):
                for i in range(num_wann):
                    data = read_floats(f)
                    m_matrix[i, j, ib, ik] = data[0] + 1j * data[1]

    wannier_centres = np.zeros((3, num_wann))
    for i in range(num_wann):
        wannier_centres[:, i] = read_floats(f)

    wannier_spreads = np.zeros((num_wann))
    for i in range(num_wann):
        wannier_spreads[i] = read_floats(f)[0]

    f.close()

    return u_matrix, m_matrix, wannier_centres, wannier_spreads


file1 = "diam.chk.fmt"
file2 = "reference/diam.chk.fmt"
u1, m1, wc1, ws1 = read_chk_fmt(file1)
u2, m2, wc2, ws2 = read_chk_fmt(file2)

assert np.allclose(u1, u2, atol=1E-9)
assert np.allclose(m1, m2, atol=1E-9)
assert np.allclose(wc1, wc2, atol=1E-9)
assert np.allclose(ws1, ws2, atol=1E-9)
print(colored('PASSED', 'green'), f": lib_diam test")