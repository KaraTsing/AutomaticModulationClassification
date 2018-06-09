#!/usr/bin/env python3
import numpy as np
import struct

# creating a floating point data vector with 256 entries
vec_float=np.arange(0,1,0.00390625, dtype=np.float32)

vec_float_2d = np.reshape(vec_float, (2, 128))

print(vec_float.shape, vec_float_2d.shape)

# write the data to file

# note on endianness
# > only applies when working with primitives larger than 1 bytes
# > x86 is little endian, networking uses big-endian
# > also of note: Microblaze uses big-endian, ARM is bi-endian
# > bi-endian     > software switch to determine which to use
# > big-endian    > byte 1 = biggest byte (most significant byte)
# > little-endian > byte 1 = littlest byte (least significant byte)
# Example: [AA BB CC DD]: 32 bit integer
# little endian --> [DD|CC|BB|AA] (higher significance bytes stored later)
# big endian    --> [AA|BB|CC|DD] (higher significance bytes stored earlier)

# one of the benefits of little endian is that different lengths can be used
# and still retain the same meaning:
# Example: 32 bit memory location: [ 4A 00 00 00 ] (holds d'74)
# read  8 bit [4A]          --> d'74
# read 16 bit [00 4A]       --> d'74
# read 32 bit [00 00 00 4A] --> d'74
# while this feature isn't often used by programmers, it is employed frequently
# by code optimizers.


example_value = vec_float[8] # 0.03125
print ('example value: ', example_value,' - ', example_value.tobytes(), ' - ',example_value.tobytes().hex())

# write the vector to file
with open('vector.dat', 'bw') as f:
    for scalar in vec_float:
        f.write(scalar.tobytes())

print('file written. Check first bytes: ',vec_float[0].tobytes().hex(),  vec_float[1].tobytes().hex(), vec_float[2].tobytes().hex())


# now read it back in and reconstruct the vector
with open('vector.dat', 'br') as f:
    read_data = f.read()

print(len(read_data), ' bytes read') 

fl_vec_recon = []
for i in range(256):
    ii = i*4
    vec_i = read_data[ii:ii+4]
    print(i, '4 bytes: ', vec_i.hex(), struct.unpack('f', vec_i))
    fl_vec_recon.append(struct.unpack('f', vec_i))
    if fl_vec_recon[i] != vec_float[i]:
        print('mismatch: ', fl_vec_recon[i], vec_float[i])

print(len(fl_vec_recon), 'floats reconstructed')

vec_recon_np = np.array(fl_vec_recon, dtype=np.float32)

print('recon = original? ', np.transpose(vec_recon_np) == vec_float)
