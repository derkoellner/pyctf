#! /usr/bin/env python

import sys
import h5py
import nibabel
import numpy as np

f = h5py.File(sys.argv[1])
exit()
H = f['H']
nvox, ntrials, nsamp = H.shape
affine = f['head/affine'].value
shape = f['head/shape'].value
idx = f['head/idx'].value

Z = np.zeros(shape, 'f')

# avg over trials

for i in range(nvox):
    x = H[i, ...]   # trials by time
    s = 0
    for t in x:
        s += t      # sum envelopes
    s /= ntrials
    Z[tuple(idx[i])] = s

n = nibabel.Nifti1Image(Z, affine)
nibabel.save(n, "/tmp/avgproj.nii")
