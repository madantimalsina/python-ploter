import os,sys
import ROOT
import numpy as np
import pdb,glob
import matplotlib.pyplot as plt
#infile = ["/global/cfs/cdirs/lz/users/qxia/lzap_waveforms_mctruth.root"]
#infile = ["/global/cfs/cdirs/lz/users/qxia/AmLiWFFiles_DoGS2HighMin1.0_ms_mctruth.root"]
#infile = glob.glob("/global/cfs/cdirs/lz/data/MDC3/background/LZAP-5.0.1/MCTRUTH/20180602/lz_*_lzap_mctruth.root")
infile1 = glob.glob("/global/cfs/cdirs/lz/data/MDC3/calibration/LZAP-4.7.0/MCTRUTH/20180222/*.root")
infile2 = glob.glob("/global/cfs/cdirs/lz/data/MDC3/calibration/LZAP-4.7.0/MCTRUTH/20180223/*.root")
infile3 = glob.glob("/global/cfs/cdirs/lz/data/MDC3/calibration/LZAP-4.7.0/MCTRUTH/20180224/*.root")
#infile = ["/global/cfs/cdirs/lz/data/MDC3/background/LZAP-5.0.1/MCTRUTH/20180602/lz_20180602033_lzap_mctruth.root","/global/cfs/cdirs/lz/data/MDC3/background/LZAP-5.0.1/MCTRUTH/20180602/lz_20180602230_lzap_mctruth.root","/global/cfs/cdirs/lz/data/MDC3/background/LZAP-5.0.1/MCTRUTH/20180602/lz_20180602122_lzap_mctruth.root"]
#infile =["/global/cfs/cdirs/lz/data/MDC3/background/LZAP-5.0.1/MCTRUTH/20180602/lz_20180602002_lzap_mctruth.root","/global/cfs/cdirs/lz/data/MDC3/background/LZAP-5.0.1/MCTRUTH/20180602/lz_20180602025_lzap_mctruth.root"]
#infile =["/global/cfs/cdirs/lz/users/qxia/alphaNWF_ss_mctruth.root","/global/cfs/cdirs/lz/users/qxia/alphaNWF_ms_mctruth.root"]
#infile =["/global/cfs/cdirs/lz/users/qxia/PTFEalphaN_ss_mctruth.root"]
#infile =["/global/cfs/cdirs/lz/users/qxia/USFWF_ss_mctruth.root","/global/cfs/cdirs/lz/users/qxia/USFWF_odtag_ms.root"]
infile = set(infile1+infile2+infile3)
#msfdfile = open("/global/homes/q/qxia/ALPACA/msfd_AmLi.txt")
#fdfile = open("/global/homes/q/qxia/ALPACA/ssfd_PTFEalphaN.txt")
#IDlist = []
#for line in fdfile.readlines():
 #       IDlist.append(int(line.split()[5]))
#print (IDlist)
#IDlist = [1981029,1981029,3312757]
#IDlist = [754561,1256636,559150]#[774402,3048030,1047737,1183048]
tMC = ROOT.TChain("RQMCTruth")
for f in infile:
        print (type(f))
        tMC.Add(f)
print ("total number of events:",tMC.GetEntries())
#tMC = infile.Get('RQMCTruth')
n = tMC.Draw("mcTruthEvent.eventID","","goff")
eventID = np.copy(np.frombuffer(tMC.GetV1(), count=n)) 
#print ("total number of events",n)
NRID = []
for i in range(n):
    if int(eventID[i]) in IDlist:
#    if int(eventID[i])==72567:
            tMC.GetEntry(i)
            particles = np.copy(getattr(tMC,"mcTruthVertices.particleName"))
            print (getattr(tMC,"mcTruthEvent.parentParticle"))
            n = tMC.Draw("mcTruthEvent.parentEnergy_keV","mcTruthEvent.eventID==%d"%eventID[i],"goff")
            parentE = np.copy(np.frombuffer(tMC.GetV1(),count=n))
#            particles = np.copy(getattr(tMC,"mcTruthEvent.parentParticle"))
            #if "proton" in particles: #or "neutron" in particles or any("Xe" in s for s in particles):
            NRID.append(str(int(eventID[i])))
            print(eventID[i],particles)
            print ("parentEnergy_keV:",parentE[0])
#for evt in eventID:
'''for evt in IDlist:
#for evt in [1570756,1981029,3312757]:
    cut = "mcTruthVertices.energyDep_keV>0.001&&mcTruthEvent.eventID==%d"%(evt)
    cut += "&&(mcTruthVertices.positionX_mm*mcTruthVertices.positionX_mm+mcTruthVertices.positionY_mm*mcTruthVertices.positionY_mm)<473344"#&& mcTruthVertices.positionZ_mm>20.&&mcTruthVertices.positionZ_mm<1326."
#    cut += "&&(mcTruthVertices.positionX_mm*mcTruthVertices.positionX_mm+mcTruthVertices.positionY_mm*mcTruthVertices.positionY_mm)<730*730 && mcTruthVertices.positionZ_mm>20.&&mcTruthVertices.positionZ_mm<1326."
   # cut += "&&(mcTruthVertices.positionX_mm*mcTruthVertices.positionX_mm+mcTruthVertices.positionY_mm*mcTruthVertices.positionY_mm)<360000 && mcTruthVertices.positionZ_mm>20.&&mcTruthVertices.positionZ_mm<1326."
    n = tMC.Draw("mcTruthVertices.positionX_mm:mcTruthVertices.positionY_mm:mcTruthVertices.positionZ_mm:mcTruthVertices.energyDep_keV",cut,"goff")
    mc_x = np.copy(np.frombuffer(tMC.GetV1(), count=n))
    mc_y = np.copy(np.frombuffer(tMC.GetV2(), count=n))
    mc_z = np.copy(np.frombuffer(tMC.GetV3(), count=n))
    mc_energy = np.copy(np.frombuffer(tMC.GetV4(), count=n))
    print (mc_x)
    print (mc_y)
    print (mc_z)
    print (mc_energy)
    plt.ion()
    cir1=plt.Circle((0,0), radius=1460/2.,color="b",fill=False,label="TPC R=730mm")
    cir2=plt.Circle((0,0), radius=688,color="r",fill=False,label="FV R=688mm")
    cir3=plt.Circle((0,0), radius=1460/2.+80,color="orange",fill=False,label="skin R=810mm")
    plt.plot(mc_x,mc_y,'o',markersize=1)
    plt.xlim(-1300,1300)
    plt.ylim(-1300,1300)
    plt.title("EventID %d"%evt)
    ax=plt.gca()
    ax.add_patch(cir1)
    ax.add_patch(cir2)
    ax.add_patch(cir3)
    plt.legend()
    plt.show()
    raw_input()
    plt.close()
    multiplicity = "ss"
    if n<1:
 #       print "EventID",int(evt),"No vertices in the FV"
        continue
    for i in range(n):
        for j in range(i+1,n):
            dis2 = (mc_x[i]-mc_x[j])**2+(mc_y[i]-mc_y[j])**2+(mc_z[i]-mc_z[j])**2
            if dis2 > 4**2:
                multiplicity = "ms"
#    print "EventID",int(evt),"Number of vertices",n,"Likely multiplicity",multiplicity'''

