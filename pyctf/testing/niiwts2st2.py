#! /usr/bin/env python

import sys, getopt, os.path, struct
from math import floor
import numpy as np
from numpy.linalg import inv
import h5py
import nibabel
import pyctf
from pyctf.st import st

__usage = """[options] -d "ds1 ds2" -w "nii1 nii2" -p "x y z"

Reads datasets in .hdf5 format and SAM weight files in .nii
format, Stockwell transforms the beamformer output for location
[x, y, z] (PRI order in cm), and computes things like relative phase."""

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
        s = arg.split()
        if len(s) != 2:
            printerror('usage: -d "ds1 ds2"')
            printusage()
            sys.exit(1)
        ds1, ds2 = s
    elif opt == '-w':
        s = arg.split()
        if len(s) != 2:
            printerror('usage: -w "nii1 nii2"')
            printusage()
            sys.exit(1)
        nii1, nii2 = s
    elif opt == '-p':
        s = arg.split()
        if len(s) != 3:
            printerror('usage: -p "x y z"')
            printusage()
            sys.exit(1)
        p, r, i = map(lambda x: float(x) * 10., s)

def round(x):
    return int(floor(x+.5))

def primm2zyx(p, r, i, ainv):
    z, y, x, w = ainv.dot([-r, p, i, 1.])
    return tuple(map(round, [z, y, x]))

H = []
for nii in [nii1, nii2]:
    n = nibabel.load(nii)
    data = n.get_data()
    M = data.shape[3]
    affine = n.get_affine()
    ainv = inv(affine)
    H.append(data[primm2zyx(p, r, i, ainv)])

ds = h5py.File(ds1)
ds2 = h5py.File(ds2)

srate = ds['srate'].value
marks = ds['marks'][:]
t0, t1 = ds['time'][:]
lo1, hi1 = ds['band'][:]
lo2, hi2 = ds2['band'][:]
M2 = ds['trial/0'].shape[0]

if M2 != M: # etc.
    printerror("wrong number of weights for this dataset")
    sys.exit(1)

# Convert frequencies in Hz into rows of the ST, given sampling rate and length.

def freq(f, n):
    return round(f * n / srate)

seglen = round((t1 - t0) * srate)
slo1 = freq(lo1, seglen)
shi1 = freq(hi1, seglen)
slo2 = freq(lo2, seglen)
shi2 = freq(hi2, seglen)

# Project all data. One source, two dataset/beamformer pairs.

vlist1 = []
for d in ds['trial'].values():
    vlist1.append(H[0].dot(d))
vlist2 = []
for d in ds2['trial'].values():
    vlist2.append(H[1].dot(d))

orig_st = st
def padst(d, l, h):
    n = len(d) / 2
    a = np.hstack((np.zeros(n), d, np.zeros(n)))
    z = orig_st(a, l * 2, h * 2)
    return z[:, n : n * 3]
st = padst

from pylab import figure, plot, show, scatter
##from plotst import plotst, cm

z1sum = 0.
p1sum = 0.
z2sum = 0.

for i in range(len(vlist1)):

    # Get the complex Stockwell of the low frequency band.
    # Average the phase across frequencies.

    z1 = st(vlist1[i], slo1, shi1)
    p1 = abs(z1)**2
    p1 = p1.sum(axis = 0)
    p1sum += p1
    z1 = z1.sum(axis = 0)
    z1sum += z1             # 1-D complex

    # Get the Stockwell power of the high frequency band.
    # Average the power across frequencies.

    z2 = st(vlist2[i], slo2, shi2)
    z2 = abs(z2)**2
    z2 = z2.sum(axis = 0)
    z2sum += z2             # 1-D real

z1 = z1sum / len(vlist1)
p1 = p1sum / len(vlist1)
z2 = z2sum / len(vlist1)

Z = z2
figure()
plot(np.linspace(t0, t1, len(Z)), Z)

#Z = p1
#figure()
#plot(np.linspace(t0, t1, len(Z)), Z)

Z = np.arctan2(z1.imag, z1.real)
if Z.max() < 0:
    Z += np.pi * 2.
figure()
plot(np.linspace(t0, t1, len(Z)), Z)

figure()
scatter(Z, z2 * 1e20)

"""
plotst(Z, srate,
    start = t0 * srate, end = t1 * srate,
    lo = lo, hi = hi,
    title = ', '.join(marks),
#    cmap = cm.hsv,
    cmap = cm.jet,
    logscale = False)
"""

show()
