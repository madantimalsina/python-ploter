import os,sys
import ROOT
import numpy as np
import pdb,glob
import matplotlib.pyplot as plt
#infile = ["/global/cfs/cdirs/lz/users/qxia/lzap_waveforms_mctruth.root"]
#infile = ["/global/cfs/cdirs/lz/users/qxia/AmLiWFFiles_DoGS2HighMin1.0_ms_mctruth.root"]
#infile = glob.glob("/global/cfs/cdirs/lz/data/MDC3/background/LZAP-5.0.1/MCTRUTH/20180602/lz_*_lzap_mctruth.root")
infile1 = glob.glob("/global/cfs/cdirs/lz/data/MDC3/calibration/LZAP-4.7.0/20180222/*.root")
infile2 = glob.glob("/global/cfs/cdirs/lz/data/MDC3/calibration/LZAP-4.7.0/20180223/*.root")
infile3 = glob.glob("/global/cfs/cdirs/lz/data/MDC3/calibration/LZAP-4.7.0/20180224/*.root")
#infile = ["/global/cfs/cdirs/lz/data/MDC3/background/LZAP-5.0.1/MCTRUTH/20180602/lz_20180602033_lzap_mctruth.root","/global/cfs/cdirs/lz/data/MDC3/background/LZAP-5.0.1/MCTRUTH/20180602/lz_20180602230_lzap_mctruth.root","/global/cfs/cdirs/lz/data/MDC3/background/LZAP-5.0.1/MCTRUTH/20180602/lz_20180602122_lzap_mctruth.root"]
#infile =["/global/cfs/cdirs/lz/data/MDC3/background/LZAP-5.0.1/MCTRUTH/20180602/lz_20180602002_lzap_mctruth.root","/global/cfs/cdirs/lz/data/MDC3/background/LZAP-5.0.1/MCTRUTH/20180602/lz_20180602025_lzap_mctruth.root"]
#infile =["/global/cfs/cdirs/lz/users/qxia/alphaNWF_ss_mctruth.root","/global/cfs/cdirs/lz/users/qxia/alphaNWF_ms_mctruth.root"]
#infile =["/global/cfs/cdirs/lz/users/qxia/PTFEalphaN_ss_mctruth.root"]
#infile =["/global/cfs/cdirs/lz/users/qxia/USFWF_ss_mctruth.root","/global/cfs/cdirs/lz/users/qxia/USFWF_odtag_ms.root"]
infile = set(infile1+infile2+infile3)
tMC = ROOT.TChain("Events")
for f in infile:
        tMC.Add(f)
print ("total number of events:",tMC.GetEntries())
n = tMC.Draw("pulsesTPC.nPulses","pulsesTPC.nPulses>0","goff")
print ("total number of events in tpc:",n)
