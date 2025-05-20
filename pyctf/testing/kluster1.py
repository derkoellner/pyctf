#! /usr/bin/python

import sys
#from pylab import ion, plot, clf; ion()
from h5py import File
import nibabel
import numpy as np
from scipy.cluster.vq import kmeans2

f = File(sys.argv[1])

W = f['W'][:]
idx = f['idx'][:]
shape = tuple(f['shape'][:3])
affine = f['affine'][:]

u, w, v = np.linalg.svd(W)
#plot(np.log(w[0:100]))

k = 10
kN, lab = kmeans2(u[:, 0:k], k, iter = 30)

# Sort clusters by size and relabel them.

l = np.zeros((k,), 'i')
for i in range(k):
    l[i] = (lab == i).sum()
a = l.argsort()
for o, n in zip(a, range(1,k+1)):
    l[o] = n
for i in range(len(lab)):
    lab[i] = l[lab[i]]

# Write the labels out.

z = np.zeros(shape, 'f')
for i in range(len(idx)):
    z[tuple(idx[i])] = lab[i]

n = nibabel.Nifti1Image(z, affine)
nibabel.save(n, "/tmp/kluster.nii")

# Write the modes. abs() for visualization purposes.

z = np.zeros(shape + (k,), 'f')
for j in range(k):
    for i in range(len(idx)):
	z[tuple(idx[i]) + (j,)] = abs(u[i, j])

n = nibabel.Nifti1Image(z, affine)
nibabel.save(n, "/tmp/modes.nii")
