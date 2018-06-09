#
# This module has methods for taking a standard complex64_t
# encoded file and saving it in the 2D [real, imag] vector format
# that caffe/tensorRT uses.
#
# Requires Python 2.7

import scipy # for opening complex64
import numpy as np # for real/compl

def convert_to_train_vec(filevec):

    f = scipy.fromfile(open(filevec), dtype=scipy.complex64)

    realf = np.real(f)
    imagf = np.imag(f)

    filelen = 128

    realf = realf[:filelen]
    imagf = imagf[:filelen]

    # rename and re-write the file
    filevec_wr =  filevec[:-4] + "_tr.dat"

    with open(filevec_wr, 'wb') as f:
        for i in realf:
            f.write(i.tobytes())
        for i in imagf:
            f.write(i.tobytes())

    return filevec_wr
