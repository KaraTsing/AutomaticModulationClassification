#!/usr/bin/env python3

import random, pickle
import numpy as np


# Load the dataset ...
dataFile = "RML2016.10a_dict.dat"
Xd = pickle.load(open(dataFile,'rb'),encoding='latin1')

# Extract the labels
snrs,mods = map(lambda j: sorted(list(set(map(lambda x: x[j], Xd.keys())))), [1,0])
# snrs:  [-20, -18, -16, -14, -12, -10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
# mods: ['8PSK', 'AM-DSB', 'AM-SSB', 'BPSK', 'CPFSK', 'GFSK', 'PAM4', 'QAM16', 'QAM64', 'QPSK', 'WBFM']

X = []  
lbl = []
for mod in mods:
    for snr in snrs:
        X.append(Xd[(mod,snr)])
        for i in range(Xd[(mod,snr)].shape[0]):  lbl.append((mod,snr))

#   stack arrays in sequence vertically
X = np.vstack(X) # len(X) -> 220,000   len(lbl) -> 220,000


# Partition the data into training and test sets of the form we can train/test on  while keeping SNR and Mod labels handy for each
np.random.seed(2016)
n_examples = X.shape[0] # dim(X) -> [220000, 2, 128]
# split the data into half (training, testing)
n_train = int(n_examples * 0.5)
train_idx = np.random.choice(range(0,n_examples), size=n_train, replace=False)
test_idx = list(set(range(0,n_examples))-set(train_idx))
X_train = X[train_idx] # (110,000, 2, 128)
X_test =  X[test_idx]

# map the labels to outputs
def to_onehot(yy):
	yy_list = list(yy)
	yy1 = np.zeros([len(yy_list), max(yy_list)+1]) # np.zeros(2,1) -> array([[0.0], 0.0]])
	yy1[np.arange(len(yy_list)), yy_list] = 1
	return yy1

Y_train = to_onehot(map(lambda x: mods.index(lbl[x][0]), train_idx))
Y_test = to_onehot(map(lambda x: mods.index(lbl[x][0]), test_idx))


# write using mnist image file type
# [offset] [type] [value] [description]
# 0000     int32   2051    magic number
# 0004     int32   11k     number of images
# 0008     int32   2       num rows -- normally this would tell you num bytes
# 0012     int32   128     num cols -- but I need to multiply by 4
# 0016     float   ??      pixel
# 0020     float   ??      pixel

magic_num = np.array([2051], dtype=np.int32)

# start with test
# numbytes = 4+4+4+4+110k*2*128*4 = 112.6 MBytes
num_bytes_expected = 4+4+4+4+110000*2*128*4
num_vecs = X_test.shape[0]
num_bytes_written = 0
with open('test_radio_vec_110k.dat', 'bw') as f:
    num_bytes_written += f.write(magic_num.tobytes()) # magic number
    num_bytes_written += f.write(np.array([num_vecs], dtype=np.int32).tobytes()) 
    num_bytes_written += f.write(np.array([X_test.shape[1]], dtype=np.int32).tobytes()) 
    num_bytes_written += f.write(np.array([X_test.shape[2]], dtype=np.int32).tobytes()) 
    for vec2 in X_test:
        for row in vec2:
            for col in row:
              num_bytes_written +=  f.write(col.tobytes())
print("X_test- wrote :", num_bytes_written, ' bytes. Expected: ', num_bytes_expected)

# not x_train
# numbytes = 4+4+4+4+110k*2*128*4 = 112.6 MBytes
num_vecs = X_train.shape[0]
num_bytes_written = 0
with open('train_radio_vec_110k.dat', 'bw') as f:
    num_bytes_written += f.write(magic_num.tobytes()) # magic number
    num_bytes_written += f.write(np.array([num_vecs], dtype=np.int32).tobytes()) 
    num_bytes_written += f.write(np.array([X_train.shape[1]], dtype=np.int32).tobytes()) 
    num_bytes_written += f.write(np.array([X_train.shape[2]], dtype=np.int32).tobytes()) 
    for vec2 in X_train:
        for row in vec2:
            for col in row:
              num_bytes_written +=  f.write(col.tobytes())
print("X_train- wrote :", num_bytes_written, ' bytes. Expected: ', num_bytes_expected)

num_bytes_expected = Y_test.shape[0] + 4*2
# now, Y_test labels (shape: (110_000, 11) e.g. [ 0 0 0 0 0 1 0 0 0 0 ])
# [offset] [type] [value] [description]
#   0000    int32  2051     magic number
#   0004    int32  110k     number of items
#   0008    ubyte   ??      label (0-10)

# vectors one-hot encoded. write the position of the '1'
num_bytes_written = 0
with open('test_radio_labels_110k.dat', 'bw') as f:
    num_bytes_written += f.write(magic_num.tobytes()) # magic number
    num_bytes_written += f.write(np.array([Y_test.shape[0]], dtype=np.int32).tobytes())
    for label in Y_test:
        num_bytes_written += f.write(np.array([label.argmax()], dtype=np.uint8).tobytes())
        
print("Y test- wrote :", num_bytes_written, ' expected: ', num_bytes_expected)
        
# now Y_train
# note that bytes() is weird. If you use bytes(2051) it creates an array of 0x00 of size 2051.
# use np.array instead where I can specify the size  
num_bytes_written = 0
with open('train_radio_labels_110k.dat', 'bw') as f:
    num_bytes_written += f.write(magic_num.tobytes()) # magic number
    num_bytes_written += f.write(np.array([Y_train.shape[0]], dtype=np.int32).tobytes())
    for label in Y_train:
        num_bytes_written += f.write(np.array([label.argmax()], dtype=np.uint8).tobytes())


print("Y test- wrote :", num_bytes_written, ' expected: ', num_bytes_expected)

