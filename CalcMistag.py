import ROOT,glob,os,sys

def main():
  getMisTagRates()

def getMisTagRates(sample, obj, wp):
  # sample: photon qcd  
  setTDRStyle()
  gROOT.SetBatch(False)
  gStyle.SetOptStat(0)
  gStyle.SetOptFit(1)
  gStyle.SetPalette(1)
  ROOT.SetDefaultSumw2(ROOT.kTrue)

  # if (sample == "photon") :
  #   path = "/eos/uscms/store/group/lpcjme/noreplica/NanoHRT/Trees/Apr08/"+sample+"/"
  #   f_mc = ROOT.TFile.Open(path+"/mc_nom/sm.root" , "READONLY" )
  #   #f_mc = ROOT.TFile.Open(path+"/mc_nom/photon_tree.root" , "READONLY" )
  #   f_mc_b = ROOT.TFile.Open(path+"/mc_nom/sm.root" , "READONLY" )
  #   f_data = ROOT.TFile.Open(path+"/data/singlephoton_tree.root" , "READONLY" )

  # if (sample == "qcd") :
  #   path = "/eos/uscms/store/group/lpcjme/noreplica/NanoHRT/Trees/Apr08/"+sample+"/"
  #   #f_mc = ROOT.TFile.Open(path+"/mc_nom/qcd-mg_tree.root" , "READONLY" )
  #   f_mc = ROOT.TFile.Open(path+"/mc_nom/qcd-herwig_tree.root" , "READONLY" )
  #   f_mc_b = ROOT.TFile.Open(path+"/mc_nom/sm_noqcd.root" , "READONLY" )
  #   f_data = ROOT.TFile.Open(path+"/data/jetht_tree.root" , "READONLY" )
  #############################################################################
  lumi = "59.74"
  INDIR="/eos/cms/store/group/phys_jetmet/nbinnorj/WTopTagging/ntuples_HRTSF/3Oct_For_Copy/"
  f_mc=ROOT.TFile.Open(INDIR+"/mc_nom/sm_tree.root","READONLY")
  f_mc_data=ROOT.TFile.Open(INDIR+"/data/singlemu_tree.root","READONLY")
  
  t_mc   = f_mc.Get("Events")
  t_mc_b = f_mc_b.Get("Events")
  t_data = f_data.Get("Events")

  algos = []
  legnames = []
  ptrange = []
  colors = []
  
  if (obj=="T") :
    algos.append("sdtau32")     ; legnames.append("m_SD+#tau_32")       ; colors.append(800)
    algos.append("sdtau32btag") ; legnames.append("m_SD+#tau_32+b-tag") ; colors.append(632)
    #algos.append("hotvr")      ;  legnames.append("HOTVR")                  ; colors.append(812)
    algos.append("ecftoptag")   ; legnames.append("CA15-ECF")               ; colors.append(419)
    algos.append("best")        ; legnames.append("BEST")                   ; colors.append(882)
    algos.append("imagetop")    ; legnames.append("ImageTop")               ; colors.append(603)
    algos.append("imagetopmd")  ; legnames.append("ImageTop-MD")            ; colors.append(600)
    algos.append("deepak8")     ; legnames.append("DeepAK8")                ; colors.append(866)
    algos.append("deepak8md")   ; legnames.append("DeepAK8-MD")             ; colors.append(616)

  if (obj=="W") 
    algos.append("sdtau21")     ; legnames.append("m_SD+#tau_21")   ; colors.append(800)
    # algos.append("sdn2")      ;   legnames.append("m_SD+N_2")       ; colors.append(408)
    # algos.append("sdn2ddt")   ;   legnames.append("m_SD+N_2^DDT") ; colors.append(419)
    # algos.append("best")      ;   legnames.append("BEST")               ; colors.append(882)
    algos.append("deepak8")     ; legnames.append("DeepAK8")            ; colors.append(866)
    # algos.append("deepak8md") ;   legnames.append("DeepAK8-MD")         ; colors.append(616)

  # baseline selection
  if (sample == "photon"):  c_base = "(passPhoton165_HE10 && n_ak8>=1 && n_ca15>=1 && nphotons>=1 && pho_1_pt>200.)" 
  if (sample == "qcd")   :  c_base = "(ht>1000 && n_ak8>=1 && n_ca15>=1)" 
  cut_incl = c_base
  
  if (sample == "photon") :
    if (obj=="T"):  bins = 7 ;xmin = 300. ;xmax = 1000. 
    if (obj=="W"):  bins = 8 ;xmin = 200. ;xmax = 1000. 
  if (sample == "qcd"):     
    if (obj=="T"):  bins = 12; xmin = 300.; xmax = 1500. 
    if (obj=="W"):  bins = 13; xmin = 200.; xmax = 1500. 

  getmed = median(algos) #?
  eff_mc = []; eff_data = []; sf = []
  for ialgo in range(0, len(algos)) :
    if (algos[ialgo] == "sdtau32")     :  c_jet = "ak8"   ; if (wp == "JMAR"):  c_algo_wp = "((1-"+c_jet+"_1_tau3/"+c_jet+"_1_tau2)>0.4909)"  
    if (algos[ialgo] == "sdtau32btag") :  c_jet = "ak8"   ; if (wp == "JMAR"):  c_algo_wp = "((1-"+c_jet+"_1_tau3/"+c_jet+"_1_tau2)>0.3881 && max("+c_jet+"_1_sj1_btagCSVV2,"+c_jet+"_1_sj2_btagCSVV2)>0.5426)"  
    if (algos[ialgo] == "ecftoptag")   :  c_jet = "ca15"  ; if (wp == "JMAR"):  c_algo_wp = "( "+c_jet+"_1_ecfTopTagBDT>-1. && (0.5+0.5*"+c_jet+"_1_ecfTopTagBDT)>0.7831)"  
    if (algos[ialgo] == "sdtau21")     :  c_jet = "ak8"   ; if (wp == "JMAR"):  c_algo_wp = "((1-"+c_jet+"_1_tau2/"+c_jet+"_1_tau1)>0.6781)"  
    if (algos[ialgo] == "sdn2")        :  c_jet = "ak8"   ; if (wp == "JMAR"):  c_algo_wp = "((1-"+c_jet+"_1_n2b1)>0.7643)"  
    if (algos[ialgo] == "sdn2ddt")     :  c_jet = "ak8"   ; if (wp == "JMAR"):  c_algo_wp = "((0.5-0.5*"+c_jet+"_1_n2b1ddt)>0.4891)"  
    if (algos[ialgo] == "hotvr")       :  c_jet = "hotvr" ; if (wp == "JMAR"):  c_algo_wp = "( && hotvr_1_fpt<0.8 && hotvr_1_nsubjets>=3 && hotvr_1_mmin>=50. && (1-hotvr_1_tau32)>0.4504)"  
    if (algos[ialgo] == "best")        :  
      c_jet = "ak8"   
      if (wp == "JMAR" && obj=="T") :  c_algo_wp = "("+c_jet+"_1_best_"+"("+obj+"vsQCD>0.8563)"  
      if (wp == "JMAR" && obj=="W") :  c_algo_wp = "("+c_jet+"_1_best_"+"("+obj+"vsQCD>0.9001)" 
 
    if (algos[ialgo] == "imagetop")    :  c_jet = "ak8"   if (wp == "JMAR"):  c_algo_wp = "("+c_jet+"_1_image_top>0.8021)"  
    if (algos[ialgo] == "imagetopmd")  :  c_jet = "ak8"   if (wp == "JMAR"):  c_algo_wp = "("+c_jet+"_1_image_top>0.7485)"  
    if (algos[ialgo] == "deepak8")     :  
      c_jet = "ak8" 
      if (wp == "JMAR" && obj=="T")  :  c_algo_wp = "("+c_jet+"_1_DeepAK8_"+"("+obj+"vsQCD>0.8537)"  
      if (wp == "JMAR" && obj=="W")  :  c_algo_wp = "("+c_jet+"_1_DeepAK8_"+"("+obj+"vsQCD>0.9383)" 
 
    if (algos[ialgo] == "deepak8md")  :    c_jet = "ak8"
      if (wp == "JMAR" && obj=="T")  :  c_algo_wp = "("+c_jet+"_1_DeepAK8MD_"+"("+obj+"vsQCD>0.4285)" 
      if (wp == "JMAR" && obj=="W")  :  c_algo_wp = "("+c_jet+"_1_DeepAK8MD_"+"("+obj+"vsQCD>0.6231)" 

    if (obj=="T"):  c_mass = "("+c_jet+"_1_mass>105. && "+c_jet+"_1_mass<210.)" 
    if (obj=="W"):  c_mass = "("+c_jet+"_1_mass>65. && "+c_jet+"_1_mass<105.)" 
    #c_mass = "("+c_jet+"_1_mass>0.)"

    xmin = xmin - (2.*(getmed)) + (2.*ialgo)
    xmax = xmax - (2.*(getmed)) + (2.*ialgo)
    
    h_incl_mc   = create1Dhisto(sample,t_mc,lumi,cut_incl,c_jet+"_1_pt",bins,xmin,xmax,False,1,1,"h_incl_mc",False,False)     
    h_incl_mc.SetFillColor(0)  
    h_num_mc = create1Dhisto(sample,t_mc,lumi,cut_incl+" && "+c_algo_wp+" && "+c_mass,c_jet+"_1_pt",bins,xmin,xmax,False,colors[ialgo],1,"h_num_mc_"+algos[ialgo],False,False) 
    h_mc_r   = h_num_mc.Clone("h_mc_r_"+algos[ialgo]) 
    h_mc_r.Divide(h_num_mc,h_incl_mc,1.,1.,"B")
    
    if (sample == "qcd") :
      h_incl_mc_b = create1Dhisto(sample,t_mc_b,lumi,cut_incl,c_jet+"_1_pt",bins,xmin,xmax,False,1,1,"h_incl_mc_b",False,False) 
      h_incl_mc_b.SetFillColor(0)  
      h_incl_data_0 = create1Dhisto(sample,t_data,lumi,cut_incl,c_jet+"_1_pt",bins,xmin,xmax,False,1,1,"h_incl_data_0",False,True) 
      h_incl_data_0.SetFillColor(0)  
      h_incl_data = h_incl_data_0.Clone("h_incl_data") h_incl_data.Add(h_incl_mc_b,-1.)
      h_incl_mc_b.Delete() 
      h_incl_data_0.Delete()
 
    else : 
      h_incl_data = create1Dhisto(sample,t_data,lumi,cut_incl,c_jet+"_1_pt",bins,xmin,xmax,False,1,1,"h_incl_data",False,True) 
      h_incl_data.SetFillColor(0) 

    if (sample == "qcd") :
      h_num_mc_b = create1Dhisto(sample,t_mc_b,lumi,cut_incl+" && "+c_algo_wp+" && "+c_mass,c_jet+"_1_pt",bins,xmin,xmax,False,colors[ialgo],1,"h_num_mc_b_"+algos[ialgo],False,False) 
      h_num_data_0 = create1Dhisto(sample,t_data,lumi,cut_incl+" && "+c_algo_wp+" && "+c_mass,c_jet+"_1_pt",bins,xmin,xmax,False,colors[ialgo],1,"h_num_data_0_"+algos[ialgo],False,True) 
      h_num_data = h_num_data_0.Clone("h_num_data") 
      h_num_data.Add(h_num_mc_b,-1.)
      h_num_mc_b.Delete() 
      h_num_data_0.Delete()
 
    else:
      h_num_data = create1Dhisto(sample,t_data,lumi,cut_incl+" && "+c_algo_wp+" && "+c_mass,c_jet+"_1_pt",bins,xmin,xmax,False,colors[ialgo],1,"h_num_data_"+algos[ialgo],False,True) 
    
    h_data_r = h_num_data.Clone("h_data_r_"+algos[ialgo]) h_data_r.Divide(h_num_data,h_incl_data,1.,1.,"B")

    h_sf = h_mc_r.Clone("h_sf_"+algos[ialgo]) 
    h_sf.Divide(h_data_r,h_mc_r)
    h_sf.SetLineColor(colors[ialgo]) 
    h_sf.SetMarkerColor(colors[ialgo]) 
    h_sf.SetFillColor(0)
    h_sf.SetMarkerSize(1.)
    
    eff_mc.append(h_mc_r)
    eff_data.append(h_data_r)
    sf.append(h_sf)
    
    h_incl_mc.Delete() 
    h_incl_data.Delete()  
    # end of looping over the algos

  if (obj=="T") : leg = ROOT.TLegend(0.75,0.46,0.92,0.89) 
  if (obj=="W") : leg = ROOT.TLegend(0.75,0.66,0.92,0.89) 
  leg.SetFillStyle(0)
  leg.SetFillColor(0)
  leg.SetLineWidth(0)

  pt_cms = ROOT.TPaveText(0.01,0.77,0.4,0.9,"NDC")
  pt_cms.SetFillStyle(0)
  pt_cms.SetFillColor(0)
  pt_cms.SetLineWidth(0)
  pt_cms.AddText("CMS")
  pt_cms.SetTextSize(0.08)

  pt_preliminary = ROOT.TPaveText(0.06,0.63,0.4,0.9,"NDC")
  pt_preliminary.SetFillStyle(0)
  pt_preliminary.SetFillColor(0)
  pt_preliminary.SetLineWidth(0)
  pt_preliminary.AddText("Preliminary")
  pt_preliminary.SetTextFont(52)
  pt_preliminary.SetTextSize(0.06)

  pt_lumi = ROOT.TLatex()
  longstring = "35.9 fb^-1 (13 TeV)"
  pt_lumi.SetTextSize(0.07)
  pt_lumi.SetTextFont(42)

  c_sf = ROOT.TCanvas("c_sf","c_sf",700,500)
  gStyle.SetErrorX(0.)
  gPad.SetLeftMargin(0.1)
  gPad.SetBottomMargin(0.13)
  gPad.SetTopMargin(1.02)
  sf[getmed].GetYaxis().SetRangeUser(0.5,2.)
  sf[getmed].GetYaxis().SetTitleOffset(0.8)
  sf[getmed].GetYaxis().SetTitle("#epsilon_DATA / #epsilon_MC")
  sf[getmed].GetXaxis().SetLabelSize(0.06)
  sf[getmed].GetXaxis().SetTitle("p_T (jet) [GeV]")
  sf[getmed].Draw("P E0")
  
  for i0 in range(0,len(sf)):
    leg.AddEntry(sf[i0],legnames[i0],"PL")
    if i0!=getmed: sf[i0].Draw("P E0 sames")
  leg.Draw("sames")
  pt_cms.Draw("sames")
  pt_preliminary.Draw("sames")
  pt_lumi.DrawLatexNDC(0.58,0.93,longstring)

  c_eff_mc = ROOT.TCanvas("c_eff_mc","c_eff_mc",700,500)
  for i0 in range(0,len(eff_mc)):
    if (i0==0): eff_mc[i0].Draw("P E0")  
    else      : eff_mc[i0].Draw("P E0 sames") 

  c_eff_data = ROOT.TCanvas("c_eff_data","c_eff_data",700,500)
  for i0 in range(0,len(eff_data)):
    if (i0==0):  eff_data[i0].Draw("P E0")  
    else      :  eff_data[i0].Draw("P E0 sames")  

def create1Dhisto(sample,tree,intLumi,cuts,branch,bins,xmin,xmax,useLog,color,style,name,norm,data):
  ROOT.SetDefaultSumw2(ROOT.kTRUE)

  if (data): cut ="("+cuts+")"
  else :
    if      ("puUp" in name)   : { cut ="(xsecWeight*puWeightUp*genWeight*"+intLumi+")*("+cuts+")"
    else if ("puDown" in name) : { cut ="(xsecWeight*puWeightDown*genWeight*"+intLumi+")*("+cuts+")"
    # else if ("herw" in name))   : { cut ="(xsecWeight*puWeight*"+intLumi+")*("+cuts+")"
    # else                        : { cut ="(xsecWeight*puWeight*genWeight*"+intLumi+")*("+cuts+")"
    else                       : { cut ="(puWeight*genWeight*"+intLumi+")*("+cuts+")"
  

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

if __name__ == '__main__':
  main()