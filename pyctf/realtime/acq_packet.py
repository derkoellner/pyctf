"""This module provides access to Acq shared packet memory."""

import struct
import numpy as np
import sysv_ipc
from sysv_ipc import SharedMemory, ExistentialError, IPC_CREX

# These constants define the shared packet memory structure.
# See ACQ_MessagePacket.h

ACQ_MSGQ_SETUP_COLLECTION = 0
ACQ_MSGQ_DATA = 1
ACQ_MSGQ_CLOSE_COLLECTION = 2
ACQ_MSGQ_INVALID = 2147483647

ACQ_MSGQ_SIZE = 600
ACQ_MESQ_SHMKEY = 0x39457f73

MESSAGE_TYPE = 0
MESSAGE_ID = 1
SAMPLE_NUMBER = 2
NUM_SAMPLES = 3
NUM_CHANNELS = 4
DATA = 5

packet_format = "<iiiii%ds" % (28160 * 4)
header_format = "<iiiii"
packet_size = struct.calcsize(packet_format)
header_size = struct.calcsize(header_format)
empty_packet = struct.pack(header_format, ACQ_MSGQ_INVALID, 0, 0, 0, 0)

# This initializes, destroys, and accesses the shared packet memory area.

class packet_memory:

    def __init__(self):
        """m = packet_memory()"""
        try:
            self.shm = SharedMemory(ACQ_MESQ_SHMKEY)
        except ExistentialError:
            self.shm = SharedMemory(ACQ_MESQ_SHMKEY, flags = IPC_CREX,
                                    size = packet_size * ACQ_MSGQ_SIZE)
        self.id = self.shm.id
        for i in range(ACQ_MSGQ_SIZE):
            self._mark_packet_empty(i)

        # we need this for __del__; sysv_ipc might go away early during shutdown
        self.ipc = sysv_ipc

    def __del__(self):
        self.shm.detach()
        self.shm.remove()

    def _mark_packet_empty(self, i):
        self.shm.write(empty_packet, i * packet_size)

    def read_packet_header(self, i):
        p = self.shm.read(header_size, i * packet_size)     # byte_count, offset
        return struct.unpack(header_format, p)

    def read_packet(self, i):
        p = self.shm.read(packet_size, i * packet_size)
        p = struct.unpack(packet_format, p)
        self._mark_packet_empty(i)
        return p

# This manages the circular array of packets and returns unpacked packets.

class packet_reader:

    def __init__(self):
        """r = packet_reader()"""
        self.current_packet = 0
        self.m = packet_memory()

    def _advance_current_packet(self):
        self.current_packet = (self.current_packet + 1) % ACQ_MSGQ_SIZE

    def packet_valid(self):
        h = self.m.read_packet_header(self.current_packet)
        return h[MESSAGE_TYPE] != ACQ_MSGQ_INVALID

    def get_next_packet(self):
        p = self.m.read_packet(self.current_packet)
        self._advance_current_packet()

        mtype = p[MESSAGE_TYPE]

        if mtype == ACQ_MSGQ_CLOSE_COLLECTION:
            self.current_packet = 0
            return (mtype,)

        if mtype == ACQ_MSGQ_SETUP_COLLECTION:
            dsname = p[DATA]
            eos = dsname.index(b'\x00')
            dsname = dsname[0:eos].decode()
            return (mtype, dsname)

        id = p[MESSAGE_ID]
        sample = p[SAMPLE_NUMBER]
        num_samples = p[NUM_SAMPLES]
        num_channels = p[NUM_CHANNELS]
        plen = num_samples * num_channels * 4
        a = np.fromstring(p[DATA][0:plen], dtype = np.int32)
        a.shape = (num_samples, num_channels)
        return (mtype, sample, a)
