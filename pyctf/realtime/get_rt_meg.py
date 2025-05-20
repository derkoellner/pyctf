#! /usr/bin/env python3

import sys, time
import numpy as np
import pyctf
from pyctf.samiir import mkfhilb, dofilt
from acq_reader import acq_reader

TYPE_MEG = pyctf.ctf.TYPE_MEG

# This keeps track of the array of channel data. Blocks of samples can be
# added to the end, or removed from the beginning.

class array_manager:

    def __init__(self, m):
        """a = array_manager(num_channels)"""
        self.data = np.zeros(dtype = np.float32, shape = (0, m))
        self.n = 0

    def add_samples(self, a):
        self.data = np.concatenate((self.data, a))
        self.n += a.shape[0]

    def del_samples(self, n):
        self.data = self.data[n:]
        self.n -= n

    def get_samples(self, n):
        if n > self.n:
            print('warning: not enough data in array')
        return self.data[:n]

    def get_nsamples(self):
        return self.n

# Functions for dealing with CTF MEG data.

def sensor_idx(ds, typ = TYPE_MEG):
    """Return a list of the channel indices of the given type."""

    nchan = ds.getNumberOfChannels()
    l = []
    for i in range(nchan):
        if ds.getChannelType(i) == typ:
            l.append(i)
    return l

def sensorlist(ds, typ = TYPE_MEG):
    """Return a list of the channel names in ds, of the given type."""

    nchan = ds.getNumberOfChannels()
    l = []
    for i in range(nchan):
        if ds.getChannelType(i) == typ:
            l.append(ds.getChannelName(i)[:5])
    return l

def gainarray(ds, typ = TYPE_MEG):
    """Return an array of the gains for the channels of the given type."""

    nchan = ds.getNumberOfChannels()
    l = []
    for i in range(nchan):
        if ds.getChannelType(i) == typ:
            l.append(ds.getChannelGain(i))
    return np.array(l, dtype = np.float32).T

# This reads packets from Acq, converts them to frames,
# and then processes the frames.

def get_rt_meg(dir):

    # This can be set with fancier options processing, but for now,

    name = "test"       # name of dir to store frames
    NSAMP = 2400        # size of a frame
    lo = 15             # bandpass edges
    hi = 25

    # Get an acq_reader.

    acq = acq_reader()

    # Wait for collection to begin.

    print("Waiting for collection to begin.")
    dsname = acq.get_dsname()

    # Open the dataset, get channel properties and other info.

    print(dsname)
    ds = pyctf.dsopen(dsname)
    M = ds.getNumberOfPrimaries()
    S = ds.getNumberOfSamples()     # trial size from Acq
    srate = ds.getSampleRate()

    slist = sensorlist(ds)
    meg_idx = sensor_idx(ds)
    gains = gainarray(ds)

    # Set up a filter. This does a bandpass and a Hilbert transform.

    filt = mkfhilb(lo, hi, srate, NSAMP)
    h = np.empty((NSAMP, M), dtype = np.complex128)

    # Set up an array manager.

    a = array_manager(M)

    # This loop processes packets.

    frame = 0
    for sample, packet in acq.packet_gen():

        # Extract just the primaries.

        d = np.take(packet, meg_idx, 1)

        # Apply the gains and add the samples to the array manager.

        a.add_samples(d * gains)

        # Wait until we have enough samples in the array for a frame.

        n = a.get_nsamples()
        if n >= NSAMP:
            x = a.get_samples(NSAMP)

            # Apply the filter and save the result.

            for c in range(M):
                h[:, c] = dofilt(x[:, c], filt)

            with open("%s/%s/f%05d" % (dir, name, frame), "wb") as f:
                np.save(f, h)
            frame += 1

            # Forget old samples we don't need any more.

            a.del_samples(NSAMP)
