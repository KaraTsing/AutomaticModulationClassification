#!/usr/bin/env python3

import lmdb
import lmdb
import os
import numpy as np
import matplotlib.pyplot as plt
import caffe

# First compile the Datum, protobuf so that we can load using protobuf
# This will create datum_pb2.py
os.system('protoc -I={0} --python_out={1} {0}datum.proto'.format("./", "./"))

import datum_pb2

#LMDB_PATH = "rfml_train_lmdb"
print("checking rfml_test")
env = lmdb.open('rfml_test_lmdb', readonly=True)


#datum = datum_pb2.Datum()
datum = caffe.proto.caffe_pb2.Datum()

txn = env.begin()
cur = txn.cursor()
cur.first()



for i in range(10):
    key, value = cur.item()
    print('key-',i, ' ', key)
    datum.ParseFromString(value)
    print('h,w,chan', datum.height, datum.width, datum.channels)
    print('data length', len(datum.float_data))
    x = np.array(datum.float_data).astype(float).reshape( datum.channels, datum.height, datum.width)
    y = datum.label
    #print('data shape', x.shape)
    print('vector mean: ', np.mean(x.flatten()))
    print('label', y)
    cur.next()

print("checking rfml_train")
env = lmdb.open('rfml_train_lmdb', readonly=True)


#datum = datum_pb2.Datum()
datum = caffe.proto.caffe_pb2.Datum()

txn = env.begin()
cur = txn.cursor()
cur.first()

for i in range(10):
    key, value = cur.item()
    print('key-',i, ' ', key)
    datum.ParseFromString(value)
    print('h,w,chan', datum.height, datum.width, datum.channels)
    print('data length', len(datum.float_data))
    x = np.array(datum.float_data).astype(float).reshape( datum.channels, datum.height, datum.width)
    y = datum.label
    #print('data shape', x.shape)
    print('vector mean: ', np.mean(x.flatten()))
    print('label', y)
    cur.next()
