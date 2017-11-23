# get info about file
import pickle
import sys

if (len(sys.argv) < 2):
	raise IOError("No file given")

filename = sys.argv[1]
print('Loading the file. Please wait')

# Load the dataset ...
Xd = pickle.load(open(filename,'rb'),encoding='latin1') 
snrs,mods = map(lambda j: sorted(list(set(map(lambda x: x[j], Xd.keys())))), [1,0])

print("snrs: ", snrs)
print("mods: ", mods)

elem1 = Xd[mods[0], snrs[0]] 
print ("Dimensions of one element of the set:" , elem1.shape)

print("Length sample: ", elem1.shape[2])
print("Quadrature?", 'true' if elem1.shape[1] > 1 else 'false' )
print("Number of sets of this sample: ", elem1.shape[0])

