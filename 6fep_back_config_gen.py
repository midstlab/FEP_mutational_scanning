from prody import *
from pylab import *
import numpy as np
from os.path import basename
import fnmatch
import os



def config_gen(pdb_name):
	file_name_wh_ex = str(os.path.splitext(pdb_name)[0])
	structure = parsePDB(str(pdb_name))
	f = open(str(file_name_wh_ex)+"_config_min_forw_back.conf", 'w')
	f.write("""

###################################################
# FEP Forward
###################################################


# INPUT

set temperature         310.0

parameters              par_all36_carb.prm
parameters              par_all36_cgenff.prm
parameters              par_all36_na.prm
parameters              par_all36_prot.prm
parameters              toppar_water_ions.str
parameters              TMPP.par
parameters              D4TMPP.par
paraTypeCharmm          on

exclude                 scaled1-4
1-4scaling              1.0

""")

	f.write("%-10s\t\t\t\t%-10s\n" % ("structure",str(file_name_wh_ex)+".psf"))
	f.write("\n")
	f.write("#COORDINATES\n")
	f.write("\n")
	f.write("%-10s\t\t\t\t\t%-10s\n" % ("coordinates",str(file_name_wh_ex)+".pdb"))
	f.write("%-10s\t\t\t\t%-10s\n" % ("bincoordinates",str(file_name_wh_ex)+"_min_forw.coor"))
	f.write("%-10s\t\t\t\t%-10s\n" % ("binvelocities",str(file_name_wh_ex)+"_min_forw.vel"))
	f.write("%-10s\t\t\t\t%-10s\n" % ("extendedsystem",str(file_name_wh_ex)+"_min_forw.xsc"))
	f.write("\n")
	f.write("\n")
	f.write("\n")
	f.write("""
# OUTPUT FREQUENCIES

outputenergies          200
outputtiming            200
outputpressure          200
restartfreq             200
XSTFreq                 200


# OUTPUT AND RESTART

dcdfreq                 10000
""")
	f.write("DCDfile     			%s_min_forw_back.dcd\n" % (str(file_name_wh_ex)))

	f.write("\n")
	f.write("\n")

	f.write("outputname     		%s_min_forw_back\n" % (str(file_name_wh_ex)))
	f.write("restartname    		%s_min_forw_back\n" % (str(file_name_wh_ex)))
	f.write("\n")
	f.write("\n")
	f.write("""
binaryoutput            yes
binaryrestart           yes

# CONSTANT-T

langevin                on
langevinTemp            310.0
langevinDamping         1.0
langevinHydrogen        no


# CELL

""")

	###################
	pdb_atom_coords = structure.getCoords()
	xmax = np.max(pdb_atom_coords[:, 0])
	ymax = np.max(pdb_atom_coords[:, 1])
	zmax = np.max(pdb_atom_coords[:, 2])
	xmin = np.min(pdb_atom_coords[:, 0])
	ymin = np.min(pdb_atom_coords[:, 1])
	zmin = np.min(pdb_atom_coords[:, 2])
	cb_vec1 = abs(xmax-xmin)+0.1
	cb_vec2 = abs(ymax-ymin)+0.1
	cb_vec3 = abs(zmax-zmin)+0.1
	cb_vec1_f = "{0:.1f}".format(cb_vec1)
	cb_vec2_f = "{0:.1f}".format(cb_vec2)
	cb_vec3_f = "{0:.1f}".format(cb_vec3)
	co_x = (xmax+xmin)/2
	co_y = (ymax+ymin)/2
	co_z = (zmax+zmin)/2
	co_x_f = "{0:.1f}".format(co_x)
	co_y_f = "{0:.1f}".format(co_y)
	co_z_f = "{0:.1f}".format(co_z)
	###################

	f.write("# Periodic Boundary Conditions\n")
	f.write("cellBasisVector1\t\t%s\t0.0\t\t0.0\n" % cb_vec1_f)
	f.write("cellBasisVector2\t\t0.0\t\t%s\t0.0\n" % cb_vec2_f)
	f.write("cellBasisVector3\t\t0.0\t\t0.0\t\t%s\n"% cb_vec3_f)
	f.write("cellOrigin\t\t\t\t%s\t%s\t%s\n" % (co_x_f, co_y_f, co_z_f))
	f.write("\n")
	f.write("\n")
	######################
	f.write("\n")
	f.write("\n")

	f.write("""

# PME

PME                     yes
pmeGridSpacing          1.0
PMETolerance            10e-6
PMEInterpOrder          4



# WRAP WATER FOR OUTPUT

wrapAll                 on
wrapWater               on


# CONSTANT-P

LangevinPiston          on
LangevinPistonTarget    1.01325
LangevinPistonPeriod    100
LangevinPistonDecay     100
LangevinPistonTemp      $temperature

StrainRate              0.0 0.0 0.0
useGroupPressure        yes

useFlexibleCell         no
useConstantArea         no

# SPACE PARTITIONING

stepspercycle           10
margin                  1.0


# CUT-OFFS

switching               on
switchdist              11.0
cutoff                  13.0
pairlistdist            15.0


# RESPA PROPAGATOR

timestep                2
fullElectFrequency      2
nonbondedFreq           1


# SHAKE

rigidbonds              all
rigidtolerance          0.000001
rigiditerations         400


# COM

commotion               no


# FEP PARAMETERS

source                  fep.tcl

alch                    on
alchType                FEP
""")
	f.write("alchFile     			%s.fep\n" % (str(file_name_wh_ex)))
	f.write("alchCol                 B\n")
	f.write("alchOutFile             %s_back.fepout\n" % (str(file_name_wh_ex)))
	f.write("alchOutFreq             1000\n")

	f.write("""
alchVdwLambdaEnd        1.0
alchElecLambdaStart     0.5
alchVdWShiftCoeff       4.0
alchDecouple            on

alchEquilSteps          50000
set numSteps            100000

runFEP 1.0 0.0 -0.03125 $numSteps

""")

	f.close()

	return

for file in os.listdir('.'):
    if fnmatch.fnmatch(file, '*_fep_wb_ionized.pdb'):
        pdb = file
        config_gen(str(pdb))
