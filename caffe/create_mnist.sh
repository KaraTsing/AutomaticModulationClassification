#!/usr/bin/env sh
# This script converts the mnist data into lmdb/leveldb format,
# depending on the value assigned to $BACKEND.
set -e

EXAMPLE=~/data_gen/rfml_db
DATA=~/data_gen
BUILD=~/caffe_src/caffe/build/examples/mnist

BACKEND="lmdb"

echo "Creating ${BACKEND}..."

rm -rf $EXAMPLE/rfml_train_${BACKEND}
rm -rf $EXAMPLE/rfml_test_${BACKEND}

$BUILD/convert_mnist_data.bin $DATA/train_radio_vec_110k.dat \
  $DATA/train_radio_labels_110k.dat $EXAMPLE/rfml_train_${BACKEND} --backend=${BACKEND}
$BUILD/convert_mnist_data.bin $DATA/test_radio_vec_110k.dat \
  $DATA/test_radio_labels_110k.dat $EXAMPLE/rfml_test_${BACKEND} --backend=${BACKEND}

echo "Done."
