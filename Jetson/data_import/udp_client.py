import socket, struct, sys
# import matplotlib
#matplotlib.use("Agg") # force to not use X win --> do this if just saving to file
import matplotlib.pyplot as plt

UDP_IP="0.0.0.0"
UDP_PORT=45000

try:
    sock = socket.socket(socket.AF_INET, #internet
                         socket.SOCK_DGRAM) # UDP
except socket.error:
        print 'Failed to create socket'
        sys.exit()
                    
sock.bind((UDP_IP, UDP_PORT))

# convert the received bytes to floating point samples
def payload_byte_to_float_vec(data, nbytes):
    n=0
    vec_sample=[]
    while(n < nbytes):
        temp_vec=[data[n],data[n+1],data[n+2],data[n+3]]
        b_cat = ''.join(chr(i) for i in temp_vec)
        vec_sample.append(struct.unpack('<f', b_cat))
        n = n+4
    return vec_sample

# convert the received bytes to complex-valued (I/Q) point samples
def payload_byte_to_IQ_vec(data, nbytes):
    n = 0
    Q_vec_sample = []
    I_vec_sample = []
    while (n < nbytes):
        temp_Q_vec=[data[n],data[n+1],data[n+2],data[n+3]]
        b_cat = ''.join(chr(i) for i in temp_vec)
        Q_vec_sample.append(struct.unpack('<f', b_cat))

        temp_I_vec=[data[n+4],data[n+5],data[n+6],data[n+7]]
        b_cat = ''.join(chr(i) for i in temp_vec)
        vec_sample.append(struct.unpack('<f', b_cat))
        n = n+8
    return Q_vec_sample, I_vec_sample


# main processing
recd_data = bytearray(2000)
print "waiting for data"

plt.axis([0, 350, -2, 2])
plt.ion() # enable interactive plotting


while True:
    plt.clf() # clear the current figure
    nbytes, addr = sock.recvfrom_into(recd_data, 1500)
    print nbytes
    if (nbytes == 0):
        print "got zero length packet, we're done"
        break
    vec_samples = payload_byte_to_float_vec(recd_data, nbytes)
    #for vec in vec_samples:
    #    print str(vec[0])
    plt.plot(vec_samples)
    plt.pause(0.05)
#    plt.show()
