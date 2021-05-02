#!/usr/bin/env python3
import sys
import numpy as np

sys.path.append("../")
from mod_test_pw2wan import *

prefix = "GaAs"

tag_list = ["amn", "eig", "mmn"]
test_pw2wan(prefix, tag_list)

# a = read_amn(f"{prefix}.amn")
# b = read_amn(f"reference/{prefix}.amn")
# print(a)
# print(b)
# print(np.amax(abs(a - b), axis=(0,1,2)))

