# This initializes the connection with Acq, gets the dataset name,
# and returns unpacked packets using a generator.

import time
from acq_packet import packet_reader
from acq_packet import ACQ_MSGQ_SETUP_COLLECTION, ACQ_MSGQ_CLOSE_COLLECTION

class acq_reader:

    def __init__(self):
        # Access packet memory and get ready to read packets.
        self.r = packet_reader()

    def get_dsname(self):
        """"Wait for Acq to send the dataset name, then return it."""

        while True:
            if self.r.packet_valid():
                p = self.r.get_next_packet()
                if p[0] != ACQ_MSGQ_SETUP_COLLECTION:
                    print("unexpected packet type: %d" % p[0])
                else:
                    dsname = p[1]
                    return dsname
            time.sleep(.15)

    def packet_gen(self):
        """Wait for the next packet, yield it."""

        while True:
            if self.r.packet_valid():
                p = self.r.get_next_packet()
                if p[0] == ACQ_MSGQ_CLOSE_COLLECTION:
                    return
                sample = p[1]
                data = p[2]
                yield (sample, data)
