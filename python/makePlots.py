import ROOT,glob,os
import array
import numpy as np

EOSDIR="/eos/user/s/ssyedoma/JMARWTag/TempFit/plots/"

def makePlots(path2file, filename, score, ptrange, xmin, xmax, nbins, xaxis, obj, wp, mistrate, year):
  ROOT.gROOT.SetBatch(False)
  ROOT.gROOT.LoadMacro("setTDRStyle.h")
  ROOT.gStyle.SetOptStat(0)
  ROOT.gStyle.SetOptFit(1)
  ROOT.gStyle.SetPalette(1)
  ROOT.gStyle.SetOptTitle(0)
  ROOT.TH1.SetDefaultSumw2()
  
  ## make pre/post fit plots
  # makeDataMCPlotsFromCombine(path2file,filename,score,ptrange,"pass",xmin,xmax,nbins,xaxis,False)
  # makeDataMCPlotsFromCombine(path2file,filename,score,ptrange,"fail",xmin,xmax,nbins,xaxis,False)

  ## make matching efficiency plots
  # print   "running makeMatchingEffPlots . . ." 
  # makeMatchingEffPlots("w",year)

  ## make data & MC efficiency plots
  # print   "running getMistag plots . . ." 
  # print   ":: "+obj+" "+mistrate+" "+year 
  # getMistag(obj, wp, year, mistrate)

  ## make SF plots
  # print   "running getSFSummarySources . . ." 
  # getSFSummarySources(year, obj, wp, path2file, mistrate,outdir)

  # make matching efficiency plots
  # print   "running makeMatchingEffPlots . . ." 
  # makeMatchingEffPlots("w",year)

  # make data & MC efficiency plots
  # print   "running getMistag plots . . ." 
  # print   ":: "+obj+" "+mistrate+" "+year 
  # getMistag(obj, wp, year, mistrate)

  # make SF plots
  # print   "running getSFSummarySources . . ." 
  # getSFSummarySources(obj, wp, path2file, mistrate)

###############################################################/

def makeDataMCPlotsFromCombine(path2file, filename, score, ptrange, category, xmin, xmax, nbins, xaxisname, log, outdir):
  ROOT.gROOT.SetBatch(True)
  ROOT.gROOT.LoadMacro("setTDRStyle.h")
  ROOT.gStyle.SetOptStat(0)
  ROOT.gStyle.SetOptFit(0)
  ROOT.gStyle.SetOptTitle(0)
  ROOT.gStyle.SetPalette(1)
  ROOT.TH1.SetDefaultSumw2()
  if xaxisname == "mass": xaxisname = "m(jet) [GeV]"
  fdiag = ROOT.TFile.Open(path2file+"/fitDiagnostics_"+filename+".root", "READONLY")

  # get prefit histograms
  prefitstr = "shapes_prefit"
  h_prefit_catp3_ = fdiag.Get(prefitstr+"/"+category+"/catp3"); h_prefit_catp3_.SetName("h_catp3_")
  h_prefit_catp2_ = fdiag.Get(prefitstr+"/"+category+"/catp2"); h_prefit_catp2_.SetName("h_catp2_")
  h_prefit_catp1_ = fdiag.Get(prefitstr+"/"+category+"/catp1"); h_prefit_catp1_.SetName("h_catp1_")
  h_prefit_total_ = fdiag.Get(prefitstr+"/"+category+"/total"); h_prefit_total_.SetName("h_total_")
  h_prefit_catp3 = rescaleXaxis(h_prefit_catp3_,xmin,xmax); h_prefit_catp3.SetName("h_catp3")
  h_prefit_catp2 = rescaleXaxis(h_prefit_catp2_,xmin,xmax); h_prefit_catp2.SetName("h_catp2")
  h_prefit_catp1 = rescaleXaxis(h_prefit_catp1_,xmin,xmax); h_prefit_catp1.SetName("h_catp1")
  h_prefit_total = rescaleXaxis(h_prefit_total_,xmin,xmax); h_prefit_total.SetName("h_total")
  
  # get postfit histograms
  tree = fdiag.Get("tree_fit_sb")
  h_fit_status = ROOT.TH1F("h_fit_status_","h_fit_status_",20,-10.,10.) 
  tree.Project("h_fit_status_","fit_status")
  postfitstr = "shapes_fit_s" 
  if h_fit_status.GetMean()<0.: postfitstr = "shapes_prefit"
  h_postfit_catp3_ = fdiag.Get(postfitstr+"/"+category+"/catp3"); h_postfit_catp3_.SetName("h_catp3_")
  h_postfit_catp2_ = fdiag.Get(postfitstr+"/"+category+"/catp2"); h_postfit_catp2_.SetName("h_catp2_")
  h_postfit_catp1_ = fdiag.Get(postfitstr+"/"+category+"/catp1"); h_postfit_catp1_.SetName("h_catp1_")
  h_postfit_total_ = fdiag.Get(postfitstr+"/"+category+"/total"); h_postfit_total_.SetName("h_total_")
  h_postfit_catp3 = rescaleXaxis(h_postfit_catp3_,xmin,xmax); h_postfit_catp3.SetName("h_catp3")
  h_postfit_catp2 = rescaleXaxis(h_postfit_catp2_,xmin,xmax); h_postfit_catp2.SetName("h_catp2")
  h_postfit_catp1 = rescaleXaxis(h_postfit_catp1_,xmin,xmax); h_postfit_catp1.SetName("h_catp1")
  h_postfit_total = rescaleXaxis(h_postfit_total_,xmin,xmax); h_postfit_total.SetName("h_total")
  
  # get data
  h_data = fdiag.Get("shapes_prefit/"+category+"/data"); h_data.SetName("h_data_")
  rescaleXaxisAsym(h_data, xmin, (xmax-xmin)/float(nbins)) 
  
  # cosmetics
  h_prefit_catp3.SetLineColor(4)            ; h_prefit_catp3.SetLineStyle(2);  h_prefit_catp3.SetLineWidth(3);  h_prefit_catp3.SetMarkerSize(0)
  h_prefit_catp2.SetLineColor(633)          ; h_prefit_catp2.SetLineStyle(2);  h_prefit_catp2.SetLineWidth(3);  h_prefit_catp2.SetMarkerSize(0)
  h_prefit_catp1.SetLineColor(415)          ; h_prefit_catp1.SetLineStyle(2);  h_prefit_catp1.SetLineWidth(3);  h_prefit_catp1.SetMarkerSize(0)
  h_prefit_total.SetLineColor(ROOT.kBlue+2) ; h_prefit_total.SetLineStyle(2);  h_prefit_total.SetLineWidth(3);  h_prefit_total.SetMarkerSize(0)
  
  h_postfit_catp3.SetLineColor(4)           ; h_postfit_catp3.SetLineStyle(1); h_postfit_catp3.SetLineWidth(4); h_postfit_catp3.SetMarkerSize(0)
  h_postfit_catp2.SetLineColor(633)         ; h_postfit_catp2.SetLineStyle(1); h_postfit_catp2.SetLineWidth(4); h_postfit_catp2.SetMarkerSize(0)
  h_postfit_catp1.SetLineColor(415)         ; h_postfit_catp1.SetLineStyle(1); h_postfit_catp1.SetLineWidth(4); h_postfit_catp1.SetMarkerSize(0)
  h_postfit_total.SetLineColor(ROOT.kBlue+2); h_postfit_total.SetLineStyle(1); h_postfit_total.SetLineWidth(4); h_postfit_total.SetMarkerSize(0)
  
  h_data.SetLineColor(1)
  h_data.SetLineWidth(3)
  h_data.SetMarkerColor(1)
  h_data.SetMarkerStyle(20)
  h_data.SetMarkerSize(1.2) 
  
  #TGraphAsymmErrors *h_r_prefit = h_data.Clone("h_r_prefit") h_r_prefit.Divide(h_data,h_prefit_total)
  h_r_prefit = getDataMCratio(h_data,h_prefit_total)
  h_r_prefit.SetName("h_r_prefit_")
  h_r_prefit.SetMarkerSize(0) 
  h_r_prefit.SetLineColor(ROOT.kMagenta)
  h_r_prefit.SetLineStyle(2)
  
  h_r_postfit = getDataMCratio(h_data,h_postfit_total) 
  h_r_postfit.SetName("h_r_postfit_")
  h_r_postfit.SetMarkerColor(1)
  h_r_postfit.SetLineColor(1)
  
  leg = ROOT.TLegend(0.60,0.55,0.94,0.86)
  leg.SetFillStyle(0)
  leg.SetFillColor(0)
  leg.SetLineWidth(0)
  leg.AddEntry(h_postfit_catp3,"top matched","L")
  leg.AddEntry(h_postfit_catp2,"W matched","L")
  leg.AddEntry(h_postfit_catp1,"unmatched","L")
  leg.AddEntry(h_postfit_total,"Total SM","L")
  leg.AddEntry(h_data,"Data","P")
  
  legfit = ROOT.TLegend(0.4,0.7,0.65,0.86)
  legfit.SetFillStyle(0)
  legfit.SetFillColor(0)
  legfit.SetLineWidth(0)
  legfit.AddEntry(h_prefit_total,"Pre-fit","L")
  legfit.AddEntry(h_postfit_total,"Post-fit","L")
  
  legfitr = ROOT.TLegend(0.35,0.80,0.55,0.93)
  legfitr.SetFillStyle(0)
  legfitr.SetFillColor(0)
  legfitr.SetLineWidth(0)
  legfitr.AddEntry(h_r_prefit,"Pre-fit","L")
  legfitr.AddEntry(h_r_postfit,"Post-fit","L")

  logstr = "lin" 
  if log: logstr = "log"
  c = ROOT.TCanvas("c_"+category+"_"+score+"_"+ptrange+"_"+logstr,"c_"+category+"_"+score+"_"+ptrange+"_"+logstr,600,600) 
  c.SetName("c_"+category+"_"+score+"_"+ptrange+"_"+logstr)
  
  pt_cms = ROOT.TPaveText(0.11,0.77,0.4,0.9,"NDC")
  pt_cms.SetFillStyle(0)
  pt_cms.SetFillColor(0)
  pt_cms.SetLineWidth(0)
  pt_cms.AddText("CMS")
  pt_cms.SetTextSize(0.08)

  pt_preliminary = ROOT.TPaveText(0.2,0.63,0.4,0.9,"NDC")
  pt_preliminary.SetFillStyle(0)
  pt_preliminary.SetFillColor(0)
  pt_preliminary.SetLineWidth(0)
  pt_preliminary.AddText("Preliminary")
  pt_preliminary.SetTextFont(52)
  pt_preliminary.SetTextSize(0.06)

  pt_info = ROOT.TPaveText(0.2,0.52,0.4,0.9,"NDC")
  pt_info.SetFillStyle(0)
  pt_info.SetFillColor(0)
  pt_info.SetLineWidth(0)
  pt_info.AddText(category +" | "+ filename.split("_")[2])
  pt_info.SetTextFont(42)
  pt_info.SetTextSize(0.05)

  pt_info2 = ROOT.TPaveText(0.29,0.39,0.4,0.9,"NDC")
  pt_info2.SetFillStyle(0)
  pt_info2.SetFillColor(0)
  pt_info2.SetLineWidth(0)
  if filename.split("_")[2]=="sdtau21":  pt_info2.AddText(ptrange +" p_{T}")
  else:                                  pt_info2.AddText(ptrange +" p_{T} | "+ filename.split("_")[5].replace("p",".") +" mistrate")
  pt_info2.SetTextFont(42)
  pt_info2.SetTextSize(0.05)
  
  pt_lumi=ROOT.TLatex()
  lumi={"2016":"35.9", "2017":"41.5", "2018":"59.7"}  
  pt_lumi.SetTextSize(0.07)
  pt_lumi.SetTextFont(42)

  pt_info=ROOT.TLatex()
  pt_info.SetTextSize(0.05)
  pt_info.SetTextFont(42)
  
  pMain = ROOT.TPad("pMain_"+category+"_"+score+"_"+ptrange+"_"+logstr,"pMain+"+category+"_"+score+"_"+ptrange+"_"+logstr,0.0,0.35,1.0,1.0)
  pMain.SetRightMargin(0.05)
  pMain.SetLeftMargin(0.17)
  pMain.SetBottomMargin(0.02)
  pMain.SetTopMargin(0.1)
  
  pRatio = ROOT.TPad("pRatio_"+category+"_"+score+"_"+ptrange+"_"+logstr,"pRatio_"+category+"_"+score+"_"+ptrange+"_"+logstr,0.0,0.0,1.0,0.35)
  pRatio.SetRightMargin(0.05)
  pRatio.SetLeftMargin(0.17)
  pRatio.SetTopMargin(0.02)
  pRatio.SetBottomMargin(0.4)
  pMain.Draw()
  pRatio.Draw()
  
  pMain.cd()
  pMain.SetTicks()
  maxyld = h_postfit_total.GetMaximum() 
  if h_prefit_total.GetMaximum()>h_postfit_total.GetMaximum(): maxyld = h_prefit_total.GetMaximum()
  if log: ROOT.gPad.SetLogy(); h_prefit_total.GetYaxis().SetRangeUser(0.1,10.*maxyld) 
  else: h_prefit_total.GetYaxis().SetRangeUser(0.,1.8*maxyld)
  h_prefit_total.GetXaxis().SetLabelSize(0.)
  h_prefit_total.GetYaxis().SetTitle("Events / bin")
  h_prefit_total.GetXaxis().SetTitle(xaxisname)
  h_prefit_total.Draw("HIST E0")
  h_prefit_catp3.Draw("HIST E0 sames")
  h_prefit_catp2.Draw("HIST E0 sames")
  h_prefit_catp1.Draw("HIST E0 sames")
  h_postfit_catp3.Draw("HIST E0 sames")
  h_postfit_catp2.Draw("HIST E0 sames")
  h_postfit_catp1.Draw("HIST E0 sames")
  h_postfit_total.Draw("HIST E0 sames")
  h_data.Draw("P sames")
  leg.Draw("sames")
  pt_cms.Draw("sames")
  pt_preliminary.Draw("sames")
  # pt_info.Draw("sames")
  # pt_info2.Draw("sames")
  pt_lumi.DrawLatexNDC(0.64,0.93,lumi[filename.split("_")[0]]+" fb^{-1} (13 TeV)")
  if filename.split("_")[2]=="sdtau21": pt_info.DrawLatexNDC(0.17,0.93,category +" | "+ filename.split("_")[2] + " | " + ptrange +" p_{T}")
  else: pt_info.DrawLatexNDC(0.17,0.93,category +" | "+ filename.split("_")[2] + " | " + ptrange +" p_{T} | "+ filename.split("_")[5].replace("p","."))
  c.RedrawAxis()
  
  pRatio.cd()
  pRatio.SetTicks()
  ROOT.gPad.SetBottomMargin(0.2)
  h_r_postfit.GetYaxis().SetTitleOffset(0.75)
  h_r_postfit.GetYaxis().SetTitleSize(0.1)
  h_r_postfit.GetYaxis().SetLabelSize(0.08)
  h_r_postfit.GetXaxis().SetTitleSize(0.1)
  h_r_postfit.GetXaxis().SetLabelSize(0.08)
  h_r_postfit.GetXaxis().SetTitle(xaxisname)
  h_r_postfit.GetYaxis().SetTitle("Data / Post-fit")
  h_r_postfit.GetYaxis().SetRangeUser(0.01,1.99)
  h_r_postfit.Draw("P E0")
  # h_r_prefit.Draw("HIST sames")
  c.RedrawAxis()
  
  if filename.split("_")[2]=="sdtau21": filename=filename.replace("_5p0","")
  c.Print(outdir+"/"+category+"/"+filename.replace("W_","")+"_"+category+"_"+logstr+".pdf")
  c.Print(outdir+"/"+category+"/"+filename.replace("W_","")+"_"+category+"_"+logstr+".png")
  #c.Delete()

def rescaleXaxis(inputhisto, xmin, xmax):
  ROOT.TH1.SetDefaultSumw2()

  nbins = inputhisto.GetNbinsX()
  name = inputhisto.GetName()
  outputhisto = ROOT.TH1F(name,name,nbins,xmin,xmax)

  for i0 in range(0,nbins):
    outputhisto.SetBinContent(i0+1,inputhisto.GetBinContent(i0+1))
    outputhisto.SetBinError(i0+1,inputhisto.GetBinError(i0+1))

  return outputhisto

def rescaleXaxisAsym(g, xmin, scaleX):
  ROOT.TH1.SetDefaultSumw2()

  N=g.GetN()
  x=g.GetX()
  xerrh=g.GetEXhigh()
  xerrl=g.GetEXlow()
  for i in range(0,N):
	x[i]=xmin+x[i]*scaleX
	xerrh[i]=0.
	xerrl[i]=0.

  g.GetHistogram().Delete()
  g.SetHistogram(0)

def getDataMCratio(indata, inMC):
  ROOT.TH1.SetDefaultSumw2()

  h_data = inMC.Clone("h_data"); h_data.SetName("h_data")
  for i0 in range(0,inMC.GetNbinsX()):
    h_data.SetBinContent(i0+1, indata.GetY()[i0])
    h_data.SetBinError(i0+1, (indata.GetEYlow()[i0]+indata.GetEYhigh()[i0])/2.)

  h_ratio = h_data.Clone("h_ratio")
  h_ratio.Divide(h_data,inMC)
  h_ratio.SetMarkerStyle(20); h_ratio.SetMarkerSize(1)
  h_ratio.SetLineWidth(2); h_ratio.SetLineStyle(1)

  return h_ratio

def getSFSummarySources(year, obj, wp, path2file, mistrates, outdir):
  ROOT.gROOT.SetBatch(1)
  ROOT.gROOT.LoadMacro("setTDRStyle.h")
  ROOT.gStyle.SetOptStat(0)
  ROOT.gStyle.SetOptFit(1)
  ROOT.gStyle.SetPalette(1)
  ROOT.TH1.SetDefaultSumw2()

  algos,legnames,ptrange,colors,markers=[],[],[],[],[]
  
  if obj=="W":
    algos.append("sdtau21"); colors.append(800); markers.append(24)
    algos.append("deepak8"); colors.append(866); markers.append(25)
    # legnames.append("m_{SD}+#tau_{21}")
    # legnames.append("DeepAK8 0p1")     
    # # algos.append("deepak8md")   legnames.append("DeepAK8-MD")         colors.append(616)
    
    ptrange.append("low")
    # ptrange.append("lowmed")
    # ptrange.append("med")
    ptrange.append("lowmed")
    ptrange.append("med")

  if obj=="W": names = ["200-300", "300-400", "400-800"]; nbins = len(names); xmax = float(len(names))
  h_dummy = ROOT.TH1F("h_dummy","",nbins,0.,xmax)
  for i1 in range(0,h_dummy.GetNbinsX()): h_dummy.GetXaxis().SetBinLabel(i1+1,names[i1])

  gr_sf=[]; gr_sf_stat=[]
  for ialgo,algo in enumerate(algos):
    for imr,mistrate in enumerate(mistrates):
      nmr="_"+mistrate
      if algo=="sdtau21":
        if not mistrate=="0p1": continue
        else: nmr=""
      print "getting SF for %s %s . . ." %(algo,nmr.replace("_",""))

      gr_tot  = getSFGraph(year,obj,algo,wp,ptrange,ialgo+imr,len(algos)*len(mistrates),colors[ialgo]+imr*10,mistrate,path2file); gr_tot.SetName("gr_tot_"+algo+nmr)
      # gr_stat = getSFGraphSyst(obj,algo,wp,ptrange,ialgo,len(algos),colors[ialgo],"stat",gr_tot,mistrate,path2file); gr_stat.SetName("gr_stat_"+algo)

      gr_tot.SetFillColor(colors[ialgo]+imr*10); gr_tot.SetFillStyle(3002); gr_tot.SetLineColor(colors[ialgo]+imr*10); gr_tot.SetMarkerStyle(markers[ialgo]+imr)
      # gr_stat.SetLineWidth(1); gr_stat.SetLineColor(colors[ialgo]); gr_stat.SetFillColor(0); gr_stat.SetFillStyle(0); gr_stat.SetMarkerSize(1)

      if algo=="sdtau21": legnames.append("m_{SD}+#tau_{21}")
      else: legnames.append(algo+nmr.replace("_"," "))

      gr_sf.append(gr_tot)
      # gr_sf_stat.append(gr_stat)

  print "end looping over files"
  legy=.85
  leg = ROOT.TLegend(.70,legy-(0.05*len(legnames)),.85,legy)
  leg.SetFillStyle(0)
  leg.SetFillColor(0)
  leg.SetLineWidth(1)
  leg.SetBorderSize(0)
  leg.SetTextFont(43)
  leg.SetTextSize(17)
  # leg.SetHeader("Taggers")

  c_sf = ROOT.TCanvas("c_sf","c_sf",800,800)
  ROOT.gPad.SetLeftMargin(0.11)
  ROOT.gPad.SetRightMargin(0.06)
  c_sf.SetTicks()

  h_dummy.GetYaxis().SetRangeUser(0.2,2)
  h_dummy.GetYaxis().SetTitleOffset(1.3)
  h_dummy.GetYaxis().SetTitle("#epsilon_{DATA} / #epsilon_{MC}")
  h_dummy.GetXaxis().SetTitleOffset(1.2)
  h_dummy.GetXaxis().SetTitle("p_{T} (jet) [GeV]")

  h_dummy.Draw("HIST")

  latex2 = ROOT.TLatex()
  latex2.SetNDC()
  latex2.SetTextSize(0.35*c_sf.GetTopMargin())
  latex2.SetTextFont(42)
  latex2.SetTextAlign(31) # align right
  lumi={"2016":"35.9", "2017":"41.5", "2018":"59.7"}  
  latex2.DrawLatex(0.94, 0.92,lumi[year]+" fb^{-1} (13 TeV)")
  latex2.SetTextAlign(11) # align left                                                                                                         
  latex2.DrawLatex(0.11, 0.92, "single-#mu | W Tagging")
  
  latex2.SetTextSize(0.5*c_sf.GetTopMargin())
  latex2.SetTextFont(62)
  latex2.SetTextAlign(11) # align right                                                                                             
  latex2.DrawLatex(0.15, 0.83, "CMS")

  latex2.SetTextSize(0.4*c_sf.GetTopMargin())
  latex2.SetTextFont(52)
  latex2.SetTextAlign(11)
  latex2.DrawLatex(0.15, 0.78, "Preliminary")
  ###
  # latex2.SetTextSize(0.33*c_sf.GetTopMargin())
  # latex2.DrawLatex(0.15, 0.73, "W boson tagging") 
  # latex2.DrawLatex(0.15, 0.68, "mistrate: "+mistrate) 

  for i0 in range(0,len(gr_sf)):
    gr_sf[i0].Draw("E2 sames")
    gr_sf[i0].Draw("P E1 sames")
    leg.AddEntry(gr_sf[i0],legnames[i0],"PL")
    
    # with stats #
    # gr_sf[i0]->Draw("E2 sames");
    # gr_sf_stat[i0]->Draw("P E1 sames");
    # leg.AddEntry(gr_sf_stat[i0],legnames[i0],"L")

  leg.Draw("sames")
  c_sf.Print(outdir+"/SF/sf_"+year+"_"+obj+"_"+wp+".pdf")
  c_sf.Print(outdir+"/SF/sf_"+year+"_"+obj+"_"+wp+".png")

def SetEx(gae, Ex):
  np = gae.GetN()
  for i in range(0,np):
    gae.SetPointEXhigh(i,Ex)
    gae.SetPointEXlow(i,Ex)

def getSFGraph(year, obj, algo, wp, ptrange, ialgo, nalgos, color, mistrate, path2file):
  
  xval,xvalerr,yval,yvalerrlo,yvalerrhi=array.array('d',[]),array.array('d',[]),array.array('d',[]),array.array('d',[]),array.array('d',[])
  mistrateN={"sdtau21":"","deepak8":"_"+mistrate}
  for iptrange in range(0,len(ptrange)):
    fdiag = ROOT.TFile.Open(path2file+"/fitDiagnostics_"+year+"_"+obj+"_"+algo+"_"+wp+"_"+ptrange[iptrange]+mistrateN[algo]+".root", "READONLY" )
    # TFile *fdiag = TFile::Open("./"+obj+"_"+algo+"_tot/"+mistrate+"/sf_fitDiagnostics_"+obj+"_"+algo+"_"+wp+"_"+ptrange[iptrange]+".root", "READONLY" )
    # TFile *fdiag = TFile::Open("./"+path2file+"/sf_fitDiagnostics_"+obj+"_"+algo+"_"+wp+"_"+ptrange[iptrange]+".root", "READONLY" )
    t_   = fdiag.Get("tree_fit_sb")
    if obj=="W": strCat = "SF_catp2"; strCatLoErr = "SF_catp2LoErr"; strCatHiErr = "SF_catp2HiErr"
    h_sf_cat      = ROOT.TH1F("h_sf_cat"      , "h_sf_cat"      , 10000,0.,10.)
    h_sf_catLoErr = ROOT.TH1F("h_sf_catLoErr" , "h_sf_catLoErr" , 10000,0.,10.)
    h_sf_catHiErr = ROOT.TH1F("h_sf_catHiErr" , "h_sf_catHiErr" , 10000,0.,10.)
    t_.Project("h_sf_cat",strCat)
    t_.Project("h_sf_catLoErr",strCatLoErr)
    t_.Project("h_sf_catHiErr",strCatHiErr)
    
    xval.append((iptrange+0.7) + 0.07*(ialgo - 1.*(nalgos-2)))
    xvalerr.append(0.03)
    yval.append(h_sf_cat.GetMean())
    yvalerrlo.append(h_sf_catLoErr.GetMean())
    yvalerrhi.append(h_sf_catHiErr.GetMean())
    #   if (algos[ialgo]=="sdtau21" && ptrange[iptrange]=="low") { yvalerrlo[iptrange] = 0.01 yvalerrhi[iptrange] = 0.01 }
    
    h_sf_cat.Delete()
    h_sf_catLoErr.Delete()
    h_sf_catHiErr.Delete()
  
  gr_sf_tmp = ROOT.TGraphAsymmErrors(len(ptrange),xval,yval,xvalerr,xvalerr,yvalerrlo,yvalerrhi) 
  gr_sf_tmp.SetLineColor(color)
  gr_sf_tmp.SetMarkerColor(color)
  return gr_sf_tmp

# def getSFGraphSyst(obj, algo, wp, ptrange, ialgo, nalgos, color, extra, gr_nom, mistrate, path2file):
  
#   xval,xvalerr,yval,yvalerrlo,yvalerrhi=array.array('d',[]),array.array('d',[]),array.array('d',[]),array.array('d',[]),array.array('d',[])
#   mistrateN={"sdtau21":"","deepak8":"_"+mistrate}
#   for iptrange in range(0,len(ptrange)): 
#     fdiag = ROOT.TFile.Open(path2file+"/ext/fitDiagnostics_"+obj+"_"+algo+"_"+wp+"_"+ptrange[iptrange]+mistrateN[algo]+".root", "READONLY" )
#     t_   = fdiag.Get("tree_fit_sb")
    
#     if (obj=="W"): strCat = "SF_catp2"; strCatLoErr = "SF_catp2LoErr"; strCatHiEr = "SF_catp2HiErr"
#     h_sf_cat      = ROOT.TH1F("h_sf_cat"      , "h_sf_cat"      , 10000,0.,10.)
#     h_sf_catLoErr = ROOT.TH1F("h_sf_catLoErr" , "h_sf_catLoErr" , 10000,0.,10.)
#     h_sf_catHiErr = ROOT.TH1F("h_sf_catHiErr" , "h_sf_catHiErr" , 10000,0.,10.)
#     t_.Project("h_sf_cat",strCat)
#     t_.Project("h_sf_catLoErr",strCatLoErr)
#     t_.Project("h_sf_catHiErr",strCatHiErr)
#     nom_x = 0; nom_y = 0; gr_nom.GetPoint(iptrange,nom_x,nom_y) 
#     xval[iptrange]    = (iptrange+0.7) + 0.07*(ialgo - 1.*(nalgos-2))
#     xvalerr[iptrange] = 0.
#     yval[iptrange]    = nom_y 
#     yvalerrlo_ = (h_sf_catLoErr.GetMean()/h_sf_cat.GetMean())*(nom_y); if (yvalerrlo_>gr_nom.GetErrorYlow(iptrange)) : yvalerrlo_ = gr_nom.GetErrorYlow(iptrange)
#     yvalerrhi_ = (h_sf_catHiErr.GetMean()/h_sf_cat.GetMean())*(nom_y); if (yvalerrhi_gr_nom.GetErrorYhigh(iptrange)) : yvalerrhi_ = gr_nom.GetErrorYhigh(iptrange) 
#     yvalerrlo[iptrange] = yvalerrlo_
#     yvalerrhi[iptrange] = yvalerrhi_
#     #   if (algos[ialgo]=="sdtau21" && ptrange[iptrange]=="low") { yvalerrlo[iptrange] = 0.01 yvalerrhi[iptrange] = 0.01 }
    
#     h_sf_cat.Delete()
#     h_sf_catLoErr.Delete()
#     h_sf_catHiErr.Delete()
    
#   # end looping over the pt bins
  
#   gr_sf_tmp = ROOT.TGraphAsymmErrors(ptrange.size(),xval,yval,xvalerr,xvalerr,yvalerrlo,yvalerrhi) 
#   gr_sf_tmp.SetLineColor(color)
#   gr_sf_tmp.SetMarkerColor(color)
#   return gr_sf_tmp

# def getdiscval(sigeff, algo, obj, cut="(0==0)"):

#   #TFile *f_sig = TFile::Open("/eos/uscms/store/user/lpcjme/LGOutputs/hrt_muon_20190225/qcd-mg_tree.root" , "READONLY" )
#   f_sig = ROOT.TFile.Open("/eos/uscms/store/group/lpcjme/noreplica/NanoHRT/Trees/Apr08/qcd/mc_nom/qcd-mg_tree.root" , "READONLY" )
#   t_sig = f_sig.Get("Events")

#   nbins = 4000
#   start = 1; end = nbins+1 
#   h_sig = ROOT.TH1F("h_sig_"+algo,"h_sig_"+algo,nbins,0.,1.)
  
#   if (algo=="sdtau21"):
#     cut_final = "(xsecWeight*puWeight)*("+cut+" && ak8_1_pt>500. && (!((ak8_1_dr_fj_top_wqmax<0.8) && (ak8_1_dr_fj_top_b<0.8))) && ((ak8_1_dr_fj_top_wqmax<0.8) && (ak8_1_dr_fj_top_b>0.8)) && (ak8_1_mass>0 && ak8_1_mass<1050000.) )"
#     t_sig.Project("h_sig_"+algo,"1-ak8_1_tau2/ak8_1_tau1",cut_final) 

#   if (algo=="deepak8"):
#     #    if (obj=="W") { cut_final = "(xsecWeight*puWeight)*("+cut+" && ak8_1_pt>200. && ((!((ak8_1_dr_fj_top_wqmax<0.8) && (ak8_1_dr_fj_top_b<0.8))) && ((ak8_1_dr_fj_top_wqmax<0.8) && (ak8_1_dr_fj_top_b>0.8))))" }
#     cut_final = "(xsecWeight*puWeight)*("+cut+" && ak8_1_pt>500. )"
#     t_sig.Project("h_sig_"+algo,"ak8_1_DeepAK8_"+obj+"vsQCD",cut_final) 

#   # if (algo=="deepak8md"):
#   #   cut_final = "(xsecWeight*puWeight)*("+cut+" && ak8_1_pt>500. && (!((ak8_1_dr_fj_top_wqmax<0.8) && (ak8_1_dr_fj_top_b<0.8))) && ((ak8_1_dr_fj_top_wqmax<0.8) && (ak8_1_dr_fj_top_b>0.8)))"
#   #   t_sig.Project("h_sig_"+algo,"ak8_1_DeepAK8MD_"+obj+"vsQCD",cut_final) 

#   ntot_sig = h_sig.Integral(0,nbins+1)
#   for i0 in range(start,end):
#     tmp_sig = h_sig.Integral(i0,nbins+1)
#     if (tmp_sig/ntot_sig)<sigeff and (tmp_sig/ntot_sig)>0.: 
#       print tmp_sig/ntot_sig+" "+h_sig.GetBinCenter(i0)+"\n" 
#       break

# def getTGraphAsymmErrorsFromHisto(TH1 *input):
#   TH1::SetDefaultSumw2(kTrue)

#   nbins = input.GetNbinsX()
#   double x[nbins], y[nbins], exl[nbins], exh[nbins], eyl[nbins], eyh[nbins]
#   for (unsigned i0=0 i0<nbins ++i0) {
#     x[i0] = input.GetBinCenter(i0+1) 
#     exl[i0] = 0.
#     exh[i0] = 0.
#     y[i0] = input.GetBinContent(i0+1)
#     eyl[i0] = input.GetBinError(i0+1)
#     eyh[i0] = input.GetBinError(i0+1)
#   }
#   TGraphAsymmErrors *gr = new TGraphAsymmErrors(nbins,x,y,exl,exh,eyl,eyh)

#   return gr

def getMistag(obj, wp, year, mistrate):
  ROOT.gROOT.SetBatch(True)
  ROOT.gROOT.LoadMacro("setTDRStyle.h")
  ROOT.gStyle.SetOptStat(0)
  ROOT.gStyle.SetOptFit(1)
  ROOT.gStyle.SetOptTitle(0)
  ROOT.gStyle.SetPalette(1)
  ROOT.TH1.SetDefaultSumw2()

  lumi_yr={"2016":"36.8","2017":"41.53","2018":"59.74"}
  lumi=lumi_yr[year]

  EOSCMS="root://eoscms.cern.ch/"
  path=EOSCMS+"/eos/cms/store/group/phys_jetmet/nbinnorj/WTopTagging/ntuples_HRTSF/"
  path_ext={"2016":"2016/","2017":"29July/","2018":"3Oct_For_Copy/"}

  path+=path_ext[year]
  f_mc   = ROOT.TFile.Open(path+"mc_nom/sm_tree.root" , "READONLY" ) 
  f_data = ROOT.TFile.Open(path+"data/singlemu_tree.root", "READONLY")

  t_mc   = f_mc.Get("Events")
  t_data = f_data.Get("Events")

  algos,legnames,ptrange,colors=[],[],[],[]
  algos.append("sdtau21") ;legnames.append("m_{SD}+#tau_{21}") ;colors.append(800)
  algos.append("deepak8") ;legnames.append("DeepAK8")          ;colors.append(866)

  # baseline selection
  # c_base = "(ht>1000 && n_ak8>=1 && n_ca15>=1)"
  # c_base = "(n_ak8>=1 && n_ca15>=1)"
  # c_base = "(n_ak8>=1 || n_ca15>=1)"
  c_base = "(n_ak8>=1)"
  cut_incl = c_base

  # xbins={200.0, 250.0, 350.0, 400.0, 500.0, 600.0, 800.0}
  bins = 20; xmin = 200.; xmax = 800.;

  getmed = median(algos)
  eff_mc,eff_data,sf=[],[],[]
  
  for ialgo,algo in enumerate(algos):
    
    rootfile=ROOT.TFile(EOSDIR+"mistag_"+year+"_"+algo+".root","RECREATE")
  
    if (algo == "sdtau21"): 
      c_jet = "ak8"   
      if (wp == "JMAR"): c_algo_wp = "((1-"+c_jet+"_1_tau2/"+c_jet+"_1_tau1)>0.6781)"
    
    if (algo == "deepak8"): 
      c_jet = "ak8"   
      if (wp == "JMAR"): c_algo_wp = "("+c_jet+"_1_DeepAK8_"+obj+"vsQCD>0.9383)" 

    c_mass = "("+c_jet+"_1_mass>65. && "+c_jet+"_1_mass<105.)"
    #c_mass = "("+c_jet+"_1_mass>0.)"

    xmin = xmin - (2.*(getmed)) + (2.*ialgo)
    xmax = xmax - (2.*(getmed)) + (2.*ialgo)

    h_den_mc = create1Dhisto("sample",t_mc,lumi,cut_incl,c_jet+"_1_pt",bins,xmin,xmax,False,1,1,"h_den_mc_"+algo,False,False); h_den_mc.SetFillColor(0)  
    h_num_mc = create1Dhisto("sample",t_mc,lumi,cut_incl+" && "+c_algo_wp+" && "+c_mass,c_jet+"_1_pt",bins,xmin,xmax,False,colors[ialgo],1,"h_num_mc_"+algo,False,False) 
    
    h_mc_r    = h_num_mc.Clone("h_mc_r_"+algo) 
    h_mc_r.Divide(h_num_mc,h_den_mc,1.,1.,"B")
    h_mc_r.Write("MC")

    h_den_data = create1Dhisto("sample",t_data,lumi,cut_incl,c_jet+"_1_pt",bins,xmin,xmax,False,1,1,"h_den_data_"+algo,False,True); h_den_data.SetFillColor(0)
    h_num_data = create1Dhisto("sample",t_data,lumi,cut_incl+" && "+c_algo_wp+" && "+c_mass,c_jet+"_1_pt",bins,xmin,xmax,False,colors[ialgo],1,"h_num_data_"+algo,False,True)
    
    h_data_r = h_num_data.Clone("h_data_r_"+algo) 
    h_data_r.Divide(h_num_data,h_den_data,1.,1.,"B")
    h_data_r.Write("Data")

    h_sf = h_mc_r.Clone("h_sf_"+algo) 
    h_sf.Divide(h_mc_r,h_data_r)
    h_sf.SetLineColor(colors[ialgo]); h_sf.SetFillColor(0); h_sf.SetMarkerColor(colors[ialgo]); h_sf.SetMarkerSize(1.)
    h_sf.Write("SF")

    eff_mc.append(h_mc_r)
    eff_data.append(h_data_r)
    sf.append(h_sf)
    print sf
    
  # end of looping over the algos

  leg = ROOT.TLegend(0.75,0.66,0.92,0.89)
  leg.SetFillStyle(0)
  leg.SetFillColor(0)
  leg.SetLineWidth(0)

  pt_cms = ROOT.TPaveText(0.10,0.77,0.4,0.9,"NDC")
  pt_cms.SetFillStyle(0)
  pt_cms.SetFillColor(0)
  pt_cms.SetLineWidth(0)
  pt_cms.AddText("CMS")
  pt_cms.SetTextSize(0.08)

  pt_preliminary = ROOT.TPaveText(0.18,0.63,0.4,0.9,"NDC")
  pt_preliminary.SetFillStyle(0)
  pt_preliminary.SetFillColor(0)
  pt_preliminary.SetLineWidth(0)
  pt_preliminary.AddText("Preliminary")
  pt_preliminary.SetTextFont(52)
  pt_preliminary.SetTextSize(0.06)
  
  pt_lumi = ROOT.TPaveText(0.8,0.9,0.9,1.0,"NDC")
  pt_lumi.SetFillStyle(0)
  pt_lumi.SetFillColor(0)
  pt_lumi.SetLineWidth(0)
  pt_lumi.AddText(lumi+" fb^{-1} (13 TeV)")
  pt_lumi.SetTextFont(52)
  pt_lumi.SetTextSize(0.06)

  # TLatex pt_lumi
  # const char *longstring = ""
  # if (year == "2016") {longstring ="36.8 fb^{-1} (13 TeV)"}
  # else if (year == "2017") {longstring ="41.53 fb^{-1} (13 TeV)"}
  # else if (year == "2018") {longstring ="59.74 fb^{-1} (13 TeV)"}
  # pt_lumi.SetTextSize(0.07)
  # pt_lumi.SetTextFont(42)

  c_sf = ROOT.TCanvas("c_sf","c_sf",700,500)
  ROOT.gStyle.SetErrorX(0.)
  ROOT.gPad.SetLeftMargin(0.1)
  ROOT.gPad.SetBottomMargin(0.13)
  ROOT.gPad.SetTopMargin(1.02)
  print sf
  sf[getmed].GetYaxis().SetRangeUser(0.5,2.)
  sf[getmed].GetYaxis().SetTitleOffset(0.8)
  sf[getmed].GetYaxis().SetTitle("#epsilon_{DATA} / #epsilon_{MC}")
  sf[getmed].GetXaxis().SetLabelSize(0.06)
  sf[getmed].GetXaxis().SetTitle("p_{T} (jet) [GeV]")
  sf[getmed].Draw("P E0")
  for i0 in range(0,len(sf)):
    leg.AddEntry(sf[i0],legnames[i0],"PL") 
    if not i0==getmed: sf[i0].Draw("P E0 sames")
  leg.Draw("sames")
  pt_cms.Draw("sames")
  pt_preliminary.Draw("sames")
  pt_lumi.Draw("sames")
  # pt_lumi.DrawLatexNDC(0.58,0.93,longstring)
  c_sf.Print(PLTDIR+"/sf_"+year+".png")
  
  leg.Clear()
  c_mistag = ROOT.TCanvas("c_mistag","c_mistag", 1200, 1200)
  c_mistag.Divide(1,2)

  c_mistag.cd(1)
  for i0 in range(0,len(eff_mc)):
    if (i0==0): 
      eff_mc[i0].GetYaxis().SetRangeUser(0.0,1.0)
      eff_mc[i0].GetYaxis().SetTitleOffset(0.8)
      eff_mc[i0].GetYaxis().SetTitle("#epsilon_{MC}")
      eff_mc[i0].GetXaxis().SetLabelSize(0.06)
      eff_mc[i0].GetXaxis().SetTitle("p_{T} (jet) [GeV]")
      eff_mc[i0].Draw("P E0")
    else: 
      eff_mc[i0].Draw("P E0 sames")
    
    leg.AddEntry(eff_mc[i0],legnames[i0],"LP")

  leg.Draw("sames")
  pt_cms.Draw("sames")
  pt_preliminary.Draw("sames")
  pt_lumi.Draw("sames")
  # pt_lumi.DrawLatexNDC(0.58,1.0,longstring)
  leg.Clear()

  c_mistag.cd(2)
  for i0 in range(0,len(eff_data)):
    if (i0==0):  
      eff_data[i0].GetYaxis().SetRangeUser(0.0,1.0)
      eff_data[i0].GetYaxis().SetTitleOffset(0.8)
      eff_data[i0].GetYaxis().SetTitle("#epsilon_{Data}")
      eff_data[i0].GetXaxis().SetLabelSize(0.06)
      eff_data[i0].GetXaxis().SetTitle("p_{T} (jet) [GeV]")
      eff_data[i0].Draw("P E0")
    else:    
      eff_data[i0].Draw("P E0 sames")
    leg.AddEntry(eff_data[i0],legnames[i0],"LP")
  
  leg.Draw("sames")
  pt_cms.Draw("sames")
  pt_preliminary.Draw("sames")
  pt_lumi.Draw("sames")
  # pt_lumi.DrawLatexNDC(0.58,1.0,longstring)

  # c_mistag.Print(EOSDIR+"mistag_"+year+"_"+mistrate+".pdf")
  c_mistag.Print(PLTDIR+"/mistag_"+year+"_"+mistrate+".png")

# def getMisTagRates(sample, obj, wp):
#   # sample: photon qcd  
#   setTDRStyle()
#   gROOT.SetBatch(False)
#   gStyle.SetOptStat(0)
#   gStyle.SetOptFit(1)
#   gStyle.SetPalette(1)
#   TH1::SetDefaultSumw2(kTrue)

#   intLumi     = 36.8
#   ostringstream tmpLumi
#   tmpLumi   intLumi
#   lumi = tmpLumi.str()


#   TFile *f_mc TFile *f_mc_b TFile *f_data
#   if (sample == "photon") {
#     path = "/eos/uscms/store/group/lpcjme/noreplica/NanoHRT/Trees/Apr08/"+sample+"/"
#     f_mc = TFile::Open(path+"/mc_nom/sm.root" , "READONLY" )
#     #f_mc = TFile::Open(path+"/mc_nom/photon_tree.root" , "READONLY" )
#     f_mc_b = TFile::Open(path+"/mc_nom/sm.root" , "READONLY" )
#     f_data = TFile::Open(path+"/data/singlephoton_tree.root" , "READONLY" )
#   }

#   if (sample == "qcd") {
#     path = "/eos/uscms/store/group/lpcjme/noreplica/NanoHRT/Trees/Apr08/"+sample+"/"
#     #f_mc = TFile::Open(path+"/mc_nom/qcd-mg_tree.root" , "READONLY" )
#     f_mc = TFile::Open(path+"/mc_nom/qcd-herwig_tree.root" , "READONLY" )
#     f_mc_b = TFile::Open(path+"/mc_nom/sm_noqcd.root" , "READONLY" )
#     f_data = TFile::Open(path+"/data/jetht_tree.root" , "READONLY" )
#   }
#   TTree *t_mc   = (TTree*)f_mc.Get("Events")
#   TTree *t_mc_b = (TTree*)f_mc_b.Get("Events")
#   TTree *t_data = (TTree*)f_data.Get("Events")

#   std::vector<TString> algos    algos.clear()
#   std::vector<TString> algo     algos.clear()
#   std::vector<TString> legnames legnames.clear()
#   std::vector<TString> ptrange  ptrange.clear()
#   std::vector<int>     colors   colors.clear()
  
#   if (obj=="T") {
#     algos.append("sdtau32")     legnames.append("m_{SD}+#tau_{32}")       colors.append(800)
#     algos.append("sdtau32btag") legnames.append("m_{SD}+#tau_{32}+b-tag") colors.append(632)
#     #algos.append("hotvr")       legnames.append("HOTVR")                  colors.append(812)
#     algos.append("ecftoptag")   legnames.append("CA15-ECF")               colors.append(419)
#     algos.append("best")        legnames.append("BEST")                   colors.append(882)
#     algos.append("imagetop")    legnames.append("ImageTop")               colors.append(603)
#     algos.append("imagetopmd")  legnames.append("ImageTop-MD")            colors.append(600)
#     algos.append("deepak8")     legnames.append("DeepAK8")                colors.append(866)
#     algos.append("deepak8md")   legnames.append("DeepAK8-MD")             colors.append(616)
#   }

#   if (obj=="W") {
#     algos.append("sdtau21")     legnames.append("m_{SD}+#tau_{21}")   colors.append(800)
#     algos.append("sdn2")        legnames.append("m_{SD}+N_{2}")       colors.append(408)
#     algos.append("sdn2ddt")     legnames.append("m_{SD}+N_{2}^{DDT}") colors.append(419)
#     algos.append("best")        legnames.append("BEST")               colors.append(882)
#     algos.append("deepak8")     legnames.append("DeepAK8")            colors.append(866)
#     algos.append("deepak8md")   legnames.append("DeepAK8-MD")         colors.append(616)
#   }

#   # baseline selection
#   c_base
#   if (sample == "photon") { c_base = "(passPhoton165_HE10 && n_ak8>=1 && n_ca15>=1 && nphotons>=1 && pho_1_pt>200.)" }
#   if (sample == "qcd")    { c_base = "(ht>1000 && n_ak8>=1 && n_ca15>=1)" }
#   cut_incl = c_base
  
#   bins xmin, xmax
#   if (sample == "photon") {
#     if (obj=="T") { bins = 7 xmin = 300. xmax = 1000. }
#     if (obj=="W") { bins = 8 xmin = 200. xmax = 1000. }
#   }
#   if (sample == "qcd")    { 
#     if (obj=="T") { bins = 12 xmin = 300. xmax = 1500. }
#     if (obj=="W") { bins = 13 xmin = 200. xmax = 1500. }
#   }

#   getmed = median(algos)
#   std::vector<TH1D*> eff_mc eff_mc.clear()
#   std::vector<TH1D*> eff_data eff_data.clear()
#   std::vector<TH1D*> sf sf.clear()
#   for (unsigned ialgo=0 ialgo<len(algos) ++ialgo) {
#     c_algo_wp, c_jet
#     if (algos[ialgo] == "sdtau32")     { c_jet = "ak8"   if (wp == "JMAR") { c_algo_wp = "((1-"+c_jet+"_1_tau3/"+c_jet+"_1_tau2)>0.4909)" } }
#     if (algos[ialgo] == "sdtau32btag") { c_jet = "ak8"   if (wp == "JMAR") { c_algo_wp = "((1-"+c_jet+"_1_tau3/"+c_jet+"_1_tau2)>0.3881 && max("+c_jet+"_1_sj1_btagCSVV2,"+c_jet+"_1_sj2_btagCSVV2)>0.5426)" } }
#     if (algos[ialgo] == "ecftoptag")   { c_jet = "ca15"  if (wp == "JMAR") { c_algo_wp = "( "+c_jet+"_1_ecfTopTagBDT>-1. && (0.5+0.5*"+c_jet+"_1_ecfTopTagBDT)>0.7831)" } }
#     if (algos[ialgo] == "sdtau21")     { c_jet = "ak8"   if (wp == "JMAR") { c_algo_wp = "((1-"+c_jet+"_1_tau2/"+c_jet+"_1_tau1)>0.6781)" } }
#     if (algos[ialgo] == "sdn2")        { c_jet = "ak8"   if (wp == "JMAR") { c_algo_wp = "((1-"+c_jet+"_1_n2b1)>0.7643)" } }
#     if (algos[ialgo] == "sdn2ddt")     { c_jet = "ak8"   if (wp == "JMAR") { c_algo_wp = "((0.5-0.5*"+c_jet+"_1_n2b1ddt)>0.4891)" } }
#     if (algos[ialgo] == "hotvr")       { c_jet = "hotvr" if (wp == "JMAR") { c_algo_wp = "( && hotvr_1_fpt<0.8 && hotvr_1_nsubjets>=3 && hotvr_1_mmin>=50. && (1-hotvr_1_tau32)>0.4504)" } }
#     if (algos[ialgo] == "best")        { c_jet = "ak8"   
#       if (wp == "JMAR" && obj=="T") { c_algo_wp = "("+c_jet+"_1_best_"+(TString)obj+"vsQCD>0.8563)" } 
#       if (wp == "JMAR" && obj=="W") { c_algo_wp = "("+c_jet+"_1_best_"+(TString)obj+"vsQCD>0.9001)" }
#     }
#     if (algos[ialgo] == "imagetop")    { c_jet = "ak8"   if (wp == "JMAR") { c_algo_wp = "("+c_jet+"_1_image_top>0.8021)" } }
#     if (algos[ialgo] == "imagetopmd")  { c_jet = "ak8"   if (wp == "JMAR") { c_algo_wp = "("+c_jet+"_1_image_top>0.7485)" } }
#     if (algos[ialgo] == "deepak8")     { c_jet = "ak8" 
#       if (wp == "JMAR" && obj=="T") { c_algo_wp = "("+c_jet+"_1_DeepAK8_"+(TString)obj+"vsQCD>0.8537)" } 
#       if (wp == "JMAR" && obj=="W") { c_algo_wp = "("+c_jet+"_1_DeepAK8_"+(TString)obj+"vsQCD>0.9383)" }
#     }
#     if (algos[ialgo] == "deepak8md")   { c_jet = "ak8"
#       if (wp == "JMAR" && obj=="T") { c_algo_wp = "("+c_jet+"_1_DeepAK8MD_"+(TString)obj+"vsQCD>0.4285)" }
#       if (wp == "JMAR" && obj=="W") { c_algo_wp = "("+c_jet+"_1_DeepAK8MD_"+(TString)obj+"vsQCD>0.6231)" }
#     }

#     c_mass
#     if (obj=="T") { c_mass = "("+c_jet+"_1_mass>105. && "+c_jet+"_1_mass<210.)" }
#     if (obj=="W") { c_mass = "("+c_jet+"_1_mass>65. && "+c_jet+"_1_mass<105.)" }
#     #c_mass = "("+c_jet+"_1_mass>0.)"

#     xmin = xmin - (2.*(getmed)) + (2.*ialgo)
#     xmax = xmax - (2.*(getmed)) + (2.*ialgo)
    
#     TH1D *h_incl_mc   = create1Dhisto(sample,t_mc,lumi,cut_incl,c_jet+"_1_pt",bins,xmin,xmax,False,1,1,"h_incl_mc",False,False)     h_incl_mc.SetFillColor(0)  
#     TH1D *h_num_mc = create1Dhisto(sample,t_mc,lumi,cut_incl+" && "+c_algo_wp+" && "+c_mass,c_jet+"_1_pt",bins,xmin,xmax,False,colors[ialgo],1,"h_num_mc_"+algos[ialgo],False,False) 
#     TH1D *h_mc_r   = (TH1D*)h_num_mc.Clone("h_mc_r_"+algos[ialgo]) h_mc_r.Divide(h_num_mc,h_incl_mc,1.,1.,"B")
    
#     TH1D *h_incl_data
#     if (sample == "qcd") {
#       TH1D *h_incl_mc_b = create1Dhisto(sample,t_mc_b,lumi,cut_incl,c_jet+"_1_pt",bins,xmin,xmax,False,1,1,"h_incl_mc_b",False,False) h_incl_mc_b.SetFillColor(0)  
#       TH1D *h_incl_data_0 = create1Dhisto(sample,t_data,lumi,cut_incl,c_jet+"_1_pt",bins,xmin,xmax,False,1,1,"h_incl_data_0",False,True) h_incl_data_0.SetFillColor(0)  
#       h_incl_data = (TH1D*)h_incl_data_0.Clone("h_incl_data") h_incl_data.Add(h_incl_mc_b,-1.)
#       h_incl_mc_b.Delete() h_incl_data_0.Delete()
#     }
#     else { h_incl_data = create1Dhisto(sample,t_data,lumi,cut_incl,c_jet+"_1_pt",bins,xmin,xmax,False,1,1,"h_incl_data",False,True) h_incl_data.SetFillColor(0) }

#     TH1D *h_num_data
#     if (sample == "qcd") {
#       TH1D *h_num_mc_b = create1Dhisto(sample,t_mc_b,lumi,cut_incl+" && "+c_algo_wp+" && "+c_mass,c_jet+"_1_pt",bins,xmin,xmax,False,colors[ialgo],1,"h_num_mc_b_"+algos[ialgo],False,False) 
#       TH1D *h_num_data_0 = create1Dhisto(sample,t_data,lumi,cut_incl+" && "+c_algo_wp+" && "+c_mass,c_jet+"_1_pt",bins,xmin,xmax,False,colors[ialgo],1,"h_num_data_0_"+algos[ialgo],False,True) 
#       h_num_data = (TH1D*)h_num_data_0.Clone("h_num_data") h_num_data.Add(h_num_mc_b,-1.)
#       h_num_mc_b.Delete() h_num_data_0.Delete()
#     }
#     else { h_num_data = create1Dhisto(sample,t_data,lumi,cut_incl+" && "+c_algo_wp+" && "+c_mass,c_jet+"_1_pt",bins,xmin,xmax,False,colors[ialgo],1,"h_num_data_"+algos[ialgo],False,True) }
#     TH1D *h_data_r = (TH1D*)h_num_data.Clone("h_data_r_"+algos[ialgo]) h_data_r.Divide(h_num_data,h_incl_data,1.,1.,"B")

#     TH1D *h_sf = (TH1D*)h_mc_r.Clone("h_sf_"+algos[ialgo]) h_sf.Divide(h_data_r,h_mc_r)
#     h_sf.SetLineColor(colors[ialgo]) h_sf.SetMarkerColor(colors[ialgo]) h_sf.SetFillColor(0)
#     h_sf.SetMarkerSize(1.)
#     #eff_mc.append(h_mc_r)
#     #eff_data.append(h_data_r)
#     sf.append(h_sf)
    
#     h_incl_mc.Delete() h_incl_data.Delete() 
#   } # end of looping over the algos

#   TLegend* leg
#   if (obj=="T") { leg = new TLegend(0.75,0.46,0.92,0.89) }
#   if (obj=="W") { leg = new TLegend(0.75,0.66,0.92,0.89) }
#   leg.SetFillStyle(0)
#   leg.SetFillColor(0)
#   leg.SetLineWidth(0)

#   TPaveText *pt_cms = new TPaveText(0.01,0.77,0.4,0.9,"NDC")
#   pt_cms.SetFillStyle(0)
#   pt_cms.SetFillColor(0)
#   pt_cms.SetLineWidth(0)
#   pt_cms.AddText("CMS")
#   pt_cms.SetTextSize(0.08)

#   TPaveText *pt_preliminary = new TPaveText(0.06,0.63,0.4,0.9,"NDC")
#   pt_preliminary.SetFillStyle(0)
#   pt_preliminary.SetFillColor(0)
#   pt_preliminary.SetLineWidth(0)
#   pt_preliminary.AddText("Preliminary")
#   pt_preliminary.SetTextFont(52)
#   pt_preliminary.SetTextSize(0.06)

#   TLatex pt_lumi
#   const char *longstring = "35.9 fb^{-1} (13 TeV)"
#   pt_lumi.SetTextSize(0.07)
#   pt_lumi.SetTextFont(42)

#   TCanvas *c_sf = new TCanvas("c_sf","c_sf",700,500)
#   gStyle.SetErrorX(0.)
#   gPad.SetLeftMargin(0.1)
#   gPad.SetBottomMargin(0.13)
#   gPad.SetTopMargin(1.02)
#   sf[getmed].GetYaxis().SetRangeUser(0.5,2.)
#   sf[getmed].GetYaxis().SetTitleOffset(0.8)
#   sf[getmed].GetYaxis().SetTitle("#epsilon_{DATA} / #epsilon_{MC}")
#   sf[getmed].GetXaxis().SetLabelSize(0.06)
#   sf[getmed].GetXaxis().SetTitle("p_{T} (jet) [GeV]")
#   sf[getmed].Draw("P E0")
#   for (unsigned i0=0 i0<sf.size() ++i0) { leg.AddEntry(sf[i0],legnames[i0],"PL") if (i0!=getmed) { sf[i0].Draw("P E0 sames") } }
#   #  for (unsigned i0=0 i0<sf.size() ++i0) {   }
#   leg.Draw("sames")
#   pt_cms.Draw("sames")
#   pt_preliminary.Draw("sames")
#   pt_lumi.DrawLatexNDC(0.58,0.93,longstring)

#   TCanvas *c_eff_mc = new TCanvas("c_eff_mc","c_eff_mc",700,500)
#   for (unsigned i0=0 i0<eff_mc.size() ++i0) { 
#     if (i0==0) { eff_mc[i0].Draw("P E0") } 
#     else       { eff_mc[i0].Draw("P E0 sames") }
#   }

#   TCanvas *c_eff_data = new TCanvas("c_eff_data","c_eff_data",700,500)
#   for (unsigned i0=0 i0<eff_data.size() ++i0) { 
#     if (i0==0) { eff_data[i0].Draw("P E0") } 
#     else       { eff_data[i0].Draw("P E0 sames") }
#   }

# def getMisTagList() :

#   eff = 0.01
#   #getdiscvalmistag(eff,"sdtau32"     ,"(1-(ak8_1_tau3/ak8_1_tau2))","ak8","T","0==0")
#   getdiscvalmistag(eff,"sdtau32btag" ,"(1-(ak8_1_tau3/ak8_1_tau2))","ak8","T","max(ak8_1_sj1_btagCSVV2,ak8_1_sj2_btagCSVV2)>0.5426")
#   getdiscvalmistag(eff,"ecftoptag"   ,"(0.5+0.5*ca15_1_ecfTopTagBDT)","ca15","T","0==0")
#   #  getdiscvalmistag(eff,"hotvr","","ak8","T","0==0")
#   #getdiscvalmistag(eff,"sdtau21"     ,"(1-(ak8_1_tau2/ak8_1_tau1))","ak8","W","0==0")
#   getdiscvalmistag(eff,"sdn2"        ,"(1-ak8_1_n2b1)","ak8","W","0==0")
#   getdiscvalmistag(eff,"sdn2ddt"     ,"(0.5-0.5*ak8_1_n2b1ddt)","ak8","W","0==0")
#   getdiscvalmistag(eff,"best"        ,"(ak8_1_best_TvsQCD)","ak8","T","0==0")
#   getdiscvalmistag(eff,"best"        ,"ak8_1_best_WvsQCD","ak8","W","0==0")
#   #getdiscvalmistag(eff,"imagetop"    ,"ak8_1_image_top","ak8","T","0==0")
#   getdiscvalmistag(eff,"imagetopmd"  ,"ak8_1_image_top_md","ak8","T","0==0")
#   #getdiscvalmistag(eff,"deepak8"     ,"ak8_1_DeepAK8_TvsQCD","ak8","T","0==0")
#   getdiscvalmistag(eff,"deepak8"     ,"ak8_1_DeepAK8_WvsQCD","ak8","W","0==0")
#   #getdiscvalmistag(eff,"deepak8md"   ,"ak8_1_DeepAK8MD_TvsQCD","ak8","T","0==0")
#   getdiscvalmistag(eff,"deepak8md"   ,"ak8_1_DeepAK8MD_WvsQCD","ak8","W","0==0")

# def getdiscvalmistag(eff, algo, algosvar, jettype, obj, cut):
#   TH1::SetDefaultSumw2(kTrue)
#   #  TFile *f_ = TFile::Open("/eos/uscms/store/group/lpcjme/noreplica/NanoHRT/Trees/Apr08/drplots/zprime_tt.root" , "READONLY" ) 
#   TFile *f_ = TFile::Open("/eos/uscms/store/group/lpcjme/noreplica/NanoHRT/Trees/Apr08/qcd/mc_nom/qcd-mg_tree.root" , "READONLY" )
#   TTree *t_ = (TTree*)f_.Get("Events")

#   # selection
#   c_r if (jettype=="ak8") { c_r = "0.6" } if (jettype=="ca15") { c_r = "1.2" }
#   c_match = "("+jettype+"_1_pt>500)"
#   c_mass 
#   if (obj=="T") { c_mass = "("+jettype+"_1_mass>105. && "+jettype+"_1_mass<210.)" }
#   if (obj=="W") { c_mass = "("+jettype+"_1_mass>65. && "+jettype+"_1_mass<105.)" }
#   #  if (obj=="T") { c_match = "("+jettype+"_1_dr_fj_top_wqmax<"+c_r+") && ("+jettype+"_1_dr_fj_top_b<"+c_r+")" }

#   # get efficiencies
#   cut_init = "(xsecWeight*puWeight)*("+c_match+")"
#   cut_final = "(xsecWeight*puWeight)*("+c_match+" && "+cut+" && "+c_mass+")"
#   nbins = 100000 start = 1 end = nbins+1
#   TH1F *h_init = new TH1F("h_"+algo+"_init","h_"+algo+"_init",nbins,-10.,10.)
#   t_.Project("h_"+algo+"_init",algosvar,cut_init)
#   TH1F *h_ = new TH1F("h_"+algo,"h_"+algo,nbins,-10.,10.)
#   t_.Project("h_"+algo,algosvar,cut_final)

#   discval_ 
#   ntot = h_init.Integral(0,nbins+1)
#   for (unsigned i0=start i0<end ++i0) {
#     tmp_eff = h_.Integral(i0,nbins+1)
#     if ( (tmp_eff/ntot)<eff && (tmp_eff/ntot)>0. ) { discval_ = h_.GetBinCenter(i0) break  }
#   } 

#   std::print   algo    " "    discval_   "\n"

# def getSFSummary(obj, wp, path2file):
#   ROOT.gROOT.SetBatch(False)
#   ROOT.gROOT.LoadMacro("setTDRStyle.h")
#   ROOT.gStyle.SetOptStat(0)
#   ROOT.gStyle.SetOptFit(1)
#   ROOT.gStyle.SetPalette(1)
#   ROOT.TH1.SetDefaultSumw2()

#   # std::vector<TString> algos    algos.clear()
#   # std::vector<TString> legnames legnames.clear()
#   # std::vector<TString> ptrange  ptrange.clear()
#   # std::vector<int> colors colors.clear()

#   algos,legnames,ptrange,colors=[],[],[],[]
  
#   if obj=="W":
#     algos.append("sdtau21")     legnames.append("m_{SD}+#tau_{21}")   colors.append(800)
#     algos.append("deepak8")     legnames.append("DeepAK8")            colors.append(866)
#     # algos.append("deepak8md")   legnames.append("DeepAK8-MD")         colors.append(616)
    
#     ptrange.append("low")
#     ptrange.append("lowmed")
#     ptrange.append("med")

#   if obj=="W": names=["200-300","300-400","400-800"]; nbins = len(names), xmax = float(len(names))
#   h_dummy = ROOT.TH1F("h_dummy","h_dummy",nbins,0.,xmax)
#   for i1 in range(0,h_dummy.GetNbinsX()): h_dummy.GetXaxis().SetBinLabel(i1+1,names[i1])

#   std::vector<TGraphAsymmErrors*> gr_sf
#   for ialgo in range(0,len(algos)):
    
#     double xval[20], xvalerr[20]
#     double yval[20], yvalerrlo[20], yvalerrhi[20]
    
#     for (unsigned iptrange=0 iptrange<ptrange.size() ++iptrange) {
#       # TFile *fdiag = TFile::Open("./"+obj+"_"+algos[ialgo]+"/sf_fitDiagnostics_"+obj+"_"+algos[ialgo]+"_"+wp+"_"+ptrange[iptrange]+".root", "READONLY" )
#       TFile *fdiag = TFile::Open("./"+path2file+"/sf_fitDiagnostics_"+obj+"_"+algos[ialgo]+"_"+wp+"_"+ptrange[iptrange]+".root", "READONLY" )

#       TTree *t_   = (TTree*)fdiag.Get("tree_fit_sb")

#       strCat, strCatLoErr, strCatHiErr   
#       if (obj=="T") { strCat = "SF_catp3" strCatLoErr = "SF_catp3LoErr" strCatHiErr = "SF_catp3HiErr" }
#       if (obj=="W") { strCat = "SF_catp2" strCatLoErr = "SF_catp2LoErr" strCatHiErr = "SF_catp2HiErr" }
#       TH1F *h_sf_cat      = new TH1F("h_sf_cat"      , "h_sf_cat"      , 10000,0.,10.)
#       TH1F *h_sf_catLoErr = new TH1F("h_sf_catLoErr" , "h_sf_catLoErr" , 10000,0.,10.)
#       TH1F *h_sf_catHiErr = new TH1F("h_sf_catHiErr" , "h_sf_catHiErr" , 10000,0.,10.)
#       t_.Draw(strCat+" >> h_sf_cat")
#       t_.Draw(strCatLoErr+" >> h_sf_catLoErr")
#       t_.Draw(strCatHiErr+" >> h_sf_catHiErr")

#       xval[iptrange]    = (iptrange+0.5) + 0.03*(ialgo - 1.*(len(algos)-2))
#       xvalerr[iptrange] = 0.
#       yval[iptrange]    = h_sf_cat.GetMean()
#       yvalerrlo[iptrange] = h_sf_catLoErr.GetMean()
#       yvalerrhi[iptrange] = h_sf_catHiErr.GetMean()
#       if (algos[ialgo]=="sdtau21" && ptrange[iptrange]=="low") { yvalerrlo[iptrange] = 0.01 yvalerrhi[iptrange] = 0.01 }

#       h_sf_cat.Delete()
#       h_sf_catLoErr.Delete()
#       h_sf_catHiErr.Delete()

#     } # end looping over the pt bins

#     TGraphAsymmErrors *gr_sf_tmp = new TGraphAsymmErrors(ptrange.size(),xval,yval,xvalerr,xvalerr,yvalerrlo,yvalerrhi)
#     gr_sf_tmp.SetLineColor(colors[ialgo])
#     gr_sf_tmp.SetMarkerColor(colors[ialgo])
#     gr_sf.append(gr_sf_tmp)

#   } # end looping over files

#   TLegend* leg
#   if (obj=="T") { leg = new TLegend(0.75,0.46,0.92,0.89) }
#   if (obj=="W") { leg = new TLegend(0.75,0.66,0.92,0.89) }
#   leg.SetFillStyle(0)
#   leg.SetFillColor(0)
#   leg.SetLineWidth(0)

#   TPaveText *pt_cms = new TPaveText(0.01,0.77,0.4,0.9,"NDC")
#   pt_cms.SetFillStyle(0)
#   pt_cms.SetFillColor(0)
#   pt_cms.SetLineWidth(0)
#   pt_cms.AddText("CMS")
#   pt_cms.SetTextSize(0.08)

#   TPaveText *pt_preliminary = new TPaveText(0.06,0.63,0.4,0.9,"NDC")
#   pt_preliminary.SetFillStyle(0)
#   pt_preliminary.SetFillColor(0)
#   pt_preliminary.SetLineWidth(0)
#   pt_preliminary.AddText("Preliminary")
#   pt_preliminary.SetTextFont(52)
#   pt_preliminary.SetTextSize(0.06)

#   TLatex pt_lumi
#   const char *longstring = "35.9 fb^{-1} (13 TeV)"
#   pt_lumi.SetTextSize(0.07)
#   pt_lumi.SetTextFont(42)

#   TCanvas *c_sf = new TCanvas("c_sf","c_sf",700,500)
#   gPad.SetLeftMargin(0.1)
#   gPad.SetBottomMargin(0.13)
#   gPad.SetTopMargin(1.02)
#   #  gPad.SetGridy()
#   h_dummy.GetYaxis().SetRangeUser(0.5,2.)
#   h_dummy.GetYaxis().SetTitleOffset(0.8)
#   h_dummy.GetYaxis().SetTitle("#epsilon_{DATA} / #epsilon_{MC}")
#   h_dummy.GetXaxis().SetLabelSize(0.06)
#   h_dummy.GetXaxis().SetTitle("p_{T} (jet) [GeV]")
#   h_dummy.Draw("HIST")
#   for (unsigned i0=0 i0<gr_sf.size() ++i0) {
#     gr_sf[i0].Draw("P sames")
#     leg.AddEntry(gr_sf[i0],legnames[i0],"PL")
#     for (unsigned igr = 0 igr<gr_sf[i0].GetN() ++igr) {
#       double x_, y_
#       gr_sf[i0].GetPoint(igr,x_,y_)
#       std::print   std::fixed
#       std::print   std::setprecision(2)
#       if (igr < (gr_sf[i0].GetN()-1)) { std::print   " & "   y_   "$^{+"   gr_sf[i0].GetErrorYhigh(igr)   "}_{-"   gr_sf[i0].GetErrorYlow(igr)   "}$" }
#       else                             { std::print   " & "   y_   "$^{+"   gr_sf[i0].GetErrorYhigh(igr)   "}_{-"   gr_sf[i0].GetErrorYlow(igr)   "}$ \\\\ \n" }
#     }
#   }
#   leg.Draw("sames")
#   pt_cms.Draw("sames")
#   pt_preliminary.Draw("sames")
#   pt_lumi.DrawLatexNDC(0.58,0.93,longstring)
#   c_sf.Print("sf_"+obj+"_"+wp+".png")

##### GENERAL FUNCTIONS #####

def median(vecb):
  vec=[]; counter = 0; 
  for i0 in range(0,len(vecb)-1): 
    vec.append(counter)
    counter+=1 
  if (len(vec) == 0): raise Exception("median of an empty vector")
  if not len(vec) % 2 == 0: return (vec[len(vec)/2] + vec[(len(vec)/2)-1]) / 2
  else:                     return vec[len(vec)]/2

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
