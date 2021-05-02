#!/usr/bin/env python3

import numpy as np
from itertools import islice
from fortio import FortranFile
from termcolor import colored

def get_inds_list(nlist, ind):
    inds_list = np.arange(1, nlist[ind]+1)
    if ind > 0:
        nrepeat = np.product(np.array(nlist[:ind]))
        inds_list = np.repeat(inds_list, nrepeat)
    if ind < len(nlist) - 1:
        ntile = np.product(np.array(nlist[ind+1:]))
        inds_list = np.tile(inds_list, ntile)
    return inds_list


def read_ints(f):
    return [int(x) for x in f.readline().split()]

def read_floats(f):
    return [float(x) for x in f.readline().split()]


def read_amn(filename, scdm=False):
    with open(filename, "r") as f:
        f.readline()
        if scdm:
            nbnd, nk, nproj = [int(x) for x in f.readline().split()[:3]]
        else:
            nbnd, nk, nproj = read_ints(f)
    data = np.loadtxt(filename, skiprows=2)

    # Check indices
    nlist = (nbnd, nproj, nk)
    for i in range(len(nlist)):
        assert np.allclose(data[:, i], get_inds_list(nlist, i))

    amn = data[:, 3] + 1j * data[:, 4]
    return amn.reshape(nk, nproj, nbnd)


def read_eig(filename):
    data = np.loadtxt(filename, skiprows=0)
    nbnd = round(data[-1, 0])
    nk = round(data[-1, 1])

    # Check indices
    nlist = (nbnd, nk)
    for i in range(len(nlist)):
        assert np.allclose(data[:, i], get_inds_list(nlist, i))

    eig = data[:, 2]
    return eig.reshape(nk, nbnd)


def read_mmn(filename):
    with open(filename, "r") as f:
        f.readline()
        nbnd, nk, nnb = read_ints(f)

        mmn = np.zeros((nk, nnb, nbnd, nbnd), dtype=complex)
        inds = []
        block = 1 + nbnd**2
        for ik in range(nk):
            for inb in range(nnb):
                data = list(islice(f, block))
                inds.append(data[0].split())
                data_split = [x.split() for x in data[1:]]
                data_float = np.array(data_split).astype(np.float)
                mmn[ik, inb] = (data_float[:, 0] + 1j * data_float[:, 1]).reshape((nbnd, nbnd))

    return mmn, np.array(inds).astype(int)


def read_spn(filename, formatted):
    if formatted:
        f = open(filename, "r")
        header = f.readline()
        nbnd, nk = read_ints(f)
    else:
        f = FortranFile(filename, mode='r', auto_endian=True, check_file=True)
        header_b = f.read_record(dtype='c')
        header = "".join(a.decode('ascii') for a in header_b)
        nbnd, nk = f.read_record(dtype=np.int32)

    spn = np.zeros((nk, 3, nbnd*(nbnd+1)//2), dtype=complex)
    for ik in range(nk):
        if formatted:
            data = np.array([f.readline().split() for i in range(3*nbnd*(nbnd+1)//2)], dtype=float)
            spn[ik] = (data[:, 0] + 1j * data[:,1]).reshape(3, -1)
        else:
            spn[ik] = f.read_record(dtype=np.complex).reshape(3, -1)

    f.close()
    return spn


def read_uXu(filename, formatted):
    if formatted:
        f = open(filename, "r")
        header = f.readline()
        nbnd, nk, nnb = read_ints(f)
    else:
        f = FortranFile(filename, mode='r', auto_endian=True, check_file=True)
        header_b = f.read_record(dtype='c')
        header = "".join(a.decode('ascii') for a in header_b)
        nbnd, nk, nnb = f.read_record(dtype=np.int32)

    if formatted:
        data = np.array([f.readline().split() for i in range(nk*nnb*nnb*nbnd*nbnd)], dtype=float)
        uxu = (data[:,0] + 1j*data[:,1]).reshape(nk, nnb, nnb, nbnd, nbnd)
    else:
        uxu = np.zeros((nk, nnb, nnb, nbnd, nbnd), dtype=complex)
        for ik in range(nk):
            for ib2 in range(nnb):
                for ib1 in range(nnb):
                    data = f.read_record('f8').reshape((2,nbnd,nbnd),order='F').transpose(2,1,0)
                    uxu[ik, ib2, ib1] = data[:,:,0] + 1j*data[:,:,1]
    f.close()
    return uxu


def read_sXu(filename, formatted):
    if formatted:
        f = open(filename, "r")
        header = f.readline()
        nbnd, nk, nnb = read_ints(f)
    else:
        f = FortranFile(filename, mode='r', auto_endian=True, check_file=True)
        header_b = f.read_record(dtype='c')
        header = "".join(a.decode('ascii') for a in header_b)
        nbnd, nk, nnb = f.read_record(dtype=np.int32)

    if formatted:
        data = np.array([f.readline().split() for i in range(nk*nnb*3*nbnd*nbnd)], dtype=float)
        sxu = (data[:,0] + 1j*data[:,1]).reshape(nk, nnb, 3, nbnd, nbnd)
        sxu = np.moveaxis(sxu, 2, -1)
    else:
        sxu = np.zeros((nk, nnb, nbnd, nbnd, 3), dtype=complex)
        for ik in range(nk):
            for inb in range(nnb):
                for ipol in range(3):
                    data = f.read_record('f8').reshape((2,nbnd,nbnd),order='F').transpose(2,1,0)
                    sxu[ik,inb,:,:,ipol] = data[:,:,0] + 1j*data[:,:,1]
    f.close()
    return sxu


def read_pw2wan_file(filename, tag, amn_scdm=False):
    # TODO: dmn
    if tag == "amn":
        return read_amn(filename, scdm=amn_scdm)
    elif tag == "eig":
        return read_eig(filename)
    elif tag == "mmn":
        return read_mmn(filename)
    elif tag == "spn":
        return read_spn(filename, formatted=False)
    elif tag == "spn.formatted":
        return read_spn(filename, formatted=True)
    elif tag == "uHu" or tag == "uIu":
        return read_uXu(filename, formatted=False)
    elif tag == "uHu.formatted" or tag == "uIu.formatted":
        return read_uXu(filename, formatted=True)
    elif tag == "sHu" or tag == "sIu":
        return read_sXu(filename, formatted=False)
    elif tag == "sHu.formatted" or tag == "sIu.formatted":
        return read_sXu(filename, formatted=True)
    else:
        raise NotImplementedError(f"tag {tag} not implemented")

def test_pw2wan(prefix, tag_list, verbose=False, amn_scdm=False):
    prefix_ref = f"reference/{prefix}"

    for tag in tag_list:
        ref = read_pw2wan_file(f"{prefix_ref}.{tag}", tag, amn_scdm=amn_scdm)
        new = read_pw2wan_file(f"{prefix}.{tag}", tag, amn_scdm=amn_scdm)

        if tag == "mmn":
            ref, inds_ref = ref
            new, inds_new = new

        if verbose:
            print(f"Tag {tag}")
            print(f"Shape {ref.shape}")
            print(f"Value {np.linalg.norm(ref)}")
            print(f"Error {np.linalg.norm(ref - new)}")

        assert ref.shape == new.shape, f"{prefix}: {tag} shape"
        assert np.allclose(ref, new, atol=1E-9), f"{prefix}: {tag} value"
        if tag == "mmn":
            assert np.allclose(inds_ref, inds_new), f"{prefix}: mmn indices"

    print(colored('PASSED', 'green'), f": {prefix} test")
