import sys, os

sys.path.append("/Users/mac/Desktop/IMSRG3/build/")
# import numpy as np
import math
from pyIMSRG import *


def find(sub_str, list_str):
    return any(sub_str in item for item in list_str)


def main_job(args_v):

    emax = 0
    e2max = 0
    e3max = 0
    emax_imsrg = -1
    e2max_imsrg = -1
    e3max_imsrg = 0
    brueckner_restart = False
    inputtbme = "none"
    input3bme = "none"
    input3bme_type = "full"
    no2b_precision = "single"
    fmt2 = "me2j"
    fmt3 = "me3j"
    hw_trap = -1
    lmax = 99999
    lmax3 = -1
    freeze_occupations = False
    discard_no2b_from_3n = False
    method = "magnus"
    smax = 500
    omega_norm_max = 1
    basis = "HF"
    BetaCM = 0
    hwBetaCM = -1
    custom_valence_space = ""
    input_op_fmt = ""
    opsfromfile = ""
    smax_core = 50
    smax_valence = 500
    core_generator = "atan"
    valence_generator = "shell-model-atan"
    # approx = 'imsrg2'
    approx = "imsrg3f2"
    # approx = 'imsrg3n7'
    ops = ""
    opsfromfile = ""

    print("\n---------------")
    print("######  imsrg++ build version: ", BuildVersion)
    print("main_job of ReadIMSRG3f2.py:", args_v)
    for args in args_v:
        arr = args.split("=")
        key = arr[0].strip()
        value = arr[1].strip()
        print(key, "=>", value)

        if key == "2bme":
            inputtbme = value
        if key == "3bme":
            input3bme = value
        if key == "3bme_type":
            input3bme_type = value
        if key == "no2b_precision":
            no2b_precision = value
        if key == "reference":
            reference = value
        if key == "valence_space":
            name_vs = value
        if key == "custom_valence_space":
            custom_valence_space = value
        if key == "basis":
            basis = value
        if key == "method":
            method = value
        if key == "flowfile":
            flowfile = value
        if key == "intfile":
            intfile = value
        if key == "core_generator":
            core_generator = value
        if key == "valence_generator":
            valence_generator = value
        if key == "fmt2":
            fmt2 = value
        if key == "fmt3":
            fmt3 = value
        if key == "input_op_fmt":
            input_op_fmt = value
        if key == "denominator_delta_orbit":
            denominator_delta_orbit = value
        if key == "LECs":
            LECs = value
        if key == "scratch":
            scratch = value
        if key == "valence_file_format":
            valence_file_format = value
        if key == "occ_file":
            occ_file = value
        if key == "physical_system":
            physical_system = value
        if key == "denominator_partitioning":
            denominator_partitioning = value
        if key == "NAT_order":
            NAT_order = value

        if key == "use_brueckner_bch":
            use_brueckner_bch = value == "true"
        if key == "nucleon_mass_correction":
            nucleon_mass_correction = value == "true"
        if key == "relativistic_correction":
            relativistic_correction = value == "true"
        if key == "IMSRG3":
            IMSRG3 = value == "true"
        if key == "imsrg3_n7":
            imsrg3_n7 = value == "true"
        if key == "imsrg3_mp4":
            imsrg3_mp4 = value == "true"
        if key == "imsrg3_at_end":
            imsrg3_at_end = value == "true"
        if key == "imsrg3_no_qqq":
            imsrg3_no_qqq = value == "true"
        if key == "write_omega":
            write_omega = value == "true"
        if key == "freeze_occupations":
            freeze_occupations = value == "true"
        if key == "discard_no2b_from_3n":
            discard_no2b_from_3n = value == "true"
        if key == "hunter_gatherer":
            hunter_gatherer = value == "true"
        if key == "goose_tank":
            goose_tank = value == "true"
        if key == "discard_residual_input3N":
            discard_residual_input3N = value == "true"
        if key == "use_NAT_occupations":
            use_NAT_occupations = value == "true"
        if key == "order_NAT_by_energy":
            order_NAT_by_energy = value == "true"
        if key == "store_3bme_pn":
            store_3bme_pn = value == "true"
        if key == "only_2b_eta":
            only_2b_eta = value == "true"
        if key == "only_2b_omega":
            only_2b_omega = value == "true"
        if key == "perturbative_triples":
            perturbative_triples = value == "true"
        if key == "write_HO_ops":
            write_HO_ops = value == "true"
        if key == "write_HF_ops":
            write_HF_ops = value == "true"

        if key == "emax":
            emax = int(value)
        if key == "lmax":
            lmax = int(value)
        if key == "e3max":
            e3max = int(value)
        if key == "lmax3":
            lmax3 = int(value)
        if key == "A":
            targetMass = int(value)
        if key == "nsteps":
            nsteps = int(value)
        if key == "file2e1max":
            file2e1max = int(value)
        if key == "file2e2max":
            file2e2max = int(value)
        if key == "file2lmax":
            file2lmax = int(value)
        if key == "file3e1max":
            file3e1max = int(value)
        if key == "file3e2max":
            file3e2max = int(value)
        if key == "file3e3max":
            file3e3max = int(value)
        if key == "atomicZ":
            atomicZ = int(value)
        if key == "emax_unocc":
            emax_unocc = int(value)
        if key == "emax_imsrg":
            emax_imsrg = int(value)
        if key == "e2max_imsrg":
            e2max_imsrg = int(value)
        if key == "e3max_imsrg":
            e3max_imsrg = int(value)
        if key == "emax_3body_imsrg":
            emax_3body_imsrg = int(value)

        if key == "hw":
            hw = float(value)
        if key == "smax":
            smax = int(value)
        if key == "ode_tolerance":
            ode_tolerance = float(value)
        if key == "dsmax":
            dsmax = float(value)
        if key == "ds_0":
            ds_0 = float(value)
        if key == "domega":
            domega = float(value)
        if key == "omega_norm_max":
            omega_norm_max = float(value)
        if key == "denominator_delta":
            denominator_delta = float(value)
        if key == "BetaCM":
            BetaCM = float(value)
        if key == "hwBetaCM":
            hwBetaCM = float(value)
        if key == "eta_criterion":
            eta_criterion = float(value)
        if key == "hw_trap":
            hw_trap = float(value)
        if key == "dE3max":
            dE3max = float(value)
        if key == "OccNat3Cut":
            OccNat3Cut = float(value)
        if key == "threebody_threshold":
            threebody_threshold = float(value)

        if key == "Z":
            Z = int(value)
        if key == "e2max":
            e2max = int(value)
        if key == "jobname":
            jobname = value
        if key == "path_omega":
            path_omega = value
        if key == "path_output":
            path_output = value

        if key == "smax_core":
            smax_core = int(value)
        if key == "smax_valence":
            smax_valence = int(value)
        if key == "approx":
            approx = value

        if key == "Operators":
            ops = value.split(",")
        if key == "OperatorsFromFile":
            opsfromfile = value.split(",")

    if emax_imsrg == -1 or e2max_imsrg == -1:
        emax_imsrg = emax
        e2max_imsrg = emax * 2
        e3max_imsrg = e3max

    print("\n---------------")
    if find("jobname", args_v):
        print("Working with:", jobname)
    if ops != "":
        print("Working for Operator:", ops)
    if opsfromfile != "":
        print("Working for Operator from file::", opsfromfile)

    rw = ReadWrite()
    # if( find('LECs',args_v) ):
    #    rw.SetLECs_preset(LECs)
    if "scratch" in args_v:
        rw.SetScratchDir(scratch)
    if find("fmt3", args_v):
        rw.Set3NFormat(fmt3)

    valence_space = name_vs
    if custom_valence_space != "":
        valence_space = custom_valence_space

    ms = ModelSpace(emax, reference, valence_space)

    if find("e3max", args_v):
        ms.SetE3max(e3max)
    ms.SetLmax(lmax)
    if find("dE3max", args_v):
        ms.SetdE3max(dE3max)
    if find("OccNat3Cut", args_v):
        ms.SetOccNat3Cut(OccNat3Cut)
    if find("emax_unocc", args_v):
        ms.SetEmaxUnocc(emax_unocc)
    if find("occ_file", args_v):
        ms.Init_occ_from_file(emax, valence_space, occ_file)

    ms.SetHbarOmega(hw)
    if find("A", args_v):
        A = targetMass
        ms.SetTargetMass(targetMass)
    if find("lmax3", args_v):
        ms.SetLmax3(lmax3)

    if find("emax_imsrg", args_v):
        ms_imsrg = ModelSpace(emax_imsrg, reference, valence_space)
        ms_imsrg.SetTargetMass(targetMass)
        ms_imsrg.SetHbarOmega(hw)
        ms_imsrg.SetE3max(e3max_imsrg)
        if find("e2max_imsrg", args_v):
            ms_imsrg.SetE2max(e2max_imsrg)
        if find("occ_file", args_v):
            ms_imsrg.Init_occ_from_file(emax_imsrg, valence_space, occ_file)

        ms2 = ModelSpace(emax_imsrg, reference, valence_space)
        ms2.SetTargetMass(targetMass)
        ms2.SetHbarOmega(hw)
        ms2.SetE3max(e3max_imsrg)
        if find("e2max_imsrg", args_v):
            ms2.SetE2max(e2max_imsrg)
        if find("occ_file", args_v):
            ms2.Init_occ_from_file(emax_imsrg, valence_space, occ_file)
        ms2.SetReference(ms2.core)

    print("\nGetAref(), GetZref():", ms.GetAref(), ms.GetZref())

    # if(os.path.exists(occ_nat_file)):
    #     fin = open(occ_nat_file,'r')
    #     for line in fin:
    #         arr = line.split()
    #         iorb = ms.GetOrbitIndex(int(arr[0]),int(arr[1]),int(arr[2]),int(arr[3]))
    #         ms.SetOccNAT( int(arr[0]),int(arr[1]),int(arr[2]),int(arr[3]),float(arr[4]) )
    #         ms_imsrg.SetOccNAT( int(arr[0]),int(arr[1]),int(arr[2]),int(arr[3]),float(arr[4]) )
    #         ms2.SetOccNAT( int(arr[0]),int(arr[1]),int(arr[2]),int(arr[3]),float(arr[4]) )
    #         # print('Read occ_nat:', arr)
    #         # print('orbit:', iorb, ' => occ:', ms.GetOrbit(iorb).occ, 'occ_nat', ms.GetOrbit(iorb).occ_nat )

    rank_j, parity, rank_Tz, particle_rank = 0, 0, 0, 2
    if input3bme != "none":
        particle_rank = 3

    Hbare = Operator(ms, rank_j, parity, rank_Tz, particle_rank)
    Hbare.SetHermitian()

    print("Reading interactions...")
    if inputtbme != "none":
        if fmt2 == "me2j":
            rw.ReadBareTBME_Darmstadt(inputtbme, Hbare, file2e1max, file2e2max, file2lmax)
        elif fmt2 == "navratil" or fmt2 == "Navratil":
            rw.ReadBareTBME_Navratil(inputtbme, Hbare)
        elif fmt2 == "oslo":
            rw.ReadTBME_Oslo(inputtbme, Hbare)
        elif find("oakridge", [fmt2]):
            f1b, f2b = inputtbme.split(",")
            if find("bin", [fmt2]):
                rw.ReadTBME_OakRidge(f1b, f2b, Hbare, "binary")
            else:
                rw.ReadTBME_OakRidge(f1b, f2b, Hbare, "ascii")
        elif fmt2 == "takayuki":
            rw.ReadTwoBody_Takayuki(inputtbme, Hbare)
        elif fmt2 == "nushellx":
            rw.ReadNuShellX_int(Hbare, inputtbme)
        elif fmt2 == "schematic":
            print("using schematic potential")
            if LECs == "Minnesota":
                Hbare += OperatorFromString(ms, "VMinnesota")
        print("done reading 2N")

    if input3bme != "none":
        if input3bme_type == "full":
            rw.Read_Darmstadt_3body(input3bme, Hbare, file3e1max, file3e2max, file3e3max)
        elif input3bme_type == "no2b":
            Hbare.ThreeBody.SetMode("no2b")
            if no2b_precision == "half":
                Hbare.ThreeBody.SetMode("no2bhalf")
            Hbare.ThreeBody.ReadFile([input3bme], [file3e1max, file3e2max, file3e3max, file3e1max])
            # rw.File3N = input3bme
        elif input3bme_type == "mono":
            Hbare.ThreeBody.SetMode("mono")
            Hbare.ThreeBody.ReadFile([input3bme], [file3e1max, file3e2max, file3e3max, file3e1max])
            # rw.File3N = input3bme
        print("done reading 3N")

    if find("store_3bme_pn", args_v) and store_3bme_pn:
        Hbare.ThreeBody.TransformToPN()

    if fmt2 != "nushellx" and hw_trap < 0:
        Hbare += OperatorFromString(ms, "Trel")
        # if(Hbare.OneBody.has_nan()):
        #    print('Looks like the Trel op is hosed from the get go. Dying...')
        #    exit()

    if find("nucleon_mass_correction", args_v) and nucleon_mass_correction:
        Hbare += OperatorFromString(ms, "TrelMassCorrection")

    if find("relativistic_correction", args_v) and relativistic_correction:
        print("Warning: The elativistic_correction is not implemented now ...")
        exit()

    if find("BetaCM", args_v) and abs(BetaCM) > 1e-6:
        if hwBetaCM < 0:
            hwBetaCM = ms.GetHbarOmega()
        hcm_opname = "HCM_%s" % (str(hwBetaCM))
        Hbare += BetaCM * OperatorFromString(ms, hcm_opname)

    print("Creating HF")
    hf = HartreeFock(Hbare)
    if not freeze_occupations:
        hf.UnFreezeOccupations()
    if discard_no2b_from_3n:
        hf.DiscardNO2Bfrom3N()
    print("Solving")

    hf.Solve()
    hf.PrintSPEandWF()

    ### Do normal ordering with respect to the HF basis
    particle_rank = 2
    if approx == "imsrg3n7":
        particle_rank = 3
    HNO = hf.GetNormalOrderedH(particle_rank)
    if particle_rank == 3:
        HNO.ThreeBody.SetMode("pn")

    HNO -= BetaCM * 1.5 * hwBetaCM
    print("Hbare 0b = ", HNO.ZeroBody)

    ### Create an instance of the IMSRGSolver class, used for solving the IMSRG flow equations
    imsrgsolver = IMSRGSolver(HNO)
    imsrgsolver.SetMethod(method)  # Solve using the Magnus formulation. Could also be 'flow_RK4'
    if find("denominator_partitioning", args_v):
        imsrgsolver.SetDenominatorPartitioning(denominator_partitioning)
    if find("eta_criterion", args_v):
        imsrgsolver.SetEtaCriterion(eta_criterion)
    # imsrgsolver.max_omega_written = 500
    if find("smax", args_v):
        imsrgsolver.SetSmax(smax)
    if find("flowfile", args_v):
        imsrgsolver.SetFlowFile(flowfile)
    if find("ds_0", args_v):
        imsrgsolver.SetDs(ds_0)
    if find("dsmax", args_v):
        imsrgsolver.SetDsmax(dsmax)
    if find("denominator_delta", args_v):
        imsrgsolver.SetDenominatorDelta(denominator_delta)
    if find("domega", args_v):
        imsrgsolver.SetdOmega(domega)
    if find("omega_norm_max", args_v):
        imsrgsolver.SetOmegaNormMax(omega_norm_max)
    if find("ode_tolerance", args_v):
        imsrgsolver.SetODETolerance(ode_tolerance)
    if find("denominator_delta_orbit", args_v):
        imsrgsolver.SetDenominatorDeltaOrbit(denominator_delta_orbit)

    if approx == "imsrg3n7":
        SetUseIMSRG3(True)
        SetUseIMSRG3N7(True)

    if approx == "imsrg3f2":
        # We only include the factorized commutators with 1b intermediates
        # during the flow, because they are cheper and the 2b intermediates
        # have a much less significant influence on Hod, so they can safely
        # be added in at the end of the flow.
        # We also use the Hunter-Gatherer mode, which works best if we
        # take OmegaNormMax to be smaller than 1
        imsrgsolver.SetHunterGatherer(True)
        imsrgsolver.SetOmegaNormMax(0.1)
        BCH.SetUseFactorizedCorrection(True)
        Commutator.FactorizedDoubleCommutator.SetUse_1b_Intermediates(True)
        Commutator.FactorizedDoubleCommutator.SetUse_2b_Intermediates(False)

    imsrgsolver.SetGenerator(core_generator)
    imsrgsolver.SetSmax(smax_core)

    ### Do the first stage of integration to decouple the core
    imsrgsolver.Solve()

    ### Now set the generator for the second stage to decouple the valence space
    if valence_space == reference:
        Hs = imsrgsolver.GetH_s()
        triples = 0
        if approx == "imsrg3f2":
            Commutator.FactorizedDoubleCommutator.SetUse_1b_Intermediates(True)
            Commutator.FactorizedDoubleCommutator.SetUse_2b_Intermediates(True)
            Hs = imsrgsolver.Transform(HNO)
            triples = imsrgsolver.CalculatePerturbativeTriples()
        Eimsrg = Hs.ZeroBody
        print("IMSRG Energy = {:.6f}  +  {:.6f}  = {:.6f}".format(Eimsrg, triples, Eimsrg + triples))

        rw.WriteTokyoFull(imsrgsolver.GetH_s(), intfile + ".snt")

    else:

        imsrgsolver.SetGenerator(valence_generator)
        imsrgsolver.SetSmax(smax_valence)
        imsrgsolver.Solve()

        ### Hs is the IMSRG-evolved Hamiltonian
        Hs = imsrgsolver.GetH_s()

        ### Turn on correction with 2b intermediates, and re-evaluate UHU+
        if approx == "imsrg3f2":
            Commutator.FactorizedDoubleCommutator.SetUse_1b_Intermediates(True)
            Commutator.FactorizedDoubleCommutator.SetUse_2b_Intermediates(True)
            Hs = imsrgsolver.Transform(HNO)

        triples = imsrgsolver.CalculatePerturbativeTriples()
        print("Adding triples correction  = {:.6f}".format(triples), flush=True)
        Hs.ZeroBody += triples

        ### Shell model codes assume the interaction is normal ordered with respect to the core
        ### and typically we choose a reference different from the core, so we need to re-normal-order
        ### with respect to the core
        if Hs.GetParticleRank() > 2:
            Hs.ThreeBody.Erase()
        Hs = Hs.UndoNormalOrdering()

        Hs = Hs.DoNormalOrderingCore()

        ### Write out the effective valence space interaction
        rw.WriteTokyo(Hs, intfile + ".snt", "")

    if opsfromfile != "":
        opall = ops + opsfromfile
    else:
        opall = ops
    opall = [element for element in opall if element != ""]

    print(opall)

    for op_temp in opall:

        name_op = op_temp.strip()

        if op_temp in ops:
            OpHO = OperatorFromString(ms, name_op)
        elif op_temp in opsfromfile:
            opff = op_temp.split("^")
            opname = opff[0]
            qnumbers = opff[1]
            f2name = opff[2]
            name_op = opname
            if len(opff) > 3:
                f3name = opff[3]
            q_temp = qnumbers.split("_")
            op_j = int(q_temp[0])
            op_t = int(q_temp[1])
            op_p = int(q_temp[2])
            op_r = int(q_temp[3])
            OpHO = Operator(ms, op_j, op_t, op_p, op_r)

            if op_r > 2:
                OpHO.ThreeBody.Allocate()
            if input_op_fmt == "navratil":
                rw.Read2bCurrent_Navratil(f2name, OpHO)
            elif input_op_fmt == "miyagi":
                if f2name != "":
                    optmp = Operator(ms, op_j, op_t, op_p, op_r)
                    optmp = rw.ReadOperator2b_Miyagi(f2name, ms)
                    OpHO.TwoBody = optmp.TwoBody
                if op_r > 2 and f3name != "":
                    rw.Read_Darmstadt_3body(f3name, OpHO, f3e1, f3e2, f3e3)

        else:
            print("The op_temp is wrong!")

        Op = hf.TransformToHFBasis(OpHO)  ### OpHO is some operator in the HO basis defined earlier
        Op = Op.DoNormalOrdering()

        print("\n   HF: " + name_op + " zero body = ", Op.ZeroBody, "\n")

        if find("emax_imsrg", args_v):
            print("Truncating modelspace for IMSRG calculation: emax, e2max, e3max =>", emax_imsrg, e2max_imsrg, e3max_imsrg)
            Op = Op.Truncate(ms_imsrg)

        if find("path_omega", args_v):
            n_omega = 0
            while True:
                name_omega = path_omega + jobname + "_Omega_%d" % (n_omega)
                if os.path.exists(name_omega):
                    print("Transforming using", jobname + "_Omega_%d" % (n_omega))
                    Omega = Operator(ms_imsrg, 0, 0, 0, 2)
                    Omega.SetAntiHermitian()
                    Omega.ReadBinary(name_omega)  ### Here Omega_x is the file name of the operator that was written to disk
                    Op = Commutator.BCH_Transform(Op, Omega)
                    print("norm of omega =", Omega.Norm())
                    print(" op zero body = ", Op.ZeroBody)
                    n_omega = n_omega + 1
                else:
                    print("File ", name_omega, " does not exist!")
                    break
        else:
            Op = imsrgsolver.Transform(Op)

        if reference != valence_space:
            print("UndoNormalOrdering")
            Op = Op.UndoNormalOrdering()
            # Op.SetModelSpace(ms2)
            # print('doNormalOrdering')
            # Op = Op.DoNormalOrdering()
            print("doNormalOrdering")
            Op = Op.DoNormalOrderingCore()

        print("\n   IMSRG: " + name_op + " zero body = ", Op.ZeroBody)

        if reference == valence_space:
            if name_op == "Rp2":
                print("\n IMSRG point proton radius = ", math.sqrt(Op.ZeroBody))
                print(" IMSRG charge radius = ", math.sqrt(Op.ZeroBody + PROTON_RCH2 + NEUTRON_RCH2 * (A - Z) / Z + DARWIN_FOLDY))
            if (Op.GetJRank() > 0) or (Op.GetTRank() > 0) or (name_op == "ISM") or (name_op == "IVM"):
                print("\nWriting operator to", path_output + jobname + "_" + name_op + ".op")
                rw.WriteOperatorHuman(Op, path_output + jobname + "_" + name_op + ".op")
        else:
            print("\nWriting operator to", path_output + jobname + "_" + name_op + ".snt")
            if ((Op.GetJRank() + Op.GetTRank() + Op.GetParity()) < 1) and (Op.GetNumberLegs() % 2 == 0):
                rw.WriteTokyo(Op, path_output + jobname + "_" + name_op + ".snt", "op")
            else:
                rw.WriteTensorTokyo(path_output + jobname + "_" + name_op + "_2b.snt", Op)

    ### Finally, print out profiling information so we know why this took so dang long to run...
    prof = IMSRGProfiler()
    prof.PrintAll()


if __name__ == "__main__":
    main_job(sys.argv[1:])
