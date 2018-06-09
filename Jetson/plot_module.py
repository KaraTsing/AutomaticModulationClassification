import matplotlib.pyplot as plt
import numpy as np
import scipy


def plot_time(filevec, file_len, skip_samples=128):

    f = scipy.fromfile(open(filevec), dtype=scipy.complex64)

    mean = np.mean(f)
    print("mean: " + str(np.abs(mean))) 

    realf = np.real(f)
    imagf = np.imag(f)

    x = range(file_len)

    if file_len > 128:
        print("Q sample at 128: " + str(realf[128]))
        print("I sample at 128: " + str(imagf[128]))

    plt.plot(x, realf[skip_samples:file_len+skip_samples])
    plt.plot(x, imagf[skip_samples:file_len+skip_samples])
    plt.show()
    
