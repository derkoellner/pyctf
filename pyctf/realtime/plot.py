#! /usr/bin/env python

import sys, os
import numpy as np
import matplotlib.pyplot as plt
import pyctf
import readfwd

dsname = sys.argv[1]
fwdname = sys.argv[2]
ds = pyctf.dsopen(dsname)
s = pyctf.sensortopo(ds)
#w, m = pyctf.readfwd(fwdname)
w, m = readfwd.readfwd(fwdname)
s.plot(w[0])
a = plt.gca()
a.set_title(os.path.basename(fwdname))
plt.show()

