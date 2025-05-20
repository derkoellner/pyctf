#! /usr/bin/env python

import sys, pyctf
import numpy as np

ds = pyctf.dsopen(sys.argv[1])
w, coords = ds.readwts(sys.argv[2])

def pri2wts(pri):
	# convert to meters
	x, y, z = pri / 100.
	# convert to .svl coordinates
	x, y, z = pyctf.PRI2WtsIdx(coords, x, y, z)
	# get the weights
	try:
		v = w[x, y, z]
	except:
		v = None
	return v

"""
while 1:
	print 'PRI?'
	l = sys.stdin.readline()
	if len(l) == 0:
		break
	pri = np.array(map(float, l.split()))
	v = pri2wts(pri)
	print v
"""

for x in range(w.shape[0]):
  for y in range(w.shape[1]):
    for z in range(w.shape[2]):
      B = w[x, y, z]
      if B.sum() != 0.:
	print '*',
      else:
	print ' ',
    print
