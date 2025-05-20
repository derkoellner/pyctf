import os, sys
from os import environ
from sys import stderr

try:
    import pyctf
    dsname = environ['ds']
    print >> stderr, "opening dataset %s" % dsname
    ds = pyctf.dsopen(dsname)
except:
    pass

def dump(x, fn='/tmp/moo'):
    f = open(fn, 'w')
    for v in x:
	f.write("%g\n" % v)
    f.close()
