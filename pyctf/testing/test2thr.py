#! /usr/bin/env python

from __future__ import division

import sys, getopt, os
from math import floor
from threading import Thread
import numpy as np
from numpy.linalg import inv
import h5py
import nibabel
import pyctf
from project import projectHD

NPROC = os.sysconf('SC_NPROCESSORS_ONLN')
print 'NPROC =', NPROC

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
data1 = n.get_data()
affine = n.get_affine()
ainv = inv(affine)
M = data1.shape[3]

n = nibabel.load(nii2)
data2 = n.get_data()

ds1 = h5py.File(ds1)
ds2 = h5py.File(ds2)

srate = ds1['srate'].value
marks = ds1['marks'][:]
t0, t1 = ds1['time'][:]
lo1, hi1 = ds1['band'][:]
lo2, hi2 = ds2['band'][:]
M1 = ds1['trial/0'].shape[0]

if M1 != M: # etc.
    printerror("wrong number of weights for this dataset")
    sys.exit(1)

D1 = ds1['trial'].values()
D2 = ds2['trial'].values()

ntrials = len(D1)
nchan, nsamp = D1[0].shape

"""
from pyctf.paramDict import paramDict

param = paramDict("/home/tomh/nback/theta.param")
X = np.array(param['XBounds']) * 10.
Y = np.array(param['YBounds']) * 10.
Z = np.array(param['ZBounds']) * 10.
step = param['ImageStep'] * 10.
"""

idx = []
for x1 in range(data1.shape[2]):
    for y1 in range(data1.shape[1]):
        for z1 in range(data1.shape[0]):
            i = (z1, y1, x1)
            if data1[i].sum() != 0.:
                idx.append(i)
nvox = len(idx)

# Create the HDF5 file. Write some header info and
# reserve all the space we'll need.

proj = h5py.File(projfile, 'w')

proj['affine'] = affine
proj['shape'] = data1.shape
proj['idx'] = idx
proj['W'] = np.zeros((nvox, nvox))
proj['H1'] = np.zeros((nvox, ntrials, nsamp))
proj['H2'] = np.zeros((nvox, ntrials, nsamp))
proj['hilbert'] = np.zeros((nvox, nsamp))

# Split the work among a pool of worker threads.

NTHREAD = NPROC

def worker(n, idx, out):
    for i in idx:
        h1 = data1[i]
        h2 = data2[i]
        r1 = projectHD(h1, D1)
        r2 = projectHD(h2, D2)
        out.append((r1, r2))
        n += 1
        if n % 100 == 0:
            print n

I = idx
idxes = []
n = int(len(I) / NTHREAD)
while 1:
    idxes.append(I[:n])
    I = I[n:]
    if len(I) < n:
        idxes[-1].extend(I)
        break

outs = [[] for x in range(NTHREAD)]

threads = []

n = 0
for i in range(NTHREAD):
    t = Thread(target = worker, args = (n, idxes[i], outs[i]))
    t.start()
    threads.append(t)
    n += len(idxes[i])

for t in threads:
    t.join()

# Write results to the HDF5 file.

H1 = proj['H1']
H2 = proj['H2']
vox = 0
for out in outs:
    for o in out:
        H1[vox, :] = o[0]
        H2[vox, :] = o[1]
        print vox
        vox += 1
