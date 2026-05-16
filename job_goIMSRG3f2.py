#!/usr/bin/env python

##########################################################################
##  goUniversal.py
##
##  A python script to run or submit jobs for the common use cases
##  of the IMSRG++ code. We check whether there is a pbs or slurm
##  scheduler, assign the relevant input parameters, set names
##  for the output files, and run or submit.
##  						-Ragnar Stroberg
##  						TRIUMF Nov 2016
######################################################################

import os,sys
from os import path,environ,mkdir,remove
from subprocess import call,PIPE
from sys import argv
from time import time,sleep
from datetime import datetime

path_pre = sys.path[0]
print("current path: "+path_pre)

### Check to see what type of batch submission system we're dealing with
BATCHSYS = 'NONE'
if call('type '+'qsub', shell=True, stdout=PIPE, stderr=PIPE) == 0: BATCHSYS = 'PBS'
elif call('type '+'srun', shell=True, stdout=PIPE, stderr=PIPE) == 0: BATCHSYS = 'SLURM'

### The code uses OpenMP and benefits from up to at least 24 threads
#NTHREADS=48
NTHREADS=62
#exe = '%s/bin/imsrg++'%(environ['HOME'])
exe = path_pre+'/ReadIMSRG3f2.py'

### Flag to swith between submitting to the scheduler or running in the current shell
#batch_mode=False
batch_mode=True
if 'terminal' in argv[1:]: batch_mode=False

mail_address = 'baishanhu4phys@gmail.com'

### This comes in handy if you want to loop over Z
ELEM = ['n','H','He','Li','Be','B','C','N',
       'O','F','Ne','Na','Mg','Al','Si','P','S','Cl','Ar','K',
       'Ca','Sc','Ti','V','Cr','Mn','Fe','Co',  'Ni','Cu','Zn','Ga','Ge','As','Se','Br','Kr','Rb','Sr','Y',
       'Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','In',  'Sn','Sb','Te','I','Xe','Cs','Ba','La','Ce','Pr','Nd','Pm','Sm','Eu','Gd','Tb','Dy','Ho','Er','Tm','Yb',
       'Lu','Hf','Ta','W','Re','Os','Ir','Pt','Au','Hg','Tl','Pb']# ,'Bi','Po','At','Rn','Fr','Ra','Ac','Th','U','Np','Pu']

### ARGS is a (string => string) dictionary of input variables that are passed to the main program
ARGS  =  {}

ARGS['smax'] = '500'
#ARGS['lmax3'] = '10' # for comparing with Heiko
ARGS['omega_norm_max'] = '0.25'
#ARGS['ode_tolerance'] = '1e-5'
#ARGS['scratch'] = 'SCRATCH' # when calculating other operators
#ARGS['scratch'] = '/home/bhu/scratch'
#ARGS['scratch'] = '/home/bhu/scratch/SCRATCH'
#ARGS['scratch'] = '/home/bhu/scratch/SCRATCH_temp'
#ARGS['scratch'] = '/dev/null' # saves memory when just energies

#ARGS['method'] = 'MP3'
ARGS['method'] = 'magnus'
#ARGS['method'] = 'NSmagnus'
#ARGS['method'] = 'brueckner'
#ARGS['method'] = 'flow'
#ARGS['method'] = 'HF'

ARGS['approx'] = 'imsrg3f2'

#ARGS['write_omega'] = 'true'

### Create the 'script' that we need for execution
if BATCHSYS == 'PBS':
  FILECONTENT = """#!/bin/bash
#PBS -N %s
#PBS -q oak
#PBS -d %s
#PBS -l walltime=48:00:00
#PBS -l nodes=1:ppn=%d
#PBS -l vmem=250gb
#PBS -m abe
#PBS -M %s
#PBS -j oe
#PBS -o pbslog/%s.o
#PBS -e pbslog/%s.e
cd $PBS_O_WORKDIR
export OMP_NUM_THREADS=%d
%s
"""

# --account=rrg-holt def-holt
# Also notice that my files are outputing to a folder called 'pbslog' which resides in the same directory as this script.
elif BATCHSYS == 'SLURM':
  FILECONTENT = """#!/bin/bash
##SBATCH --account=def-holt
#SBATCH --account=rrg-holt
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=%d
#SBATCH --output=imsrg_log/%s.%%j
#SBATCH --time=%s
##SBATCH --mem=187G
#SBATCH --mem=250G
#SBATCH --job-name=%s
#SBATCH --mail-user=%s
#SBATCH --mail-type=FAIL
cd $SLURM_SUBMIT_DIR
echo NTHREADS = %d
export OMP_NUM_THREADS=%d
time srun %s
"""

### Make a directory for the log files, if it doesn't already exist
if not path.exists('imsrg_log'): mkdir('imsrg_log')

ARGS['nucleon_mass_correction'] = 'true'

#ARGS['goose_tank'] = 'true'

#As=[49,51,53,55]
#Zs=[21,23,25,27]
#As=[41,42,43,44,45,46,47,48,49]
#Zs=[21,21,21,21,21,21,21,21,21]
#As=[42]
#Zs=[21]

#As=[120,132,48,68]
#Zs=[50,50,20,28]
#As=[120,132]
#Zs=[50,50]
#As=[48,68]
#Zs=[20,28]
#As=[100,114]
#Zs=[50,50]
#As=[40,56,78,90,100,114]
#Zs=[20,28,28,40,50,50]
#As=[78]
#Zs=[28]
#As=[14,14]
#Zs=[6,7]
#As=[28]
#Zs=[8]
#As=[196,197,198,199,200,201,202,203,204,205,206,207]
#Zs=[70,71,72,73,74,75,76,77,78,79,80,81]
#As=[196,197,198]
#Zs=[70,71,72]
#As=[206]
#Zs=[80]
#As=[48,47,46,45,44,43,42,41]
#Zs=[28,27,26,25,24,23,22,21]
#As=[19,23,27,29]
#Zs=[9,11,13,14]
#As=[73]
#Zs=[32]
#As=[127,129,131]
#Zs=[53,54,54]
#As=[127]
#Zs=[53]
#As=[40] ##Ar
#Zs=[18]
#As=[19,23] ##F, Na
#Zs=[9,11]
#As=[28,29,30] ##Si
#Zs=[14,14,14]
#As=[70,72,73,74,76]  ##Ge
#Zs=[32,32,32,32,32]
#As=[127,133] ##I, Cs
#Zs=[53,55]
#As=[128,129,130,131,132,134,136] ##Xe
#Zs=[54,54,54,54,54,54,54]
#As=[128,130,132,134,136] ##Xe
#Zs=[54,54,54,54,54]
#As=[133]
#Zs=[55]
#As=[56,56,56,56,56]
#Zs=[28,26,24,22,20]
#As=[56,56,56,56]
#Zs=[28,26,24,22]
#As=[56]
#Zs=[28]
#As=[25,26,27,28]
#Zs=[ 8, 8, 8, 8]
#As=[24]
#Zs=[ 8]
#As = []; Zs = []
#Ai=list(range(14,29)); Zi=[8]*len(Ai);  As.extend(Ai); Zs.extend(Zi)
#As = []; Zs = []
#Ai=list(range(92,108)); Zi=[47]*len(Ai);  As.extend(Ai); Zs.extend(Zi)
#Ai=list(range(92,93)); Zi=[47]*len(Ai);  As.extend(Ai); Zs.extend(Zi)

### Si
#As = []; Zs = []
#Ai=list(range(26,37)); Zi=[14]*len(Ai);  As.extend(Ai); Zs.extend(Zi)
#As=[144]
#Zs=[ 54]
### Sr
#As = []; Zs = []
#Ai=list(range(72,77)); Zi=[38]*len(Ai);  As.extend(Ai); Zs.extend(Zi)
#As=[74,74,74]
#Zs=[36,37,38]
#As=[75,75]
#Zs=[37,38]

### N=51
As=[79,81,83,85,87,89,91]
Zs=[28,30,32,34,36,38,40]
#As=[81,87,89,91]
#Zs=[30,36,38,40]

### Cd 
#As = []; Zs = []
#Ai=list(range(92,108)); Zi=[48]*len(Ai);  As.extend(Ai); Zs.extend(Zi)
#As = [96,97,98,99,100]
#Zs = [48,48,48,48, 48]
#As = [92,93,94,95,101,102,103,104,105,106,107]
#Zs = [48,48,48,48, 48, 48, 48, 48, 48, 48, 48]

### Ne
#As = []; Zs = []
#Ai=list(range(20,36)); Zi=[10]*len(Ai);  As.extend(Ai); Zs.extend(Zi)
#As = [28]
#Zs = [10]


#As=[36,36,38,38]
#Zs=[20,16,20,18]
#As=[36,36]
#Zs=[16,20]
#As=[38,38,41,41]
#Zs=[18,20,21,20]
#As=[32,32]
#Zs=[14,18]
As=[36,36,48,48]
Zs=[16,20,20,28]
#As = [54,54]
#Zs = [26,28]
#As = [52,52]
#Zs = [28,24]
#As = [42,44,46,48]
#Zs = [21,21,21,21]
As = [50,52,54]
Zs = [23,25,27]

As = [40]
Zs = [18]
As = [133]
Zs = [ 49]

### Ne
As = []; Zs = []
Ai=list(range(20,36,2)); Zi=[10]*len(Ai);  As.extend(Ai); Zs.extend(Zi)
#As = [20,21,22,23,24,25,26,27,29,30,31,32,33,34,35]
#Zs = [10,10,10,10,10,10,10,10,10,10,10,10,10,10,10]


As=[4,16,22,24,36,40,48,52,54,56,68,78,90,100,114,120,132,208]
Zs=[2, 8, 8, 8,20,20,20,20,20,28,28,28,40, 50, 50, 50, 50, 82]
As=[4]
Zs=[2]

As=[52,54]
Zs=[20,20]

### Ca
#As = []; Zs = []
#Ai=list(range(40,62,2)); Zi=[20]*len(Ai);  As.extend(Ai); Zs.extend(Zi)
#Ai=list(range(41,63,2)); Zi=[20]*len(Ai);  As.extend(Ai); Zs.extend(Zi)
#As=[60,50,52,54,56,58]
#Zs=[20,20,20,20,20,20]

### Mo92,Ru94,Pd96,Cd98  pf5g9-Ni56
#As = [92,94,96,98]
#Zs = [42,44,46,48]


#intes=['PWA2.0_2.0','EM2.2_2.0','EM2.0_2.0','N2LO_sat','DNNLOgo450','DNLOgo450','DNNLOgo','EM1.8_2.0']
#intes=['PWA2.0_2.0','EM2.2_2.0','EM2.0_2.0','N2LO_sat','DNNLOgo450','DNLOgo450','DNNLOgo']
#intes=['EM2.2_2.0','EM2.0_2.0','N2LO_sat','DNNLOgo450','DNLOgo450','DNNLOgo','EM1.8_2.0']
#intes=['N3LO_LNL2','DNNLOgo','EM1.8_2.0']
#intes=['N2LO_sat']
#intes=['EM1.8_2.0','N2LOgo','N3LO_EM500_LNL']
#intes=['N3LO_EM500_LNL']
#intes=['N3LO_LNL2']
#intes=['N3LO_EM500_LNL','N2LO_sat','DNNLOgo','EM1.8_2.0']
#intes=['N3LO_EM500_LNL']
#intes=['EM1.8_2.0','DNNLOgo','N2LO_sat']
#intes=['EM1.8_2.0','DNNLOgo']
intes=['EM1.8_2.0']
#intes=['DNNLOgo']
#intes=['DNLOgo450','DNNLOgo450']
#intes=['DNNLOgo450']
#intes=['Texas']

## Loop over multiple jobs to submit
#for A in range(68,69):
#for A in [48]:
# Z=28
for i in range(0,len(As)):
    Z=Zs[i]
    A=As[i]
    for reference in ['%s%d'%(ELEM[Z],A)]:
        ARGS['reference'] = reference
        ARGS['e3max'] = '28'
        for inte in intes:
            if(inte == 'N3LO_EM500_LNL'): ARGS['e3max'] = '22'
            #for e in [6,8,10,12,14]:
            for e in [12]:
                for hw in [12,16]:
                # for hw in [8,10,12]:
                    ARGS['A'] = '%d'%A
                    ARGS['Z'] = '%d'%Z
                    ARGS['hw'] = '%d'%hw
                    ARGS['emax'] = '%d'%e

                    #ARGS['emax_imsrg'] = '12'
                    #ARGS['e2max_imsrg'] = '24'
                    #ARGS['e3max_imsrg'] = '0'

                    ARGS['valence_file_format'] = 'tokyo'
                    #ARGS['valence_file_format'] = 'nushellx'
                    #ARGS['core_generator'] = 'white'
                    #ARGS['valence_generator'] = 'shell-model'
                    # ARGS['core_generator'] = 'atan'
                    # ARGS['valence_generator'] = 'shell-model-atan'
                    #ARGS['core_generator'] = 'atan'
                    #ARGS['valence_generator'] = 'shell-model-atan-npnh'
                    #ARGS['core_generator'] = 'atan'
                    #ARGS['valence_generator'] = '1PA'

                    #ARGS['denominator_delta_orbit'] = 'all'
                    #ARGS['denominator_delta'] = '10'
                    #ARGS['BetaCM'] = '3'
                    ARGS['BetaCM'] = '4'

                    #ARGS['occ_file'] = 'occ_file_In107.dat'
                    #ARGS['occ_file'] = './occ_file/occ_file_%s_1.dat'%(reference)
                    #ARGS['occ_file'] = './occ_file/occ_file_%s_P1N1.dat'%(reference)
                    #ARGS['occ_name'] = 'OccP1N1'
                    #ARGS['freeze_occupations'] = 'true'

                    #ARGS['basis'] = 'NAT'
               #     ARGS['use_NAT_occupations'] = 'true'
               #     ARGS['basis'] = 'oscillator'
               #     ARGS['hwBetaCM'] = '12'
                    #ARGS['goose_tank']='true'
                    ARGS['goose_tank']='false'
                    #ARGS['eta_criterion'] = '1e-5'


                    ARGS['valence_space'] = reference  # Select for Single Ref. calculation
                    #ARGS['valence_space'] = '0hw-shell'
                    #ARGS['valence_space'] = 'p-shell'
                    #ARGS['valence_space'] = 'sd-shell'
                    #ARGS['valence_space'] = 'fp-shell'
               #     ARGS['valence_space'] = 'sdfp-shell'
               #     ARGS['valence_space'] = 'psdnp-shell'
               #     ARGS['custom_valence_space'] = 'O10,p0d5,p0d3,p1s1,n0p1,n0p3'
               #     ARGS['valence_space'] = 'ppnsd-shell'
               #     ARGS['custom_valence_space'] = 'He10,p0p1,p0p3,n0d5,n0d3,n1s1'
               #     ARGS['valence_space'] = 'psdnpf-shell'
               #     ARGS['custom_valence_space'] = 'O28,p0d5,p0d3,p1s1,n0f7,n0f5,n1p3,n1p1'
               #     ARGS['valence_space'] = 'ppnsd-shell'
               #     ARGS['custom_valence_space'] = 'He10,p0p1,p0p3,n0d5,n0d3,n1s1'
               #     ARGS['valence_space'] = 'ppfnsd-shell'
               #     ARGS['custom_valence_space'] = 'Ca28,p0f7,p0f5,p1p3,p1p1,n0d5,n0d3,n1s1'
               #     ARGS['valence_space'] = 'Ni%d'%A
               #     ARGS['valence_space'] = 'pd5-shell'
               #     ARGS['custom_valence_space'] = 'He4,p0p1,p0p3,p0d5,n0p1,n0p3,n0d5'
               #     ARGS['valence_space'] = 'npf5g9-48Ca'
               #     ARGS['custom_valence_space'] = 'Ca48,n0f5,n1p3,n1p1,n0g9'
               #     ARGS['valence_space'] = 'npf5g9d5-48Ca'
               #     ARGS['custom_valence_space'] = 'Ca48,n0f5,n1p3,n1p1,n0g9,n1d5'
               #     ARGS['valence_space'] = 'npf5g9d5s1-48Ca'
               #     ARGS['custom_valence_space'] = 'Ca48,n0f5,n1p3,n1p1,n0g9,n1d5,n2s1'
                    #ARGS['valence_space'] = 'pf5-Ca48'
                    #ARGS['custom_valence_space'] = 'Ca48,p0f7,p0f5,n0f5,p1p3,n1p3,p1p1,n1p1'
               #     ARGS['valence_space'] = 'pf5g9-48Ca'
               #     ARGS['custom_valence_space'] = 'Ca48,p0f7,p0f5,n0f5,p1p3,n1p3,p1p1,n1p1,n0g9'
               #     ARGS['valence_space'] = 'pf5g9d5-48Ca'
               #     ARGS['custom_valence_space'] = 'Ca48,p0f7,p0f5,n0f5,p1p3,n1p3,p1p1,n1p1,n0g9,n1d5'
               #     ARGS['valence_space'] = 'pf5g9d5s1-48Ca'
               #     ARGS['custom_valence_space'] = 'Ca48,p0f7,p0f5,n0f5,p1p3,n1p3,p1p1,n1p1,n0g9,n1d5,n2s1'
               #     ARGS['valence_space'] = 'pf5g9-52Ca'
               #     ARGS['custom_valence_space'] = 'Ca52,p0f7,p0f5,n0f5,p1p3,p1p1,n1p1,n0g9'
               #     ARGS['valence_space'] = 'pf5g9-56Ni'
               #     ARGS['custom_valence_space'] = 'Ni56,p0f5,n0f5,p1p3,n1p3,p1p1,n1p1,p0g9,n0g9'
               #     ARGS['valence_space'] = 'pf5g9d5-52Ca-hw10'
               #     ARGS['custom_valence_space'] = 'Ca52,p0f7,p0f5,n0f5,p1p3,n1p3,p1p1,n1p1,n0g9,n1d5'
               #     ARGS['valence_space'] = 'pf5g9d5-56Ni'
               #     ARGS['custom_valence_space'] = 'Ni56,p0f5,n0f5,p1p3,n1p3,p1p1,n1p1,p0g9,n0g9,p1d5,n1d5'
               #     ARGS['valence_space'] = 'pfsdg'
               #     ARGS['custom_valence_space'] = 'Ca40,p0f7,n0f7,p0f5,n0f5,p1p3,n1p3,p1p1,n1p1,p0g9,n0g9,p1d5,n1d5,p2s1,n2s1,p1d3,n1d3,p0g7,n0g7'
               #     ARGS['valence_space'] = 'sdgh11-100Sn'
               #     ARGS['custom_valence_space'] = 'Sn100,p0g7,p1d5,p1d3,p2s1,n0g7,n1d5,n1d3,n2s1,n0h11'
               #     ARGS['valence_space'] = 'h11f7p3-120Sn'
               #     ARGS['custom_valence_space'] = 'Sn120,p0g7,p1d5,p1d3,p2s1,n0h11,n1f7,n2p3'
               #     ARGS['valence_space'] = 's1d3h11f7p3-114Sn'
               #     ARGS['custom_valence_space'] = 'Sn114,p0g7,p1d5,p1d3,p2s1,n2s1,n1d3,n0h11,n1f7,n2p3'
               #     ARGS['valence_space'] = 's1d3h11f7p3-Ni92' # neutron-rich Cd-Sn-Te
               #     ARGS['custom_valence_space'] = 'Ni92,p0f5,p1p3,p1p1,p0g9,n2s1,n1d3,n0h11,n1f7,n2p3'
               #     ARGS['valence_space'] = 'h11f7p3-Ni98'
               #     ARGS['custom_valence_space'] = 'Ni98,p0f5,p1p3,p1p1,p0g9,n0h11,n1f7,n2p3'
                    #ARGS['valence_space'] = 'Zr104a-shell'
                    #ARGS['custom_valence_space'] = 'Zr104,p0g9,p1d5,p0g7,p2s1,p1d3,n2s1,n1d3,n0h11,n1f7,n2p3'
               #     ARGS['valence_space'] = 'Zr90a-shell'
               #     ARGS['custom_valence_space'] = 'Zr90,p0g9,p1d5,p0g7,p2s1,p1d3,n1d5,n0g7,n2s1,n1d3,n0h11'
               #     ARGS['valence_space'] = 'fph9-132Sn'
               #     ARGS['custom_valence_space'] = 'Sn132,p1f7,p1f5,p2p3,p2p1,p0h9'
                    #ARGS['valence_space'] = 'sd3f7p3-Si28'
                    #ARGS['custom_valence_space'] = 'Si28,p0d3,n0d3,p1s1,n1s1,p0f7,n0f7,p1p3,n1p3'
               #     ARGS['valence_space'] = 'sdf7p3-34Si'
               #     ARGS['custom_valence_space'] = 'Si34,p0d3,p1s1,p0f7,n0f7,p1p3,n1p3,n1p1,n0f5'
               #     ARGS['valence_space'] = 'sdf7p3-32S'
               #     ARGS['custom_valence_space'] = 'S32,p0d3,n0d3,p0f7,n0f7,p1p3,n1p3'
               #     ARGS['valence_space'] = 'df7p3-36S'
               #     ARGS['custom_valence_space'] = 'S36,p0d3,p0f7,n0f7,p1p3,n1p3,n1p1,n0f5'
               #     ARGS['valence_space'] = 'sdf7p-22O'
               #     ARGS['custom_valence_space'] = 'O22,p0d5,p0d3,n0d3,p1s1,n1s1,n0f7,n1p3,n1p1'
                    #ARGS['valence_space'] = 'sdf7p-16O'
                    #ARGS['custom_valence_space'] = 'O16,p0d5,n0d5,p0d3,n0d3,p1s1,n1s1,n0f7,n1p3,n1p1'
                    #ARGS['valence_space'] = 'sdf7p3-O16'
                    #ARGS['custom_valence_space'] = 'O16,p0d5,n0d5,p0d3,n0d3,p1s1,n1s1,n0f7,n1p3'
                    #ARGS['valence_space'] = 'sdf7p3-O16'
                    #ARGS['custom_valence_space'] = 'O16,p0d5,n0d5,p0d3,n0d3,p1s1,n1s1,p0f7,n0f7,p1p3,n1p3'
               #     ARGS['valence_space'] = 'sd3f7-22O'
               #     ARGS['custom_valence_space'] = 'O22,p0d5,p0d3,n0d3,p1s1,n1s1,n0f7'
                    #ARGS['valence_space'] = 'd3f7p-O24n'
                    #ARGS['custom_valence_space'] = 'O24,n0d3,n0f7,n1p3,n1p1'
               #     ARGS['valence_space'] = 'sdfpg9-36O'
               #     ARGS['custom_valence_space'] = 'O36,p0d5,p0d3,p1s1,n0f5,n1p3,n1p1,n0g9'
               #     ARGS['custom_valence_space'] = 'Sn100,p0g7,n0g7,p1d5,n1d5,p1d3,n1d3,p2s1,n2s1,p0h11,n0h11'
#                    ARGS['valence_space'] = 'jj45'
#                    ARGS['custom_valence_space'] = 'Ni78,p0g9,p0f5,p1p3,p1p1,n0h11,n0g7,n1d5,n1d3,n2s1'
                    #ARGS['valence_space'] = 'pfg9ds-Ca52'
                    #ARGS['custom_valence_space'] = 'Ca52,p0f7,p0f5,p1p3,p1p1,n0f5,n1p1,n0g9,n1d5,n1d3,n2s1'
                    #ARGS['valence_space'] = 'Ppfg9Nf5g9ds-Ca54'
                    #ARGS['custom_valence_space'] = 'Ca54,p0f7,p0f5,p1p3,p1p1,p0g9,n0f5,n0g9,n1d5,n1d3,n2s1'
                    #ARGS['valence_space'] = 'Ppfg9Ng9ds-Ca60'
                    #ARGS['custom_valence_space'] = 'Ca60,p0f7,p0f5,p1p3,p1p1,p0g9,n0g9,n1d5,n1d3,n2s1'
                    #ARGS['valence_space'] = 'psd5-shell'
                    #ARGS['custom_valence_space'] = 'He4,p0p1,p0p3,p0d5,p1s1,n0p1,n0p3,n0d5,n1s1'
                    #ARGS['valence_space'] = 'fph9i13-Sn132'
                    #ARGS['custom_valence_space'] = 'Sn132,p0g7,p1d5,p1d3,p2s1,p0h11,n1f7,n1f5,n2p3,n2p1,n0h9,n0i13'
                    #ARGS['valence_space'] = 'fph9-Sn132'
                    #ARGS['custom_valence_space'] = 'Sn132,p0g7,p1d5,p1d3,p2s1,p0h11,n1f7,n1f5,n2p3,n2p1,n0h9'
                    #ARGS['valence_space'] = 'sdg7h11-Sn100'
                    #ARGS['custom_valence_space'] = 'Sn100,p0g7,n0g7,p1d5,n1d5,p1d3,n1d3,p2s1,n2s1,p0h11,n0h11'
                    #ARGS['valence_space'] = 'pf5g9-Ni56'
                    #ARGS['custom_valence_space'] = 'Ni56,p0f5,n0f5,p1p3,n1p3,p1p1,n1p1,p0g9,n0g9'
                    #ARGS['valence_space'] = 'sdf7p-Si28'
                    #ARGS['custom_valence_space'] = 'Si28,p0d3,n0d3,p1s1,n1s1,p0f7,n0f7,p1p3,n1p3,p1p1,n1p1'
                    #ARGS['valence_space'] = 'sd3f7p3-Si28'
                    #ARGS['custom_valence_space'] = 'Si28,p0d3,n0d3,p1s1,n1s1,p0f7,n0f7,p1p3,n1p3'
                    #ARGS['valence_space'] = 'PxNsd'
                    #ARGS['custom_valence_space'] = 'O16,n0d5,n0d3,n1s1'
                    #ARGS['valence_space'] = 'd3-O24n'
                    #ARGS['custom_valence_space'] = 'O24,n0d3'
                    #ARGS['valence_space'] = 'sdgh-Zr80'
                    #ARGS['custom_valence_space'] = 'Zr80,p0g9,n0g9,p0g7,n0g7,p1d5,n1d5,p1d3,n1d3,p2s1,n2s1,p0h11,n0h11,p0h9,n0h9'
                    #ARGS['valence_space'] = 'sdg-Zr80'
                    #ARGS['custom_valence_space'] = 'Zr80,p0g9,n0g9,p0g7,n0g7,p1d5,n1d5,p1d3,n1d3,p2s1,n2s1'
                    #ARGS['valence_space'] = 'pgd5-Se68'
                    #ARGS['custom_valence_space'] = 'Se68,p1p1,p1p3,p1d5,p0g7,p0g9,n1p1,n1p3,n1d5,n0g7,n0g9'
                    #ARGS['valence_space'] = 'sdg-Zr80'
                    #ARGS['custom_valence_space'] = 'Zr80,p0g9,n0g9,p0g7,n0g7,p1d5,n1d5,p1d3,n1d3,p2s1,n2s1'
                    #ARGS['valence_space'] = 'Pg9Nsdg-Zr80'
                    #ARGS['custom_valence_space'] = 'Zr80,p0g9,n0g9,n0g7,n1d5,n1d3,n2s1'
                    #ARGS['valence_space'] = 'Npf5g9d5s1-48Ca'
                    #ARGS['custom_valence_space'] = 'Ca48,n0f5,n1p3,n1p1,n0g9,n1d5,n2s1'


               #     ARGS['3bme'] = 'none'
               #     ARGS['LECs'] = 'EM1.8'

                    ARGS['fmt2'] = 'me2j'
                    ARGS['no2b_precision'] = 'single'


                    if inte == 'PWA2.0_2.0':
                        ARGS['LECs'] = 'PWA2.0_2.0'
                        ARGS['file2e1max'] = '16 file2e2max=32 file2lmax=16'
                        ARGS['2bme'] = '/project/6006601/shared/me2j/TwBME-HO_NN-only_N3LO_EM500_srg2.0_hw%d_emax16_e2max32.me2j.gz'%(hw)
                        ARGS['file3e1max'] = '16 file3e2max=32 file3e3max=24'
                        ARGS['3bme'] = '/project/6006601/shared/me3j/NO2B_ThBME_PWA2.0_2.0_3NFJmax15_IS_hw%d_ms16_32_24.stream.bin'%(hw)
                        ARGS['3bme_type'] = "no2b"
                    elif inte == 'EM2.2_2.0':
                        ARGS['LECs'] = 'EM2.2_2.0'
                        ARGS['file2e1max'] = '16 file2e2max=32 file2lmax=16'
                        ARGS['2bme'] = '/project/6006601/shared/me2j/TwBME-HO_NN-only_N3LO_EM500_srg2.2_hw%d_emax16_e2max32.me2j.gz'%(hw)
                        ARGS['file3e1max'] = '16 file3e2max=32 file3e3max=24'
                        ARGS['3bme'] = '/project/6006601/shared/me3j/NO2B_ThBME_EM2.2_2.0_3NFJmax15_IS_hw%d_ms16_32_24.stream.bin'%(hw)
                        ARGS['3bme_type'] = "no2b"
                    elif inte == 'EM2.0_2.0':
                        ARGS['LECs'] = 'EM2.0_2.0'
                        ARGS['file2e1max'] = '16 file2e2max=32 file2lmax=16'
                        ARGS['2bme'] = '/project/6006601/shared/me2j/TwBME-HO_NN-only_N3LO_EM500_srg2.0_hw%d_emax16_e2max32.me2j.gz'%(hw)
                        ARGS['file3e1max'] = '16 file3e2max=32 file3e3max=24'
                        ARGS['3bme'] = '/project/6006601/shared/me3j/NO2B_ThBME_EM2.0_2.0_3NFJmax15_IS_hw%d_ms16_32_24.stream.bin'%(hw)
                        ARGS['3bme_type'] = "no2b"
                    elif inte == 'EM1.8_2.0':
                        ARGS['LECs'] = 'EM1.8_2.0'
#                        ARGS['file2e1max'] = '16 file2e2max=32 file2lmax=16'
#                        ARGS['2bme'] = '/project/6006601/shared/me2j/TwBME-HO_NN-only_N3LO_EM500_srg1.8_hw%d_emax16_e2max32.me2j.gz'%(hw)
                        #ARGS['file3e1max'] = '18 file3e2max=36 file3e3max=24'
                        #ARGS['3bme'] = '/project/6006601/shared/me3j/NO2B_ThBME_EM1.8_2.0_3NFJmax15_IS_hw%d_ms18_36_24.stream.bin'%(hw)
                        #ARGS['3bme_type'] = "no2b"
#                        ARGS['file3e1max'] = '16 file3e2max=32 file3e3max=24'
#                        ARGS['3bme'] = '/project/6006601/shared/me3j/NO2B_ThBME_EM1.8_2.0_3NFJmax15_IS_hw%d_ms16_32_24.stream.bin'%(hw)
#                        ARGS['3bme_type'] = "no2b"
                        #ARGS['file2e1max'] = '18 file2e2max=36 file2lmax=18'
                        #ARGS['2bme'] = '/project/6006601/shared/me2j/TwBME-HO_NN-only_N3LO_EM500_srg1.80_hw%d_emax18_e2max36.me2j.gz'%(hw)
                        #ARGS['file3e1max'] = '18 file3e2max=36 file3e3max=24'
                        #ARGS['3bme'] = '/project/6006601/shared/me3j/NO2B_ThBME_EM1.8_2.0_3NFJmax15_IS_hw%d_ms18_36_24.stream.bin'%(hw)
                        #ARGS['3bme_type'] = "no2b"
                        ARGS['file2e1max'] = '18 file2e2max=36 file2lmax=18'
                        ARGS['2bme'] = '/home/bhu/projects/rrg-holt/tmiyagi/run_vhamil/TwBME-HO_NN-only_N3LO_EM500_srg1.8_hw%d_emax18_e2max36.me2j.gz'%(hw)
                        ARGS['file3e1max'] = '18 file3e2max=36 file3e3max=28'
                        ARGS['3bme'] = '/home/bhu/projects/rrg-holt/tmiyagi/run_vhamil/NO2B_half_ThBME_EM1.8_2.0_3NFJmax15_IS_hw%d_ms18_36_28.stream.bin'%(hw)
                        ARGS['3bme_type'] = "no2b"
                        ARGS['no2b_precision'] = "half"
                    elif inte == 'N2LO_sat':
                        ARGS['LECs'] = 'N2LO_sat'
                        ARGS['file2e1max'] = '16 file2e2max=32 file2lmax=16'
                        ARGS['2bme'] = '/project/6006601/shared/me2j/TwBME-HO_NN-only_N2LO_sat_bare_hw%d_emax16_e2max32.me2j.gz'%(hw)
                        ARGS['file3e1max'] = '16 file3e2max=32 file3e3max=24'
                        ARGS['3bme'] = '/project/6006601/shared/me3j/NO2B_ThBME_N2LOsat_3NFJmax15_IS_hw%d_ms16_32_24.stream.bin'%(hw)
                        #ARGS['file3e1max'] = '18 file3e2max=36 file3e3max=24'
                        #ARGS['3bme'] = '/project/6006601/shared/me3j/NO2B_ThBME_N2LOsat_3NFJmax15_IS_hw%d_ms18_36_24.stream.bin'%(hw)
                        ARGS['3bme_type'] = "no2b"
                    elif inte == 'DNNLOgo' or inte == 'N2LOgo':
                        ARGS['LECs'] = inte
                        ARGS['file2e1max'] = '18 file2e2max=36 file2lmax=18'
                        ARGS['2bme'] = '/project/6006601/shared/me2j/TwBME-HO_NN-only_DNNLOgo_bare_hw%d_emax18_e2max36.me2j.gz'%(hw)
                        ARGS['file3e1max'] = '16 file3e2max=32 file3e3max=24'
                        ARGS['3bme'] = '/project/6006601/shared/me3j/NO2B_ThBME_DNNLOgo_3NFJmax15_IS_hw%d_ms16_32_24.stream.bin'%(hw)
                        ARGS['3bme_type'] = "no2b"
                    elif inte == 'DNNLOgo450':
                        ARGS['LECs'] = 'DNNLOgo450'
                        ARGS['file2e1max'] = '16 file2e2max=32 file2lmax=16'
                        ARGS['2bme'] = '/project/6006601/shared/me2j/TwBME-HO_NN-only_DN2LOGO450_bare_hw%d_emax16_e2max32.me2j.gz'%(hw)
                        ARGS['file3e1max'] = '16 file3e2max=32 file3e3max=26'
                        ARGS['3bme'] = '/project/6006601/shared/me3j/NO2B_ThBME_DN2LOGO450_3NFJmax15_IS_hw%d_ms16_32_26.stream.bin'%(hw)
                        ARGS['3bme_type'] = "no2b"
                    elif inte == 'DNLOgo450':
                        ARGS['LECs'] = 'DNLOgo450'
                        ARGS['file2e1max'] = '16 file2e2max=32 file2lmax=16'
                        ARGS['2bme'] = '/project/6006601/shared/me2j/TwBME-HO_NN-only_DNLOGO450_bare_hw%d_emax16_e2max32.me2j.gz'%(hw)
                        ARGS['file3e1max'] = '16 file3e2max=32 file3e3max=26'
                        ARGS['3bme'] = '/project/6006601/shared/me3j/NO2B_ThBME_DNLOGO450_3NFJmax15_IS_hw%d_ms16_32_26.stream.bin'%(hw)
                        ARGS['3bme_type'] = "no2b"
                    elif inte == 'N3LO_LNL2':
                        ARGS['LECs'] = 'N3LO_LNL2'
                        ARGS['file2e1max'] = '16 file2e2max=32 file2lmax=16'
                        ARGS['2bme'] = '/project/6006601/shared/me2j/TwBME-HO_NN-only_N3LO_EM500_srg2.0_hw%d_emax16_e2max32.me2j.gz'%(hw)
                        ARGS['file3e1max'] = '18 file3e2max=36 file3e3max=24'
                        ARGS['3bme'] = '/project/6006601/shared/me3j/NO2B_ThBME_srg2.0_ramp46_N3LO_EM500_JJmax13_c1_-0.81_c3_-3.2_c4_5.4_cD_0.7_cE_-0.06_LNL2_650_500_IS_hw%dfrom30_ms18_36_24.stream.bin'%(hw)
                        ARGS['3bme_type'] = "no2b"
                    elif inte == 'N3LO_EM500_LNL':
                        ARGS['LECs'] = 'N3LO_EM500_LNL'
                        ARGS['file2e1max'] = '16 file2e2max=32 file2lmax=16'
                        ARGS['2bme'] = '/project/6006601/shared/me2j/TwBME-HO_NN-only_N3LO_EM500_srg2.0_hw%d_emax16_e2max32.me2j.gz'%(hw)
                        #ARGS['file3e1max'] = '18 file3e2max=36 file3e3max=24'
                        #ARGS['3bme'] = '/project/6006601/shared/me3j/NO2B_ThBME_srg2.0_ramp46_N3LO_EM500_JJmax13_c1_-0.81_c3_-3.2_c4_5.4_cD_0.7_cE_-0.06_LNL2_650_500_IS_hw%dfrom30_ms18_36_24.stream.bin'%(hw)
                        ARGS['file3e1max'] = '16 file3e2max=32 file3e3max=22'
                        ARGS['3bme'] = '/project/6006601/shared/me3j/NO2B_ThBME_srg2.0_ramp46-9-44-15-42_N3LO_EM500_3NFJmax15_c1_-0.81_c3_-3.2_c4_5.4_cD_0.7_cE_-0.06_LNL2_650_500_IS_hw%dfrom30_ms16_32_22.stream.bin'%(hw)
                        ARGS['3bme_type'] = "no2b"
                    elif inte == 'Texas':
                        ARGS['LECs'] = 'Texas'
                        ARGS['fmt2'] = 'oakridge_bin'
                        ARGS['file2e1max'] = '14 file2e2max=28 file2lmax=14'
                        ARGS['2bme'] = '/home/bhu/scratch/me2j/sp_energy_N14_hw%d.dat,/home/bhu/scratch/me2j/vn3lo394_ini2160_544p_n4_N14_hw%d.dat'%(hw,hw)
                        ARGS['file3e1max'] = '18 file3e2max=36 file3e3max=28'
                        ARGS['3bme'] = '/project/rrg-holt/shared/me_texas/NO2B_half_ThBME_Texas_3NFJmax15_IS_hw%d_ms18_36_28.stream.bin'%(hw)
                        ARGS['3bme_type'] = "no2b"
                        ARGS['no2b_precision'] = "half"
                    else: print('Please check input of intes:', inte); break




               #     ARGS['LECs'] = 'EM2.0_2.5'
               #     ARGS['file2e1max'] = '16 file2e2max=32 file2lmax=16'
               #     ARGS['2bme'] = '/project/6006601/shared/me2j/TwBME-HO_NN-only_N3LO_EM500_srg2.0_hw%d_emax16_e2max32.me2j.gz'%(hw)
               #     ARGS['file3e1max'] = '16 file3e2max=32 file3e3max=24'
               #     ARGS['3bme'] = '/project/6006601/shared/me3j/NO2B_ThBME_EM2.0_2.5_3NFJmax15_IS_hw%d_ms16_32_24.stream.bin'%(hw)
               #     ARGS['3bme_type'] = "no2b"

                    #ARGS['LECs'] = 'EM1.8_2.0'
               #     ARGS['LECs'] = 'gst_EM1.8_2.0'
                    #ARGS['file2e1max'] = '16 file2e2max=32 file2lmax=16'
                    #ARGS['2bme'] = '/project/6006601/shared/me2j/TwBME-HO_NN-only_N3LO_EM500_srg1.8_hw%d_emax16_e2max32.me2j.gz'%(hw)
                    #ARGS['file3e1max'] = '16 file3e2max=32 file3e3max=24'
                    #ARGS['3bme'] = '/project/6006601/shared/me3j/NO2B_ThBME_EM1.8_2.0_3NFJmax15_IS_hw%d_ms16_32_24.stream.bin'%(hw)
                    #ARGS['3bme_type'] = "no2b"
                    #ARGS['file3e1max'] = '18 file3e2max=36 file3e3max=24'
                    #ARGS['3bme'] = '/project/6006601/shared/me3j/NO2B_ThBME_EM1.8_2.0_3NFJmax15_IS_hw%d_ms18_36_24.stream.bin'%(hw)
                    #ARGS['3bme_type'] = "no2b"
               ##     ARGS['file2e1max'] = '14 file2e2max=28 file2lmax=14'
               ##     ARGS['2bme'] = '/home/bhu/projects/def-holt/shared/exch/ME_share/vnn_hw%d.00_kvnn10_lambda1.80_mesh_kmax_7.0_100_pc_R15.00_N15.dat_to_me2j.gz'%(hw)
               ##     ARGS['3bme'] = '/home/holt/projects/def-holt/tmiyagi/MtxElmnt/3BME/NO2B_ThBME_ChEFT_N2LO_cD1.26cE-0.12_NonLocal4_IS_hw%d_ms18_36_22_Jmax15.stream.bin'%(hw)
               ##     ARGS['file3e1max'] = '18 file3e2max=36 file3e3max=22'
               ##     ARGS['3bme_type'] = "no2b"
               ##     ARGS['file3e1max'] = '14 file3e2max=28 file3e3max=16'
               ##     ARGS['3bme'] = '/home/bhu/projects/def-holt/shared/exch/ME_share/jsTNF_Nmax_16_J12max_8_hbarOmega_%d.00_Fit_cutoff_2.00_nexp_4_c1_1.00_c3_1.00_c4_1.00_cD_1.00_cE_1.00_2pi_0.00_2pi1pi_0.00_2picont_0.00_rings_0.00_J3max_9_new_E3_16_e_14_ant_EM1.8_2.0.h5_to_me3j.gz'%(hw)
               ##     ARGS['file3e1max'] = '14 file3e2max=28 file3e3max=18'
               ##     ARGS['3bme'] = '/global/scratch/jholt/ME_share/jsTNF_Nmax_18_J12max_8_hbarOmega_%d.00_Fit_cutoff_2.00_nexp_4_c1_1.00_c3_1.00_c4_1.00_cD_1.00_cE_1.00_2pi_0.00_2pi1pi_0.00_2picont_0.00_rings_0.00_J3max_9_new_E3_18_e_14_ant_EM1.8_2.0.h5_to_me3j.gz'%(hw)
                    #ARGS['file2e1max'] = '18 file2e2max=36 file2lmax=18'
                    #ARGS['2bme'] = '/project/6006601/shared/me2j/TwBME-HO_NN-only_N3LO_EM500_srg1.8_hw%d_emax18_e2max36.me2j.gz'%(hw)
                    #ARGS['file3e1max'] = '16 file3e2max=32 file3e3max=28'
                    #ARGS['3bme'] = '/project/6006601/shared/me3j/NO2B_half_ThBME_EM1.8_2.0_3NFJmax15_IS_hw%d_ms16_32_28.stream.bin'%(hw)
                    #ARGS['3bme_type'] = "no2b"
                    #ARGS['no2b_precision'] = "half"


                    #ARGS['LECs'] = 'N4LO_LNL2'
                    #ARGS['file2e1max'] = '16 file2e2max=32 file2lmax=16'
                    #ARGS['2bme'] = '/project/6006601/shared/me2j/TwBME-HO_NN-only_N4LO_EMN500_srg2.0_hw%d_emax16_e2max32.me2j.gz'%(hw)
                    #ARGS['file3e1max'] = '16 file3e2max=32 file3e3max=22'
                    #ARGS['3bme'] = '/project/6006601/shared/me3j/NO2B_ThBME_srg2.0_ramp46-9-44-15-42_N4LO_EMN500_3NFJmax15_c1_-0.73_c3_-3.38_c4_1.69_cD_-1.8_cE_-0.31_LNL2_650_500_IS_hw%dfrom30_ms16_32_22.stream.bin'%(hw)
                    #ARGS['3bme_type'] = "no2b"
               # Corrected N4LO LNL potential
               #     ARGS['LECs'] = 'N4LO_LNL2'
               #     ARGS['file2e1max'] = '14 file2e2max=28 file2lmax=14'
               #     ARGS['2bme'] = '/home/bhu/projects/def-holt/shared/exch/ME_share/TBMEA2n4lo500-srg2.0_14_28.%d_TUD.int.gz'%(hw)
               #     ARGS['file3e1max'] = '14 file3e2max=28 file3e3max=16'
               #     ARGS['3bme'] = '/home/bhu/projects/def-holt/shared/exch/ME_share/v3trans_J3T3.int_NNn4lo500_3NlnlcD-1.8cE-0.31_-1.8-srg2.0_220_161616.%d_from24_form.gz'%(hw)

                    #ARGS['LECs'] = 'N3LO_LNL2'
                    #ARGS['file2e1max'] = '16 file2e2max=32 file2lmax=16'
                    #ARGS['2bme'] = '/project/6006601/shared/me2j/TwBME-HO_NN-only_N3LO_EM500_srg2.0_hw%d_emax16_e2max32.me2j.gz'%(hw)
                    #ARGS['file3e1max'] = '18 file3e2max=36 file3e3max=24'
                    #ARGS['3bme'] = '/project/6006601/shared/me3j/NO2B_ThBME_srg2.0_ramp46_N3LO_EM500_JJmax13_c1_-0.81_c3_-3.2_c4_5.4_cD_0.7_cE_-0.06_LNL2_650_500_IS_hw%dfrom30_ms18_36_24.stream.bin'%(hw)
                    #ARGS['3bme_type'] = "no2b"



               #     ARGS['LECs'] = 'PWA'
               #     ARGS['file2e1max'] = '14 file2e2max=28 file2lmax=14'
               #     ARGS['file3e1max'] = '14 file3e2max=28 file3e3max=16'
               #     ARGS['2bme'] = '/global/scratch/exch/ME_share/vnn_hw%d.00_kvnn10_lambda2.00_mesh_kmax_7.0_100_pc_R15.00_N15.dat_to_me2j.gz'%(hw)
               #     ARGS['3bme'] = '/global/scratch/exch/ME_share/jsTNF_Nmax_16_J12max_8_hbarOmega_%d.00_Fit_cutoff_2.00_nexp_4_c1_1.00_c3_1.00_c4_1.00_cD_1.00_cE_1.00_2pi_0.00_2pi1pi_0.00_2picont_0.00_rings_0.00_J3max_9_new_E3_16_e_14_ant_PWA.h5_to_me3j.gz'%(hw)

                    #ARGS['LECs'] = 'N2LO_sat'
                    #ARGS['file2e1max'] = '16 file2e2max=32 file2lmax=16'
                    #ARGS['2bme'] = '/project/6006601/shared/me2j/TwBME-HO_NN-only_N2LO_sat_bare_hw%d_emax16_e2max32.me2j.gz'%(hw)
                    #ARGS['file3e1max'] = '16 file3e2max=32 file3e3max=24'
                    #ARGS['3bme'] = '/project/6006601/shared/me3j/NO2B_ThBME_N2LOsat_3NFJmax15_IS_hw%d_ms16_32_24.stream.bin'%(hw)
                    #ARGS['3bme_type'] = "no2b"
               ##     ARGS['file2e1max'] = '14 file2e2max=28 file2lmax=14'
               ##     ARGS['2bme'] = '/home/bhu/projects/def-holt/shared/exch/ME_share/TBMEA2n2losat_14_28.%d_TUD.int.gz'%(hw)
               ##     ARGS['file3e1max'] = '14 file3e2max=28 file3e3max=16'
               ##     ARGS['3bme'] = '/home/bhu/projects/def-holt/shared/exch/ME_share/v3trans_J3T3.int_NN3Nnnlosat_nu3_330_161615.%d_form.gz'%(hw)

                    #ARGS['LECs'] = 'DNNLOgo'
               #     ARGS['LECs'] = 'gst_DNNLOgo'
                    #ARGS['file2e1max'] = '18 file2e2max=36 file2lmax=18'
                    #ARGS['2bme'] = '/project/6006601/shared/me2j/TwBME-HO_NN-only_DNNLOgo_bare_hw%d_emax18_e2max36.me2j.gz'%(hw)
                    #ARGS['file3e1max'] = '16 file3e2max=32 file3e3max=24'
                    #ARGS['3bme'] = '/project/6006601/shared/me3j/NO2B_ThBME_DNNLOgo_3NFJmax15_IS_hw%d_ms16_32_24.stream.bin'%(hw)
                    #ARGS['3bme_type'] = "no2b"
               #     ARGS['file3e1max'] = '16 file3e2max=32 file3e3max=28'
               #     ARGS['3bme'] = '/project/6006601/shared/me3j/NO2B_half_ThBME_DNNLOgo_3NFJmax15_IS_hw%d_ms16_32_28.stream.bin'%(hw)
               #     ARGS['3bme_type'] = "no2b"
               #     ARGS['no2b_precision'] = "half"
               ##     ARGS['file3e1max'] = '18 file3e2max=36 file3e3max=22'
               ##     ARGS['3bme'] = '/project/6006601/tmiyagi/MtxElmnt/3BME/NO2B_ThBME_DNNLOgo_3NFJmax15_IS_hw%d_ms18_36_22.stream.bin'%(hw)
               ##     ARGS['file3e1max'] = '16 file3e2max=32 file3e3max=26'
               ##     ARGS['3bme'] = '/project/6006601/tmiyagi/MtxElmnt/NO2B_compact/NO2B_ThBME_DNNLOgo_3NFJmax15_IS_hw%d_ms16_32_26.stream.bin'%(hw)
               ##     ARGS['3bme_type'] = "no2b"
               ##     ARGS['file3e1max'] = '16 file3e2max=32 file3e3max=28'
               ##     ARGS['3bme'] = '/project/6006601/tmiyagi/MtxElmnt/NO2B_half/NO2B_ThBME_DNNLOgo_3NFJmax15_IS_hw%d_ms16_32_28.stream.bin'%(hw)
               ##     ARGS['3bme_type'] = "no2b"


                    #rho_r=''; rhox=0.0
                    #for irho in range(0,89):
#                    rho_r=''; rhox=4.4
#                    for irho in range(0,15):
#                        rhox = rhox + 0.1
                    #    rho_r += 'rhon_%2.1f,'%rhox
                        #rho_r += 'rhop_%2.1f,'%rhox
#                        rho_r += 'rhop_%2.1f,rhon_%2.1f,'%(rhox,rhox)
#                    ARGS['Operators'] = rho_r[:-1]
               #     ARGS['Operators'] = rho_r[:-1] + ',Rp2,Rn2'
                    ARGS['Operators'] = ''
                    #ARGS['Operators'] = 'ISM,ISQ'
                    #ARGS['Operators'] = 'Rp2,Rn2'
                    #ARGS['Operators'] = 'Rp2'
                    #ARGS['Operators'] = 'VCoul'
                    #ARGS['Operators'] = 'Rp2,Rn2,VCoul'
                    #ARGS['Operators'] = 'Rp2,M1,E2'
                    #ARGS['Operators'] = 'E2,Rp2,Rn2,M1'
                    #ARGS['Operators'] = 'E2,Rp2,Rn2'
                    #ARGS['Operators'] = 'M1,GamowTeller'
#                    ARGS['Operators'] = 'M1'
                    #ARGS['Operators'] = 'GamowTeller'
                    #ARGS['Operators'] = 'E2'
                    #ARGS['Operators'] = 'Rp2'
               #     ARGS['Operators'] = 'Rp2,IVD'
               #     ARGS['Operators'] = 'IVD,Rp2,Rn2'
               #     ARGS['Operators'] = 'IVD,Rp2,Rn2,Rm2'
               #     ARGS['Operators'] = 'M2'
               #     ARGS['Operators'] = 'GamowTeller'
               #     ARGS['Operators'] = 'Fermi'
               #     ARGS['Operators'] = 'Rp2,Rn2,M1,E2,GamowTeller,Fermi'
               #     ARGS['Operators'] = 'M1p,M1n,Sigma_p,Sigma_n'
               #     ARGS['Operators'] = 'Sigma_n'
               #     ARGS['Operators'] = 'rhop0.0,R2CM'
               #     ARGS['Operators'] = 'rhop_0.1'
               #     ARGS['input_op_fmt'] = 'navratil'
               #     ARGS['OperatorsFromFile'] = 'GTMECcD2^1_1_0_2^/project/6006601/shared/exch/GT_share/MEC2bind_NNn4lo500cDp45-srg2.0_N1max12_N12max24_hbo%d.dat.gz,'%(hw)
               #     ARGS['OperatorsFromFile'] += 'GTn32b2^1_1_0_2^/project/6006601/shared/exch/GT_share/GT2bind_NNn4lo500-srg2.0_N1max12_N12max24_hbo%d.dat.gz,'%(hw)

               # 1.8/2.0 EM
               #     ARGS['OperatorsFromFile'] = 'GT2b^1_1_0_2^/work/hda21/hda212/GT_share/GT_N1max12_N12max24_hbo12.dat.gz'
               #     ARGS['OperatorsFromFile'] = 'GTMEC^1_1_0_2^/work/hda21/hda212/GT_share/MEC_Park2003nl0_HebelerLamreg394_N1max12_N12max24_hbo16.dat.gz'

               # N2LO_sat
               #     ARGS['OperatorsFromFile'] = 'GTMECsat^1_1_0_2^/work/hda21/hda212/GT_share/MEC2b_Park2003nl0_N2LOsatcD-0.204_N1max12_N12max24_hbo16.dat.gz'

               # N3LO_LNL
               #     ARGS['OperatorsFromFile'] = 'GTMECcD^1_1_0_2^/work/hda21/hda212/GT_share/MEC2bind_Park2003nl0_n3lo500cD-0.175-srg2.0_N1max12_N12max24_hbo16.dat.gz'
               #     ARGS['OperatorsFromFile'] = 'GTn32b^1_1_0_2^/work/hda21/hda212/GT_share/GT2bind_NNn3lo500-srg2.0_N1max12_N12max24_hbo16.dat.gz'

               # N4LO_LNL hw=16
               #     ARGS['OperatorsFromFile'] = 'GTMECcD2^1_1_0_2^/global/scratch/exch/GT_share/MEC2bind_NNn4lo500cDp45-srg2.0_N1max12_N12max24_hbo16.dat.gz'
               #     ARGS['OperatorsFromFile'] = 'GTn32b2^1_1_0_2^/global/scratch/exch/GT_share/GT2bind_NNn4lo500-srg2.0_N1max12_N12max24_hbo16.dat.gz'

               # N4LO_LNL hw=14
               #     ARGS['OperatorsFromFile'] = 'GT2^1_1_0_2^/work/hda21/hda212/GT_share/GT2bind_NNn4lo500-srg2.0_N1max12_N12max24_hbo14.dat.gz'
               #     ARGS['OperatorsFromFile'] = 'GT2MEC^1_1_0_2^/work/hda21/hda212/GT_share/MEC2bind_NNn4lo500cDp45-srg2.0_N1max12_N12max24_hbo14.dat.gz'

               #     ARGS['core_generator'] = 'imaginary-time'
               #     ARGS['valence_generator'] = 'shell-model-imaginary-time'

                   ### Make an estimate of how much time to request. Only used for slurm at the moment.
                    time_request = '168:00:00'
                    if e<5: time_request = '24:10:00'
                    if e < 8 : time_request = '48:00:00'
                    elif e < 10 : time_request = '72:00:00'
                    elif e < 12 : time_request = '120:00:00'

                    #time_request = '2:59:59'
                    #time_request = '11:59:00'
                    time_request = '23:59:00'
                    #time_request = '47:59:00'
                    #time_request = '71:59:59'
                    #time_request = '168:00:00'

                    jobname  = '%s_%s_%s_%s_e%s_E%s_s%s_hw%s_A%s' %(ARGS['valence_space'], ARGS['LECs'],ARGS['method'],ARGS['reference'],ARGS['emax'],ARGS['e3max'],ARGS['smax'],ARGS['hw'],ARGS['A'])
                    #jobname  = '%s_%s_%s_%s_e%s_E%s_hw%s_A%s' %(ARGS['valence_space'], ARGS['LECs'],ARGS['method'],ARGS['reference'],ARGS['emax'],ARGS['e3max'],ARGS['hw'],ARGS['A'])
                    #jobname  = '%s_%s_%s_e%s_E%s_hw%s_A%s' %(ARGS['valence_space'], ARGS['LECs'],ARGS['reference'],ARGS['emax'],ARGS['e3max'],ARGS['hw'],ARGS['A'])
                    #jobname = "ref_{0}_basis_{1}_emax_{2}_hw_{3}".format(ARGS['reference'],ARGS['systemBasis'],emax,hw)
                    cmd = ' '.join([exe] + ['%s=%s'%(x,ARGS[x]) for x in ARGS])

               ### Some optional parameters that we probably want in the output name if we're using them
                    if 'lmax3' in ARGS:  jobname  += '_l%d'%(ARGS['lmax3'])
                    if 'eta_criterion' in ARGS: jobname += '_eta%s'%(ARGS['eta_criterion'])
                    if 'core_generator' in ARGS: jobname += '_' + ARGS['core_generator']
                    if 'BetaCM' in ARGS: jobname += '_BetaCM' + ARGS['BetaCM']
                    if 'denominator_delta' in ARGS: jobname += '_dE' + ARGS['denominator_delta']
                    if 'emax_imsrg' in ARGS: jobname += '_eimsrg' + ARGS['emax_imsrg']
                    if 'e2max_imsrg' in ARGS: jobname += '_e2imsrg' + ARGS['e2max_imsrg']
                    if 'basis' in ARGS: jobname += '_' + ARGS['basis']
                    if ARGS['goose_tank'] == 'true': jobname += '_gst'
                    if 'NAT_order' in ARGS: jobname += '_' + ARGS['NAT_order']
                    if 'occ_file' in ARGS: jobname += '_' + ARGS['occ_name']
                    if 'approx' in ARGS: jobname += '_' + ARGS['approx']
                    #ARGS['flowfile'] = 'output/BCH_' + jobname + '.dat'
                    #ARGS['intfile']  = 'output/' + jobname
                    ARGS['flowfile']  = '/home/bhu/scratch/BCH/BCH_' + jobname
                    #ARGS['intfile']  = '/home/bhu/scratch/output/' + jobname
                    #ARGS['intfile']  = '/home/bhu/scratch/output_Omega/' + jobname
                    ARGS['intfile']  = '/home/bhu/scratch/output_texas/' + jobname

                    #ARGS['path_omega'] = '/home/bhu/scratch/output_Omega/'
                    #ARGS['path_output'] = '/home/bhu/scratch/output_Omega/'
                    ARGS['path_output'] = '/home/bhu/scratch/output_texas/'
                    ARGS['jobname'] = jobname

                    jobnamep = jobname
                    #jobnamep = jobname + '_rpn'
                    logname = jobnamep + datetime.fromtimestamp(time()).strftime('_%y%m%d%H%M.log')

                    jobshow = f'imsrg3f2_e{e}_hw{hw}'

                    path_shared = '/home/bhu/scratch/output'
                    #path_shared = '/home/bhu/scratch/output_Omega'
                    #file_check = path_shared+'/'+jobname+'.sp'
                    file_check = path_shared+'/'+jobname+'.snt'
                    #file_check = path_shared+'/'+jobname+'Rn2.snt'
                    #file_check = path_shared+'/'+jobname+'_occ.dat'
                    if(os.path.exists(file_check)):
                        print('The file is exist:', file_check)
                        continue



                    cmd = '%s %s'%(exe,' '.join(['%s=%s'%(x,ARGS[x]) for x in ARGS]) )

                    if batch_mode==True:
                     sfile = open(jobnamep+'.batch','w')
               #      print ("Submitting to cluster: jobname=" + jobname+".batch")
               #   for c in cmd.split():
               #     print (c) #Verify the correct command is being executed
                     if BATCHSYS == 'PBS':
                      sfile.write(FILECONTENT%(jobname,environ['PWD'],NTHREADS,mail_address,logname,logname,NTHREADS,cmd))
                      sfile.close()
                      call(['qsub', jobname+'.batch'])
                     elif BATCHSYS == 'SLURM':
                      sfile.write(FILECONTENT%(NTHREADS,jobnamep,time_request,jobshow,mail_address,NTHREADS,NTHREADS,cmd))
               #      sfile.write(FILECONTENT.format(jobname,environ['PWD'],logname,NTHREADS,cmd))
                      sfile.close()
                      call(['sbatch', jobnamep+'.batch'])
                     remove(jobnamep+'.batch') # delete the file
                     sleep(0.1)
                    else:
                     call(cmd.split())  # Run in the terminal, rather than submitting






#      if path.isfile(jobname+'.batch'):
#     if BATCHSYS is 'PBS':
#      elif BATCHSYS is 'SLURM':

#   else:
#      print("Unable to locate .batch file!")
#else:
#   if BATCHSYS is 'PBS':
#      call(cmd.split())
#   elif BATCHSYS is 'SLURM':
#      call(['srun', jobname+'.batch'])

#     logname = jobname + datetime.fromtimestamp(time()).strftime('_%y%m%d%H%M.log')
#
#
#  ### Submit the job if we're running in batch mode, otherwise just run in the current shell
#     if batch_mode==True:
#       sfile = open(jobname+'.batch','w')
#       if BATCHSYS == 'PBS':
#         sfile.write(FILECONTENT%(jobname,environ['PWD'],NTHREADS,mail_address,logname,NTHREADS,cmd))
#         sfile.close()
#         call(['qsub', jobname+'.batch'])
#       elif BATCHSYS == 'SLURM':
#         sfile.write(FILECONTENT%(NTHREADS,jobname,time_request,mail_address,NTHREADS,NTHREADS,cmd))
#         sfile.close()
#         call(['sbatch', jobname+'.batch'])
#       remove(jobname+'.batch') # delete the file
#       sleep(0.1)
#     else:
#       call(cmd.split())  # Run in the terminal, rather than submitting

#     if batch_mode==True:
#       sfile = open(jobname,'w')
#       sfile.write(FILECONTENT%(NTHREADS,jobname,time_request,mail_address,NTHREADS,NTHREADS,cmd))
#       sfile.close()
#       call(['sbatch', jobname])
#       remove(jobname) # delete the file
#       sleep(0.1)
#     else:
#       call(cmd.split())  # Run in the terminal, rather than submitting


#     if batch_mode==True:
#       sfile = open(jobname,'w')
#       sfile.write(FILECONTENT%(jobname,environ['PWD'],NTHREADS,mail_address,logname,NTHREADS,cmd))
#       sfile.close()
#       call(['qsub', jobname+'.batch'])
#       remove(jobname) # delete the file
#       sleep(0.1)
#     else:
#       call(cmd.split())  # Run in the terminal, rather than submitting

  ### Submit the job if we're running in batch mode, otherwise just run in the current shell
#     if batch_mode==True:
#       sfile = open(jobname+'.batch','w')
#       if BATCHSYS == 'PBS':
#         sfile.write(FILECONTENT%(jobname,environ['PWD'],NTHREADS,mail_address,logname,NTHREADS,cmd))
#         sfile.close()
#         call(['qsub', jobname+'.batch'])
#       elif BATCHSYS == 'SLURM':
#         sfile.write(FILECONTENT%(NTHREADS,jobname,time_request,mail_address,NTHREADS,NTHREADS,cmd))
#         sfile.close()
#         call(['sbatch', jobname])
#       remove(jobname+'.batch') # delete the file
#       sleep(0.1)
#     else:
#       call(cmd.split())  # Run in the terminal, rather than submitting


#     ARGS['LECs'] = 'EM2.0_2.0'
#     ARGS['file2e1max'] = '14 file2e2max=28 file2lmax=14'
#     ARGS['file3e1max'] = '14 file3e2max=28 file3e3max=16'
#     ARGS['2bme'] = '/global/scratch/exch/ME_share/vnn_hw%d.00_kvnn10_lambda2.00_mesh_kmax_7.0_100_pc_R15.00_N15.dat_to_me2j.gz'%(hw)
#     ARGS['3bme'] = '/global/scratch/exch/ME_share/jsTNF_Nmax_16_J12max_8_hbarOmega_%d.00_Fit_cutoff_2.00_nexp_4_c1_1.00_c3_1.00_c4_1.00_cD_1.00_cE_1.00_2pi_0.00_2pi1pi_0.00_2picont_0.00_rings_0.00_J3max_9_new_E3_16_e_14_ant_EM2.0_2.0.h5_to_me3j.gz'%(hw)
#     ARGS['file3e1max'] = '14 file3e2max=28 file3e3max=18'
#     ARGS['3bme'] = '/work/hda21/hda215/ME_share/jsTNF_Nmax_18_J12max_8_hbarOmega_%d.00_Fit_cutoff_2.00_nexp_4_c1_1.00_c3_1.00_c4_1.00_cD_1.00_cE_1.00_2pi_0.00_2pi1pi_0.00_2picont_0.00_rings_0.00_J3max_9_new_E3_18_e_14_ant_EM2.0_2.0.h5_to_me3j.gz'%(hw)

#     ARGS['LECs'] = 'EM2.2_2.0'
#     ARGS['file2e1max'] = '14 file2e2max=28 file2lmax=14'
#     ARGS['file3e1max'] = '14 file3e2max=28 file3e3max=16'
#     ARGS['2bme'] = '/global/scratch/exch/ME_share/vnn_hw%d.00_kvnn10_lambda2.20_mesh_kmax_7.0_100_pc_R15.00_N15.dat_to_me2j.gz'%(hw)
#     ARGS['3bme'] = '/global/scratch/exch/ME_share/jsTNF_Nmax_16_J12max_8_hbarOmega_%d.00_Fit_cutoff_2.00_nexp_4_c1_1.00_c3_1.00_c4_1.00_cD_1.00_cE_1.00_2pi_0.00_2pi1pi_0.00_2picont_0.00_rings_0.00_J3max_9_new_E3_16_e_14_ant_EM2.2_2.0.h5_to_me3j.gz'%(hw)

#     ARGS['LECs'] = 'N3LO_LNL'
#     ARGS['file2e1max'] = '14 file2e2max=28 file2lmax=14'
#     ARGS['file3e1max'] = '14 file3e2max=28 file3e3max=16'
#     ARGS['2bme'] = '/work/hda21/hda212/ME_share/TBMEA2n3lo-srg2.0_14_28.%d_TUD.int.gz'%(hw)
#     ARGS['3bme'] = '/work/hda21/hda212/ME_share/v3trans_J3T3.int_3NFlocnonloc-srg2.0_from24_330_161615.%d_form.gz'%(hw)

#
# New Darmstadt potentials - Jan Hoppe
#     ARGS['LECs'] = 'N3LO_3N450'
#     ARGS['file2e1max'] = '14 file2e2max=28 file2lmax=14'
#     ARGS['file3e1max'] = '14 file3e2max=28 file3e3max=16'
#     ARGS['2bme'] = '/global/scratch/exch/ME_share/HO_VNN_N3LO_EM450new_lambda_1.80_Maverage_new_Vc_eMax14_hwHO020.me2j.gzTBMEA2n4lo500-srg2.0_14_28.%d_TUD.int.gz'%(hw)
#     ARGS['3bme'] = '/global/scratch/exch/ME_share/v3trans_J3T3.int_NNn4lo500_3NlnlcD-1.8cE-0.31_-1.8-srg2.0_220_161616.%d_from24_form.gz'%(hw)

#     ARGS['LECs'] = 'N2LO_opt'
#     ARGS['file2e1max'] = '14 file2e2max=28 file2lmax=14'
#     ARGS['file3e1max'] = '14 file3e2max=28 file3e3max=16'
#     ARGS['2bme'] = '/work/hda21/hda212/ME_share/TBMEA2n2loopt_14_28.%d_TUD.int.gz'%(hw)
#     ARGS['3bme'] = 'none'

#     ARGS['LECs'] = 'NN3N400'
#     ARGS['file2e1max'] = '14 file2e2max=28 file2lmax=14'
#     ARGS['file3e1max'] = '14 file3e2max=28 file3e3max=16'
#     ARGS['2bme'] = '/work/hda21/hda212/ME_share/TBMEA2n3lo-srg2.0_14_28.%d_TUD.int.gz'%(hw)
#     ARGS['3bme'] = '/work/hda21/hda212/ME_share/v3trans_J3T3.int_N3LO3NF400_-0.2-srg2.0_330_161615.%d_form.gz'%(hw)
#
#     ARGS['LECs'] = 'N3LO_3N450'
#     ARGS['file2e1max'] = '14 file2e2max=28 file2lmax=14'
#     ARGS['2bme'] = '/global/scratch/jholt/ME_share/3N_SRG/HO_VNN_N3LO_EM450new_lambda_1.80_Maverage_new_Vc_eMax14_hwHO020.me2j.gz'
#     ARGS['file3e1max'] = '14 file3e2max=28 file3e3max=14'
#     ARGS['3bme'] = '/global/scratch/jholt/ME_share/3N_SRG/jsTNF_Nmax_16_J12max_5_hbarOmega_20.00_N3LO_EM450new_lambda_1.80_c1_-1.20_c3_-4.43_c4_2.67_cD_5.00_cE_-0.64_2pi_1.00_2pi1pi_1.00_2picont_-0.01_rings_1.00_relCS_-4.60_relCT_-0.01_rel2pi_1.00_CSB_3_id_1_J3max_7_Kyle_new_E3_14_e_14_Hspo_t.h5_to_me3j.gz'
