#! /usr/bin/env python

import pyctf
import pylab
from math import pi, sqrt
import numpy
from pyctf.fid import fid, fid_transform

import sys
dsname = sys.argv[1]
#dsname = "/tmp/VKZEKTMO_rest_20050711_01.ds"
#dsname = "/home/tomh/MEG_Noise_20090323_01.ds"
#dsname = "/tako_data3/tomh/20050711/VKZEKTMO_rest_20050711_01.ds"
#dsname = "/data1/pacing/tomh_pacing_20041104_01.ds"
print 'dataset', dsname

ds = pyctf.dsopen(dsname)
print 'sample rate is', ds.getSampleRate()
print 'number of trials is', ds.getNumberOfTrials()
print 'number of samples per trial is', ds.getNumberOfSamples()

for k in ds.marks.keys():
	print '%d %s marks' % (len(ds.marks[k]), k)

def dump(a, fn = "/tmp/moo"):
	f = open(fn, "w")
	for val in a:
		f.write("%g\n" % val)
	f.close()

"""
n = ds.getNumberOfSamples() / ds.getSampleRate()
for t in [0, n / 2, n]:
	print t, ds.getSampleNo(t)

def Point2Array(p):
	return numpy.array([p.getX(), p.getY(), p.getZ()])

nasion = pyctf.Point()
le = pyctf.Point()
re = pyctf.Point()
ds.getMsdHeadCoilPositions(nasion, le, re)
nasion = Point2Array(nasion)
le = Point2Array(le)
re = Point2Array(re)

print 'measured coil positions relative to dewar'
print 'nasion', nasion
print 'le', le
print 're', re

m = fid(nasion, le, re)

print 'transformed into fid basis'
print 'nasion', fid_transform(m, nasion)
print 'le', fid_transform(m, le)
print 're', fid_transform(m, re)

nasion = pyctf.Point()
le = pyctf.Point()
re = pyctf.Point()
ds.getFiducials(nasion, le, re)
nasion = Point2Array(nasion)
le = Point2Array(le)
re = Point2Array(re)

print 'measured coil positions relative to head'
print 'nasion', nasion
print 'le', le
print 're', re

#print ds.rotAndTransMatrix();

#       // dewar to head transform
#       const SMatrix& rotAndTransMatrix();
"""

print 'get data'
l = numpy.zeros((ds.getNumberOfPrimaries(),))
l[:] = ds.getPriArray(0)[:, 350]

dump(l, "/tmp/moo")

pylab.plot(l)
pylab.show()

sys.exit(0)
cname = 'MRF12'
c = ds.getChannel(cname)
print 'channel', cname
print 'number of coils is', c.getNumberOfCoils()
print 'gradiometer order is', c.getGradOrder()
for coil in range(c.getNumberOfCoils()):
	print 'coil', coil
	print 'number of turns is', c.getNumberOfCoilTurns(coil)
	print 'area is', c.getCoilArea(coil)
	print 'radius is %g' % sqrt(c.getCoilArea(coil) / pi)
	p = c.getHeadCoilPosition(coil)
	print 'position is', [p.getX(), p.getY(), p.getZ()]
	p = c.getHeadCoilOrientation(coil)
	print 'orientation is', [p.getX(), p.getY(), p.getZ()]

"""
	const Point& getDewarCoilPosition(Coil_t coilNum);
	const Point& getDewarCoilOrientation(Coil_t coilNum);
"""

print 'file gradient order is', ds.getFileGradOrder()

ds.removeProcessing()
#x = c.getCopyData(0, 0, ds.getNumberOfSamples())
x = c.getCopyData(0, 1000, 1000)
print x.dtype
pylab.plot(x)
pylab.show()

f = open("/tmp/moo", "w")
for d in x:
	f.write("%g\n" % d)
f.close()
