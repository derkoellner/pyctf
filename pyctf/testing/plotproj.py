#! /usr/bin/python

import sys
import h5py
from pylab import plot, figure, show
from pyctf.st import st, hilbert
from plotst import plotst

h = h5py.File(sys.argv[1])

a = h['H'][2, :]

b = a.sum(axis=0) / a.shape[0]
#plot(b)

z = abs(st(b, 0, 40))

#z = 0
#for d in a:
#    s = abs(st(d, 0, 40))
#    z += s
#z /= a.shape[0]

plotst(z, 600., norm = 'norm', logscale = False, range = [0, 5])

show()
