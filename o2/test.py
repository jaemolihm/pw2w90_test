#!/usr/bin/env python3
import sys
import numpy as np

sys.path.append("../")
from mod_test_pw2wan import *

prefix = "o2"

tag_list = ["amn", "eig", "mmn", "unkg"]

test_pw2wan("o2.up", tag_list)
test_pw2wan("o2.dn", tag_list)

#a, i = read_mmn(f"o2.up.mmn")
#b, j = read_mmn(f"reference/o2.up.mmn")
#print(np.linalg.norm(i - j))
#print(a.shape)
#print(np.amax(abs(a - b), axis=(0,2)))
