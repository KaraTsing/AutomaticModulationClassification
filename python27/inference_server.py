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


# # map the labels to outputs
def to_onehot(yy):
    yy_list = list(yy)
    yy1 = np.zeros([len(yy_list), max(yy_list)+1]) # np.zeros(2,1) -> array([[0.0], 0.0]])
    yy1[np.arange(len(yy_list)), yy_list] = 1
    return yy1

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
	
read_err=False
# run a continuous loop accepting and analyzing any file given as input
while(True):
	data_file = input("Give a data file: ")
	try:
		# load the data
		Xd = pickle.load(open(data_file,'rb'),encoding='latin1') # latin encoding used for python3 support
		read_err = False
		print("keys in data file: " + str(list(Xd.keys())))
	except:
		print("trouble reading the file")
		read_err = True
		
	# start processing the data
	if (not read_err):
		snrs,mods = map(lambda j: sorted(list(set(map(lambda x: x[j], Xd.keys())))), [1,0])
		X = []  
		lbl = []
		for mod in mods:
			for snr in snrs:
				X.append(Xd[(mod,snr)]) # example len(Xd[('CPFSK', 20)]) = 1000, len(...[0]) = 2, len(...[0][0]) = 128
				for i in range(Xd[(mod,snr)].shape[0]):  lbl.append((mod,snr)) # lbl = [('CPFSK', 20), ('CPFSK', 20), ('CPFSK', 20), ('CPFSK', 20), ...

		X = np.vstack(X) # X.shape[0:] = (1000, 2, 128)
		n_examples = X.shape[0] 
		test_idx = list(set(range(0,n_examples)))
		X_test =  X[test_idx]
		
		Y_test = to_onehot(map(lambda x: mods.index(lbl[x][0]), test_idx)) # lbl[x][0] = e.g. 'CPFSK', mods.index(value) returns the first index of value 
		
		in_shp = list(X_test.shape[1:]) # probabaly (2, 128)
		print ("input shape of vectors: " + str(in_shp)) 
		classes = ['8PSK', 'AM-DSB', 'AM-SSB', 'BPSK', 'CPFSK', 'GFSK', 'PAM4', 'QAM16', 'QAM64', 'QPSK', 'WBFM']
		
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
		
		batch_size = 256
		filepath = 'convmodrecnets_CNN2_0.5.wts.h5'
		model.load_weights(filepath)
		
		y_hat = model.predict(X_test, batch_size=256) # y_hat.shape = (1000, 11)
		
		
		
		
		# plot the confusion matrix	
		conf = np.zeros([len(classes),len(classes)]) # conf: [1x11]
		confnorm = np.zeros([len(classes),len(classes)]) # confnorm: [1x11]

		for i in range(0,X_test.shape[0]):
			j = classes.index(mod)
			#j = list(Y_test[i,:]).index(1)
			k = int(np.argmax(y_hat[i,:]))
			conf[j,k] = conf[j,k] + 1 # increment each time

		for i in range(0,len(classes)):
			confnorm[i,:] = conf[i,:] / np.sum(conf[i,:])

		for mod in mods: 
			print ("For true label: " + mod)
			y_predict = confnorm[classes.index(mod),:]
			for i in range(0, len(classes)):
				print (str(classes[i]) + " : " + str(y_predict[i]))
			
		plt.figure()
		plot_confusion_matrix(confnorm, labels=classes)  
		plt.show()



# stop for debugging
# pdb.set_trace()

# Show loss curves 
# plt.figure() # creates a new figure
# plt.title('Training performance')
# plt.plot(history.epoch, history.history['loss'], label='train loss+error') # plot: [x:epoch, y:loss]
# plt.plot(history.epoch, history.history['val_loss'], label='val_error')    # plot: [x:epoch, y:val_error]
# plt.legend()

# def plot_confusion_matrix(cm, title='Confusion matrix', cmap=plt.cm.Blues, labels=[]):
    # plt.imshow(cm, interpolation='nearest', cmap=cmap)
    # plt.title(title)
    # plt.colorbar()
    # tick_marks = np.arange(len(labels))
    # plt.xticks(tick_marks, labels, rotation=45)
    # plt.yticks(tick_marks, labels)
    # plt.tight_layout()
    # plt.ylabel('True label')
    # plt.xlabel('Predicted label')
 
# # Plot confusion matrix
# test_Y_hat = model.predict(X_test, batch_size=batch_size) # generates output predictions for the inputs

# conf = np.zeros([len(classes),len(classes)]) # conf: [11x11]

# confnorm = np.zeros([len(classes),len(classes)]) # confnorm: [11x11]

# for i in range(0,X_test.shape[0]):
    # j = list(Y_test[i,:]).index(1)
    # k = int(np.argmax(test_Y_hat[i,:]))
    # conf[j,k] = conf[j,k] + 1 # increment each time

# for i in range(0,len(classes)):
    # confnorm[i,:] = conf[i,:] / np.sum(conf[i,:])


# plt.figure()
# plot_confusion_matrix(confnorm, labels=classes)  


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


