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

def txt_to_cmplx(line):
    data = [float(x) for x in line.strip().strip("(").strip(")").split(",")]
    return data[0] + 1j * data[1]


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

def read_unkg(filename):
    with open(filename, "r") as f:
        num_G = read_ints(f)[0]
        assert num_G == 32
    unkg = np.loadtxt(filename, skiprows=1)
    nbnd = unkg.shape[0] // 32
    assert np.all(unkg[:, 0].astype(int) == np.repeat(np.arange(1, nbnd+1), 32))
    assert np.all(unkg[:, 1].astype(int) == np.tile(np.arange(1, 32+1), nbnd))
    # sort unkg according to (iband, Gx, Gy, Gz) because the G vectors can be in any order
    # remove iband and iG from data
    unkg = unkg[np.lexsort((unkg[:,0], unkg[:,2], unkg[:,3], unkg[:,4]))][:, 2:]
    return unkg

def read_dmn(filename):
    with open(filename, "r") as f:
        f.readline()
        nbnd, nsym, nir, nk = read_ints(f)
        f.readline()
        ik2ir = []
        for line in f:
            if len(line.strip()) == 0: break
            ik2ir += [int(x) for x in line.split()]

        ir2ik = []
        for line in f:
            if len(line.strip()) == 0: break
            ir2ik += [int(x) for x in line.split()]

        iks2k = []
        for ir in range(nir):
            iks2k += [[]]
            for line in f:
                if len(line.strip()) == 0: break
                iks2k[-1] += [int(x) for x in line.split()]

        # count lines until blank, and it is num_wann^2
        data_tmp = []
        for i in range((2*nbnd)**2+1):
            line = f.readline().strip()
            if len(line) == 0: break
            data_tmp += [txt_to_cmplx(line)]
        num_wann = int(np.sqrt(i + 1))
        assert i == num_wann**2
        assert num_wann > 0

        dmn = np.zeros((nir, nsym, num_wann, num_wann), dtype=complex)
        dmn[0, 0, :, :] = np.array(data_tmp).reshape((num_wann, num_wann))
        for ir in range(nir):
            for isym in range(nsym):
                if (ir, isym) == (0, 0): continue
                for iw in range(num_wann):
                    for jw in range(num_wann):
                        dmn[ir, isym, iw, jw] = txt_to_cmplx(f.readline())
                f.readline()

        Dmn = np.zeros((nir, nsym, nbnd, nbnd), dtype=complex)
        for ir in range(nir):
            for isym in range(nsym):
                for i in range(nbnd):
                    for j in range(nbnd):
                        Dmn[ir, isym, i, j] = txt_to_cmplx(f.readline())
                f.readline()

    return dmn, Dmn, ik2ir, ir2ik, iks2k

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
    elif tag == "unkg":
        return read_unkg(filename)
    elif tag == "sym":
        return np.loadtxt(filename, skiprows=1)
    elif tag == "dmn":
        return read_dmn(filename)
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

        if tag == "dmn":
            ref1, ref2, ref_ik2ir, ref_ir2ik, ref_iks2k = ref
            new1, new2, new_ik2ir, new_ir2ik, new_iks2k = new
            for ref, new, name in zip([ref1, ref2], [new1, new2], ["dmn", "Dmn"]):
                if verbose:
                    print(f"Tag {tag}, {name}")
                    print(f"Shape {ref.shape}")
                    print(f"Value {np.linalg.norm(ref)}")
                    print(f"Error {np.linalg.norm(ref - new)}")
                assert ref.shape == new.shape, f"{prefix}: {tag} {name} shape"
                assert np.allclose(ref, new, atol=1E-9), f"{prefix}: {tag} {name} value"
            assert ref_ik2ir == new_ik2ir, "ik2ir"
            assert ref_ir2ik == new_ir2ik, "ir2ik"
            assert ref_iks2k == new_iks2k, "iks2k"
            continue

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
