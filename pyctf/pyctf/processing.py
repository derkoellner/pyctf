
"""Read and write processing.cfg files.
Usage:

    from pyctf import processing

    f = open("processing.cfg")
    proc = processing.read(f)

    f = open("processing.cfg", "w")
    processing.write(proc, f)

"""

import datetime

__all__ = ['read', 'write']

def read(f):
    """Read processing parameters from the open file f,
    which must be a "processing.cfg" file in a dataset.

    Returns a dict containing the fields:
        balance: [order, adapted]
        lowpass: [enable, filterOrder, fc]
        highpass: [enable, filterOrder, fc]
        bandpass: [enable, filterOrder, fc1, fc2]
        bandreject: [[enable, filterOrder, fc1, fc2], ...]
            (Note: bandreject is a list of filter parameters)
        offset: [enable, baselineSelection, startPt, endPt]
    """
    p = {}
    p['bandreject'] = []

    for l in f:
        l = l.split()
        # ignore blank lines, short lines, and comments
        if len(l) <= 1 or l[0] == '//':
            continue
        name = l[0]
        l = l[1].split(',')
        if name == "balance:":
            p['balance'] = [int(l[0]), int(l[1])]
        elif name == "lowpass:":
            p['lowpass'] = [int(l[0]), int(l[1]), float(l[2])]
        elif name == "highpass:":
            p['highpass'] = [int(l[0]), int(l[1]), float(l[2])]
        elif name == "bandpass:":
            p['bandpass'] = [int(l[0]), int(l[1]), float(l[2]), float(l[3])]
        elif name == "bandreject:":
            p['bandreject'].append([int(l[0]), int(l[1]), float(l[2]), float(l[3])])
        elif name == "offset:":
            p['offset'] = [int(l[0]), int(l[1]), int(l[2]), int(l[3])]

    return p

def write(proc, f):
    """Write the processing parameters (as returned from read_processing())
    to the open file f."""

    # The header just contains the current time and date.

    t = datetime.datetime.now()
    print("// Processing configuration.", file = f)
    print(t.strftime("// %H:%M  %d/%m/%Y"), file = f)

    # Write the parameters themselves.

    print("\n// PROCESSING PARAMETERS", file = f)
    print("processing\n{", file = f)

    print("\t// balance: order, adapted", file = f)
    print("\t// (adapted=0 -> not adapted)", file = f)
    print("\t// (adapted=1 -> adapted)", file = f)
    print("\tbalance:\t{},{}".format(*proc['balance']), file = f)

    print("\t// lowpass: enable, filterOrder, fc", file = f)
    print("\tlowpass:\t{},{},{}".format(*proc['lowpass']), file = f)

    print("\t// highpass: enable, filterOrder, fc", file = f)
    print("\thighpass:\t{},{},{}".format(*proc['highpass']), file = f)

    print("\t// bandpass: enable, filterOrder, fc1, fc2", file = f)
    print("\tbandpass:\t{},{},{},{}".format(*proc['bandpass']), file = f)

    # There can be several notch filters.

    for notch in proc['bandreject']:
        print("\t// bandreject: enable, filterOrder, fc1, fc2", file = f)
        print("\tbandreject:\t{},{},{},{}".format(*notch), file = f)

    print("\t// offset: enable, baselineSelection, startPt, endPt", file = f)
    print("\t// (baseline=0 --> use pretrigger data)", file = f)
    print("\t// (baseline=1 --> use from startPt to endPt)", file = f)
    print("\t// (baseline=2 --> use whole trial)", file = f)
    print("\t// (baseline+=10 --> do trend removal)", file = f)
    print("\toffset:\t{},{},{},{}".format(*proc['offset']), file = f)

    print("}", file = f)
