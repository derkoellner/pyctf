#! /usr/bin/python

import numpy as np

f = open("dofind.log")

l = []
for s in f:
    name, val = s.split()
    val = float(val)
    l.append((val, name))

def cmp(a, b):
    if a[0] < b[0]:
	return -1
    return 1

l.sort(cmp)

for x in l:
    print x[1], x[0]
