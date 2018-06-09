"""
This function trains and evaluates a model from RFML

Requires: Python 3.5
Last modified: 9/13/2017
Last modified by: Boston Clark Terry
"""

import os, random
os.environ["KERAS_BACKEND"] = "tensorflow"
os.environ["THEANO_FLAGS"]  = "device=gpu%d"%(1)
import numpy as np
from keras.utils import np_utils
import keras.models as models
from keras.layers.core import Reshape,Dense,Dropout,Activation,Flatten
from keras.layers.noise import GaussianNoise
from keras.layers.convolutional import Convolution2D, MaxPooling2D, ZeroPadding2D
from keras.regularizers import *
from keras.optimizers import adam
import matplotlib.pyplot as plt
import pickle
import random, sys, keras
import pdb

# opens and analyzes a file given as a parameter
if (len(sys.argv) < 2):
	print ("needs more args - arg1: data sample to run")
data_file = sys.argv[1]

# Load the file ...
Xd = pickle.load(open(data_file,'rb'),encoding='latin1') # latin encoding used for python3 support

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
    print(str(mod))
X = np.vstack(X)

n_examples = X.shape[0] 
test_idx = list(set(range(0,n_examples)))
X_test =  X[test_idx]

# map the labels to outputs
def to_onehot(yy):
	yy_list = list(yy)
	yy1 = np.zeros([len(yy_list), max(yy_list)+1]) # np.zeros(2,1) -> array([[0.0], 0.0]])
	yy1[np.arange(len(yy_list)), yy_list] = 1
	return yy1

Y_test = to_onehot(map(lambda x: mods.index(lbl[x][0]), test_idx))
	
# set the input shape [2,1024]
in_shp = list(X_test.shape[1:])
print (X_test.shape, in_shp) # (110000, 2, 1024) [2, 1024]
classes = ['BPSK', '8PSK', 'QPSK', 'PAM4', 'QAM16', 'QAM64', 'GFSK', 'CPFSK', 'WBFM', 'AM-DSB', 'AM-SSB']
# all_keys = {"bpsk":0,"8psk":0, "qpsk":0, "pam4":0, "qam16":0, "qam64":0, "gfsk":0, "cpfsk":0, "fm": 1, "am": 1, "amssb": 1 }

# Build VT-CNN2 Neural Net model using Keras primitives -- 
#  - Reshape [N,2,1024] to [N,1,2,1024] on input
#  - Pass through 2 2DConv/ReLu layers
#  - Pass through 2 Dense layers (ReLu and Softmax)
#  - Perform categorical cross entropy optimization

dr = 0.5 # dropout rate (%)
model = models.Sequential()
model.add(Reshape([1]+in_shp, input_shape=in_shp))
model.add(ZeroPadding2D((0, 2), data_format="channels_first"))
model.add(Convolution2D(256, (1, 3), activation="relu", name="conv1", data_format="channels_first"))
model.add(Dropout(dr))
model.add(ZeroPadding2D((0, 2), data_format="channels_first"))
model.add(Convolution2D(80, (2, 3), activation="relu", name="conv2", data_format="channels_first"))
model.add(Dropout(dr))
model.add(Flatten())
model.add(Dense(256, activation='relu', kernel_initializer='he_normal', name="dense1"))
model.add(Dropout(dr))
model.add(Dense( len(classes), kernel_initializer='he_normal', name="dense2" ))
model.add(Activation('softmax'))
model.add(Reshape([len(classes)]))
model.compile(loss='categorical_crossentropy', optimizer='adam')
model.summary()

# Set up some params 
batch_size = 256

# open the previously trained model
filepath = 'convmodrecnets_CNN2_0.5.wts.h5'
model.load_weights(filepath)

# returns an array of predictions
y_hat = model.predict(X_test, batch_size=256)
print(y_hat)
print(y_hat.shape)

def plot_confusion_matrix(cm, title='Confusion matrix', cmap=plt.cm.Blues, labels=[]):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(labels))
    plt.xticks(tick_marks, labels, rotation=45)
    plt.yticks(tick_marks, labels)
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

# plot the confusion matrix	
conf = np.zeros([len(classes),len(classes)]) # conf: [11x11]
confnorm = np.zeros([len(classes),len(classes)]) # confnorm: [11x11]

for i in range(0,X_test.shape[0]):
    j = list(Y_test[i,:]).index(1)
    k = int(np.argmax(y_hat[i,:]))
    conf[j,k] = conf[j,k] + 1 # increment each time

for i in range(0,len(classes)):
    confnorm[i,:] = conf[i,:] / np.sum(conf[i,:])

plt.figure()
plot_confusion_matrix(confnorm, labels=classes)  
plt.show()

# # These errors are probably from trying to divide by zero or NaN
# # example_training.py:208: RuntimeWarning: invalid value encountered in true_divide
# #  confnorm[i,:] = conf[i,:] / np.sum(conf[i,:])

# # example_training.py:214: RuntimeWarning: invalid value encountered in double_scalars
# #  print ("Overall Accuracy: ", cor / (cor+ncor))

# # Overall Accuracy:  nan

# # example_training.py:215: RuntimeWarning: invalid value encountered in double_scalars
# #  acc[snr] = 1.0*cor/(cor+ncor)

# # just in case we picked up some NaNs
# np.nan_to_num(confnorm)

# # Plot confusion matrix
# acc = {}
# for snr in snrs:

    # # extract classes @ SNR
    # test_SNRs = list(map(lambda x: lbl[x][1], test_idx))
    # test_X_i = X_test[np.where(np.array(test_SNRs)==snr)]
    # test_Y_i = Y_test[np.where(np.array(test_SNRs)==snr)]    

    # # estimate classes
    # test_Y_i_hat = model.predict(test_X_i)
    # conf = np.zeros([len(classes),len(classes)])
    # confnorm = np.zeros([len(classes),len(classes)])

    # for i in range(0,test_X_i.shape[0]):
        # j = list(test_Y_i[i,:]).index(1)
        # k = int(np.argmax(test_Y_i_hat[i,:]))
        # conf[j,k] = conf[j,k] + 1

    # for i in range(0,len(classes)):
        # confnorm[i,:] = conf[i,:] / np.sum(conf[i,:])
    
    # np.nan_to_num(confnorm)
    
    # plt.figure()
    # plot_confusion_matrix(confnorm, labels=classes, title="ConvNet Confusion Matrix (SNR=%d)"%(snr))
    
    # cor = np.sum(np.diag(conf))
    # ncor = np.sum(conf) - cor
    # print ("Overall Accuracy: ", cor / (cor+ncor))
    # acc[snr] = 1.0*cor/(cor+ncor)
    
  # # Save results to a pickle file for plotting later
# print (acc)
# fd = open('results_cnn2_d0.5.dat','wb')
# pickle.dump( ("CNN2", 0.5, acc) , fd )

  

# # Plot accuracy curve
# plt.figure()
# plt.plot(snrs, list(map(lambda x: acc[x], snrs)))
# plt.xlabel("Signal to Noise Ratio")
# plt.ylabel("Classification Accuracy")
# plt.title("CNN2 Classification Accuracy on RadioML 2016.10 Alpha")
# plt.show()


