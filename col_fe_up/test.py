#!/usr/bin/env python3
import sys
import numpy as np

sys.path.append("../")
from mod_test_pw2wan import *

prefix = "collinear_Fe"

tag_list = ["amn", "eig", "mmn"]
tag_list += ["uIu", "uHu"]

test_pw2wan(prefix, tag_list)

# a = read_uXu(f"{prefix}.uHu", False)
# b = read_uXu(f"reference/{prefix}.uHu", False)
# print(np.amax(abs(a - b), axis=(2,3,4)))
