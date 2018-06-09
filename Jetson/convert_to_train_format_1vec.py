import sys
import struct
import matplotlib.pyplot as plt
import numpy as np
import scipy

if len(sys.argv) < 3:
    raise Exception ("needs file arg, len arg")

filevec = sys.argv[1]
should_plot = sys.argv[2]

will_plot = False
if should_plot == "plot":
    will_plot = True

f = scipy.fromfile(open(filevec), dtype=scipy.complex64)

realf = np.real(f)
imagf = np.imag(f)

filelen = 128

realf = realf[:filelen]
imagf = imagf[:filelen]

filevec_wr =  filevec[:-4] + "_tr.dat"

print(len(realf))
print(len(imagf))

with open(filevec_wr, 'wb') as f:
    for i in realf:
        f.write(i.tobytes())
    for i in imagf:
        f.write(i.tobytes())

#print("wrote: " + str(numbytes_wr) + " bytes")
# python 2 f.write returns None instead of num bytes. Just check below

if will_plot:
    # reopen saved file
    f = scipy.fromfile(open(filevec_wr), dtype=scipy.complex64)
    realf = np.real(f)
    imagf = np.imag(f)
    print (len(realf))
    print (len(imagf))
    
    x = range(filelen)

    plt.plot(x, realf[0:filelen])
    plt.plot(x, imagf[0:filelen])
    plt.show()
    
# def char_arr_2_float(char_arr):
#     if len(char_arr) != 4:
#         print("got a char_arr not equal to 4 bytes")
#         return
    
#         float_samp_arr = ''.join(chr(i) for i in char_arr)
#         float_samp = struct.unpack('<f', float_samp_arr))
#         return float_samp

# vec_h = 2
# vec_w = 128

# with open(filevec, 'rb') as f:
#     byte = []
    
