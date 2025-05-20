#! /usr/bin/python

import sys
from h5py import File
import nibabel
import numpy as np

f = File(sys.argv[1])

W = f['W'][:]
idx = f['idx'][:]
shape = tuple(f['shape'][:3])
affine = f['affine'][:]
print shape

n = len(idx)
w = np.zeros(shape + (n,), 'f')
i = 0
for col in W.T:
    w[tuple(idx[i])] = col
    i += 1
    if i % 100 == 0: print i

i = nibabel.Nifti1Image(w, affine)
nibabel.save(i, "/tmp/w.nii")
