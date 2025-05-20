import serial, struct

def sopen(port):
    ser = serial.Serial(port)
    return ser

# Wire format: type (2), len (4), data (len)

FMT = '<HI'
FMT_size = struct.calcsize(FMT)

def sread(ser):
    s = ser.read(FMT_size)
    t, n = struct.unpack(FMT, s)
    s = ser.read(n)
    return t, s

def speek(ser):
    n = ser.inWaiting()
    return n

def swrite(ser, s, t = 0):
    ser.write(struct.pack(FMT, t, len(s)))
    ser.write(s)
