import os,sys
import ROOT
from ROOT import TBrowser
b = TBrowser()
#infile= ROOT.TFile.Open('SS_TPC_Neutron_April07.root', 'read')
infile= ROOT.TFile.Open('/global/cfs/cdirs/lz/users/madan12/SR1_WIMPs_Search/ALPACA_April06/run/SR1WS/SS_TPC_Neutron_April07.root', 'read')
canvas = ROOT.TCanvas('canvas', '', 700, 500)
#s1vs2 = infile.Get('s1s2Area_SS_BC_FV_HR_S2W_AA_s2ST_ET')
s1vs2 = infile.Get('s1s2Area_SS_BC_FV_HR_S2W_AA_s2ST_ET')
s1vs2.Draw()
s1vs2.GetXaxis().SetRangeUser(0,200)
s1vs2.GetYaxis().SetRangeUser(2.5,5.0)
canvas.SetGrid()
s1vs2.SetStats(0)
s1vs2.GetXaxis().SetTitle(" S1c [phd]")
s1vs2.GetYaxis().SetTitle(" Log10 (S2c [phd])")
s1vs2.SetMarkerStyle(7)

# For ER Band from NEST
meanband_par_er=[-3.78620965e+01,  4.27796511e+01,  1.46575451e-03,  4.39121562e+00]
lowband_par_er=[-5.16028480e+01,  5.43521700e+01,  1.27207032e-03,  4.36329951e+00]
upband_par_er=[-2.88117645e+01,  3.40210278e+01,  1.61744907e-03,  4.44200032e+00]

meanband_er=ROOT.TF1("mean","[0]/(x+[1]) + [2]*x +[3]" ,0,200)
meanband_er.SetParameter(0,meanband_par_er[0])
meanband_er.SetParameter(1,meanband_par_er[1])
meanband_er.SetParameter(2,meanband_par_er[2])
meanband_er.SetParameter(3,meanband_par_er[3])
meanband_er.SetLineColor(2)
meanband_er.Draw("SAME")
upband_er=ROOT.TF1("mean","[0]/(x+[1]) + [2]*x +[3]" ,0,200)
upband_er.SetParameter(0,upband_par_er[0])
upband_er.SetParameter(1,upband_par_er[1])
upband_er.SetParameter(2,upband_par_er[2])
upband_er.SetParameter(3,upband_par_er[3])
upband_er.SetLineColor(2)
upband_er.Draw("SAME")
lowband_er=ROOT.TF1("mean","[0]/(x+[1]) + [2]*x +[3]" ,0,200)
lowband_er.SetParameter(0,lowband_par_er[0])
lowband_er.SetParameter(1,lowband_par_er[1])
lowband_er.SetParameter(2,lowband_par_er[2])
lowband_er.SetParameter(3,lowband_par_er[3])
lowband_er.SetLineColor(2)
lowband_er.Draw("SAME")


# For NR Band from NEST
# meanband_par=[-1.60931538e+01,  1.65998549e+01,  7.09441586e-04,  4.00711490e+00]
# lowband_par=[-1.82215616e+01, 1.48849458e+01,  6.96463078e-04,  3.95633716e+00]
# upband_par=[-1.45372497e+01,  2.01601309e+01,  7.09942200e-04,  4.06280681e+00]

# For NR Band from LZLAMA
meanband_par=[-1.31216616e+01,  1.34771408e+01,  9.85038258e-04,  3.94915711e+00]
lowband_par=[-1.56112495e+01,  1.30260273e+01,  1.01107232e-03,  3.89212313e+00]
upband_par=[-1.06828902e+01,  1.42526704e+01,  9.56068952e-04,  4.00686705e+00]

meanband=ROOT.TF1("mean","[0]/(x+[1]) + [2]*x +[3]" ,0,200)
meanband.SetParameter(0,meanband_par[0])
meanband.SetParameter(1,meanband_par[1])
meanband.SetParameter(2,meanband_par[2])
meanband.SetParameter(3,meanband_par[3])
meanband.SetLineColor(4)
meanband.Draw("SAME")
upband=ROOT.TF1("mean","[0]/(x+[1]) + [2]*x +[3]" ,0,200)
upband.SetParameter(0,upband_par[0])
upband.SetParameter(1,upband_par[1])
upband.SetParameter(2,upband_par[2])
upband.SetParameter(3,upband_par[3])
upband.SetLineColor(4)
upband.Draw("SAME")
lowband=ROOT.TF1("mean","[0]/(x+[1]) + [2]*x +[3]" ,0,200)
lowband.SetParameter(0,lowband_par[0])
lowband.SetParameter(1,lowband_par[1])
lowband.SetParameter(2,lowband_par[2])
lowband.SetParameter(3,lowband_par[3])
lowband.SetLineColor(4)
lowband.Draw("SAME")

canvas.SaveAs('s1s2Area_SS_BC_FV_HR_S2W_AA_s2ST_ET_April07_v2.png')