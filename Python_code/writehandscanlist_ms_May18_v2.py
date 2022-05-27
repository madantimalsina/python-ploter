import os,sys
import glob
#outfile=open("handscanlist_ms.txt","w")
#outfile1=open("handscanlist_ms_s.txt","w")
#infiles = glob.glob("/global/cfs/cdirs/lz/users/madan12/SR1_WIMPs_Search/logFile_SS_all_April23/log_*.txt")

infiles = glob.glob("/global/cfs/cdirs/lz/users/madan12/SR1_WIMPs_Search/logFile_MS_April22/log_*.txt")
for infile in infiles:
        for line in open(infile).readlines()[28:]:
                    if ("MSET:" in line and " " in line):
                    #if ("WSEVT:" in line and " " in line):
                    #if ("MS: " in line):
                        #print ("I am here")
                	#if ("MS: " in line):
#                if ("Other" in line and "    " in line):
#                if ("PileUp" in line and "    " in line):
						#run=line.split(" ")[1]
                        run=line.split(" ")[1]
                        event=line.split(" ")[2]
                        S1c=line.split(" ")[3]
                        logS2c=line.split(" ")[4]
                        # X=line.split(" ")[5]
                        # Y=line.split(" ")[6]
                        # R=line.split(" ")[7]
                        # Z=line.split(" ")[8]
                        #M=line.split(" ")[9]
                        #outfile.write(run+" "+event+" "+S1c+" "+logS2c+" "+X+" "+Y+" "+R+" "+Z+"\n")
                        #outfile.write(run+" "+event+" "+S1c+" "+logS2c+"\n") #+"    "+S1c+"    "+logS2c+"\n")#+"    "+E)
                        a = float(S1c)
                        b = float(logS2c)
                        r = int(run)
                        e = int(event)
 
                        #if (b <= 3.2):
                        if (a <= 160. and a >= 100. and b >= 3.9 and b <= 4.5):
                        #if (a <= 120. and a >= 0. and b >= 2.8 and b <= 4.5):
                         #print (b)
                         #outfile1.write(r+" "+e+" "+a+" "+b+"\n")
                         print (r," ",e," ",a," ",b)
                         #print (r," ",e)