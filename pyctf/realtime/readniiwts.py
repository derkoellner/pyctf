#! /usr/bin/env python

import sys, getopt, os.path, struct
from math import floor
from numpy.linalg import inv
import nibabel

__usage = """niifile [x y z]
Reads a SAM weight file in .nii format. Optionally dump the beamformer at
[x, y, z] (PRI order in mm)."""

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

optlist, args = parseargs("")

for opt, arg in optlist:
    pass

if len(args) != 1 and len(args) != 4:
    printusage()
    sys.exit(1)

niiname = args[0]
nii = nibabel.load(niiname)

data = nii.get_data()       # shape is Z, Y, X, M
affine = nii.get_affine()
ainv = inv(affine)

def round(x):
    return int(floor(x+.5))

def pri2zyx(p, r, i):
    z, y, x, w = ainv.dot([-r, p, i, 1.])
    return tuple(map(round, [z, y, x]))

if len(args) == 4:
    p, r, i = map(lambda x: float(x), args[1:])
    h = data[pri2zyx(p, r, i)]
    for v in h:
        print v
