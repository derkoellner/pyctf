#! /usr/bin/env python

import os, sys, time
import fcntl
import signal
import tty, termios

class rawtty:

    def __init__(self, hand):
        "install hand as an asynchronous IO handler on stdin"

        # get the file descriptor and check that it's a tty
        self.fd = fd = sys.stdin.fileno()
        if not os.isatty(fd):
            raise RuntimeError("stdin must be a tty")

        # save the old tty attributes
        self.old_attr = termios.tcgetattr(fd)
        # put it in raw mode
        tty.setraw(fd)

        # wrap the handler, to pass the fd
        def handle(sig, frame, fd = fd, hand = hand):
            hand(fd)

        # install the SIGIO handler
        signal.signal(signal.SIGIO, handle)

        # put stdin into async mode, and send SIGIO to us
        fcntl.fcntl(fd, fcntl.F_SETFL, fcntl.FASYNC)
        fcntl.fcntl(fd, fcntl.F_SETOWN, os.getpid())

    def __del__(self):
        # restore the old tty modes
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_attr)

# This gets called on every keystroke

def hand(fd):
    s = os.read(fd, 20).decode()
    for ch in s:
        print("0x{:02X} ".format(ch), end = '', flush = True)

if __name__ == '__main__':
    R = rawtty(hand)    # stay in raw mode until R goes away
    time.sleep(10)
