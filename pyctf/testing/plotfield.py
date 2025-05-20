#! /usr/bin/env python

import sys, pyctf
from pyctf.sensortopo import sensortopo
from pylab import show

ds = pyctf.dsopen(sys.argv[1])
f = open(sys.argv[2])
x = map(float, f.readlines())
s = sensortopo(ds)
s.plot(x)
show()
