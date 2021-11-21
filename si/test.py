#!/usr/bin/env python3
import sys
import numpy as np

sys.path.append("../")
from mod_test_pw2wan import *

prefix = "si"

tag_list = ["amn", "eig", "mmn", "uHu", "uIu", "unkg"]

test_pw2wan(prefix, tag_list)

# a = read_mmn("si.mmn")
# b = read_mmn("reference/si.mmn")
# print(np.sum(abs(a - b), axis=(1,2,3)))
