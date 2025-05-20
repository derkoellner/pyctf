#! /usr/bin/env python

import sys, pyctf
from numpy import *
import nifti

ds = pyctf.dsopen(sys.argv[1])
w, wc = ds.readwts(sys.argv[2])

w = w.astype('f')

# Create qform. Get the coefficients for each coordinate.

m = zeros((4, 4), 'f')
for i in (0, 1, 2):
    n = len(wc[i])
    x0 = wc[i][0] * 1000.   # convert meters to millimeters
    x1 = wc[i][n-1] * 1000.
    a = (x1 - x0) / (n - 1)
    b = x0
    m[i, i] = a
    m[i, 3] = b
m[3, 3] = 1.

# The matrix m above is for PRI, not RAI. The matrix T, here, permutes the
# axes so that the resulting file is displayed properly.

T = array([
    [ 0.,-1., 0., 0. ],
    [ 1., 0., 0., 0. ],
    [ 0., 0., 1., 0. ],
    [ 0., 0., 0., 1. ]])
n = m.copy()
m = dot(T, m)

"""
i = nifti.NiftiImage(w.T)
i.setQForm(m)
i.setFilename("w.nii.gz")
i.save()
"""

f = open('doit.out')
nx, ny, nz = w.shape[0:3]
p = zeros((nx, ny, nz), 'f')
for l in f:
    name, t = l.split()
    if name[0] == 'p' and name[-7:] == '.nii.gz':
	x = int(name[1:3])
	y = int(name[3:5])
	z = int(name[5:7])
	p[x, y, z] = float(t)

i = nifti.NiftiImage(p.T)
i.setQForm(m)
i.setFilename("f.nii.gz")
i.save()
