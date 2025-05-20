#! /usr/bin/env python

# Parse a simple key=value .param file, return a dict

def ParseParam(filename):
    d = {}
    ll = open(filename).readlines()
    for l in ll:
        # Ignore all past a '#'
        l = l.partition('#')[0].split()
        if len(l) == 0:
            continue

        # The first word is a key name ...
        name = l.pop(0).lower()
        # ... collect the typed arguments.
        ll = []
        for x in l:
            try:
                x = float(x)
            except ValueError:
                pass
            ll.append(x)
        if len(ll) == 1:
            ll = ll[0]
        d[name] = ll
    return d

if __name__ == '__main__':
    import sys, pprint

    d = ParseParam(sys.argv[1])
    pprint.pprint(d)

    import json
    print(json.dumps(d))
