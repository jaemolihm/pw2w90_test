#!/usr/bin/env python3
import sys
import numpy as np

sys.path.append("../")
from mod_test_pw2wan import *

prefix = "Fe"

tag_list = ["amn", "eig", "mmn"]
tag_list += ["spn", "uHu", "uIu", "sHu", "sIu"]
tag_list += [x + ".formatted" for x in ["spn", "uHu", "uIu", "sHu", "sIu"]]

test_pw2wan(prefix, tag_list)

# a = read_mmn(f"{prefix}.mmn")
# b = read_mmn(f"reference/{prefix}.mmn")
# print(np.amax(abs(a - b), axis=(1,2,3)))