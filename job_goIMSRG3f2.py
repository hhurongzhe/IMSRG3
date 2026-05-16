import os, sys
from os import path, environ, mkdir, remove
from subprocess import call, PIPE
from sys import argv
from time import time, sleep
from datetime import datetime

path_pre = sys.path[0]
print("current path: " + path_pre)

### Check to see what type of batch submission system we're dealing with
BATCHSYS = "NONE"
if call("type " + "qsub", shell=True, stdout=PIPE, stderr=PIPE) == 0:
    BATCHSYS = "PBS"
elif call("type " + "srun", shell=True, stdout=PIPE, stderr=PIPE) == 0:
    BATCHSYS = "SLURM"


NTHREADS = 32
# exe = '%s/bin/imsrg++'%(environ['HOME'])
exe = path_pre + "/ReadIMSRG3f2.py"

### Flag to swith between submitting to the scheduler or running in the current shell
# batch_mode=False
batch_mode = True
if "terminal" in argv[1:]:
    batch_mode = False

mail_address = "baishanhu4phys@gmail.com"

### This comes in handy if you want to loop over Z
ELEM = [
    "n",
    "H",
    "He",
    "Li",
    "Be",
    "B",
    "C",
    "N",
    "O",
    "F",
    "Ne",
    "Na",
    "Mg",
    "Al",
    "Si",
    "P",
    "S",
    "Cl",
    "Ar",
    "K",
    "Ca",
    "Sc",
    "Ti",
    "V",
    "Cr",
    "Mn",
    "Fe",
    "Co",
    "Ni",
    "Cu",
    "Zn",
    "Ga",
    "Ge",
    "As",
    "Se",
    "Br",
    "Kr",
    "Rb",
    "Sr",
    "Y",
    "Zr",
    "Nb",
    "Mo",
    "Tc",
    "Ru",
    "Rh",
    "Pd",
    "Ag",
    "Cd",
    "In",
    "Sn",
    "Sb",
    "Te",
    "I",
    "Xe",
    "Cs",
    "Ba",
    "La",
    "Ce",
    "Pr",
    "Nd",
    "Pm",
    "Sm",
    "Eu",
    "Gd",
    "Tb",
    "Dy",
    "Ho",
    "Er",
    "Tm",
    "Yb",
    "Lu",
    "Hf",
    "Ta",
    "W",
    "Re",
    "Os",
    "Ir",
    "Pt",
    "Au",
    "Hg",
    "Tl",
    "Pb",
]

### ARGS is a (string => string) dictionary of input variables that are passed to the main program
ARGS = {}

ARGS["smax"] = "500"
ARGS["omega_norm_max"] = "0.25"
# ARGS['ode_tolerance'] = '1e-5'
# ARGS['scratch'] = 'temp'

# ARGS['method'] = 'MP3'
ARGS["method"] = "magnus"
# ARGS['method'] = 'NSmagnus'
# ARGS['method'] = 'brueckner'
# ARGS['method'] = 'flow'
# ARGS['method'] = 'HF'

ARGS["approx"] = "imsrg3f2"

# ARGS['write_omega'] = 'true'


if BATCHSYS == "SLURM":
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
if not path.exists("imsrg_log"):
    mkdir("imsrg_log")

ARGS["nucleon_mass_correction"] = "true"

# ARGS['goose_tank'] = 'true'

As = [4, 16, 22, 24, 36, 40, 48, 52, 54, 56, 68, 78, 90, 100, 114, 120, 132, 208]
Zs = [2, 8, 8, 8, 20, 20, 20, 20, 20, 28, 28, 28, 40, 50, 50, 50, 50, 82]
As = [4]
Zs = [2]


intes = ["EM1.8_2.0"]


## Loop over multiple jobs to submit
# for A in range(68,69):
# for A in [48]:
# Z=28
for i in range(0, len(As)):
    Z = Zs[i]
    A = As[i]
    for reference in ["%s%d" % (ELEM[Z], A)]:
        ARGS["reference"] = reference
        ARGS["e3max"] = "28"
        for inte in intes:
            if inte == "N3LO_EM500_LNL":
                ARGS["e3max"] = "22"
            # for e in [6,8,10,12,14]:
            for e in [12]:
                for hw in [12, 16]:
                    # for hw in [8,10,12]:
                    ARGS["A"] = "%d" % A
                    ARGS["Z"] = "%d" % Z
                    ARGS["hw"] = "%d" % hw
                    ARGS["emax"] = "%d" % e

                    ARGS["valence_file_format"] = "tokyo"

                    # ARGS['denominator_delta_orbit'] = 'all'
                    # ARGS['denominator_delta'] = '10'
                    ARGS["BetaCM"] = "4"

                    # ARGS['occ_file'] = 'occ_file_In107.dat'
                    # ARGS['occ_file'] = './occ_file/occ_file_%s_1.dat'%(reference)
                    # ARGS['occ_file'] = './occ_file/occ_file_%s_P1N1.dat'%(reference)
                    # ARGS['occ_name'] = 'OccP1N1'
                    # ARGS['freeze_occupations'] = 'true'

                    # ARGS['basis'] = 'NAT'
                    # ARGS['use_NAT_occupations'] = 'true'
                    # ARGS['basis'] = 'oscillator'
                    # ARGS['hwBetaCM'] = '12'
                    # ARGS['goose_tank']='true'
                    ARGS["goose_tank"] = "false"
                    # ARGS['eta_criterion'] = '1e-5'

                    ARGS["valence_space"] = reference

                    ARGS["fmt2"] = "me2j"
                    ARGS["no2b_precision"] = "single"

                    if inte == "PWA2.0_2.0":
                        ARGS["LECs"] = "PWA2.0_2.0"
                        ARGS["file2e1max"] = "16 file2e2max=32 file2lmax=16"
                        ARGS["2bme"] = "/project/6006601/shared/me2j/TwBME-HO_NN-only_N3LO_EM500_srg2.0_hw%d_emax16_e2max32.me2j.gz" % (hw)
                        ARGS["file3e1max"] = "16 file3e2max=32 file3e3max=24"
                        ARGS["3bme"] = "/project/6006601/shared/me3j/NO2B_ThBME_PWA2.0_2.0_3NFJmax15_IS_hw%d_ms16_32_24.stream.bin" % (hw)
                        ARGS["3bme_type"] = "no2b"
                    elif inte == "EM2.2_2.0":
                        ARGS["LECs"] = "EM2.2_2.0"
                        ARGS["file2e1max"] = "16 file2e2max=32 file2lmax=16"
                        ARGS["2bme"] = "/project/6006601/shared/me2j/TwBME-HO_NN-only_N3LO_EM500_srg2.2_hw%d_emax16_e2max32.me2j.gz" % (hw)
                        ARGS["file3e1max"] = "16 file3e2max=32 file3e3max=24"
                        ARGS["3bme"] = "/project/6006601/shared/me3j/NO2B_ThBME_EM2.2_2.0_3NFJmax15_IS_hw%d_ms16_32_24.stream.bin" % (hw)
                        ARGS["3bme_type"] = "no2b"
                    elif inte == "EM2.0_2.0":
                        ARGS["LECs"] = "EM2.0_2.0"
                        ARGS["file2e1max"] = "16 file2e2max=32 file2lmax=16"
                        ARGS["2bme"] = "/project/6006601/shared/me2j/TwBME-HO_NN-only_N3LO_EM500_srg2.0_hw%d_emax16_e2max32.me2j.gz" % (hw)
                        ARGS["file3e1max"] = "16 file3e2max=32 file3e3max=24"
                        ARGS["3bme"] = "/project/6006601/shared/me3j/NO2B_ThBME_EM2.0_2.0_3NFJmax15_IS_hw%d_ms16_32_24.stream.bin" % (hw)
                        ARGS["3bme_type"] = "no2b"
                    elif inte == "EM1.8_2.0":
                        ARGS["LECs"] = "EM1.8_2.0"
                        ARGS["file2e1max"] = "18 file2e2max=36 file2lmax=18"
                        ARGS["2bme"] = "/home/bhu/projects/rrg-holt/tmiyagi/run_vhamil/TwBME-HO_NN-only_N3LO_EM500_srg1.8_hw%d_emax18_e2max36.me2j.gz" % (hw)
                        ARGS["file3e1max"] = "18 file3e2max=36 file3e3max=28"
                        ARGS["3bme"] = "/home/bhu/projects/rrg-holt/tmiyagi/run_vhamil/NO2B_half_ThBME_EM1.8_2.0_3NFJmax15_IS_hw%d_ms18_36_28.stream.bin" % (hw)
                        ARGS["3bme_type"] = "no2b"
                        ARGS["no2b_precision"] = "half"
                    elif inte == "N2LO_sat":
                        ARGS["LECs"] = "N2LO_sat"
                        ARGS["file2e1max"] = "16 file2e2max=32 file2lmax=16"
                        ARGS["2bme"] = "/project/6006601/shared/me2j/TwBME-HO_NN-only_N2LO_sat_bare_hw%d_emax16_e2max32.me2j.gz" % (hw)
                        ARGS["file3e1max"] = "16 file3e2max=32 file3e3max=24"
                        ARGS["3bme"] = "/project/6006601/shared/me3j/NO2B_ThBME_N2LOsat_3NFJmax15_IS_hw%d_ms16_32_24.stream.bin" % (hw)
                        # ARGS['file3e1max'] = '18 file3e2max=36 file3e3max=24'
                        # ARGS['3bme'] = '/project/6006601/shared/me3j/NO2B_ThBME_N2LOsat_3NFJmax15_IS_hw%d_ms18_36_24.stream.bin'%(hw)
                        ARGS["3bme_type"] = "no2b"
                    elif inte == "DNNLOgo" or inte == "N2LOgo":
                        ARGS["LECs"] = inte
                        ARGS["file2e1max"] = "18 file2e2max=36 file2lmax=18"
                        ARGS["2bme"] = "/project/6006601/shared/me2j/TwBME-HO_NN-only_DNNLOgo_bare_hw%d_emax18_e2max36.me2j.gz" % (hw)
                        ARGS["file3e1max"] = "16 file3e2max=32 file3e3max=24"
                        ARGS["3bme"] = "/project/6006601/shared/me3j/NO2B_ThBME_DNNLOgo_3NFJmax15_IS_hw%d_ms16_32_24.stream.bin" % (hw)
                        ARGS["3bme_type"] = "no2b"
                    elif inte == "DNNLOgo450":
                        ARGS["LECs"] = "DNNLOgo450"
                        ARGS["file2e1max"] = "16 file2e2max=32 file2lmax=16"
                        ARGS["2bme"] = "/project/6006601/shared/me2j/TwBME-HO_NN-only_DN2LOGO450_bare_hw%d_emax16_e2max32.me2j.gz" % (hw)
                        ARGS["file3e1max"] = "16 file3e2max=32 file3e3max=26"
                        ARGS["3bme"] = "/project/6006601/shared/me3j/NO2B_ThBME_DN2LOGO450_3NFJmax15_IS_hw%d_ms16_32_26.stream.bin" % (hw)
                        ARGS["3bme_type"] = "no2b"
                    elif inte == "DNLOgo450":
                        ARGS["LECs"] = "DNLOgo450"
                        ARGS["file2e1max"] = "16 file2e2max=32 file2lmax=16"
                        ARGS["2bme"] = "/project/6006601/shared/me2j/TwBME-HO_NN-only_DNLOGO450_bare_hw%d_emax16_e2max32.me2j.gz" % (hw)
                        ARGS["file3e1max"] = "16 file3e2max=32 file3e3max=26"
                        ARGS["3bme"] = "/project/6006601/shared/me3j/NO2B_ThBME_DNLOGO450_3NFJmax15_IS_hw%d_ms16_32_26.stream.bin" % (hw)
                        ARGS["3bme_type"] = "no2b"
                    elif inte == "N3LO_LNL2":
                        ARGS["LECs"] = "N3LO_LNL2"
                        ARGS["file2e1max"] = "16 file2e2max=32 file2lmax=16"
                        ARGS["2bme"] = "/project/6006601/shared/me2j/TwBME-HO_NN-only_N3LO_EM500_srg2.0_hw%d_emax16_e2max32.me2j.gz" % (hw)
                        ARGS["file3e1max"] = "18 file3e2max=36 file3e3max=24"
                        ARGS["3bme"] = "/project/6006601/shared/me3j/NO2B_ThBME_srg2.0_ramp46_N3LO_EM500_JJmax13_c1_-0.81_c3_-3.2_c4_5.4_cD_0.7_cE_-0.06_LNL2_650_500_IS_hw%dfrom30_ms18_36_24.stream.bin" % (hw)
                        ARGS["3bme_type"] = "no2b"
                    elif inte == "N3LO_EM500_LNL":
                        ARGS["LECs"] = "N3LO_EM500_LNL"
                        ARGS["file2e1max"] = "16 file2e2max=32 file2lmax=16"
                        ARGS["2bme"] = "/project/6006601/shared/me2j/TwBME-HO_NN-only_N3LO_EM500_srg2.0_hw%d_emax16_e2max32.me2j.gz" % (hw)
                        # ARGS['file3e1max'] = '18 file3e2max=36 file3e3max=24'
                        # ARGS['3bme'] = '/project/6006601/shared/me3j/NO2B_ThBME_srg2.0_ramp46_N3LO_EM500_JJmax13_c1_-0.81_c3_-3.2_c4_5.4_cD_0.7_cE_-0.06_LNL2_650_500_IS_hw%dfrom30_ms18_36_24.stream.bin'%(hw)
                        ARGS["file3e1max"] = "16 file3e2max=32 file3e3max=22"
                        ARGS["3bme"] = "/project/6006601/shared/me3j/NO2B_ThBME_srg2.0_ramp46-9-44-15-42_N3LO_EM500_3NFJmax15_c1_-0.81_c3_-3.2_c4_5.4_cD_0.7_cE_-0.06_LNL2_650_500_IS_hw%dfrom30_ms16_32_22.stream.bin" % (hw)
                        ARGS["3bme_type"] = "no2b"
                    elif inte == "Texas":
                        ARGS["LECs"] = "Texas"
                        ARGS["fmt2"] = "oakridge_bin"
                        ARGS["file2e1max"] = "14 file2e2max=28 file2lmax=14"
                        ARGS["2bme"] = "/home/bhu/scratch/me2j/sp_energy_N14_hw%d.dat,/home/bhu/scratch/me2j/vn3lo394_ini2160_544p_n4_N14_hw%d.dat" % (hw, hw)
                        ARGS["file3e1max"] = "18 file3e2max=36 file3e3max=28"
                        ARGS["3bme"] = "/project/rrg-holt/shared/me_texas/NO2B_half_ThBME_Texas_3NFJmax15_IS_hw%d_ms18_36_28.stream.bin" % (hw)
                        ARGS["3bme_type"] = "no2b"
                        ARGS["no2b_precision"] = "half"
                    else:
                        print("Please check input of intes:", inte)
                        break

                    # rho_r=''; rhox=0.0
                    # for irho in range(0,89):
                    #                    rho_r=''; rhox=4.4
                    #                    for irho in range(0,15):
                    #                        rhox = rhox + 0.1
                    #    rho_r += 'rhon_%2.1f,'%rhox
                    # rho_r += 'rhop_%2.1f,'%rhox
                    #                        rho_r += 'rhop_%2.1f,rhon_%2.1f,'%(rhox,rhox)
                    #                    ARGS['Operators'] = rho_r[:-1]
                    #     ARGS['Operators'] = rho_r[:-1] + ',Rp2,Rn2'
                    ARGS["Operators"] = ""
                    # ARGS['Operators'] = 'ISM,ISQ'
                    # ARGS['Operators'] = 'Rp2,Rn2'
                    # ARGS['Operators'] = 'Rp2'
                    # ARGS['Operators'] = 'VCoul'
                    # ARGS['Operators'] = 'Rp2,Rn2,VCoul'
                    # ARGS['Operators'] = 'Rp2,M1,E2'
                    # ARGS['Operators'] = 'E2,Rp2,Rn2,M1'
                    # ARGS['Operators'] = 'E2,Rp2,Rn2'
                    # ARGS['Operators'] = 'M1,GamowTeller'
                    #                    ARGS['Operators'] = 'M1'
                    # ARGS['Operators'] = 'GamowTeller'
                    # ARGS['Operators'] = 'E2'
                    # ARGS['Operators'] = 'Rp2'
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

                    #     ARGS['core_generator'] = 'imaginary-time'
                    #     ARGS['valence_generator'] = 'shell-model-imaginary-time'

                    ### Make an estimate of how much time to request. Only used for slurm at the moment.
                    time_request = "168:00:00"
                    if e < 5:
                        time_request = "24:10:00"
                    if e < 8:
                        time_request = "48:00:00"
                    elif e < 10:
                        time_request = "72:00:00"
                    elif e < 12:
                        time_request = "120:00:00"

                    # time_request = '2:59:59'
                    # time_request = '11:59:00'
                    time_request = "23:59:00"
                    # time_request = '47:59:00'
                    # time_request = '71:59:59'
                    # time_request = '168:00:00'

                    jobname = "%s_%s_%s_%s_e%s_E%s_s%s_hw%s_A%s" % (ARGS["valence_space"], ARGS["LECs"], ARGS["method"], ARGS["reference"], ARGS["emax"], ARGS["e3max"], ARGS["smax"], ARGS["hw"], ARGS["A"])
                    # jobname  = '%s_%s_%s_%s_e%s_E%s_hw%s_A%s' %(ARGS['valence_space'], ARGS['LECs'],ARGS['method'],ARGS['reference'],ARGS['emax'],ARGS['e3max'],ARGS['hw'],ARGS['A'])
                    # jobname  = '%s_%s_%s_e%s_E%s_hw%s_A%s' %(ARGS['valence_space'], ARGS['LECs'],ARGS['reference'],ARGS['emax'],ARGS['e3max'],ARGS['hw'],ARGS['A'])
                    # jobname = "ref_{0}_basis_{1}_emax_{2}_hw_{3}".format(ARGS['reference'],ARGS['systemBasis'],emax,hw)
                    cmd = " ".join([exe] + ["%s=%s" % (x, ARGS[x]) for x in ARGS])

                    ### Some optional parameters that we probably want in the output name if we're using them
                    if "lmax3" in ARGS:
                        jobname += "_l%d" % (ARGS["lmax3"])
                    if "eta_criterion" in ARGS:
                        jobname += "_eta%s" % (ARGS["eta_criterion"])
                    if "core_generator" in ARGS:
                        jobname += "_" + ARGS["core_generator"]
                    if "BetaCM" in ARGS:
                        jobname += "_BetaCM" + ARGS["BetaCM"]
                    if "denominator_delta" in ARGS:
                        jobname += "_dE" + ARGS["denominator_delta"]
                    if "emax_imsrg" in ARGS:
                        jobname += "_eimsrg" + ARGS["emax_imsrg"]
                    if "e2max_imsrg" in ARGS:
                        jobname += "_e2imsrg" + ARGS["e2max_imsrg"]
                    if "basis" in ARGS:
                        jobname += "_" + ARGS["basis"]
                    if ARGS["goose_tank"] == "true":
                        jobname += "_gst"
                    if "NAT_order" in ARGS:
                        jobname += "_" + ARGS["NAT_order"]
                    if "occ_file" in ARGS:
                        jobname += "_" + ARGS["occ_name"]
                    if "approx" in ARGS:
                        jobname += "_" + ARGS["approx"]
                    # ARGS['flowfile'] = 'output/BCH_' + jobname + '.dat'
                    # ARGS['intfile']  = 'output/' + jobname
                    ARGS["flowfile"] = "/home/bhu/scratch/BCH/BCH_" + jobname
                    # ARGS['intfile']  = '/home/bhu/scratch/output/' + jobname
                    # ARGS['intfile']  = '/home/bhu/scratch/output_Omega/' + jobname
                    ARGS["intfile"] = "/home/bhu/scratch/output_texas/" + jobname

                    # ARGS['path_omega'] = '/home/bhu/scratch/output_Omega/'
                    # ARGS['path_output'] = '/home/bhu/scratch/output_Omega/'
                    ARGS["path_output"] = "/home/bhu/scratch/output_texas/"
                    ARGS["jobname"] = jobname

                    jobnamep = jobname
                    # jobnamep = jobname + '_rpn'
                    logname = jobnamep + datetime.fromtimestamp(time()).strftime("_%y%m%d%H%M.log")

                    jobshow = f"imsrg3f2_e{e}_hw{hw}"

                    path_shared = "/home/bhu/scratch/output"
                    # path_shared = '/home/bhu/scratch/output_Omega'
                    # file_check = path_shared+'/'+jobname+'.sp'
                    file_check = path_shared + "/" + jobname + ".snt"
                    # file_check = path_shared+'/'+jobname+'Rn2.snt'
                    # file_check = path_shared+'/'+jobname+'_occ.dat'
                    if os.path.exists(file_check):
                        print("The file is exist:", file_check)
                        continue

                    cmd = "%s %s" % (exe, " ".join(["%s=%s" % (x, ARGS[x]) for x in ARGS]))

                    if batch_mode == True:
                        sfile = open(jobnamep + ".batch", "w")
                        #      print ("Submitting to cluster: jobname=" + jobname+".batch")
                        #   for c in cmd.split():
                        #     print (c) #Verify the correct command is being executed
                        if BATCHSYS == "PBS":
                            sfile.write(FILECONTENT % (jobname, environ["PWD"], NTHREADS, mail_address, logname, logname, NTHREADS, cmd))
                            sfile.close()
                            call(["qsub", jobname + ".batch"])
                        elif BATCHSYS == "SLURM":
                            sfile.write(FILECONTENT % (NTHREADS, jobnamep, time_request, jobshow, mail_address, NTHREADS, NTHREADS, cmd))
                            #      sfile.write(FILECONTENT.format(jobname,environ['PWD'],logname,NTHREADS,cmd))
                            sfile.close()
                            call(["sbatch", jobnamep + ".batch"])
                        remove(jobnamep + ".batch")  # delete the file
                        sleep(0.1)
                    else:
                        call(cmd.split())  # Run in the terminal, rather than submitting
