#! /usr/bin/env python3

import sys, os
import numpy as np
import matplotlib.pyplot as plt
import pyctf
from get_PRI_from_AFNI import get_PRI_from_AFNI
import nolteFwd
from rawtty import rawtty

if len(sys.argv) != 3:
    print("usage: {} brain+tlrc dataset.ds [covname.cov]".format(sys.argv[0]), file = sys.stderr)
    sys.exit(1)

# Connect to a running AFNI that's set up to send TLRC coordinates.

pri = get_PRI_from_AFNI(sys.argv[1])

ds = pyctf.dsopen(sys.argv[2])
nolteFwd.dsopen(sys.argv[2])
print("done")

s = pyctf.sensortopo(ds)

#C = ds.readcov("rt,20-30Hz/Orient.cov")
#Cinv = np.linalg.inv(C)

Cinv = np.load("/tmp/Cinv.npy")

# Regularization test
#C = np.linalg.inv(Cinv)
#C += np.eye(C.shape[0]) * 3.	# regularize
#Cinv = np.linalg.inv(C)

# The beamformers are saved in Slots, selected by the user.

Slotdir = "/tmp/slot"
Slots = {}
Slot = '0'
print("slot {} selected".format(Slot))

os.system("mkdir -p {}".format(Slotdir))

# sometimes we'll respond to single keys,
# other times we'll buffer them.

SINGLE, BUFFER = range(2)

Namebuf = []
Istate = SINGLE

def save_slot(h, name):
    "When the users names a slot, we save the beamformer."

    # to keep things synchronized, we first save to slot.npy
    slot = os.path.join(Slotdir, "slot")
    np.save(slot, h)
    # then rename it to the final name
    slotname = os.path.join(Slotdir, name)
    os.rename("{}.npy".format(slot), slotname)

def get_key(fd):
    global Slot, Istate, Namebuf, Cinv

    s = os.read(fd, 20).decode()
    if Istate == SINGLE:
        if s[0].isdigit():
            Slot = s[0]
            print("slot {} selected".format(Slot))
        elif s[0] == 'n':   # name
            print("Name? ", end = '', flush = True)
            Istate = BUFFER
            Namebuf = []
        elif s[0] == 'c':
            print("reload Cinv")
            Cinv = np.load("/tmp/Cinv.npy")
    elif Istate == BUFFER:
        for c in s:
            if c == '\n':
                Istate = SINGLE
                name = ''.join(Namebuf)
                print("saving to {}".format(name))
                save_slot(Slots[Slot][2], name)
            else:
                if c == '\b': # backspace
                    print('\b \b', end = '', flush = True)
                    Namebuf = Namebuf[:-1]
                elif c == 0x1B:
                    print('***')
                    Istate = SINGLE
                    return
                else:
                    print(c, end = '', flush = True)
                    Namebuf.append(c)

R = rawtty(get_key)     # stay in raw mode until R goes away

# Wait for clicks from AFNI. When we get one, compute the forward solution b,
# using the current inverse covariance estimate to compute the orientation,
# then compute the beamformer h, and plot them both. Meanwhile, R allows
# keypresses to control how to save them.

for pos in pri:
    b = nolteFwd.doFwdMoment(pos, Cinv)
    x = Cinv.dot(b)
    h = x / x.dot(b)

    plt.subplot(1, 2, 1)
    s.plot(b, zrange = [b.min(), b.max()])
    plt.subplot(1, 2, 2)
    s.plot(h, zrange = [h.min(), h.max()])

    plt.savefig("/tmp/fwdNbf.png")
    plt.clf()

    if Slot:
        Slots[Slot] = (pos, b, h)
        print("slot {}: {}".format(Slot, pos))
