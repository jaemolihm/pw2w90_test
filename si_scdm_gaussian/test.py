#!/usr/bin/env python3
import sys
import numpy as np

sys.path.append("../")
from mod_test_pw2wan import *

#a = read_amn("si.scdm.amn", scdm=True)
#b = read_amn("reference/si.scdm.amn", scdm=True)
#print(np.sum(abs(a - b), axis=(2,1,)))

prefix = "si"

tag_list = ["amn"]

test_pw2wan(prefix, tag_list, amn_scdm=True)
