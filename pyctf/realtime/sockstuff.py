import socket
import struct
import numpy as np

# Client.

def client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.setblocking(1)
    return sock

# Server.

def server(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', port))
    sock.listen(1)
    conn, addr = sock.accept()
    print('Connection from', addr)
    return conn

# Simple string I/O.

def swriteline(sock, s):
    sock.sendall(s)

def sreadline(sock):
    try:
        s = sock.recv(256)
    except:
        return None     # happens if non-blocking and no data
    s = s.decode()
    p = s.find('\n')
    if p >= 0:
        return s[:p]
    return s

# Send and receive 2D numpy arrays. @@@ handle different types

# Wire format: nbytes, shape, data

FMT = '<III'
FMT_size = struct.calcsize(FMT)
DTYPE = np.complex128

def swritearray(sock, a):
    nbytes = a.data.nbytes
    sock.sendall(struct.pack(FMT, nbytes, a.shape[0], a.shape[1]))
    sock.sendall(a.data.tobytes())

def sreadarray(sock):
    s = sock.recv(FMT_size)
    print(len(s))
    n, nr, nc = struct.unpack(FMT, s)
    print(n, nr, nc)
    buf = bytearray(n)
    view = memoryview(buf)
    while n > 0:
        i = sock.recv_into(view, n)
        view = view[i:]
        n -= i
    a = np.frombuffer(buf, DTYPE)
    a.shape = (nr, nc)
    return a
