#! /usr/bin/env python

import sys
import numpy as np
from numpy.linalg import eig
from functools import cmp_to_key
import pyctf
from pyctf.sensortopo import sensortopo
import matplotlib.pyplot as plt
#from scipy.cluster.vq import kmeans2

if len(sys.argv) != 3:
    print("usage: %s dsname covname" % sys.argv[0])
    sys.exit(1)

dsname = sys.argv[1]
covname = sys.argv[2]

ds = pyctf.dsopen(dsname)
C = ds.readcov(covname)
topo = sensortopo(ds)

# Compute eigenstuff.

w, v = eig(C)

# Sort by eigenvalue, largest first.

def cmp(aa, bb):
    a = aa[0]
    b = bb[0]
    if a < b: return 1
    if a > b: return -1
    return 0

wv = list(zip(w, v.T))
wv.sort(key = cmp_to_key(cmp))

#w = np.array(map(lambda x: x[0], wv))
v = np.array(map(lambda x: x[1], wv)).T

# Now the columns of v are the eigenvectors.

topo.plot(v[:, 2], label = False)
#topo.plot(v[:, 2])


"""

k = 5
j = 1
for i in range(k * 2):
    if i == 3:
        plt.title(covname)
    plt.subplot(2, k, j)
    j += 1
    topo.plot(v[:, i])


k = 5
kN, lab = kmeans2(v[:, 0:k], k, iter = 30)

j = 1
for w in range(k):
    z = 0.
    for i in range(k):
        z += kN[w][i] * v[:, i]
    if w == 3:
        plt.title(covname)
    plt.subplot(2, k, j)
    j += 1
    topo.plot(z)

for i in range(k):
    plt.subplot(2, k, j)
    j += 1
    topo.plot(lab == i)

"""

plt.show()

