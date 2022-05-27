import os,sys
import ROOT
from ROOT import TBrowser
b = TBrowser()
infile= ROOT.TFile.Open('AmLi_run6134_6160_lzap-dev-d4c7bc27_s1rmsCut85_eachS2MScut_shortlist_skipnonSSevents.root', 'read')
canvas = ROOT.TCanvas('canvas', '', 700, 500)
s1vs2 = infile.Get('ssFidu_S1_logS2')
s1vs2.Draw()
s1vs2.GetXaxis().SetRangeUser(0,150)
s1vs2.GetYaxis().SetRangeUser(0,5.0)
canvas.SetGrid()
s1vs2.SetStats(0)
# meanband_par=[-7.72995437e+00,  8.34764422e+00,  1.78275197e-03,  3.96718944e+00]
# lowband_par=[-1.10109039e+01,9.35132463e+00,1.70673559e-03,3.94017015e+00]
# upband_par=[-4.62132359e+00,6.75134220e+00,1.84482607e-03,3.99690084e+00]

meanband_par=[[-7.62389062e+00  8.18385455e+00  1.85490379e-03  3.94664975e+00]
lowband_par=[-9.83397552e+00  8.17459001e+00  1.99459614e-03  3.89237459e+00]
upband_par=[-5.41393480e+00  8.20093975e+00  1.71519130e-03  4.00092794e+00]

meanband=ROOT.TF1("mean","[0]/(x+[1]) + [2]*x +[3]" ,0,150)
meanband.SetParameter(0,meanband_par[0])
meanband.SetParameter(1,meanband_par[1])
meanband.SetParameter(2,meanband_par[2])
meanband.SetParameter(3,meanband_par[3])
meanband.SetLineColor(4)
meanband.Draw("SAME")
upband=ROOT.TF1("mean","[0]/(x+[1]) + [2]*x +[3]" ,0,150)
upband.SetParameter(0,upband_par[0])
upband.SetParameter(1,upband_par[1])
upband.SetParameter(2,upband_par[2])
upband.SetParameter(3,upband_par[3])
upband.SetLineColor(4)
upband.Draw("SAME")
lowband=ROOT.TF1("mean","[0]/(x+[1]) + [2]*x +[3]" ,0,150)
lowband.SetParameter(0,lowband_par[0])
lowband.SetParameter(1,lowband_par[1])
lowband.SetParameter(2,lowband_par[2])
lowband.SetParameter(3,lowband_par[3])
lowband.SetLineColor(4)
lowband.Draw("SAME")
canvas.SaveAs('AmLi_S1vslogS2.png')