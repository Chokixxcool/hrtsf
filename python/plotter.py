import ROOT, os, glob
from makePlots import *
from MakeMatchingEffPlot import *

INDIR="/eos/user/s/ssyedoma/JMARWTag/TempFit/plots/"

EOSUSER="root://eosuser.cern.ch/"
USER="s/ssyedoma"
TEMPDIR="/eos/user/"+USER+"/JMARWTag/TempFit/SFtemplates"
DCDIR="/eos/user/"+USER+"/JMARWTag/TempFit/SFdatacards"
FDDIR="/eos/user/"+USER+"/JMARWTag/TempFit/SFfitdiags"
PLTDIR="/eos/user/"+USER+"/JMARWTag/TempFit/plots"

years=["2016","2017","2018"]
mistrates=["0p1","0p5","1p0","5p0"]
taggers=["sdtau21","deepak8"]
ptranges=["incl","low","lowmed","med"]
obj="W"
wp="JMAR"
# years=["2016"]

def main2():
  ### Matching Efficiency
  for year in years:
    makeMatchingEffPlots(obj,year,PLTDIR+"/"+year)

  ### Mistag
  # for year in years:
    # for mistrate in mistrates:
    #   getMistag(obj, wp, year, mistrate)

  ### Data/MC 
  # for year in years:
  #   for tag in taggers:
  #     for ptrange in ptranges:
  #       for mistrate in mistrates:
  #         if tag=="sdtau21": 
  #           if not mistrate=="5p0": continue
  #         filename=year+"_"+obj+"_"+tag+"_"+wp+"_"+ptrange+"_"+mistrate
  #         ## lin
  #         makeDataMCPlotsFromCombine(FDDIR, filename, wp, ptrange, "pass", 50.,250.,20,"mass", False, PLTDIR+"/"+year)
  #         makeDataMCPlotsFromCombine(FDDIR, filename, wp, ptrange, "fail", 50.,250.,20,"mass", False, PLTDIR+"/"+year)
          ## log
          # makeDataMCPlotsFromCombine(FDDIR, filename, wp, ptrange, "pass", 50.,250.,20,"mass", True, PLTDIR+"/"+year)
          # makeDataMCPlotsFromCombine(FDDIR, filename, wp, ptrange, "fail", 50.,250.,20,"mass", True, PLTDIR+"/"+year)

  ## Scale Factor
  # for year in years:
  #   getSFSummarySources(year, "W", "JMAR", FDDIR, mistrates, PLTDIR+"/"+year)

def main1():
  for year in years:
    h_sf,h_data,h_mc=[],[],[]
    c_mistag=ROOT.TCanvas("","",800,800)
    c_mistag.Divide(1,2)
    dum=dummy("p_{T}^jet [GeV]","#epsilon_{MC}",0,1.2)
    dum2=dummy("p_{T}^jet [GeV]","#epsilon_{DATA}",0,1.2)
    c_mistag.cd(1)
    dum.Draw()
    c_mistag.cd(2)
    dum2.Draw()

    # draw mistag #
    for tagger in taggers:
      f=ROOT.TFile.Open(INDIR+"mistag_%s_%s.root"%(year,tagger), "READONLY")
      h_data=f.Get("Data")
      h_mc=f.Get("MC")

      c_mistag.cd(1)
      h_mc.Draw("sames")
      c_mistag.cd(2)
      h_data.Draw("sames")
    
      c_mistag.Print(INDIR+"mistag_%s_%s.png"%(year,tagger))
    c_mistag.Close()
    
    c_sf=ROOT.TCanvas("","",800,800)
    dum_sf=dummy("p_{T}^{jet} [GeV]","#epsilon_{DATA}/#epsilon_{MC}",0,2)
    dum_sf.Draw()
    
    # draw scale factor #
    for tagger in taggers:
      f=ROOT.TFile.Open(INDIR+"mistag_%s_%s.root"%(year,tagger), "READONLY")
      h_sf=f.Get("SF")
    
      h_sf.Draw("sames")

    # c_sf.Print(INDIR+"sf_%s.pdf"%year)
    c_sf.Print(INDIR+"sf_%s.png"%year)
    c_sf.Close()

def dummy(xname="xaxis",yname="yaxis", ymin=0, ymax=1.4):
  dummy = ROOT.TH1D("","", 500, 200, 800)
  dummy.SetBinContent(1,0.0)
  dummy.GetXaxis().SetTitle(xname)
  dummy.GetYaxis().SetTitle(yname)
  dummy.SetLineColor(0)
  dummy.SetLineWidth(0)
  dummy.SetFillColor(0)
  dummy.SetMinimum(ymin)
  dummy.SetMaximum(ymax)
  dummy.GetYaxis().SetLabelSize(.03)
  dummy.GetXaxis().SetLabelSize(.03)
  dummy.SetStats(0)
  return dummy

if __name__ == '__main__':
  timerMain=ROOT.TStopwatch()
  timerMain.Start()

  # main1()
  main2()

  timerMain.Print()