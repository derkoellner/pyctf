#! /usr/bin/env python

import sys
from pylab import *
import numpy as np
import pyctf
from pyctf import ctf
from pyctf.sensortopo import sensortopo
from pyctf.st import fft

def plural(x):
    if x > 1:
        return 's'
    return ''

dsname = sys.argv[1]
ds = pyctf.dsopen(dsname)

# Some basic things about the dataset.

S = ds.getNumberOfSamples()
M = ds.getNumberOfChannels()
T = ds.getNumberOfTrials()
P = ds.getNumberOfPrimaries()

srate = ds.getSampleRate()

for t in range(T):
    d = ds.getPriArray(t)
#    for m in range(P):
    for m in range(1):
        x = d[m, :]
        x -= x.mean()
        x /= x.var()
        for v in x:
            print(v)

sys.exit()

topo = sensortopo(ds)
topo.make_grid(100)

im, ticks = topo.plot(np.log(t) + 75., zrange = 'auto')
title("70-110 Hz noisy", fontsize = 24)
text(.04, -.07, "%s" % ds.setname, fontsize = 20)
cax = axes([.85, .15, .03, .65])
colorbar(im, cax, format = '%g', ticks = ticks)
show()
