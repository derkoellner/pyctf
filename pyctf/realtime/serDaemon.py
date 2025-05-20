#! /usr/bin/env python3

# This client reads frames from the real time server,
# and applies the SER algorithm.

import sys, os
from time import time, sleep
import numpy as np
from ser import ser
from sockstuff import *

# Estimated length of stationarity.

SRATE = 1200
TAU = 30 * SRATE        # seconds * sample rate

# Connect to the server and start reading frames.

sleep(1)
sock = client('', 5555)
S = None
nframes = 0

while True:
    a = sreadarray(sock)
    m, n = a.shape
    if S is None:
        S = ser(m, TAU)
        t0 = time()
    for i in range(n):
        S.add(a[:, i])
    np.save("/tmp/Cinv0", S.r())
    os.rename("/tmp/Cinv0.npy", "/tmp/Cinv.npy")
    t = time() - t0
    nframes += 1
    print("{} frames, {} seconds, {} elapsed.".format(nframes, nframes * n / SRATE, t))
