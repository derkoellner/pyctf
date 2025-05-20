#! /usr/bin/env python

import sys
import numpy as np
import pyctf
from pyctf import cmap
from PIL import Image

dsname = sys.argv[1]

ds = pyctf.dsopen(dsname)
c = np.load("/tmp/moo.npy")
N = c.shape[0]

ch0 = ds.getFirstPrimary()

c /= np.trace(c)
#u, w, v = np.linalg.svd(c)

from matplotlib.pyplot import figure, plot, show

C = c.copy()
c = np.sqrt(abs(c))
c -= c.min()
c /= c.max()
c *= 256

m = cmap.meg_cmap(np.linspace(0, 1, 256))

pal = m[:,:3].flatten() * 255
pal = np.uint8(pal).tolist()

i = Image.fromarray(c)
p = i.convert(mode = 'P')
p.putpalette(pal)
p.show()
