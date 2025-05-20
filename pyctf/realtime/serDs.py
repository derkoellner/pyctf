#! /usr/bin/env python

import sys, getopt
from math import floor
import numpy as np
import pyctf
from pyctf.samiir import mkfhilb, dofilt
from pyctf.segments import get_segment_list
from ser import ser

__usage = """-d dataset [-n] -b "lo hi" -m mark... -t "t0 t1"

Read a dataset, bandpass filter it, and apply the SER algorithm.
With -n, substitute real data with realistic noise."""

__scriptname = sys.argv[0]

def printerror(s):
    sys.stderr.write("%s: %s\n" % (__scriptname, s))

def printusage():
    sys.stderr.write("usage: %s %s\n" % (__scriptname, __usage))

def parseargs(opt):
    try:
        optlist, args = getopt.getopt(sys.argv[1:], opt)
    except Exception as msg:
        printerror(msg)
        printusage()
        sys.exit(1)
    return optlist, args

def round(x):
    return int(floor(x + .5))

optlist, args = parseargs("d:nb:m:t:")

dsname = None
mlist = []
noise = False

for opt, arg in optlist:
    if opt == '-d':
        dsname = arg
    elif opt == '-n':
        noise = True
    elif opt == '-b':
        s = arg.split()
        if len(s) != 2:
            printerror('usage: -b "lo hi"')
            printusage()
            sys.exit(1)
        lo, hi = [float(x) for x in s]
    elif opt == '-m':
        mlist.extend(arg.split())
    elif opt == '-t':
        s = arg.split()
        if len(s) != 2:
            printerror('usage: -t "t0 t1"')
            printusage()
            sys.exit(1)
        t0, t1 = [float(x) for x in s]

if dsname is None:
    printerror("Please specify an input dataset.")
    printusage()
    sys.exit(1)

ds = pyctf.dsopen(dsname)

srate = ds.getSampleRate()
nsamp = ds.getNumberOfSamples()
M = ds.getNumberOfPrimaries()
marks = ds.marks

seglist = []
seglen = -1
for m in mlist:
    sl, slen = get_segment_list(ds, m, t0, t1)
    for tr, s in sl:
        seglist.append((tr, s, m))
    if seglen < 0:
        seglen = slen
    else:
        assert seglen == slen

# Sort by trial [0] and time [1].
seglist.sort(key = lambda x: (x[0], x[1]))

# Make a Fhilbert filter: bandpass + Hilbert

filt = pyctf.mkfhilb(lo, hi, srate, nsamp)

if noise:
    from pyctf.meg_noise import meg_noise

lasttr = None
dtyp = 'D'

#d = np.zeros((M, nsamp), dtype = dtyp)
d = np.zeros((M, nsamp), dtype = 'd')

S = ser(M, int(srate * 30))
C = np.zeros((M, M))

for tr, s, m in seglist:
    if tr != lasttr:
        # read and filter the next trial
        print('Trial %d' % tr)
        D = ds.getPriArray(tr)
        for ch in range(M):
            x = D[ch, :] * 1e12     # convert to picoTesla
            x -= x.mean()
            if noise:
                x = meg_noise(nsamp) * x.std()
            x = pyctf.dofilt(x, filt)
            d[ch, :] = x.real
        lasttr = tr

    e = d[:, s : s + seglen]
    C += e.dot(e.T)

    # pass to SER

    for i in range(seglen):
        S.add(d[:, s + i])

C /= len(seglist) * seglen
r = S.r()
r = np.linalg.inv(r)

np.save("/tmp/moo", r)
np.save("/tmp/mu", C)
