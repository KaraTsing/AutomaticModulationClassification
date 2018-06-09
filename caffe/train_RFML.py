#!/usr/env python3

import caffe

caffe.set_mode_cpu()
try:
    net = caffe.Net('rfml_train_test.prototxt', caffe.TEST)
except:
    print("failure to set up net")

print(net.inputs)

print(net.blobs['conv'].data.shape)
