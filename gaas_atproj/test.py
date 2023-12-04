#!/usr/bin/env python3
import sys
import numpy as np

sys.path.append("../")
from mod_test_pw2wan import *

prefix = "GaAs"

tag_list = ["amn", "eig"]

test_pw2wan(prefix, tag_list)

# a = read_spn(f"{prefix}.spn", False)
# # b = read_spn(f"reference/{prefix}.spn", False)
# print(np.amax(abs(a - b), axis=(2)))

