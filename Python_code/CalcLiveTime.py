import os,sys
import ROOT
import numpy as np
import pdb
totallivetime=0
totalphyLivetime=0
totalphyLivetime_ns=0
totaldeadtime=0
linenum=0
totalevents=0
filename=sys.argv[1]
line_skip=9 #number of lines to skip in the filelist
num_lines = sum(1 for line in open(filename))-line_skip
for i in range(num_lines):
    tMC = ROOT.TChain("Events")
    tMC2 = ROOT.TChain("Events")
    infile=open(filename)
    line = infile.readlines()[line_skip+i]
    linenum+=1
    run=int((line.split("/")[-3]).split("_")[-1])
    index=int((line.split("/")[-1]).split("_")[-2])
#    print ("run,index:",run,",",index," totallivetime so far:",totallivetime)
    tMC.Add(line.split()[0])
    tMC2.Add(line.split()[0])
    if (not os.path.exists(line.split()[0])):
        print (line.split()[0]," doesn't exist")
        continue
    else:
        if "5.3.8" in filename:
            n = tMC.Draw("eventHeader.daqLivetime_ns:eventHeader.daqDeadtime_ns","","goff")
        else:
            n = tMC.Draw("eventHeader.daqLivetime_ns:eventHeader.daqDeadtime_ns:eventHeader.physicsLivetime_ns","","goff")
            n2 = tMC2.Draw("eventHeader.physicsLivetime_s","eventHeader.physicsLivetime_s>0","goff")
            phyLivetime_s = np.copy(np.frombuffer(tMC2.GetV1(),count=n2))
            phyLivetime_ns = np.copy(np.frombuffer(tMC.GetV3(),count=n))
            totalphyLivetime = totalphyLivetime+np.sum(phyLivetime_s)/3600.
            totalphyLivetime_ns = totalphyLivetime_ns+np.sum(phyLivetime_ns)/3600/10**9
        daqLivetime_ns = np.copy(np.frombuffer(tMC.GetV1(),count=n))
        daqDeadtime_ns = np.copy(np.frombuffer(tMC.GetV2(),count=n))
        totallivetime = totallivetime+np.sum(daqLivetime_ns)/3600/10**9
        totaldeadtime = totaldeadtime+np.sum(daqDeadtime_ns)/3600/10**9
        totalevents = totalevents+n
totalphyLivetime = totalphyLivetime+totalphyLivetime_ns
print ("total number of files:",num_lines)
print ("total number of events:",totalevents)
print ("total daq livetime (h):",totallivetime)
print ("total physics livetime (h):",totalphyLivetime)
