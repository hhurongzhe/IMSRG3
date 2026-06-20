import sys
from subprocess import call, PIPE, Popen, STDOUT
from time import sleep

# fmt: off
ELEM = ['n','H','He','Li','Be','B','C','N','O','F','Ne','Na','Mg','Al','Si','P','S','Cl','Ar','K','Ca','Sc','Ti','V','Cr','Mn','Fe','Co',  'Ni','Cu','Zn','Ga','Ge','As','Se','Br','Kr','Rb','Sr','Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','In',  'Sn','Sb','Te','I','Xe','Cs','Ba','La','Ce','Pr','Nd','Pm','Sm','Eu','Gd','Tb','Dy','Ho','Er','Tm','Yb','Lu','Hf','Ta','W','Re','Os','Ir','Pt','Au','Hg','Tl','Pb']
# fmt: on

path_pre = sys.path[0]
print("current path: " + path_pre)
exe = sys.executable + " " + path_pre + "/pyIMSRG3f2.py"


ARGS = {}
ARGS["smax"] = "500"
ARGS["omega_norm_max"] = "0.25"
# ARGS['ode_tolerance'] = '1e-5'
ARGS["scratch"] = "temp"
ARGS["method"] = "magnus"
# ARGS['method'] = 'HF'
ARGS["nucleon_mass_correction"] = "true"
# ARGS["goose_tank"] = "true"


ARGS["approx"] = "imsrg2"
# ARGS["approx"] = "imsrg3f2"

intes = ["N2LO_opt"]

# A_list = [4, 16, 22, 24, 36, 40, 48, 52, 54, 56, 68, 78, 90, 100, 114, 120, 132, 208]
# Z_list = [2, 8, 8, 8, 20, 20, 20, 20, 20, 28, 28, 28, 40, 50, 50, 50, 50, 82]
A_list = [4]
Z_list = [2]

hw_list = [20]
emax_list = [6]
e3max_list = [18]


NTHREADS = 64
slurm_mode = False
# slurm_mode = True

FILECONTENT = """#!/bin/bash
##SBATCH --account=hrz
#SBATCH --partition=c128m512
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=%d
#SBATCH --output=result/%s.txt
#SBATCH --job-name=imsrg
cd $SLURM_SUBMIT_DIR
echo NTHREADS = %d
export OMP_NUM_THREADS=%d
time srun %s
"""

## Loop over multiple jobs to submit
for i in range(0, len(A_list)):
    Z = Z_list[i]
    A = A_list[i]
    for reference in ["%s%d" % (ELEM[Z], A)]:
        ARGS["reference"] = reference
        for inte in intes:
            for e in emax_list:
                for e3 in e3max_list:
                    for hw in hw_list:
                        ARGS["A"] = "%d" % A
                        ARGS["Z"] = "%d" % Z
                        ARGS["hw"] = "%d" % hw
                        ARGS["emax"] = "%d" % e
                        ARGS["e3max"] = "%d" % e3
                        ARGS["valence_file_format"] = "tokyo"

                        # ARGS['denominator_delta_orbit'] = 'all'
                        # ARGS['denominator_delta'] = '10'
                        # ARGS["BetaCM"] = "0"
                        # ARGS['occ_file'] = 'occ_file_In107.dat'
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
                        if inte == "N2LO_opt":
                            ARGS["file2e1max"] = "6 file2e2max=12 file2lmax=6"
                            ARGS["2bme"] = "/Users/mac/Desktop/2BME/TwBME_N2LO_opt_bare_hw20_emax6_e2max12.me2j.gz"
                            ARGS["3bme"] = "none"
                        elif inte == "EM1.8_2.0":
                            ARGS["file2e1max"] = "18 file2e2max=36 file2lmax=18"
                            ARGS["2bme"] = "/home/bhu/projects/rrg-holt/tmiyagi/run_vhamil/TwBME-HO_NN-only_N3LO_EM500_srg1.8_hw16_emax18_e2max36.me2j.gz"
                            ARGS["file3e1max"] = "18 file3e2max=36 file3e3max=28"
                            ARGS["3bme"] = "/home/bhu/projects/rrg-holt/tmiyagi/run_vhamil/NO2B_half_ThBME_EM1.8_2.0_3NFJmax15_IS_hw16_ms18_36_28.stream.bin"
                            ARGS["3bme_type"] = "no2b"
                        else:
                            print("Please check input of intes:", inte)
                            break

                        ARGS["Operators"] = "Rp2,Rn2,Rm2"
                        # ARGS['Operators'] = 'Rp2,Rn2,Rm2,M1,E2,GamowTeller,Fermi'

                        # ARGS['core_generator'] = 'imaginary-time'
                        # ARGS['valence_generator'] = 'shell-model-imaginary-time'

                        jobname = f"{ARGS['reference']}_{ARGS['approx']}_{inte}_hw{ARGS['hw']}_emax{ARGS['emax']}"
                        if ARGS["3bme"] != "none":
                            jobname += f"_e3max{ARGS['e3max']}"
                        cmd = " ".join([exe] + ["%s=%s" % (x, ARGS[x]) for x in ARGS])

                        ### Some optional parameters that we probably want in the output name if we're using them
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
                        ARGS["flowfile"] = "output/BCH_" + jobname + ".dat"
                        ARGS["intfile"] = "output/" + jobname
                        ARGS["path_output"] = "output/"
                        ARGS["jobname"] = jobname
                        cmd = "%s %s" % (exe, " ".join(["%s=%s" % (x, ARGS[x]) for x in ARGS]))

                        if slurm_mode == True:
                            sfile = open("script/" + jobname + ".sh", "w")
                            slurm_cmd = " \\\n    ".join(cmd.split())
                            sfile.write(FILECONTENT % (NTHREADS, jobname, NTHREADS, NTHREADS, slurm_cmd))
                            sfile.close()
                            call(["sbatch", "script/" + jobname + ".sh"])
                            sleep(0.5)
                        else:
                            call(["mkdir", "-p", "result"])
                            logfile = "result/" + jobname + ".txt"
                            with open(logfile, "w") as fout:
                                proc = Popen(cmd.split(), stdout=PIPE, stderr=STDOUT, text=True, bufsize=1)
                                for line in proc.stdout:
                                    print(line, end="")
                                    fout.write(line)
                                proc.wait()
