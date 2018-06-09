import sys
#import struct
import matplotlib.pyplot as plt
import numpy as np
import scipy

if len(sys.argv) < 3:
    raise Exception ("needs file arg, len arg")

filevec = sys.argv[1]
file_len = int(sys.argv[2])

f = scipy.fromfile(open(filevec), dtype=scipy.complex64)

mean = np.mean(f)
print("mean: " + str(np.abs(mean))) 

realf = np.real(f)
imagf = np.imag(f)

x = range(file_len)

if file_len > 128:
    print("Q sample at 128: " + str(realf[128]))
    print("I sample at 128: " + str(imagf[128]))

plt.plot(x, realf[0:file_len])
plt.plot(x, imagf[0:file_len])
plt.show()
    
