import ROOT,glob,os
import array
import numpy as np

def makeMatchingEffPlots(obj_, year, outdir):
  ROOT.gROOT.SetBatch(True)
  ROOT.gROOT.LoadMacro("setTDRStyle.h")
  ROOT.gStyle.SetOptStat(0)
  ROOT.gStyle.SetOptFit(0)
  ROOT.gStyle.SetOptTitle(0)
  ROOT.gStyle.SetPalette(1)
  ROOT.TH1.SetDefaultSumw2()

  EOSCMS="root://eoscms.cern.ch/"
  path=EOSCMS+"/eos/cms/store/group/phys_jetmet/nbinnorj/WTopTagging/ntuples_HRTSF/"
  if obj_ == "W":
    if   year == "2016": f_ = ROOT.TFile.Open(path+"2016/mc_nom/sm_tree.root" , "READONLY" );          intLumi="36.8"
    elif year == "2017": f_ = ROOT.TFile.Open(path+"29July/mc_nom/sm_tree.root" , "READONLY" );        intLumi="41.53"
    elif year == "2018": f_ = ROOT.TFile.Open(path+"3Oct_For_Copy/mc_nom/sm_tree.root" , "READONLY" ); intLumi="59.74"
  
  t_ = f_.Get("Events")

  if obj_ == "W":
    c_base         	= "(n_ak8>=1 && ak8_1_pt>200 && abs(ak8_1_eta)<2.4)"
    c_ak8 			= "("+c_base+"&& (ak8_1_dr_fj_top_wqmax<3.))"
    c_ak8 = c_base
    c_W = "(ak8_1_dr_fj_top_wqmax<0.8)"
    c_b = "(ak8_1_dr_fj_top_b<0.8)"

    # c_had_ak8_dr0p6_q  = "(ak8_1_pt>200 && abs(ak8_1_eta)<2.4)" 
    c_ak8_dr_Wub   = "("+c_base+" && "+c_W+" || "+c_b+")" 
    c_ak8_dr_Wnb   = "("+c_base+" && "+c_W+" && "+c_b+")"
    c_ak8_dr_WmWnb = "("+c_base+" && "+c_W+" && !"+c_b+")"
    c_ak8_dr_bmWnb = "("+c_base+" && "+c_b+" && !"+c_W+")"
    c_ak8_dr_xWub  = "("+c_base+" && !("+c_W+" || "+c_b+"))"
    c_ak8_dr_W   = "("+c_base+" && "+c_W+")"
    c_ak8_dr_b   = "("+c_base+" && "+c_b+")"

    # c_had_ca15         = "(ca15_1_pt>200 && abs(ca15_1_eta)<2.4 && ca15_1_dr_fj_"+obj_+"<3.)" 
    # c_had_ca15_dr1p2   = "(ca15_1_dr_fj_"+obj_+"<1.2  && abs(ca15_1_eta)<2.4)" 
    # c_had_ca15_dr1p2_q = "(ca15_1_pt>200 && ca15_1_dr_fj_"+obj_+"<1.2 && (ca15_1_dr_fj_top_wqmax<1.2) && abs(ca15_1_eta)<2.4)" 

  bins = 20; xmin = 100.; xmax = 1200.
  # h_pt_ak8   = create1Dhisto("sample",t_,"1",c_had_ak8,"ak8_1_gen"+obj_+"pt",bins,xmin,xmax,False,1,1,"h_pt",False,False)             
  # h_pt_ak8   = create1Dhisto("sample",t_,intLumi,c_had_ak8,"leptonicW_pt",bins,xmin,xmax,False,1,1,"h_pt",False,False)             
  # h_pt_dr0p6 = create1Dhisto("sample",t_,"1",c_had_ak8_dr0p6,"ak8_1_gen"+obj_+"pt",bins,xmin,xmax,False,2,1,"h_pt_dr0p6",False,False) 
  # h_pt_dr0p6_q = create1Dhisto("sample",t_,"1",c_had_ak8_dr0p6_q,"ak8_1_gen"+obj_+"pt",bins,xmin,xmax,False,2,1,"h_pt_dr0p6_q",False,False)
  # h_pt_dr0p6 = create1Dhisto("sample",t_,intLumi,c_had_ak8_dr0p6,"leptonicW_pt",bins,xmin,xmax,False,2,1,"h_pt_dr0p6",False,False)
  # h_pt_dr0p6_q = create1Dhisto("sample",t_,intLumi,c_had_ak8_dr0p6_q,"leptonicW_pt",bins,xmin,xmax,False,2,1,"h_pt_dr0p6_q",False,False)  
  # h_pt_ca15  = create1Dhisto("sample",t_,"1",c_had_ca15,"ca15_1_gen"+obj_+"pt",bins,xmin,xmax,False,1,1,"h_pt",False,False)             
  # h_pt_dr1p2 = create1Dhisto("sample",t_,"1",c_had_ca15_dr1p2,"ca15_1_gen"+obj_+"pt",bins,xmin,xmax,False,1,1,"h_pt_dr1p2",False,False)
  # h_pt_dr1p2_q = create1Dhisto("sample",t_,"1",c_had_ca15_dr1p2_q,"ca15_1_gen"+obj_+"pt",bins,xmin,xmax,False,1,1,"h_pt_dr1p2_q",False,False)
  
  evt_legnames=[]
  h_ak8           = create1Dhisto("sample",t_,intLumi, c_ak8   		  ,"leptonicW_pt",bins,xmin,xmax,False,1,1,"h_ak8",False,False)          ;evt_legnames.append("all")
  h_ak8_dr_Wub    = create1Dhisto("sample",t_,intLumi, c_ak8_dr_Wub   ,"leptonicW_pt",bins,xmin,xmax,False,1,1,"h_ak8_dr_Wub",False,False)   ; evt_legnames.append("W #vee b")
  h_ak8_dr_Wnb    = create1Dhisto("sample",t_,intLumi, c_ak8_dr_Wnb   ,"leptonicW_pt",bins,xmin,xmax,False,1,1,"h_ak8_dr_Wnb",False,False)   ; evt_legnames.append("W #wedge b")
  h_ak8_dr_WmWnb  = create1Dhisto("sample",t_,intLumi, c_ak8_dr_WmWnb ,"leptonicW_pt",bins,xmin,xmax,False,1,1,"h_ak8_dr_WmWnb",False,False) ; evt_legnames.append("W - (W #wedge b)")
  h_ak8_dr_bmWnb  = create1Dhisto("sample",t_,intLumi, c_ak8_dr_bmWnb ,"leptonicW_pt",bins,xmin,xmax,False,1,1,"h_ak8_dr_bmWnb",False,False) ; evt_legnames.append("b - (W #wedge b)")
  h_ak8_dr_xWub   = create1Dhisto("sample",t_,intLumi, c_ak8_dr_xWub  ,"leptonicW_pt",bins,xmin,xmax,False,1,1,"h_ak8_dr_xWub",False,False)  ; evt_legnames.append("#corner(W #vee b)")
  h_ak8_dr_W      = create1Dhisto("sample",t_,intLumi, c_ak8_dr_W     ,"leptonicW_pt",bins,xmin,xmax,False,1,1,"h_ak8_dr_W",False,False)   	 ; evt_legnames.append("W")
  h_ak8_dr_b   	  = create1Dhisto("sample",t_,intLumi, c_ak8_dr_b  	  ,"leptonicW_pt",bins,xmin,xmax,False,1,1,"h_ak8_dr_b",False,False)     ; evt_legnames.append("b")
  
  ## cosmetics
  # h_pt_ak8.SetFillColor(0); h_pt_ak8.SetMarkerColor(1); h_pt_ak8.SetMarkerStyle(20); h_pt_ak8.SetMarkerSize(1.);
  # h_pt_dr0p6.SetFillColor(0); h_pt_dr0p6.SetMarkerColor(2); h_pt_dr0p6.SetMarkerStyle(20); h_pt_dr0p6.SetMarkerSize(1.);
  # h_pt_dr0p6_q.SetFillColor(0); h_pt_dr0p6_q.SetMarkerColor(2); h_pt_dr0p6_q.SetMarkerStyle(24); h_pt_dr0p6_q.SetMarkerSize(1.);
  # h_pt_ca15.SetFillColor(0) h_pt_ca15.SetMarkerColor(1) h_pt_ca15.SetMarkerStyle(20) h_pt_ca15.SetMarkerSize(1.)
  # h_pt_dr1p2.SetFillColor(0) h_pt_dr1p2.SetMarkerColor(1) h_pt_dr1p2.SetMarkerStyle(21) h_pt_dr1p2.SetMarkerSize(1.)
  # h_pt_dr1p2_q.SetFillColor(0) h_pt_dr1p2_q.SetMarkerColor(1) h_pt_dr1p2_q.SetMarkerStyle(25) h_pt_dr1p2_q.SetMarkerSize(1.)
  
  evt_histos= [
    h_ak8,
    h_ak8_dr_Wub,
    h_ak8_dr_Wnb,
    h_ak8_dr_WmWnb,
    h_ak8_dr_bmWnb,
    h_ak8_dr_xWub,
    h_ak8_dr_W,
    h_ak8_dr_b,
  ]

  ## eff calculation
  eff_legnames=[]
  h_ak8_dr_Wub_r     = h_ak8_dr_Wub.Clone("h_ak8_dr_Wub_r")    ; h_ak8_dr_Wub_r.Divide(h_ak8_dr_Wub,h_ak8)         ; eff_legnames.append("W #vee b")
  h_ak8_dr_Wnb_r   = h_ak8_dr_Wnb.Clone("h_ak8_dr_Wnb_r")      ; h_ak8_dr_Wnb_r.Divide(h_ak8_dr_Wnb,h_ak8)     ; eff_legnames.append("W #wedge b")
  h_ak8_dr_WmWnb_r = h_ak8_dr_WmWnb.Clone("h_ak8_dr_WmWnb_r")  ; h_ak8_dr_WmWnb_r.Divide(h_ak8_dr_WmWnb,h_ak8) ; eff_legnames.append("W - (W #wedge b)")
  h_ak8_dr_bmWnb_r = h_ak8_dr_bmWnb.Clone("h_ak8_dr_bmWnb_r")  ; h_ak8_dr_bmWnb_r.Divide(h_ak8_dr_bmWnb,h_ak8) ; eff_legnames.append("b - (W #wedge b)")
  h_ak8_dr_xWub_r  = h_ak8_dr_xWub.Clone("h_ak8_dr_xWub_r")    ; h_ak8_dr_xWub_r.Divide(h_ak8_dr_xWub,h_ak8)   ; eff_legnames.append("#corner(W #vee b)")
  h_ak8_dr_W_r     = h_ak8_dr_W.Clone("h_ak8_dr_W_r")      	   ; h_ak8_dr_W_r.Divide(h_ak8_dr_W,h_ak8)   	   ; eff_legnames.append("W")
  h_ak8_dr_b_r     = h_ak8_dr_b.Clone("h_ak8_dr_b_r")          ; h_ak8_dr_b_r.Divide(h_ak8_dr_b,h_ak8)   	   ; eff_legnames.append("b")
  
  eff_histos = [
    h_ak8_dr_Wub_r,
    h_ak8_dr_Wnb_r,
    h_ak8_dr_WmWnb_r,
    h_ak8_dr_bmWnb_r,
    h_ak8_dr_xWub_r,
    h_ak8_dr_W_r,
    h_ak8_dr_b_r,
  ]

  pt_cms = ROOT.TPaveText(0.11,0.77,0.4,0.9,"NDC")
  pt_cms.SetFillStyle(0)
  pt_cms.SetFillColor(0)
  pt_cms.SetLineWidth(0)
  pt_cms.AddText("CMS")
  pt_cms.SetTextSize(0.08)

  pt_preliminary = ROOT.TPaveText(0.2,0.63,0.42,0.9,"NDC")
  pt_preliminary.SetFillStyle(0)
  pt_preliminary.SetFillColor(0)
  pt_preliminary.SetLineWidth(0)
  pt_preliminary.AddText("Preliminary")
  pt_preliminary.SetTextFont(52)
  pt_preliminary.SetTextSize(0.06)

  pt_lumi=ROOT.TLatex()
  # const char *longstring ="35.9 fb^{-1} (13 TeV)"
  lumi={"2016":"35.9", "2017":"41.5", "2018":"59.7"}  
  longstring=lumi[year]+" fb^{-1} (13 TeV)"
  pt_lumi.SetTextSize(0.05)
  pt_lumi.SetTextFont(42)

  leg = ROOT.TLegend(0.55,0.68,0.92,0.9)
  leg.SetFillStyle(0)
  leg.SetFillColor(0)
  leg.SetLineWidth(0)

  c_eff = ROOT.TCanvas("c_eff","c_eff",800,800)
  ROOT.gPad.SetRightMargin(0.05)
  ROOT.gPad.SetLeftMargin(0.13)
  ROOT.gPad.SetBottomMargin(0.15)
  ROOT.gPad.SetTopMargin(0.09)
  
  for i,histo in enumerate(eff_histos):
    histo.SetLineColor(1+i); histo.SetFillColor(0); histo.SetMarkerColor(1+i); histo.SetMarkerStyle(20+i); histo.SetMarkerSize(1.);
    leg.AddEntry(histo,eff_legnames[i],"PL")
    if i==0:
      histo.GetYaxis().SetRangeUser(0.,1.5)
      histo.GetYaxis().SetTitle("Reconstruction efficiency")
      histo.GetXaxis().SetTitle("W boson p_{T} [GeV]")
      histo.GetYaxis().SetTitleOffset(1.08)
      histo.GetXaxis().SetTitleOffset(1.1)
      histo.Draw("P")
    else:
      histo.Draw("P SAME")
  pt_cms.Draw("same")
  pt_preliminary.Draw("same")
  pt_lumi.DrawLatexNDC(0.55,0.93,longstring)
  leg.Draw("same")

  c_eff.Print(outdir+"/eff_"+obj_+year+".png")
  
  leg.Clear()
  leg.SetFillStyle(0)
  leg.SetFillColor(0)
  leg.SetLineWidth(0)

  c_evt = ROOT.TCanvas("c_evt","c_evt",800,800)
  ROOT.gPad.SetRightMargin(0.05)
  ROOT.gPad.SetLeftMargin(0.13)
  ROOT.gPad.SetBottomMargin(0.15)
  ROOT.gPad.SetTopMargin(0.09)
  tempmax=0
  for i,histo in enumerate(evt_histos):
    histo.SetLineColor(1+i); histo.SetFillColor(0); histo.SetMarkerColor(1+i); histo.SetMarkerStyle(20+i); histo.SetMarkerSize(1.);
    leg.AddEntry(histo,evt_legnames[i],"PL")
    if histo.GetMaximum()>tempmax: 
      tempmax=histo.GetMaximum()
      histo.GetYaxis().SetRangeUser(0.,1.2*tempmax)
    if i==0:
      histo.GetYaxis().SetTitle("Number of events")
      histo.GetXaxis().SetTitle("W boson p_{T} [GeV]")
      histo.GetYaxis().SetTitleOffset(2)
      histo.GetXaxis().SetTitleOffset(1.1)
      histo.Draw("HIST")
    else:
      histo.Draw("HIST SAME")
  
  leg.Draw("same")
  c_evt.SetTicks()
  c_evt.Print(outdir+"/evt_"+obj_+year+".png")

def create1Dhisto(sample,tree,intLumi,cuts,branch,bins,xmin,xmax, useLog, color, style,name,norm,data) :
  ROOT.TH1.SetDefaultSumw2()
  if (data) : cut ="("+cuts+")" 
  else :
    if      "puUp" in name : cut = "(xsecWeight*puWeightUp*genWeight*"+intLumi+")*("+cuts+")"
    elif  "puDown" in name : cut = "(xsecWeight*puWeightDown*genWeight*"+intLumi+")*("+cuts+")"
    # elif    "herw" in name : cut = "(xsecWeight*puWeight*"+intLumi+")*("+cuts+")"
    else                   : cut ="(xsecWeight*puWeight*genWeight*"+intLumi+")*("+cuts+")"
 
  
  print "cut = " + cut + "\n"

  hTemp = ROOT.TH1D(name,name,bins,xmin,xmax) # hTemp.SetName(name)
  tree.Project(name,branch,cut)

  hTemp.SetLineWidth(3)
  hTemp.SetMarkerSize(0)
  hTemp.SetLineColor(color)
  hTemp.SetFillColor(color)
  hTemp.SetLineStyle(style)

  # ad overflow bin             
  error =0.; integral = hTemp.IntegralAndError(bins,bins+1,ROOT.Double(error))
  hTemp.SetBinContent(bins,integral)
  hTemp.SetBinError(bins,error)

  if (norm) : hTemp.Scale(1./(hTemp.Integral()))

  return hTemp
