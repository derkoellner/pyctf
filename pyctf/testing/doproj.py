#! /usr/bin/env python

import sys, getopt
import numpy as np
from numpy.linalg import inv
import h5py
import nibabel
import pyctf

__usage = """-d ds -w nii -p projections

Reads a dataset in .hdf5 format and a SAM weight file in .nii
format, and creates projections."""

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
        dsname = arg
    elif opt == '-w':
        nii = arg
    elif opt == '-p':
        projfile = arg

n = nibabel.load(nii)
wts = n.get_data()
affine = n.get_affine()
ainv = inv(affine)
M = wts.shape[3]

ds = h5py.File(dsname)

srate = ds['srate'].value
marks = ds['marks'][:]
t0, t1 = ds['time'][:]
lo, hi = ds['band'][:]
ntrials = len(ds['trial'].keys())
M1, nsamp = ds['trial/0'].shape

if M1 != M: # etc.
    printerror("wrong number of weights for this dataset")
    sys.exit(1)

#from random import shuffle

idx = []
for x1 in range(wts.shape[2]):
    for y1 in range(wts.shape[1]):
        for z1 in range(wts.shape[0]):
            i = (z1, y1, x1)
            if wts[i].sum() != 0.:
                idx.append(i)
# if -n:
#                shuffle(wts[i])
nvox = len(idx)

proj = h5py.File(projfile, 'w')

proj['affine'] = affine
shape = wts.shape[:3]
proj['shape'] = shape
proj['idx'] = idx

H = np.zeros((nvox, ntrials, nsamp), dtype = 'd')

D = ds['trial'].values()

print 'Projecting data'

nvox = 0
for i in idx:
    h = wts[i]
    vl = []
    for d in D:
        vl.append(h.dot(d))
    H[nvox, ...] = vl
    nvox += 1
    print i

proj['H'] = H
