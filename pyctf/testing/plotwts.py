#! /usr/bin/env python

import sys, pyctf
from pyctf.sensortopo import sensortopo
from pylab import show

ds = pyctf.dsopen(sys.argv[1])
w, coords = ds.readwts(sys.argv[2])
#i, j, k = map(int, sys.argv[3:6])
i = int(sys.argv[3])

print w.shape

s = sensortopo(ds)
#s.plot(w[i, j, k])
s.plot(w[i, :])
show()
