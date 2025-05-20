# Utilities for watching a directory.

import os
from os.path import splitext
import fcntl
import signal

def notify(f):
    "send SIGIO when f changes"
    #fcntl.fcntl(f, fcntl.F_NOTIFY, fcntl.DN_MODIFY)
    # we only care about renames
    fcntl.fcntl(f, fcntl.F_NOTIFY, fcntl.DN_RENAME)

def watchdir(dir, handle):
    "Watch dir. When a file is renamed, call handle(dir)."

    # get a file descriptor
    f = os.open(dir, os.O_RDONLY)

    # wrap a signal handler for SIGIO
    def hand(sig, frame, f = f, dir = dir, handle = handle):
        handle(dir)
        # retrigger notification
        notify(f)
    signal.signal(signal.SIGIO, hand)

    # trigger 1st notification
    notify(f)

def isnpy(name):
    return splitext(name)[1] == '.npy'

def listnpy(dir):
    "return a list of filenames matching dir/*.npy"
    return filter(isnpy, os.listdir(dir))
