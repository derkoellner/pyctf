#! /usr/bin/env python

import sys, getopt, os.path, struct
from math import floor
import numpy as np
from numpy.linalg import inv
import h5py
import nibabel
import pyctf
from pyctf.st import hilbert

__usage = """[options] -d "ds1 ds2" -w "nii1 nii2" -p projections

Reads datasets in .hdf5 format and SAM weight files in .nii
format, Stockwell transforms the beamformer output for locations
[x, y, z] (PRI order in cm), and computes things."""

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
        projfile = arg

def round(x):
    return int(floor(x+.5))

def primm2zyx(p, r, i, ainv):
    z, y, x, w = ainv.dot([-r, p, i, 1.])
    return tuple(map(round, [z, y, x]))

n = nibabel.load(nii1)
wts1 = n.get_data()
affine = n.get_affine()
ainv = inv(affine)
M = wts1.shape[3]

n = nibabel.load(nii2)
wts2 = n.get_data()

ds1 = h5py.File(ds1)
ds1h = ds1['head']
ds2 = h5py.File(ds2)
ds2h = ds2['head']

srate = ds1h['srate'].value
marks = ds1h['marks'][:]
t0, t1 = ds1h['time'][:]
lo1, hi1 = ds1h['band'][:]
lo2, hi2 = ds2h['band'][:]
ntrials, M1, nsamp = ds1['trials'].shape

if M1 != M: # etc., could check M2, nsamp2, ...
    printerror("wrong number of weights for this dataset")
    sys.exit(1)

"""
from pyctf.paramDict import paramDict

param = paramDict("/home/tomh/nback/theta.param")
X = np.array(param['XBounds']) * 10.
Y = np.array(param['YBounds']) * 10.
Z = np.array(param['ZBounds']) * 10.
step = param['ImageStep'] * 10.
"""

from random import shuffle

idx = []
for x1 in range(wts1.shape[2]):
    for y1 in range(wts1.shape[1]):
        for z1 in range(wts1.shape[0]):
            i = (z1, y1, x1)
            if wts1[i].sum() != 0. and wts2[i].sum() != 0.:
                idx.append(i)
# if -n:
#                shuffle(wts1[i])
#                shuffle(wts2[i])
nvox = len(idx)

# we're interested in a particular time range, 200 ms starting at resp - .125 ms
hsamp = 200 - 75

proj = h5py.File(projfile, 'w')

h1 = proj.create_group('h1')
h2 = proj.create_group('h2')
proj.copy(ds1h, h1)
proj.copy(ds2h, h2)
proj['affine'] = affine
shape = wts1.shape[:3]
proj['shape'] = shape
proj['idx'] = idx

W = np.zeros((nvox, nvox))

H1 = np.zeros((nvox, ntrials, nsamp), dtype = 'd')
H2 = np.zeros((nvox, ntrials, nsamp), dtype = 'd')
H = np.zeros((nvox, hsamp))

D1 = ds1['trials'][:].real
D2 = ds2['trials'][:]

print 'Projecting data.'

nvox = 0
for i in idx:
    h1 = wts1[i]
    v = map(lambda d: h1.dot(d), D1)
    H1[nvox, ...] = v

    h2 = wts2[i]
    v = map(lambda d: abs(h2.dot(d)), D2)
    H2[nvox, ...] = v

    nvox += 1
    print i

proj['H1'] = H1
proj['H2'] = H2

print 'Average H2 envelopes over trials'

for j in range(nvox):
    if j % 100 == 0: print j
    xj = H2[j, ...]     # trials by time
    s = 0.
    for z in xj:
        s += z          # sum envelopes
    s /= len(xj)
    s = s[75:200]       # trim
    s -= s.mean()       # normalize
    s /= s.std()
    H[j, :] = s

print 'Compute W'

for i in range(nvox):
    if i % 100 == 0: print i
    xi = H1[i, :, 75:200]
    x = xi.sum(axis=0) / len(xi)    # average over trials
    x -= x.mean()                   # normalize
    x /= x.std()
    for j in range(nvox):
        W[i, j] = x.dot(H[j])

proj['W'] = W

"""
print 'Compute relative phases'

R = np.zeros((ntrials, 125), dtype = 'D')
X0 = np.zeros((ntrials, 125), dtype = 'D')
Z = np.zeros(shape, 'f')

for v0 in range(nvox):
    x = H1[v0, :, 75:200]
    x = x / abs(x)
    #x = x / (x.real * x.real + x.imag * x.imag)
    X0[...] = x.conj()

    S = 0.
    for v in range(nvox):
        x = H2[v, :, 75:200]
        x = x / abs(x)
        #x = x / (x.real * x.real + x.imag * x.imag)
        R[...] = X0 * x                 # relative phase, a.conj() * b
        s = R.sum(axis=1) / R.shape[1]  # .sum complex phases over time
        q = s.real * s.real + s.imag * s.imag
        S += q.sum() / q.shape[0]

    Z[tuple(idx[v0])] = S / nvox
    print v0

n = nibabel.Nifti1Image(Z, affine)
nibabel.save(n, "/tmp/phase.nii")
"""
