#!/usr/bin/env python

from prody import *
from pylab import *
import numpy as np
from os.path import basename
import fnmatch
import os


file_names_sorted = []
for file in os.listdir('.'):
    if fnmatch.fnmatch(file, '*_min.conf'):
        file_name_wh_ex = str(os.path.splitext(file)[0])
        file_names_sorted.append(file_name_wh_ex)
        file_names_sorted = sorted(file_names_sorted, key=str.lower)


f = open("config_joblist", 'w')

f.write("""#!/bin/bash

# Job to submit to a GPU node.
#SBATCH --account DD-22-92
#SBATCH --nodes 1
#SBATCH --partition qgpu
#SBATCH --time 08:00:00
#SBATCH --gpus 8
cd $SLURM_SUBMIT_DIR

\n
""")
f.write("echo config jobs started\n")

range_list = len(file_names_sorted)

for i in range(range_list):
    if i == 8:
    	print("Extremely FATAL error: device number cannot be larger than 7!!!")
    	break
    f.write("/home/it4i-cananat/NAMD_3.0alpha8_Linux-x86_64-multicore-CUDA/namd3 +p16 +devices %s %s.conf > %s.log && /home/it4i-cananat/NAMD_3.0alpha8_Linux-x86_64-multicore-CUDA/namd3 +p16 --CUDASOAintegrate on +devices %s %s_forw.conf > %s_forw.log && /home/it4i-cananat/NAMD_3.0alpha8_Linux-x86_64-multicore-CUDA/namd3 +p16 --CUDASOAintegrate on +devices %s %s_forw_back.conf > %s_forw_back.log &\n" %(str(i), str(file_names_sorted[i]), str(file_names_sorted[i]), str(i), str(file_names_sorted[i]), str(file_names_sorted[i]), str(i), str(file_names_sorted[i]), str(file_names_sorted[i]) ))
    f.write("\n")
    
f.write("wait\n")
f.write(" echo all jobs are finished")
f.close()
