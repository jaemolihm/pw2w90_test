#!/usr/bin/env python3
import sys
import numpy as np

sys.path.append("../")
from mod_test_pw2wan import *

prefix = "mn3ir"

tag_list = ["amn", "eig", "mmn", "spn"]

test_pw2wan(prefix, tag_list, amn_scdm=True)

# a = read_spn(f"{prefix}.spn", False)
# # b = read_spn(f"reference/{prefix}.spn", False)
# print(np.amax(abs(a - b), axis=(2)))

