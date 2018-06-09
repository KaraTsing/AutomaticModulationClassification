# load 1024 length data and plot
import pickle

# Load the dataset ...
dataFile = "Data/RML2016.10a_dict.dat"
Xd = pickle.load(open(dataFile,'rb'),encoding='latin1') 
# takes about 30 seconds

# len(Xd)  :  220
# type(Xd) : dict
# Xd.keys(): every permutation of < mod_type >, < snr > 
#   for 11 mod types and 20 snrs --> 200 different data sets
 
# xmap = map(lambda x: x[j], Xd.keys()) --> map takes lambda and applies it to every element in the list given in the second arg 
#  --> j not defined

# xmap = map(lambda x: x[0], Xd.keys())
# len(list(xmap))
# --> 220
# Xd['8PSK', -20] --> array

# map(lambda j: , [0,1])


# Extract the labels
snrs,mods = map(lambda j: sorted(list(set(map(lambda x: x[j], Xd.keys())))), [1,0])

# snrs:  [-20, -18, -16, -14, -12, -10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
# mods: ['8PSK', 'AM-DSB', 'AM-SSB', 'BPSK', 'CPFSK', 'GFSK', 'PAM4', 'QAM16', 'QAM64', 'QP


# python dictionaries:
# 
#
