#
# This module abstracts the call to execute the classification
# engine. 
#
# Requires Python 2.7

import subprocess # for the bash process call
import os         # to change directories

def classify(filevec):

    # directories (note that directories must be changed in the child process)
    current_dir = os.getcwd()
    root_RFML_dir = r'/home/ubuntu/RFML'
    data_RFML_dir = r'/home/ubuntu/RFML/data/rfml_data/'
    # get the name of the file without any path info
    filename = os.path.basename(filevec)
    print("filename: " + filename)
    print("filevec: " + filevec)
    # must be called from rootRFML_dir
    classify_cmd = "bin/rfml"
        

    # move the file into the classifier directory
    if subprocess.call(["/bin/cp", "-f", filevec, data_RFML_dir]) != 0:
        print("Problem copying files")
        raise Exception

    # move to RFML directory
    try:
        os.chdir(root_RFML_dir)
    except:
        print("problem changing to: " + root_RFML_dir)
        raise Exception
    
    # now execute classifer
    output = subprocess.check_output([classify_cmd, filename])
    print(output)

    os.chdir(current_dir)
