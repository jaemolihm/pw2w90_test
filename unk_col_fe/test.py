#!/usr/bin/env python3
import sys
import numpy as np

sys.path.append("../")
from mod_test_pw2wan import *

prefix = "collinear_Fe"

for i in range(1, 3):
    lsda_ispin = i
    test_unk(8, lsda_ispin=lsda_ispin, formatted=False, folder=f"unk_{i}")
