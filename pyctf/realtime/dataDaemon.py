#! /usr/bin/env python3

# This client reads frames from the real time server,
# and projects beamformed data ...

import sys, os
from time import time, sleep
import numpy as np
from sockstuff import *

# Connect to the server and start reading frames.

sleep(1)
sock = client('', 5556)

while True:
    a = sreadarray(sock)
    m, n = a.shape
