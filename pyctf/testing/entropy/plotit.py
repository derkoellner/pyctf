#! /usr/bin/env python

import sys
import numpy as np
import h5py
from pylab import plot, show

f = h5py.File(sys.argv[1])
relph = f['relph']

for i in [1200]: #range(relph.shape[0]):
    ch1 = relph[i].T
    plot(ch1.real, ch1.imag, '.')
    #s = ch1.sum(axis=0) / ch1.shape[0]
    #plot(s.real, s.imag, '.')

#plot(ch1[75,:].real, ch1[75,:].imag, 'bo')
#plot(ch1.real, ch1.imag)
show()
