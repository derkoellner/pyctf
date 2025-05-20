#! /usr/bin/env python

import sys
from subprocess import Popen, PIPE
import numpy as np

class get_PRI_from_AFNI(object):

    def __init__(self, mri):
        self.xform = get_matvec_xform(mri)

        p = Popen(['/usr/bin/env', 'plugout_xyz', '-name', 'get_PRIcm'],
                  bufsize = 1, close_fds = True, stdout = PIPE, universal_newlines = True)
        self.p = p
        self.pr = p.stdout

    def __del__(self):
        self.pr.close()
        self.p.terminate()

    def __iter__(self):
        while 1:
            l = self.pr.readline()
            if len(l) == 0:
                raise StopIteration

            if l.startswith('DICOM_XYZ'):
                l = l.split()
                # apply the transform from tlrc -> ortho
                a = self.xform([float(x) for x in l[1:]])
                # convert RAI mm to PRI cm
                r, a, i = a * .1
                yield -a, r, i

def get_matvec_xform(mri):
    p = Popen(["cat_matvec", "{}::WARPDRIVE_MATVEC_FOR_000000".format(mri)],
              bufsize = 1, close_fds = True, stdout = PIPE, stderr = PIPE, universal_newlines = True)
    r = p.stdout.read()
    if p.wait() != 0:
        raise Exception("MRI {} does not contain a template transform".format(mri))
    a = np.array([float(x) for x in r.split()])
    a.shape = (3, 4)

    def xform(p, m = a[:3,:3], t = a[:,3]):
        return m.dot(p) + t

    return xform

if __name__ == '__main__':
    for x in get_PRI_from_AFNI(sys.argv[1]):
        print(x)
