#! /usr/bin/env python

import sys, getopt
import numpy as np
import h5py
from pyctf.st import hilbert

__usage = """[options] -p projections

Reads projections file in .hdf5 format, and does analyses."""

__scriptname = sys.argv[0]

def printerror(s):
    sys.stderr.write("%s: %s\n" % (__scriptname, s))

def printusage():
    sys.stderr.write("usage: %s %s\n" % (__scriptname, __usage))

def parseargs(opt):
    try:
        optlist, args = getopt.getopt(sys.argv[1:], opt)
    except Exception as msg:
        printerror(msg)
        printusage()
        sys.exit(1)
    return optlist, args

optlist, args = parseargs("p:")

for opt, arg in optlist:
    if opt == '-p':
        projfile = arg

proj = h5py.File(projfile)

idx = proj['idx'][:]
nvox = len(idx)

H1 = proj['H1']
H2 = proj['H2']

print 'average H2'
h = proj['hilbert']
for j in range(nvox):
    if j % 100 == 0: print j
    xj = H2[j, :, 75:200]
    x = xj.sum(axis=0) / len(xj)
    x -= x.mean()
    x /= x.std()
    h[j, :] = x

h = h[:]        # use np array, not h5py file object
n = len(h[0])

print 'Compute W'
W = proj['W']

w = np.zeros(W.shape)   # use np array, not h5py file object
for i in range(nvox):
    if i % 100 == 0: print i
    x = h[i]
    for j in range(nvox):
        w[i, j] = abs(x.dot(h[j]))

W[:] = w
