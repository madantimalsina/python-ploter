import os,sys
import ROOT
import numpy as np
import matplotlib.pyplot as plt
#infile = ROOT.TFile("/global/cfs/cdirs/lz/users/qxia/lzap_waveforms_mctruth.root") #AmLi
infile = ROOT.TFile("/global/cfs/cdirs/lz/users/qxia/XeNR10keVWFFiles_DoGS2HighMin1.0_mctruth.root")
tMC = infile.Get('RQMCTruth')
n = tMC.Draw("mcTruthEvent.eventID","","goff")
eventID = np.copy(np.frombuffer(tMC.GetV1(), count=n)) 
print "total number of events",n
for evt in eventID:
#for evt in [1665026,698016,1077696,1823633,173991]:#problematic events
#for evt in [698016,173991]:#problematic events
#for evt in [1181389,443965,203047,1465517]:#good events
#for evt in [380652,161833,944617]:
#for evt in [72,88,90]:
#for evt in range(100):
    cut = "mcTruthVertices.energyDep_keV>0.001&&mcTruthEvent.eventID==%d"%(evt)
    cutfv = cut+"&&(mcTruthVertices.positionX_mm*mcTruthVertices.positionX_mm+mcTruthVertices.positionY_mm*mcTruthVertices.positionY_mm)<473344&& mcTruthVertices.positionZ_mm>20.&&mcTruthVertices.positionZ_mm<1326."
    cutskin = cut+"&&(mcTruthVertices.positionX_mm*mcTruthVertices.positionX_mm+mcTruthVertices.positionY_mm*mcTruthVertices.positionY_mm)>730*730&&(mcTruthVertices.positionX_mm*mcTruthVertices.positionX_mm+mcTruthVertices.positionY_mm*mcTruthVertices.positionY_mm)<810*810&&mcTruthVertices.positionZ_mm>20.&&mcTruthVertices.positionZ_mm<1326."
    cut += "&&(mcTruthVertices.positionX_mm*mcTruthVertices.positionX_mm+mcTruthVertices.positionY_mm*mcTruthVertices.positionY_mm)<5329000&& mcTruthVertices.positionZ_mm>20.&&mcTruthVertices.positionZ_mm<1326."
    n = tMC.Draw("mcTruthVertices.positionX_mm:mcTruthVertices.positionY_mm:mcTruthVertices.positionZ_mm:mcTruthVertices.time_ns",cutfv,"goff")
    mc_x = np.copy(np.frombuffer(tMC.GetV1(), count=n))
    mc_y = np.copy(np.frombuffer(tMC.GetV2(), count=n))
    mc_z = np.copy(np.frombuffer(tMC.GetV3(), count=n))
    mc_t = np.copy(np.frombuffer(tMC.GetV4(), count=n))
    n2 = tMC.Draw("mcTruthVertices.positionX_mm:mcTruthVertices.positionY_mm:mcTruthVertices.positionZ_mm:mcTruthVertices.energyDep_keV",cutfv,"goff")
    mc_energy = np.copy(np.frombuffer(tMC.GetV4(), count=n2))
    n3 = tMC.Draw("mcTruthVertices.positionX_mm:mcTruthVertices.positionY_mm:mcTruthVertices.positionZ_mm:mcTruthVertices.energyDep_keV",cutskin,"goff")
    mc_energy_skin = np.copy(np.frombuffer(tMC.GetV4(), count=n3))
    print "FV energy",mc_energy
    print "skin energy",mc_energy_skin
    print "X:",mc_x
    print "Y:",mc_y
    print "Z:",mc_z
    print "energy:",mc_energy
    print "time",mc_t
    multiplicity = "ss"
    if n<1:
        print "EventID",int(evt),"No vertices in the FV"
        continue
    for i in range(n):
        for j in range(i+1,n):
            dis2 = (mc_x[i]-mc_x[j])**2+(mc_y[i]-mc_y[j])**2+(mc_z[i]-mc_z[j])**2
            if dis2 > 4**2:
                multiplicity = "ms"
    plt.ion()
    cir1=plt.Circle((0,0), radius=1460/2.,color="b",fill=False,label="TPC R=730mm")
    cir2=plt.Circle((0,0), radius=688,color="r",fill=False,label="FV R=688mm")
    cir3=plt.Circle((0,0), radius=1460/2.+80,color="orange",fill=False,label="skin R=810mm")
    plt.plot(mc_x,mc_y,'o')
    plt.xlim(-1300,1300)
    plt.ylim(-1300,1300)
    plt.title("EventID %d"%evt)
    ax=plt.gca()
    ax.add_patch(cir1)
    ax.add_patch(cir2)
    ax.add_patch(cir3)
    plt.legend()
    plt.show()
    print "EventID",int(evt),"Number of vertices",n,"Likely multiplicity",multiplicity
    raw_input()
    plt.close()

