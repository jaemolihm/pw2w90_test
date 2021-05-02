#!/usr/bin/env python3
import sys
import numpy as np

sys.path.append("../")
from mod_test_pw2wan import *

prefix = "Pt"

tag_list = ["mmn", "amn", "eig"]

test_pw2wan(prefix, tag_list, amn_scdm=True)

# a = read_mmn(f"{prefix}.mmn")
# # b = read_mmn(f"reference/{prefix}.mmn")
# b = read_mmn(f"{prefix}.np1.mmn")
# print(np.amax(abs(a - b), axis=(2,3)))