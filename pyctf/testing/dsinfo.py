#! /usr/bin/env python

import os
import math
import numpy as np
import pyctf
from pyctf import ctf
from pyctf.sensortopo import sensortopo
from pylab import plot, show

# Get the dataset name from the environment variable $ds
ds = pyctf.dsopen(os.environ['ds'])

s = sensortopo(ds)
#s = ds.sensortopo()

#coeffInfo = {}
#for ci in ds.r.coeffInfo:
#    name = ci[ctf.ci_sensorName]
#    i = ds.getChannelIndex(name)
#    if ds.getChannelType(i) == ctf.TYPE_MEG and ci[ctf.ci_type] == 'G3BR':
#        coeffInfo[name] = ci[ctf.ci_sensorList]

#ch = ds.channel['HADC003']
#adc = ds.getDsData(0, ch)

m = ds.dewar_to_head    # 4x4 transform for verts
r = m[0:3, 0:3]         # 3x3 rotation for normals

C = ds.getNumberOfChannels()
for i in range(C):
    name = ds.getChannelName(i)
    typ = ds.getChannelType(i)
    sr = ds.r.sensRes[i][0]
    crd = ds.r.sensRes[i][1]
    pol = -np.sign(sr[ctf.sr_properGain])
    #go = sr[ctf.sr_gradOrder]
    #sp = sr[ctf.sr_stimPol]
    if typ == ctf.TYPE_MEG or typ < 2:
	c0 = crd[0]
	x = c0[ctf.cr_x]
	y = c0[ctf.cr_y]
	z = c0[ctf.cr_z]
	nx = pol * c0[ctf.cr_nx]
	ny = pol * c0[ctf.cr_ny]
	nz = pol * c0[ctf.cr_nz]

	a = c0[ctf.cr_area]
	radius = math.sqrt(a / math.pi)

	# Transform to head coordinates.

	hx, hy, hz, hw = np.dot(m, np.array([x, y, z, 1.]))
	hnx, hny, hnz = np.dot(r, np.array([nx, ny, nz]))

	nc = sr[ctf.sr_numCoils]

	if nc == 2:
	    c1 = crd[1]
	    x1 = c1[ctf.cr_x]
	    y1 = c1[ctf.cr_y]
	    z1 = c1[ctf.cr_z]
	    a = np.array([x, y, z])
	    b = np.array([x1, y1, z1])
	    baseline = math.sqrt(((b - a)**2).sum())
	    print name, hx, hy, hz, hnx, hny, hnz, radius, baseline
	else:
	    print name, hx, hy, hz, hnx, hny, hnz, radius

exit()

M = ds.getNumberOfPrimaries()
x = ds.getDsArray(0)

s.plot(x[:, 0]); show()

s1 = np.zeros((M,))
for i in range(M):
    s1[i] = math.sqrt(np.dot(x[i], x[i]) / len(x[i]))

x *= adc

s2 = np.zeros((M,))
for i in range(M):
    s2[i] = math.sqrt(np.dot(x[i], x[i]) / len(x[i]))

print s2[0] / s1[0]
plot(s2 / s1); show()
#plot(s1); show()

s.plot(s2 / s1); show()
#s.plot(s1); show()
