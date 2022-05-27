import os,sys
import ROOT
upperE=120
markersize=0.25
canvasS1 = ROOT.TCanvas('canvas', '', 1000, 800)
pad1 = ROOT.TPad("pad1","pad1",0,0.33,1,1);
pad2 = ROOT.TPad("pad2","pad2",0,0,1,0.33);
pad1.SetBottomMargin(0.00001);
pad1.SetBorderMode(0);
pad1.SetLogy()
pad2.SetTopMargin(0.00001);
pad2.SetBottomMargin(0.2);
pad2.SetBorderMode(0);
pad1.Draw()
pad2.Draw()
#datafile="run/MSSS_analysis/AmLi_run6134_6160_lzap-5.3.8_s1rmsCut85.root"
datafile="AmLi/AmLi_run6134_6160_lzap5.3.8_s1rmsCut85_eachS2MScut_v2.root"
datafile_dev="AmLi/AmLi_run6134_6160_lzap-dev1f2c9fa2_s1rmsCut85_eachS2MScut.root"
#infile1=ROOT.TFile.Open('run/lzlama_EvalSSClassification/AmLi_BACCARAT-6.2.9_LZLAMA-3.0.0_700mm_Pipe1_withE.root')
#infile1=ROOT.TFile.Open('~/alpaca/run/lzlama_EvalSSClassification/AmLi_BACCARAT-6.2.9_LZLAMA-3.0.0_700mm_Pipe1_WSFV.root')
infile1=ROOT.TFile.Open('BACCARAT-6.2.9_PROD-0_LZLAMA-3.1.6_PROD-0-PreSR1_eachS2MScut_plots.root')
#infile1=ROOT.TFile.Open('/global/cfs/cdirs/lz/users/qxia/AmLi/BACCARAT-6.2.9_PROD-0_LZLAMA-3.1.6_PROD-0-PreSR1_plots.root')
#infile1=ROOT.TFile.Open('/global/cfs/cdirs/lz/users/qxia/AmLi/BACCARAT-6.2.9_PROD-0_LZLAMA-swk_s2_merge_area_sqrt_ratio_eachS2WSFV_plots.root')
infile2= ROOT.TFile.Open(datafile, 'read')
infile3= ROOT.TFile.Open(datafile_dev, 'read')
infile2_copy= ROOT.TFile.Open(datafile, 'read')
infile3_copy= ROOT.TFile.Open(datafile_dev, 'read')
#infile2= ROOT.TFile.Open('run/MSSS_analysis/AmLi_run6134_6160_lzap5.3.8_s1rmsCut85_FVR67cm.root', 'read')
#TruthE1 = infile1.Get('ss_ROI_Erecon_TruthFV_NeutronSelection_TruthEtrain')
TruthE1 = infile1.Get('ss_ROI_Erecon_NR_WSFV_NeutronSelection_TruthEtrain')
#TruthE1 =  infile1.Get('Eparent_neutron')
#TruthE1_weighted =  infile_weighted.Get('Eparent_neutron')
ReconE1 = infile2.Get('ssFidu_Erecon_NR')
ReconE1_copy = infile2_copy.Get('ssFidu_Erecon_NR')
ReconE1_dev = infile3.Get('ssFidu_Erecon_NR')
ReconE1_dev_copy = infile3_copy.Get('ssFidu_Erecon_NR')
print("Number of events:",ReconE1.Integral())
print("Number of events (dev)",ReconE1_dev.Integral())
TruthE1.Scale(0.145)
#TruthE1.Scale(6)
TruthE1.SetLineColor(4)
ReconE1.SetLineColor(1)
ReconE1_dev.SetLineColor(2)
#ReconE1.SetStats(0)
TruthE1.SetStats(0)
ReconE1_copy.SetStats(0)
ReconE1_dev_copy.SetStats(0)
TruthE1.GetXaxis().SetRangeUser(0,upperE)
ReconE1.GetXaxis().SetRangeUser(0,upperE)
ReconE1_copy.GetXaxis().SetRangeUser(0,upperE)
ReconE1_dev.GetXaxis().SetRangeUser(0,upperE)
ReconE1_dev_copy.GetXaxis().SetRangeUser(0,upperE)
pad1.cd()
TruthE1.Draw("HIST")
ReconE1.Draw("SAME")
ReconE1_dev.Draw("SAME")
legend=ROOT.TLegend(0.45,0.7,0.9,0.9)
legend.SetTextSize(0.005);
legend.AddEntry(ReconE1,"Data Energy (run 6134-6160) lzap-5.3.8",'lep');
legend.AddEntry(ReconE1_dev,"Data Energy (run 6134-6160) Michael's dev lzap",'lep');
legend.AddEntry(TruthE1,"Simulated Energy (BACCARAT-6.2.9_LZLAMA-3.1.6)",'l p');

 TruthE1.SetTitle("DD SS Reconstructed NR Energy [keV]")
 TruthE1.GetXaxis().SetTitle("Reconstructed NR Energy [keV]")
 TruthE1.GetYaxis().SetTitle("counts / keV / 1e+10 iso neutron")


# TruthE1.SetTitle("AmLi SS Energy") 
# TruthE1.GetXaxis().SetTitle("Energy (keV)")
#ReconE1.GetXaxis().SetRangeUser(0,10)
legend.Draw()
legend.SetTextSize(0.035)
pad2.cd()
ReconE1_copy.Divide(TruthE1)
ReconE1_dev_copy.Divide(TruthE1)
ReconE1_copy.SetLineColor(1)
ReconE1_dev_copy.SetLineColor(2)
ReconE1_copy.Draw()
ReconE1_dev_copy.Draw("SAME")
ReconE1_copy.GetYaxis().SetTitle("Efficiency (Detected/Simulated)")
ReconE1_copy.GetXaxis().SetTitle("Energy (keV)")
ReconE1_copy.GetXaxis().SetTitleSize(0.1)
ReconE1_copy.GetYaxis().SetTitleSize(0.05)
ReconE1_copy.GetXaxis().SetLabelSize(0.05)
ReconE1_copy.GetYaxis().SetLabelSize(0.05)
ReconE1_copy.SetTitle("")
ReconE1_copy.GetYaxis().SetRangeUser(0,4.5)
canvasS1.SaveAs('AmLi_SS.pdf')


'''infile01=ROOT.TFile.Open('run/lzlama_EvalSSClassification/AmLi_BACCARAT-6.2.9_LZLAMA-3.0.0_700mm_Pipe1_withE.root')
infile02= ROOT.TFile.Open('run/MSSS_analysis/AmLi_run6134_6160_lzap5.3.8_s1rmsCut85.root', 'read')
TruthE01 = infile01.Get('ss_ROI_Erecon_TruthFV_NeutronSelection_TruthEtrain')
ReconE01 = infile02.Get('ssFidu_Erecon')
TruthE01.Scale(0.03)
ReconE01.SetLineColor(4)
ReconE01.SetStats(0)

infile11 = ROOT.TFile.Open('run/lzlama_EvalSSClassification/AmLi_BACCARAT-6.2.9_LZLAMA-3.0.0_700mm_Pipe1_FVR66cm.root ', 'read')
infile12= ROOT.TFile.Open('run/MSSS_analysis/AmLi_run6134_6160_lzap5.3.8_s1rmsCut85_FVR66cm.root', 'read')
TruthE11 = infile11.Get('ss_ROI_Erecon_TruthFV_NeutronSelection_TruthEtrain')
ReconE11 = infile12.Get('ssFidu_Erecon')
TruthE11.Scale(0.03)
ReconE11.SetLineColor(6)
ReconE11.SetStats(0)

infile21 = ROOT.TFile.Open('run/lzlama_EvalSSClassification/AmLi_BACCARAT-6.2.9_LZLAMA-3.0.0_700mm_Pipe1_FVR67cm.root ', 'read')
infile22= ROOT.TFile.Open('run/MSSS_analysis/AmLi_run6134_6160_lzap5.3.8_s1rmsCut85_FVR67cm.root', 'read')
TruthE21 = infile21.Get('ss_ROI_Erecon_TruthFV_NeutronSelection_TruthEtrain')
ReconE21 = infile22.Get('ssFidu_Erecon')
TruthE21.Scale(0.03)
ReconE21.SetLineColor(1)
ReconE21.SetStats(0)

infile31 = ROOT.TFile.Open('run/lzlama_EvalSSClassification/AmLi_BACCARAT-6.2.9_LZLAMA-3.0.0_700mm_Pipe1_FVR64cm.root ', 'read')
infile32= ROOT.TFile.Open('run/MSSS_analysis/AmLi_run6134_6160_lzap5.3.8_s1rmsCut85_FVR64cm.root', 'read')
TruthE31 = infile31.Get('ss_ROI_Erecon_TruthFV_NeutronSelection_TruthEtrain')
ReconE31 = infile32.Get('ssFidu_Erecon')
TruthE31.Scale(0.03)
ReconE31.SetLineColor(7)
ReconE31.SetStats(0)

canvasS2 = ROOT.TCanvas('canvas', '', 700, 500)
ReconE1.Divide(TruthE1)
ReconE1.SetStats(0)
ReconE01.Divide(TruthE01)
ReconE01.SetStats(0)
ReconE11.Divide(TruthE11)
ReconE11.SetStats(0)
ReconE21.Divide(TruthE21)
ReconE21.SetStats(0)
ReconE31.Divide(TruthE31)
ReconE31.SetStats(0)
ReconE1.GetYaxis().SetTitle("Efficiency (Detected/Simulated)")
ReconE1.GetXaxis().SetTitle("Energy (keV)")
ReconE1.SetTitle("AmLi SS Detection efficiency") 
#legend=ROOT.TLegend(0.2,0.7,0.6,0.9)
#legend.AddEntry(ReconE1,"FV R=70cm",'lep');
#legend.AddEntry(ReconE01,"FV R=68.8cm",'lep');
#legend.AddEntry(ReconE21,"FV R=67cm",'lep');
#legend.AddEntry(ReconE11,"FV R=66cm",'lep');
#legend.AddEntry(ReconE31,"FV R=64cm",'lep');
ReconE1.Draw()
#ReconE01.Draw("SAME")
#ReconE21.Draw("SAME")
#ReconE11.Draw("SAME")
#ReconE31.Draw("SAME")
legend.Draw()
legend.SetTextSize(0.035)
ReconE1.GetXaxis().SetRangeUser(0,50)
ReconE1.GetYaxis().SetRangeUser(0,5)
canvasS2.SaveAs('AmLi_Efficiency.pdf')
'''
