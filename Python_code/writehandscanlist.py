import os,sys
import glob
outfile=open("handscanlist.txt","w")
infiles = glob.glob("~/alpaca/analysisScripts/tmp/log_*.txt")
for infile in infiles:
        for line in open(infile).readlines()[28:]:
                if ("SS" in line and "    " in line):
#                if ("Other" in line and "    " in line):
#                if ("PileUp" in line and "    " in line):
                        run=line.split("    ")[1]
                        event=line.split("    ")[2]
                        S1c=line.split("    ")[3]
                        logS2c=line.split("    ")[4]
#                        E=line.split("    ")[5]
                        outfile.write(run+"    "+event+"\n")#+"    "+S1c+"    "+logS2c+"\n")#+"    "+E)
                        print (run," ",event)
