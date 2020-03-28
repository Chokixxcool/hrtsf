import ROOT,glob,os,sys

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

    h_den_mc = create1Dhisto("sample",t_mc,lumi,cut_incl,c_jet+"_1_pt",bins,xmin,xmax,false,1,1,"h_den_mc",false,false); h_den_mc.SetFillColor(0)  
    h_num_mc  = create1Dhisto("sample",t_mc,lumi,cut_incl+" && "+c_algo_wp+" && "+c_mass,c_jet+"_1_pt",bins,xmin,xmax,false,colors[ialgo],1,"h_num_mc_"+algo,false,false) 
    
    h_mc_r    = h_num_mc.Clone("h_mc_r_"+algo) 
    h_mc_r.Divide(h_num_mc,h_den_mc,1.,1.,"B")
    h_mc_r.Write("MC")

    h_den_data = create1Dhisto("sample",t_data,lumi,cut_incl,c_jet+"_1_pt",bins,xmin,xmax,false,1,1,"h_den_data",false,true); h_den_data.SetFillColor(0)
    h_num_data = create1Dhisto("sample",t_data,lumi,cut_incl+" && "+c_algo_wp+" && "+c_mass,c_jet+"_1_pt",bins,xmin,xmax,false,colors[ialgo],1,"h_num_data_"+algo,false,true)
    
    h_data_r = h_num_data.Clone("h_data_r_"+algo) 
    h_data_r.Divide(h_num_data,h_den_data,1.,1.,"B")
    h_data_r.Write("Data")

    h_sf = h_mc_r.Clone("h_sf_"+algo) 
    h_sf.Divide(h_data_r,h_mc_r)
    h_sf.SetLineColor(colors[ialgo]); h_sf.SetFillColor(0); h_sf.SetMarkerColor(colors[ialgo]); h_sf.SetMarkerSize(1.)
    h_sf.Write("SF")

    eff_mc.append(h_mc_r)
    eff_data.append(h_data_r)
    sf.append(h_sf)
    
    h_den_mc.Delete(); h_den_data.Delete() 
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
  gStyle.SetErrorX(0.)
  gPad.SetLeftMargin(0.1)
  gPad.SetBottomMargin(0.13)
  gPad.SetTopMargin(1.02)
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

# def getMisTagRates(sample, obj, wp, year):
#   # sample: photon qcd  
#   setTDRStyle()
#   gROOT.SetBatch(False)
#   gStyle.SetOptStat(0)
#   gStyle.SetOptFit(1)
#   gStyle.SetPalette(1)
#   ROOT.SetDefaultSumw2(ROOT.kTrue)

#   # if (sample == "photon") :
#   #   INDIR = "/eos/uscms/store/group/lpcjme/noreplica/NanoHRT/Trees/Apr08/"+sample+"/"
#   #   f_mc = ROOT.TFile.Open(INDIR+"/mc_nom/sm.root" , "READONLY" )
#   #   #f_mc = ROOT.TFile.Open(INDIR+"/mc_nom/photon_tree.root" , "READONLY" )
#   #   f_mc_b = ROOT.TFile.Open(INDIR+"/mc_nom/sm.root" , "READONLY" )
#   #   f_data = ROOT.TFile.Open(INDIR+"/data/singlephoton_tree.root" , "READONLY" )

#   # if (sample == "qcd") :
#   #   INDIR = "/eos/uscms/store/group/lpcjme/noreplica/NanoHRT/Trees/Apr08/"+sample+"/"
#   #   #f_mc = ROOT.TFile.Open(INDIR+"/mc_nom/qcd-mg_tree.root" , "READONLY" )
#   #   f_mc = ROOT.TFile.Open(INDIR+"/mc_nom/qcd-herwig_tree.root" , "READONLY" )
#   #   f_mc_b = ROOT.TFile.Open(INDIR+"/mc_nom/sm_noqcd.root" , "READONLY" )
#   #   f_data = ROOT.TFile.Open(INDIR+"/data/jetht_tree.root" , "READONLY" )
#   #############################################################################
#   sample="sample"
#   lumi={"2016":"36.8","2017":"41.53","2018":"59.74"}

#   EOSCMS="root://eoscms.cern.ch/"
#   INDIR=EOSCMS+"/eos/cms/store/group/phys_jetmet/nbinnorj/WTopTagging/ntuples_HRTSF/"
#   INDIR_ext={"2016":"2016/","2017":"29July/","2018":"3Oct_For_Copy/"}
#   INDIR+=INDIR_ext[year]  

#   f_mc=ROOT.TFile.Open(INDIR+"/mc_nom/sm_tree.root","READONLY")
#   f_data=ROOT.TFile.Open(INDIR+"/data/singlemu_tree.root","READONLY")
  
#   t_mc   = f_mc.Get("Events")
#   # t_mc_b = f_mc_b.Get("Events")
#   t_data = f_data.Get("Events")

#   algos,legnames,ptrange,colors = [],[],[],[]
  
#   if (obj=="W") :
#     algos.append("sdtau21")     ; legnames.append("m_SD+#tau_21")   ; colors.append(800)
#     algos.append("deepak8")     ; legnames.append("DeepAK8")        ; colors.append(866)
#     # algos.append("deepak8md") ;   legnames.append("DeepAK8-MD")         ; colors.append(616)

#   # baseline selection
#   # if (sample == "photon"):  c_base = "(passPhoton165_HE10 && n_ak8>=1 && n_ca15>=1 && nphotons>=1 && pho_1_pt>200.)" 
#   # if (sample == "qcd")   :  c_base = "(ht>1000 && n_ak8>=1 && n_ca15>=1)" 
#   c_base = "(n_ak8>=1 && ak8_1_pt>200 && abs(ak8_1_eta)<2.4)"
#   cut_incl = c_base
  
#   # if (sample == "photon") :
#   #   if (obj=="T"):  bins = 7 ;xmin = 300. ;xmax = 1000. 
#   #   if (obj=="W"):  bins = 8 ;xmin = 200. ;xmax = 1000. 
#   # if (sample == "qcd"):     
#   #   if (obj=="T"):  bins = 12; xmin = 300.; xmax = 1500. 
#   #   if (obj=="W"):  bins = 13; xmin = 200.; xmax = 1500. 

#   getmed = median(algos) #?
#   eff_mc = []; eff_data = []; sf = []
#   for algo in algos:
#     if (algo == "sdtau21")     :  c_jet = "ak8"   ; if (wp == "JMAR"):  c_algo_wp = "((1-"+c_jet+"_1_tau2/"+c_jet+"_1_tau1)>0.6781)"  
#     if (algo == "deepak8")     :  c_jet = "ak8"   ; if (wp == "JMAR"):  c_algo_wp = "("+c_jet+"_1_DeepAK8_"+obj+"vsQCD>0.9383)" 
 
#     # if (algo == "deepak8md")  :    c_jet = "ak8"
#     #   if (wp == "JMAR" && obj=="T")  :  c_algo_wp = "("+c_jet+"_1_DeepAK8MD_"+"("+obj+"vsQCD>0.4285)" 
#     #   if (wp == "JMAR" && obj=="W")  :  c_algo_wp = "("+c_jet+"_1_DeepAK8MD_"+"("+obj+"vsQCD>0.6231)" 

#     c_mass = "("+c_jet+"_1_mass>65. && "+c_jet+"_1_mass<105.)" 
#     #c_mass = "("+c_jet+"_1_mass>0.)"

#     xmin = xmin - (2.*(getmed)) + (2.*ialgo)
#     xmax = xmax - (2.*(getmed)) + (2.*ialgo)
    
#     h_incl_mc   = create1Dhisto(sample,t_mc,lumi,cut_incl,c_jet+"_1_pt",bins,xmin,xmax,False,1,1,"h_incl_mc",False,False)     
#     h_incl_mc.SetFillColor(0)  
#     h_num_mc = create1Dhisto(sample,t_mc,lumi,cut_incl+" && "+c_algo_wp+" && "+c_mass,c_jet+"_1_pt",bins,xmin,xmax,False,colors[ialgo],1,"h_num_mc_"+algo,False,False) 
#     h_mc_r   = h_num_mc.Clone("h_mc_r_"+algo) 
#     h_mc_r.Divide(h_num_mc,h_incl_mc,1.,1.,"B")
    
#     if (sample == "qcd") :
#       h_incl_mc_b = create1Dhisto(sample,t_mc_b,lumi,cut_incl,c_jet+"_1_pt",bins,xmin,xmax,False,1,1,"h_incl_mc_b",False,False) 
#       h_incl_mc_b.SetFillColor(0)  
#       h_incl_data_0 = create1Dhisto(sample,t_data,lumi,cut_incl,c_jet+"_1_pt",bins,xmin,xmax,False,1,1,"h_incl_data_0",False,True) 
#       h_incl_data_0.SetFillColor(0)  
#       h_incl_data = h_incl_data_0.Clone("h_incl_data") h_incl_data.Add(h_incl_mc_b,-1.)
#       h_incl_mc_b.Delete() 
#       h_incl_data_0.Delete()
 
#     else : 
#       h_incl_data = create1Dhisto(sample,t_data,lumi,cut_incl,c_jet+"_1_pt",bins,xmin,xmax,False,1,1,"h_incl_data",False,True) 
#       h_incl_data.SetFillColor(0) 

#     if (sample == "qcd") :
#       h_num_mc_b = create1Dhisto(sample,t_mc_b,lumi,cut_incl+" && "+c_algo_wp+" && "+c_mass,c_jet+"_1_pt",bins,xmin,xmax,False,colors[ialgo],1,"h_num_mc_b_"+algo,False,False) 
#       h_num_data_0 = create1Dhisto(sample,t_data,lumi,cut_incl+" && "+c_algo_wp+" && "+c_mass,c_jet+"_1_pt",bins,xmin,xmax,False,colors[ialgo],1,"h_num_data_0_"+algo,False,True) 
#       h_num_data = h_num_data_0.Clone("h_num_data") 
#       h_num_data.Add(h_num_mc_b,-1.)
#       h_num_mc_b.Delete() 
#       h_num_data_0.Delete()
 
#     else:
#       h_num_data = create1Dhisto(sample,t_data,lumi,cut_incl+" && "+c_algo_wp+" && "+c_mass,c_jet+"_1_pt",bins,xmin,xmax,False,colors[ialgo],1,"h_num_data_"+algo,False,True) 
    
#     h_data_r = h_num_data.Clone("h_data_r_"+algo) h_data_r.Divide(h_num_data,h_incl_data,1.,1.,"B")

#     h_sf = h_mc_r.Clone("h_sf_"+algo) 
#     h_sf.Divide(h_data_r,h_mc_r)
#     h_sf.SetLineColor(colors[ialgo]) 
#     h_sf.SetMarkerColor(colors[ialgo]) 
#     h_sf.SetFillColor(0)
#     h_sf.SetMarkerSize(1.)
    
#     eff_mc.append(h_mc_r)
#     eff_data.append(h_data_r)
#     sf.append(h_sf)
    
#     h_incl_mc.Delete() 
#     h_incl_data.Delete()  
#     # end of looping over the algos

#   if (obj=="T") : leg = ROOT.TLegend(0.75,0.46,0.92,0.89) 
#   if (obj=="W") : leg = ROOT.TLegend(0.75,0.66,0.92,0.89) 
#   leg.SetFillStyle(0)
#   leg.SetFillColor(0)
#   leg.SetLineWidth(0)

#   pt_cms = ROOT.TPaveText(0.01,0.77,0.4,0.9,"NDC")
#   pt_cms.SetFillStyle(0)
#   pt_cms.SetFillColor(0)
#   pt_cms.SetLineWidth(0)
#   pt_cms.AddText("CMS")
#   pt_cms.SetTextSize(0.08)

#   pt_preliminary = ROOT.TPaveText(0.06,0.63,0.4,0.9,"NDC")
#   pt_preliminary.SetFillStyle(0)
#   pt_preliminary.SetFillColor(0)
#   pt_preliminary.SetLineWidth(0)
#   pt_preliminary.AddText("Preliminary")
#   pt_preliminary.SetTextFont(52)
#   pt_preliminary.SetTextSize(0.06)

#   pt_lumi = ROOT.TLatex()
#   longstring = "35.9 fb^-1 (13 TeV)"
#   pt_lumi.SetTextSize(0.07)
#   pt_lumi.SetTextFont(42)

#   c_sf = ROOT.TCanvas("c_sf","c_sf",700,500)
#   gStyle.SetErrorX(0.)
#   gPad.SetLeftMargin(0.1)
#   gPad.SetBottomMargin(0.13)
#   gPad.SetTopMargin(1.02)
#   sf[getmed].GetYaxis().SetRangeUser(0.5,2.)
#   sf[getmed].GetYaxis().SetTitleOffset(0.8)
#   sf[getmed].GetYaxis().SetTitle("#epsilon_DATA / #epsilon_MC")
#   sf[getmed].GetXaxis().SetLabelSize(0.06)
#   sf[getmed].GetXaxis().SetTitle("p_T (jet) [GeV]")
#   sf[getmed].Draw("P E0")
  
#   for i0 in range(0,len(sf)):
#     leg.AddEntry(sf[i0],legnames[i0],"PL")
#     if i0!=getmed: sf[i0].Draw("P E0 sames")
#   leg.Draw("sames")
#   pt_cms.Draw("sames")
#   pt_preliminary.Draw("sames")
#   pt_lumi.DrawLatexNDC(0.58,0.93,longstring)

#   c_eff_mc = ROOT.TCanvas("c_eff_mc","c_eff_mc",700,500)
#   for i0 in range(0,len(eff_mc)):
#     if (i0==0): eff_mc[i0].Draw("P E0")  
#     else      : eff_mc[i0].Draw("P E0 sames") 

#   c_eff_data = ROOT.TCanvas("c_eff_data","c_eff_data",700,500)
#   for i0 in range(0,len(eff_data)):
#     if (i0==0):  eff_data[i0].Draw("P E0")  
#     else      :  eff_data[i0].Draw("P E0 sames")  

def create1Dhisto(sample,tree,intlumi,cuts,branch,bins,xmin,xmax,useLog,color,style,name,norm,data):
  ROOT.SetDefaultSumw2(ROOT.kTRUE)

  if (data): cut ="("+cuts+")"
  else :
    if      ("puUp" in name)   : cut ="(xsecWeight*puWeightUp*genWeight*"+intlumi+")*("+cuts+")"
    elif ("puDown" in name) : cut ="(xsecWeight*puWeightDown*genWeight*"+intlumi+")*("+cuts+")"
    # else if ("herw" in name))   : { cut ="(xsecWeight*puWeight*"+intlumi+")*("+cuts+")"
    # else                        : { cut ="(xsecWeight*puWeight*genWeight*"+intlumi+")*("+cuts+")"
    else                       : cut ="(puWeight*genWeight*"+intlumi+")*("+cuts+")"
  

  hTemp = ROOT.TH1D(name,name,bins,xmin,xmax)
  tree.Project(name,branch,cut)

  hTemp.SetLineWidth(3)
  hTemp.SetMarkerSize(0)
  hTemp.SetLineColor(color)
  hTemp.SetFillColor(color)
  hTemp.SetLineStyle(style)

  # ad overflow bin
  error =0.; integral = hTemp.IntegralAndError(bins,bins+1,error)
  # hTemp.SetBinContent(bins,integral);
  # hTemp.SetBinError(bins,error);

  if (norm): hTemp.Scale(1./(hTemp.Integral()))

  return hTemp;
  # end of create1Dhisto

def median(vecb):
  vec=[]; counter = 0; 
  for i0 in range(0,len(vecb)): 
    vec.append(counter)
    counter+=1 
  if (len(vec) == 0): raise Exception("median of an empty vector")
  vec.sort()
  if len(vec) % 2 == 0: 
    return (vec[len(vec)/2] + vec[len(vec)/2-1]) / 2
  else:                 
    return vec[len(vec)]/2