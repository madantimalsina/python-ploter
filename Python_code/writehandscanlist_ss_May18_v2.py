import os,sys
import glob
import math
#outfile=open("handscanlist_ms.txt","w")
#outfile1=open("handscanlist_ms_s.txt","w")
infiles = glob.glob("/global/cfs/cdirs/lz/users/madan12/SR1_WIMPs_Search/logFile_SS_all_April23/log_*.txt")

#infiles = glob.glob("/global/cfs/cdirs/lz/users/madan12/SR1_WIMPs_Search/logFile_MS_April22/log_*.txt")
for infile in infiles:
        for line in open(infile).readlines()[28:]:
                    #if ("SS:" in line and " " in line):
                    if ("WSEVT:" in line and " " in line):
                    #if ("MS: " in line):
                        #print ("I am here")
                	#if ("MS: " in line):
#                if ("Other" in line and "    " in line):
#                if ("PileUp" in line and "    " in line):
						#run=line.split(" ")[1]
                        run=line.split(" ")[1]
                        event=line.split(" ")[2]
                        S1c=line.split(" ")[3]
                        S2c=line.split(" ")[4]
                        # X=line.split(" ")[5]
                        # Y=line.split(" ")[6]
                        # R=line.split(" ")[7]
                        # Z=line.split(" ")[8]
                        #M=line.split(" ")[9]
                        #outfile.write(run+" "+event+" "+S1c+" "+logS2c+" "+X+" "+Y+" "+R+" "+Z+"\n")
                        #outfile.write(run+" "+event+" "+S1c+" "+logS2c+"\n") #+"    "+S1c+"    "+logS2c+"\n")#+"    "+E)
                        a = float(S1c)
                        b = float(S2c)
                        c = float(math.log10(b)) # accidently s2 is printed so making log10(s2)
                        r = int(run)
                        e = int(event)
 
                        #if (a <= 4):
                        #if (a <= 160. and a >= 10. and b >= 3.9 and b <= 4.5):
                        if (a <= 60. and a >= 50. and c >= 2.8 and c <= 3.95):
                         #print (b)
                         #outfile1.write(r+" "+e+" "+a+" "+b+"\n")
                         print (r," ",e," ",a," ",c)
                         #print (r," ",e)