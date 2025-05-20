#! /usr/bin/python

import sys
from h5py import File
import nibabel
import numpy as np
from scipy.cluster.vq import kmeans2
from scipy.sparse.linalg import lobpcg

f = File(sys.argv[1])

W = f['W'][:]
idx = f['idx'][:]
shape = tuple(f['shape'][:3])
affine = f['affine'][:]

# Compute the graph matrix Laplacian (rw).

d = W.sum(axis=1)
I = np.eye(W.shape[0])
D = d * I
Dinv = (1. / d) * I
L = Dinv.dot(D - W)

print "SVD graph Laplacian"
u, w, v = np.linalg.svd(L)

#print "SVD raw weight matrix"
#u, w, v = np.linalg.svd(W)
#print "sparse solve graph Laplacian"
#w, v = lobpcg(L, x, b, ...)

k = 20
##kN, lab = kmeans2(u[:, :k], k)
kN, lab = kmeans2(u[:, -k-1:-1], k, iter = 20) # don't include the single eigenvalue 0 vector ([-1])

# Sort clusters by size and relabel them.

l = np.zeros((k,), 'i')
for i in range(k):
    l[i] = (lab == i).sum()
a = l.argsort()
for x in a:
    print l[x]
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
