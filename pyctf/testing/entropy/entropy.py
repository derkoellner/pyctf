#! /usr/bin/env python

"""
Created on Fri Dec 26 15:42:59 2014

@author: tomh
"""

import sys
import h5py
import nibabel
from numpy import zeros, pi, linspace
from pylab import plot, show
from pyctf.st import hilbert

#ds = pyctf.dsopen(sys.argv[1])
#dsname = "/home/tomh/projects/AEDTPJOU_nback_20050422_01.ds"
#ds = pyctf.dsopen(dsname)

#dsname = "/home/tomh/projects/pyctf/testing/filtered/AEDTPJOU_9r0_gamma"
dsname = "/home/tomh/projects/pyctf/testing/filtered/AEDTPJOU_9r0_theta"
#projname = "/home/tomh/projects/pyctf/testing/proj/AEDTPJOU_9r0"
projname = "/tmp/AEDTPJOU_9r0"

ds = h5py.File(dsname)

srate = ds['srate'].value
marks = ds['marks'][:]
t0, t1 = ds['time'][:]
lo, hi = ds['band'][:]
ntrials = len(ds['trial'].keys())
M, nsamp = ds['trial/0'].shape
tr = ds['trial']
trials = tr.keys()

proj = h5py.File(projname)

affine = proj['affine'][:]
shape = tuple(proj['shape'][:3])
idx = proj['idx'][:]

H1 = proj['H1'][:]
H2 = proj['H2'][:]
nvox, ntrials, nsamp = H1.shape

R = zeros((ntrials, 125), dtype = 'D')
X0 = zeros((ntrials, 125), dtype = 'D')
Z = zeros(shape, 'f')

for v0 in range(nvox):
    s = H1[v0, :, 75:200].copy()
    s /= abs(s)
    #s /= s.real * s.real + s.imag * s.imag
    X0[...] = s.conj()

    S = 0.
    for v in range(nvox):
	X = H2[v, :, 75:200].copy()
	X /= abs(X)
	#X /= X.real * X.real + X.imag * X.imag
	R[...] = X0 * X                 # relative phase, a.conj() * b
	s = R.sum(axis=1) / R.shape[1]  # .sum complex phases over time
	q = s.real * s.real + s.imag * s.imag
	S += q.sum() / q.shape[0]

    Z[tuple(idx[v0])] = S / nvox
    print(v0)

n = nibabel.Nifti1Image(Z, affine)
nibabel.save(n, "/tmp/testphase.nii")

#f = h5py.File("/tmp/mu.hdf", 'w')
#f['relph'] = R
#f.close()
