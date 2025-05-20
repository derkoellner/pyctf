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
