import numpy as np

XDIM = 500
YDIM = 500
ZDIM = 100
TDIM = 1
ZRANGE = 19.8

def idx(x,y,z):
    return x+XDIM*(y+YDIM*z)

def readbin(filename):
    print "reading file %s..." %(filename)
    data = np.fromfile(filename, dtype='>f4')
    print "file read: %s" %(filename)
    return data

height_data = readbin("data/HGTdata.bin")
TC_data = readbin("data/TCf01.bin")

TC_height = int(ZDIM/ZRANGE)