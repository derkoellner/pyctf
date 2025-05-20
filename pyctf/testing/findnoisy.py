#! /usr/bin/env python

import sys
import numpy as np
from numpy.fft import fftfreq
from math import floor
import pyctf
from pyctf import ctf
from pyctf.st import fft

dsname = sys.argv[1]
ds = pyctf.dsopen(dsname)

# Some basic things about the dataset.

S = ds.getNumberOfSamples()
M = ds.getNumberOfChannels()
T = ds.getNumberOfTrials()
P = ds.getNumberOfPrimaries()

srate = ds.getSampleRate()

filt = pyctf.mkiir(70., 110., srate)

cts = np.array([ds.getChannelType(m) for m in range(M)])

delta = fftfreq(S * 2, d = 1. / srate)[1]
lo = int(floor(70. / delta + .5))
hi = int(floor(110. / delta + .5))

from pylab import plot, show
A = 0
for m in range(M):
    cht = cts[m]
    if cht == ctf.TYPE_MEG:
	for t in range(T):
	    d = ds.getDsRawData(t, m)
	    d -= d.mean()
	    X = np.zeros((S * 2,))
	    X[S/2 : S/2 + S] = d
	    D = abs(fft(X))
	    A += D[lo : hi]

# Average over trials.

A /= T * P

print dsname, A.max()
