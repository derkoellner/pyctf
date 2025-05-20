#! /usr/bin/env python

from watchdir import watchdir, listnpy

def hand(dir):
    for x in listnpy(dir):
        print(x)

watchdir("/tmp", hand)
