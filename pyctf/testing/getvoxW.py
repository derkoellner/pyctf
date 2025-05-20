#! /usr/bin/python

import sys
from pylab import plot, subplot, figure, draw, clf, ion; ion()
from math import floor
from h5py import File
import nibabel
import numpy as np
from get_PRImm_from_AFNI import get_PRImm_from_AFNI

def round(x):
    return int(floor(x+.5))

def zyx2primm(z, y, x, a):
    l, p, i, w = a.dot([z, y, x, 1.])
    return p, -l, i

def primm2zyx(p, r, i, ainv):
    z, y, x, w = ainv.dot([-r, p, i, 1.])
    return tuple(map(round, [z, y, x]))

f = File(sys.argv[1])

W = f['W'][:]
idx = f['idx'][:]
shape = tuple(f['shape'][:3])
affine = f['affine'][:]
ainv = np.linalg.inv(affine)
H1 = f['H1']
h = f['hilbert']

for p, r, i in get_PRImm_from_AFNI():
    idx1 = primm2zyx(p, r, i, ainv)
    print idx1
    for j in range(len(idx)):
	if np.all(idx1 == idx[j]):
	    break

    # find largest of W[j, ...]

    v = W[j][:]
    a = v.argsort()
    i = a[-1]
    print idx[i], v[i], zyx2primm(idx[i][0], idx[i][1], idx[i][2], affine)

    x = H1[j, :, 75:200]
    x = x.sum(axis=0) / len(x)
    x -= x.mean()
    x /= x.std()

    figure(1)
    clf()
    subplot(211)
    plot(x)
    subplot(212)
    plot(h[i])          # use largest of W[j, ...]
    draw()
