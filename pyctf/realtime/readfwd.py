#! /usr/bin/env python

import sys, struct
import numpy as np
import nibabel

def readfwd(fwdname, label = False):
    """w, m = readfwd(filename) returns the array w of forward solutions
    found in the given .fwd file, and the transform m needed to map
    voxels of the array into ortho space. If label is true also return
    the channel id."""

    fwd = open(fwdname, 'rb')

    # Read the header.

    fmt = "<8s1i"
    h = fwd.read(struct.calcsize(fmt))
    l = struct.unpack(fmt, h)
    if l[0] != b'SAMFWDSL' or l[1] != 3:
        raise Exception("%s is not a SAM .fwd file" % fwdname)

    fmt = "<256s2i4x11d256s3i3i3i2i4x"
    head = fwd.read(struct.calcsize(fmt))
    l = struct.unpack(fmt, head)

    N = l[1]                    # num chan
    W = l[2]                    # num weights
    x1, x2 = l[3], l[4]         # ROI start & end
    y1, y2 = l[5], l[6]
    z1, z2 = l[7], l[8]
    step = l[9]

    print(N, W)
    print(x1, x2)
    print(y1, y2)
    print(z1, z2)
    print(step)

    coords = None
    if step:
        x = np.arange(x1, x2 + 1e-8, step) # include endpoints
        y = np.arange(y1, y2 + 1e-8, step)
        z = np.arange(z1, z2 + 1e-8, step)
        coords = (x, y, z)

    # Read the channel index.

    fmt = "<%di" % N
    s = struct.calcsize(fmt)
    buf = fwd.read(s)
    chan_idx = struct.unpack(fmt, buf)

    # Read the values.

    w = np.zeros((W, N))
    for i in range(W):
        fmt = "<%dd" % N
        s = struct.calcsize(fmt)
        buf = fwd.read(s)
        w[i, :] = np.array(struct.unpack(fmt, buf))
    if step:
        w.shape = len(x), len(y), len(z), N

    # Create the transform. Get linear coefficients for each coordinate.

    m = None
    if coords:
        m = np.zeros((4, 4), 'f')
        c = coords
        for i in (0, 1, 2):
            n = len(c[i])
            x0 = c[i][0] * 1000.    # convert meters to millimeters
            x1 = c[i][n-1] * 1000.
            a = (x1 - x0) / (n - 1)
            b = x0
            m[i, i] = a
            m[i, 3] = b
        m[3, 3] = 1.

        # The above matrix is in PRI, not RAI. Permute the axes appropriately.

        T = np.array([
                [ 0.,-1., 0., 0. ],
                [ 1., 0., 0., 0. ],
                [ 0., 0., 1., 0. ],
                [ 0., 0., 0., 1. ]])
        m = np.dot(T, m)

    if label:
        return w, m, chan_idx
    return w, m

def write_nii_weights(w, xform, name):
    i = nibabel.Nifti1Image(w, xform)
    i.set_sform(xform, code = 1)    # code 1 is orig view, 2 is tlrc
    nibabel.save(i, "%s.nii.gz" % name)

# test

if __name__ == '__main__':

    fwdname = sys.argv[1]
    w, m = readfwd(fwdname)
    write_nii_weights(w, m, "/tmp/moo")
