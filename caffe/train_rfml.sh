#!/usr/bin/env sh
set -e

caffe train --solver=/home/boston/RFML/rfml_solver.prototxt $@
