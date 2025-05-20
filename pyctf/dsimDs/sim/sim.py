"""Simulate MEG data."""

import numpy as np
from pyctf import _samlib
from .atlas import getAtlasNode
from .noiseModel import mkNoise

# unused
"""
def simulateRAW(ds, chs, nsamp, noiseLevel, filt):
    "return simulated raw channel data"

    M = len(chs)
    d = np.zeros((M, nsamp))

    for ch in range(M):
        n = mkNoise(nsamp, noiseLevel)  # noise in Tesla
        d[ch, :] = dofilt(n, filt)

    return d
"""

def simulateAtlas(p, atlas, noise):
    "return simulated data, primaries and references are returned separately"

    nsamp = p.Nsamp
    nRef = len(p.ref)
    nPri = len(p.pri)

    dRef = np.zeros((nRef, nsamp))
    dPri = np.zeros((nPri, nsamp))

    cinv = getattr(p, 'cinv', None)

    # for each source
    n = 0
    for pos, ori in getAtlasNode(p, atlas):
        if p.Verbose:
            print(n, end = '\r')
        n += 1

        # Compute the forward solution.

        if cinv:
            Br, Bp, v, cond = _samlib.SolveFwdRefs(cinv, pos)
        else:
            Br, Bp = _samlib.SolveFwdRefs(None, pos, ori)

        # Compute nsamp samples of noise.

        x = mkNoise(p)

        # Add B * x to the channel data.

        dRef += np.outer(Br, x)
        dPri += np.outer(Bp, x)

    if p.Verbose:
        print()

    # Normalize.

    s = np.sqrt(n)                  # central limit theorem
    for ch in range(nRef):
        dRef[ch, :] = dRef[ch] * s
    for ch in range(nPri):
        dPri[ch, :] = dPri[ch] * s

    return dRef, dPri

""" ancient code to produce sinusoidal signals
sim = zeros((Mpri, nsamp))
for d in diplist:
    (nAm, freq, phaseDeg) = d[0]
    nAm /= 1e9
    phase = phaseDeg * pi / 180.
    pos, ori = d[1:3]
    b = nolteFwd.doFwd(pos, ori)
    #b = zeros(Mpri)
    t = arange(newlen) / srate * 2. * pi
    for i, t in enumerate(t):
        sim[:, i] += (nAm * sin(freq * t + phase)) * b
"""

