#! /usr/bin/env python

import sys, getopt
from math import floor
import numpy as np
from numpy.linalg import inv
import h5py
import nibabel
import pyctf

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

optlist, args = parseargs("d:w:")

for opt, arg in optlist:
    if opt == '-d':
        ds = arg
    elif opt == '-w':
        nii = arg

def round(x):
    return int(floor(x + .5))

def primm2zyx(p, r, i, ainv):
    z, y, x, w = ainv.dot([-r, p, i, 1.])
    return tuple(map(round, [z, y, x]))

n = nibabel.load(nii)
wts = n.get_data()
affine = n.get_affine()
ainv = inv(affine)
M = wts.shape[3]

idx = []
for x in range(wts.shape[2]):
    for y in range(wts.shape[1]):
        for z in range(wts.shape[0]):
            i = (z, y, x)
            if wts[i].sum() != 0.:
                idx.append(i)

nvox = len(idx)
print nvox
print idx[:10]
print idx[-10:]
