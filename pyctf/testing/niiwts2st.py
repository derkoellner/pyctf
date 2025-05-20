#! /usr/bin/env python

import sys, getopt, os.path, struct
from math import floor
import numpy as np
from numpy.linalg import inv
import h5py
import nibabel
import pyctf
from pyctf.st import st

__usage = """[options] -d dataset -w niifile -p "x y z"

Reads a dataset and a SAM weight file in .nii format, and Stockwell
transforms the beamformer output for location [x, y, z] (PRI order in cm)."""

__scriptname = sys.argv[0]

def printerror(s):
    sys.stderr.write("%s: %s\n" % (__scriptname, s))

def printusage():
    sys.stderr.write("usage: %s %s\n" % (__scriptname, __usage))

def parseargs(opt):
    try:
	optlist, args = getopt.getopt(sys.argv[1:], opt)
    except Exception, msg:
	printerror(msg)
	printusage()
	sys.exit(1)
    return optlist, args

optlist, args = parseargs("d:w:p:")

for opt, arg in optlist:
    if opt == '-d':
	dsname = arg
    elif opt == '-w':
	niiname = arg
    elif opt == '-p':
	s = arg.split()
	if len(s) != 3:
	    printerror('usage: -p "x y z"')
	    printusage()
	    sys.exit(1)
	p, r, i = map(lambda x: float(x) * 10., s)

nii = nibabel.load(niiname)

data = nii.get_data()
Z, Y, X, M = data.shape
affine = nii.get_affine()
ainv = inv(affine)

def round(x):
    return int(floor(x+.5))

def pri2zyx(p, r, i):
    z, y, x, w = ainv.dot([-r, p, i, 1.])
    return tuple(map(round, [z, y, x]))

h = data[pri2zyx(p, r, i)]

ds = h5py.File(dsname)

srate = ds['srate'].value
marks = ds['marks'][:]
t0, t1 = ds['time'][:]
lo, hi = ds['band'][:]
M2 = ds['trial/0'].shape[0]

if M2 != M:
    printerror("wrong number of weights for this dataset")
    sys.exit(1)

# Convert frequencies in Hz into rows of the ST, given sampling rate and length.

def freq(f, n):
    return round(f * n / srate)

seglen = round((t1 - t0) * srate)
slo = freq(lo, seglen)
shi = freq(hi, seglen)

vlist = []
for d in ds['trial'].values():
    vlist.append(h.dot(d))

from pylab import plot, show, clf
from plotst import plotst

z = 0.

for v in vlist:
    s = st(v, slo, shi)
    z += np.abs(s)**2
    #p = np.arctan2(s.imag, s.real)

z /= len(vlist)
plotst(z, srate, start = t0 * srate, end = t1 * srate, lo = lo, hi = hi, title = ', '.join(marks), logscale = False)
show()
