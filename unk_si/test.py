#!/usr/bin/env python3
import sys
import numpy as np

sys.path.append("../")
from mod_test_pw2wan import *

prefix = "si"

for i in range(1, 5):
    formatted = i in [2, 4]
    test_unk(8, formatted=formatted, noncolin=False, folder=f"unk_{i}")
