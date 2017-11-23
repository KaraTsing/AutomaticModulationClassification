## GNURadio WIN test
from transmitters_WIN import transmitters
from source_alphabet_WIN import source_alphabet
import analyze_stats
from gnuradio import channels, gr, blocks
import numpy as np
import numpy.fft, cPickle, gzip
import random
import sys


# set the data parameters
if (len(sys.argv) < 3):
	print ("needs more arguments - arg1: modulation type, -arg2: SNR")
	raise IOError
	
modulation_type_requested = sys.argv[1]
SNR_requested = sys.argv[2]

snr = 	int(SNR_requested)
if (((snr % 2 ) != 0) or (abs(snr) > 20)):
	print "SNR value not in range. Must be even and between -20 and 20"
	raise IOError

#"discrete":[transmitter_bpsk, transmitter_8psk, transmitter_qpsk, transmitter_pam4, transmitter_qam16, transmitter_qam64, transmitter_gfsk, transmitter_cpfsk],
#    "continuous":[transmitter_fm, transmitter_am, transmitter_amssb]
all_keys = {"bpsk":0,"8psk":0, "qpsk":0, "pam4":0, "qam16":0, "qam64":0, "gfsk":0, "cpfsk":0, "fm": 1, "am": 1, "amssb": 1 }
discrete_keys = {"bpsk":0,"8psk":1, "qpsk":2, "pam4":3, "qam16":4, "qam64":5, "gfsk":6, "cpfsk":7 }
continuous_keys = {"fm": 0, "am": 1, "amssb": 2}

mod_type_key = 0
mod_alphabet = 0

try:
	mod_alphabet = all_keys[modulation_type_requested]
except: 
	print "Couldn't register the modulation type. Try again"
	raise IOError

try:
	if (mod_alphabet == 0):
		mod_type_key = discrete_keys[modulation_type_requested]
	else:
		mod_type_key = continuous_keys[modulation_type_requested]
except:
	print "Error registering the modulation type. Try again"


'''
Generate dataset with dynamic channel model across range of SNRs
'''

write_to_file = True
write_to_net = False

apply_channel = True

dataset = {}

# The output format looks like this
# {('mod type', SNR): np.array(nvecs_per_key, 2, vec_length), etc}

# CIFAR-10 has 6000 samples/class. CIFAR-100 has 600. Somewhere in there seems like right order of magnitude
nvecs_per_key = 1000
vec_length = 128
snr_vals = range(-20,20,2)
transmitter_keys = transmitters.keys() # list:['discrete', 'continuous']

#snr = snr_vals[mod_output_id]
alphabet_type = transmitter_keys[mod_alphabet]

mod_type = transmitters[alphabet_type] # [<class 'transmitters_WIN.transmitter_bpsk'>, <class 'transmitters_WIN.transmitter_qpsk'>, <class 'transmitters_WIN.transmitter_pam4'>, <class 'transmitters_WIN.transmitter_qam16'>, <class 'transmitters_WIN.transmitter_qam64'>, <class 'transmitters_WIN.transmitter_gfsk'>, <class 'transmitters_WIN.transmitter_cpfsk'>]
print "Mod type: " + str(mod_type[mod_type_key].modname)
print "SNR: " + str(snr)
dataset[(mod_type[mod_type_key].modname, snr)] = np.zeros([nvecs_per_key, 2, vec_length], dtype=np.float32)
#data set is [1000, 2, 128]

modvec_indx = 0
tx_len = int(10e3)
if mod_type[mod_type_key].modname == "QAM16":
  tx_len = int(20e3)
if mod_type[mod_type_key].modname == "QAM64":
  tx_len = int(30e3)
  

src = source_alphabet(alphabet_type, tx_len, True) # works okay with FIFO file
mod = mod_type[mod_type_key]()

sample_rate = 200e3 # Input sample rate in Hz
sro_std_dev = 0.01  # sample rate drift process standard deviation per sample in Hz
sro_max_dev = 50    # maximum sample rate offset in Hz
cfo_std_dev = 0.01  # carrier frequnecy drift process standard deviation per sample in Hz
cfo_max_dev = 500  # maximum carrier frequency offset in Hz
N_sinusoids = 8     # number of sinusoids used in frequency selective fading simulation
fD = 1				# doppler frequency
LOS_model = True    # defines whether the fading model should include a line of site component. LOS->Rician, NLOS->Rayleigh
K_factor = 4        # Rician K-factor, the ratio of specular to diffuse power in the model
delays = [0.0, 0.9, 1.7] # A list of fractional sample delays making up the power delay profile
mags = [1, 0.8, 0.3]     # A list of magnitudes corresponding to each delay time in the power delay profile
ntaps = 8				 # The length of the filter to interpolate the power delay profile over. Delays in the PDP must lie between 0 and ntaps_mpath, fractional delays will be sinc-interpolated only to the width of this filter.
noise_amp = 10**(-snr/10.0) # Specifies the standard deviation of the AWGN process
chan = channels.dynamic_channel_model( sample_rate, sro_std_dev, sro_max_dev, cfo_std_dev, cfo_max_dev,
									   N_sinusoids, fD, LOS_model, K_factor, delays, mags, ntaps, noise_amp, 0x1337 )

# add an optional eth sink 
#snk_udp = blocks.udp_sink(gr.sizeof_float*1, '192.168.1.187', 45000, 1472, True))		  
snk = blocks.vector_sink_c()

tb = gr.top_block()

# connect blocks
print "starting source: " + str(src) + "and mod: " + str(mod)
if apply_channel:
    tb.connect(src, mod, chan, snk)
else:
    tb.connect(src, mod, snk)
tb.run()

# vec_length = 128
# sampler_indx: some in [50, 500]
#len(raw_output_vector) = 79993
if write_to_file:
	insufficient_modsnr_vectors = True
	raw_output_vector = np.array(snk.data(), dtype=np.complex64)
	# start the sampler some random time after channel model transients (arbitrary values here)
	sampler_indx = random.randint(50, 500)
	while(insufficient_modsnr_vectors):
		while modvec_indx < nvecs_per_key:
			# sampler_indx + vec_length < len(raw_output_vector) and
			sampled_vector = raw_output_vector[sampler_indx:sampler_indx+vec_length]
			# Normalize the energy in this vector to be 1
			energy = np.sum((np.abs(sampled_vector)))
			sampled_vector = sampled_vector / energy
			dataset[(mod_type[mod_type_key].modname, snr)][modvec_indx,0,:] = np.real(sampled_vector)
			dataset[(mod_type[mod_type_key].modname, snr)][modvec_indx,1,:] = np.imag(sampled_vector)
			# bound the upper end very high so it's likely we get multiple passes through
			# independent channels
			#sampler_indx += random.randint(vec_length, round(len(raw_output_vector)*.05))
			sampler_indx += random.randint(vec_length, round(len(raw_output_vector)*.05)) 
			sampler_indx = sampler_indx % (len(raw_output_vector) - vec_length)
			modvec_indx += 1
			
		
		
		if modvec_indx == nvecs_per_key:
			# we're all done
			insufficient_modsnr_vectors = False


			
if write_to_file:
	print "all done. writing to disk"
	filename = "" + mod_type[mod_type_key].modname + "_" + str(snr) + "out.dat"
	cPickle.dump( dataset, file(filename, "wb" ) )

	
print("percentage non-zero: " + str(100*np.count_nonzero(dataset[(mod_type[mod_type_key].modname, snr)]) / (2*vec_length*nvecs_per_key)))
print("")

