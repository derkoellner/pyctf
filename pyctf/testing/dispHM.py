#! /usr/bin/env python

from __future__ import print_function

import sys, os
import pyctf
import numpy
import pylab

THRESH = .5

if len(sys.argv) == 2:
    dsname = sys.argv[1]
elif os.environ.get('ds'):
    dsname = os.environ['ds']
    print('reading dataset', dsname)
else:
    print('usage: {} dataset'.format(sys.argv[0]))
    sys.exit(1)

ds = pyctf.dsopen(dsname)
nsamp = ds.getNumberOfSamples()

t0 = ds.getTimePt(0)
t1 = ds.getTimePt(nsamp - 1)

D = numpy.zeros((nsamp, 3))
print('Coil mean')
for i, s in enumerate(['Na', 'Le', 'Re']):
    n = ds.getHLCData(0, s)
    d = n.mean(axis = 0)
    print(s, d)
    D[:, i] = numpy.sqrt((n * n).mean(axis = 1))
    D[:, i] -= D[0, i]

#exit()

x = D.max(1)
try:
    s = (x > THRESH).tolist().index(True)
    t = ds.getTimePt(s)
    print('Max head movement exceeds threshold of', THRESH, 'at t =', t)
except:
    print('Max head movement does not exceed threshold of', THRESH)

time = pylab.linspace(t0, t1, D.shape[0])
for i in [0, 1, 2]:
    pylab.plot(time, D[:,i])
pylab.title("RMS movement for each fiducial marker")
pylab.xlabel("seconds")
pylab.ylabel("cm")
pylab.show()
