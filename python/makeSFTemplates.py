import ROOT,glob,os
import array
import numpy as np

def makeSFTemplates(obj, algo, wp, ptrange, syst, Pass, mistRate, WP_Top_binarized, WP_Top_binarizedMD, WP_Top_raw, WP_Top_rawMD, year, workdir) :

  if Pass: passstr = "pass"
  else: passstr = "fail"
  name = year+"_"+obj+"_"+algo+"_"+wp+"_"+ptrange+"_"+mistRate+"_"+passstr
  
  ROOT.gROOT.SetBatch(True)
  ROOT.gROOT.LoadMacro("setTDRStyle.h")
  ROOT.gStyle.SetOptStat(0)
  ROOT.gStyle.SetOptFit(1)
  ROOT.gStyle.SetPalette(1)
  ROOT.TH1.SetDefaultSumw2()

  if year == "2016": intLumi = "36.8"
  elif year == "2017": intLumi = "41.53"
  elif year == "2018": intLumi = "59.74"
  
  lumi=intLumi

  ## baseline selection
  if year == "2016": c_base = "(n_ak8>=1 && n_ca15>=1)"
  elif year == "2017" or year == "2018": c_base = "(n_ak8>=1)"
  
  ## selection on algo
  if (algo == "sdtau21") : 
    c_jet = "ak8"; c_r = "0.8"
    if (wp == "JMAR") : c_algo_wp = "((1-"+c_jet+"_1_tau2/"+c_jet+"_1_tau1)>0.6514)"

  elif (algo == "deepak8") : 
    c_jet = "ak8"; c_r = "0.8"
    # if (wp == "JMAR" and obj=="T") : c_algo_wp = "("+c_jet+"_1_DeepAK8_"+(obj+"vsQCD>0.852861)"
    if (wp == "JMAR" and obj=="T") : c_algo_wp = "("+c_jet+"_1_DeepAK8_"+"("+obj+"vsQCD>"+str(WP_Top_binarized)+")"
    elif (wp == "JMAR" and obj=="W") : c_algo_wp = "("+c_jet+"_1_DeepAK8_"+obj+"vsQCD>"+str(WP_Top_binarized)+")" 
    elif (wp == "L")    : c_algo_wp = "("+c_jet+"_1_DeepAK8_"+obj+"vsQCD>0.1883)" 
    elif (wp == "M")    : c_algo_wp = "("+c_jet+"_1_DeepAK8_"+obj+"vsQCD>0.8511)" 
    elif (wp == "T")    : c_algo_wp = "("+c_jet+"_1_DeepAK8_"+obj+"vsQCD>0.9377)" 
    elif (wp == "VT")   : c_algo_wp = "("+c_jet+"_1_DeepAK8_"+obj+"vsQCD>0.9897)" 

  elif (algo == "deepak8md") :
    c_jet = "ak8"; c_r = "0.8"
    # if (wp == "JMAR" and obj=="T") : c_algo_wp = "("+c_jet+"_1_DeepAK8MD_"+(obj+"vsQCD>0.436951)"
    if (wp == "JMAR" and obj=="T") : c_algo_wp = "("+c_jet+"_1_DeepAK8MD_"+"("+obj+"vsQCD>"+str(WP_Top_binarizedMD)+"))"
    elif (wp == "JMAR" and obj=="W") : c_algo_wp = "("+c_jet+"_1_DeepAK8MD_"+"("+obj+"vsQCD>"+str(WP_Top_binarizedMD)+"))"
    elif (wp == "L")    : c_algo_wp = "("+c_jet+"_1_DeepAK8MD_"+"("+obj+"vsQCD>0.1883))"
    elif (wp == "M")    : c_algo_wp = "("+c_jet+"_1_DeepAK8MD_"+"("+obj+"vsQCD>0.8511))"
    elif (wp == "T")    : c_algo_wp = "("+c_jet+"_1_DeepAK8MD_"+"("+obj+"vsQCD>0.9377))"
    elif (wp == "VT")   : c_algo_wp = "("+c_jet+"_1_DeepAK8MD_"+"("+obj+"vsQCD>0.9897))"

  elif (algo == "deepak8_raw"):
     c_jet = "ak8"; c_r = "0.8"
     # if (wp == "JMAR" and obj=="T") : c_algo_wp = "("+c_jet+"_1_DeepAK8_Top > 0.4)"
     if (wp == "JMAR" and obj=="T") : c_algo_wp = "("+c_jet+"_1_DeepAK8_Top >"+str(WP_Top_raw)+")"
     elif (wp == "JMAR" and obj=="W") : c_algo_wp = "("+c_jet+"_1_DeepAK8_W >"+str(WP_Top_raw)+")"

  elif (algo == "deepak8md_raw"):
     c_jet = "ak8"; c_r = "0.8"
     # if (wp == "JMAR" and obj=="T") : c_algo_wp = "("+c_jet+"_1_DeepAK8MD_Top > 0.0138089)"
     if (wp == "JMAR" and obj=="T") : c_algo_wp = "("+c_jet+"_1_DeepAK8MD_Top > "+str(WP_Top_rawMD)+")"
     elif (wp == "JMAR" and obj=="W") : c_algo_wp = "("+c_jet+"_1_DeepAK8MD_W > "+str(WP_Top_rawMD)+")"
 
  ## mass selection
  c_mass = "("+c_jet+"_1_mass>50. && "+c_jet+"_1_mass<250.)" 

  ## pt range
  if obj=="T" and ptrange == "incl"   : c_ptrange = "("+c_jet+"_1_pt>300.)"
  if obj=="T" and ptrange == "low"    : c_ptrange = "("+c_jet+"_1_pt>300. && "+c_jet+"_1_pt<=400.)" 
  if obj=="T" and ptrange == "lowmed" : c_ptrange = "("+c_jet+"_1_pt>400. && "+c_jet+"_1_pt<=480.)" 
  if obj=="T" and ptrange == "med"    : c_ptrange = "("+c_jet+"_1_pt>480. && "+c_jet+"_1_pt<=600.)" 
  if obj=="T" and ptrange == "medhi"  : c_ptrange = "("+c_jet+"_1_pt>600. && "+c_jet+"_1_pt<=1200.)"

  if obj=="W" and ptrange == "incl"   : c_ptrange = "("+c_jet+"_1_pt>200.)"
  if obj=="W" and ptrange == "low"    : c_ptrange = "("+c_jet+"_1_pt>200. && "+c_jet+"_1_pt<=300.)" 
  if obj=="W" and ptrange == "lowmed" : c_ptrange = "("+c_jet+"_1_pt>300. && "+c_jet+"_1_pt<=400.)" 
  if obj=="W" and ptrange == "med"    : c_ptrange = "("+c_jet+"_1_pt>400. && "+c_jet+"_1_pt<=800.)" 

  # pass or fail tagging score
  if Pass: c_algo_wp = "("+c_algo_wp+")" 
  else   : c_algo_wp = "!("+c_algo_wp+")"

  # matching definition
  c_p3 = "( ("+c_jet+"_1_dr_fj_top_wqmax<("+c_r+")) && ("+c_jet+"_1_dr_fj_top_b<("+c_r+")) )"
  c_p2 = "( (!"+c_p3+") && ("+c_jet+"_1_dr_fj_top_wqmax<"+c_r+") && ("+c_jet+"_1_dr_fj_top_b>"+c_r+") )"
  c_p1 = "(!("+c_p3+" || "+c_p2+"))"
  # c_p3 = "("+c_jet+"_1_isFullyMerged)" // && ak8_1_topSize>-1. && ak8_1_topSize<0.8 
  # c_p2 = "("+c_jet+"_1_isSemiMerged)"
  # c_p1 = "(!("+c_p3+" || "+c_p2+"))"

  # final set of cuts
  cut = c_base+" && "+c_algo_wp+" && "+c_mass+" && "+c_ptrange 
  print cut+"\n"
  
  cuts=[]
  cuts.append(cut)
  cuts.append(cut+" && "+c_p3)
  cuts.append(cut+" && "+c_p2)
  cuts.append(cut+" && "+c_p1)

  leg_sample=[]
  leg_sample.append("t-matched")
  leg_sample.append("W-matched")
  leg_sample.append("unmatched")
  leg_sample.append("Data")

  EOSCMS="root://eoscms.cern.ch/"
  # path = "/eos/uscms/store/group/lpcjme/noreplica/NanoHRT/Trees/Apr08/muon/"
  if year=="2016":
      path = EOSCMS
      path += "/eos/cms/store/group/phys_jetmet/nbinnorj/WTopTagging/ntuples_HRTSF/2016/"
 
  elif year=="2017":
      path = EOSCMS
      path += "/eos/cms/store/group/phys_jetmet/nbinnorj/WTopTagging/ntuples_HRTSF/29July/"
   
  elif year=="2018":
      # path = "/eos/uscms/store/user/pakontax/2018_Samples_From_Sicheng_For_Copy_V2/"
      path = EOSCMS
      path += "/eos/cms/store/group/phys_jetmet/nbinnorj/WTopTagging/ntuples_HRTSF/3Oct_For_Copy/"
 
  f_mc = ROOT.TFile.Open(path+"/mc_nom/sm_tree.root" , "READONLY" )
  print "path: "+path
  f_data = ROOT.TFile.Open(path+"/data/singlemu_tree.root" , "READONLY" )
  t_mc   = f_mc.Get("Events")
  t_data = f_data.Get("Events")

  ## inclusive distributions -- get overall normalization factor
  cut_incl  = c_base+" && "+c_mass+" && "+c_ptrange ## init 20,50.,250.
  h_mc_incl   = create1Dhisto(name,t_mc,lumi,cut_incl,c_jet+"_1_mass",20,50.,250.,False,1,1,"h_"+name+"_mc_incl",False,False) 
  h_mc_incl.SetFillColor(0)
  h_data_incl = create1Dhisto(name,t_data,lumi,cut_incl,c_jet+"_1_mass",20,50.,250.,False,1,1,"h_"+name+"_data_incl",False,True) 
  h_data_incl.SetFillColor(0)
  scalemc2data = h_data_incl.Integral()/h_mc_incl.Integral() 
  print str(h_data_incl.Integral()) + " " + str(h_mc_incl.Integral()) + " overall norm = " + str(scalemc2data) + "\n"
  tmpscalemc2data = scalemc2data
  scalemc2datastr = str(tmpscalemc2data) 
  print scalemc2datastr + "\n"
  
  h_data = create1Dhisto(name,t_data,lumi,cuts[0],c_jet+"_1_mass",20,50.,250.,False,1,1,"h_"+name+"_data",False,True) 
  h_data.SetFillColor(0)
  h_data.SetMarkerColor(1) 
  h_data.SetMarkerSize(1.2) 
  h_data.SetMarkerStyle(20)
  h_data.SetLineWidth(1)

  # make dir
  # dirname1 = workdir+"/"+obj+"_"+algo+"_"+syst+"_mist_rate_"+mistRate
  # dir_err = os.system("mkdir -p ./"+dirname1)
  # if (-1 == dir_err) : 
  #   print "Error creating directory!\n"
  #   exit(1)

  fout = ROOT.TFile(workdir+"/"+name+".root","RECREATE")
  h_data.Write("data_obs")

  makeHisto(name, path,lumi+"*"+scalemc2datastr,cuts,c_jet,"nom","nom",fout)
  makeHisto(name, path,lumi+"*"+scalemc2datastr,cuts,c_jet,"pu","up",fout)
  makeHisto(name, path,lumi+"*"+scalemc2datastr,cuts,c_jet,"pu","down",fout)
  makeHisto(name, path,lumi+"*"+scalemc2datastr,cuts,c_jet,"jer","up",fout)
  makeHisto(name, path,lumi+"*"+scalemc2datastr,cuts,c_jet,"jer","down",fout)
  makeHisto(name, path,lumi+"*"+scalemc2datastr,cuts,c_jet,"jes","up",fout)
  makeHisto(name, path,lumi+"*"+scalemc2datastr,cuts,c_jet,"jes","down",fout)
  makeHisto(name, path,lumi+"*"+scalemc2datastr,cuts,c_jet,"met","up",fout)
  makeHisto(name, path,lumi+"*"+scalemc2datastr,cuts,c_jet,"met","down",fout)
  makeHisto(name, path,lumi+"*"+scalemc2datastr+"*LHEScaleWeight[5]*LHEScaleWeightNorm[5]",cuts,c_jet,"lhescalemuf","up",fout)
  makeHisto(name, path,lumi+"*"+scalemc2datastr+"*LHEScaleWeight[3]*LHEScaleWeightNorm[3]",cuts,c_jet,"lhescalemuf","down",fout)
  makeHisto(name, path,lumi+"*"+scalemc2datastr+"*LHEScaleWeight[7]*LHEScaleWeightNorm[7]",cuts,c_jet,"lhescalemur","up",fout)
  makeHisto(name, path,lumi+"*"+scalemc2datastr+"*LHEScaleWeight[1]*LHEScaleWeightNorm[1]",cuts,c_jet,"lhescalemur","down",fout)
  makeHistoLHEPDF(name,path,lumi+"*"+scalemc2datastr,cuts,c_jet,"lhepdf","def",fout)
  if year==2016:
    makeHistoHerwig(name,path,lumi+"*"+scalemc2datastr,cuts,c_jet,"herwig",fout)
 

  fout.Close()
  print "\n\n"

def makeHisto(name_, path_, wgt_, cuts_, c_jet_, sys_, var_, f_) :

  if sys_=="nom" or sys_=="pu" : f_mc_ = ROOT.TFile.Open(path_+"/mc_nom/sm_tree.root","READONLY")
  elif "lhe" in sys_           : f_mc_ = ROOT.TFile.Open(path_+"/mc_sys/LHEWeight/sm_tree.root","READONLY")
  else                         : f_mc_ = ROOT.TFile.Open(path_+"/mc_sys/"+sys_+"_"+var_+"/sm_tree.root","READONLY")
  t_mc_ = f_mc_.Get("Events")

  ## create histos
  h_p3 = create1Dhisto(name_,t_mc_,wgt_,cuts_[1],c_jet_+"_1_mass",20,50.,250.,False,ROOT.kBlue,1,"h_"+name_+"_p3_"+sys_+var_,False,False)    ; h_p3.SetFillColor(0)
  h_p2 = create1Dhisto(name_,t_mc_,wgt_,cuts_[2],c_jet_+"_1_mass",20,50.,250.,False,ROOT.kRed+1,1,"h_"+name_+"_p2_"+sys_+var_,False,False)   ; h_p2.SetFillColor(0)
  h_p1 = create1Dhisto(name_,t_mc_,wgt_,cuts_[3],c_jet_+"_1_mass",20,50.,250.,False,ROOT.kGreen-1,1,"h_"+name_+"_p1_"+sys_+var_,False,False) ; h_p1.SetFillColor(0)

  ## avoid zero bins in mc
  for ii in range(0,h_p3.GetNbinsX()):
    if (h_p3.GetBinContent(ii)<=0) : h_p3.SetBinContent(ii,0.001); h_p3.SetBinError(ii,0.001)
    if (h_p2.GetBinContent(ii)<=0) : h_p2.SetBinContent(ii,0.001); h_p2.SetBinError(ii,0.001)
    if (h_p1.GetBinContent(ii)<=0) : h_p1.SetBinContent(ii,0.001); h_p1.SetBinError(ii,0.001)

  xname = "m_:SD} [GeV]"
  h_p3.GetXaxis().SetTitle(xname)
  h_p2.GetXaxis().SetTitle(xname)
  h_p1.GetXaxis().SetTitle(xname)

  if var_=="up" : var_f = "Up" 
  else          : var_f = "Down" 
  f_.cd()
  if sys_=="nom":
    h_p3.Write("catp3")
    h_p2.Write("catp2")
    h_p1.Write("catp1")
 
  else:
    h_p3.Write("catp3_"+sys_+var_f)
    h_p2.Write("catp2_"+sys_+var_f)
    h_p1.Write("catp1_"+sys_+var_f)

def makeHistoHerwig(name_, path_, wgt_,cuts_, c_jet_, sys_, f_) :

  f_mc_     = ROOT.TFile.Open(path_+"/mc_nom/sm_tree.root","READONLY")
  f_mc_her_ = ROOT.TFile.Open(path_+"/mc_nom/sm_herwig_tree.root","READONLY")

  t_mc_     = f_mc_.Get("Events")
  t_mc_her_ = f_mc_her_.Get("Events")

  ## fix normalization of incl sm and sm_her
  h_incl     = create1Dhisto(name_,t_mc_,wgt_,cuts_[0],c_jet_+"_1_mass",20,50.,250.,False,ROOT.kBlue,1,"h_"+name_+"_incl_"+sys_,False,False)    
  h_incl_her = create1Dhisto(name_,t_mc_her_,wgt_,cuts_[0],c_jet_+"_1_mass",20,50.,250.,False,ROOT.kBlue,1,"h_"+name_+"_incl_her_"+sys_,False,False)    
  her2mg = 1.; her2mg = (h_incl.Integral())/(h_incl_her.Integral())
  her2mg_ = str(her2mg)

  ## create histos
  h_p3 = create1Dhisto(name_,t_mc_,wgt_,cuts_[1],c_jet_+"_1_mass",20,50.,250.,False,ROOT.kBlue,1,"h_"+name_+"_p3_"+sys_+"_nom",False,False)    ; h_p3.SetFillColor(0)
  h_p2 = create1Dhisto(name_,t_mc_,wgt_,cuts_[2],c_jet_+"_1_mass",20,50.,250.,False,ROOT.kRed+1,1,"h_"+name_+"_p2_"+sys_+"_nom",False,False)   ; h_p2.SetFillColor(0)
  h_p1 = create1Dhisto(name_,t_mc_,wgt_,cuts_[3],c_jet_+"_1_mass",20,50.,250.,False,ROOT.kGreen-1,1,"h_"+name_+"_p1_"+sys_+"_nom",False,False) ; h_p1.SetFillColor(0)

  h_p3_up = create1Dhisto(name_,t_mc_her_,wgt_+"*"+her2mg_,cuts_[1],c_jet_+"_1_mass",20,50.,250.,False,ROOT.kBlue,1,"h_"+name_+"_p3_"+sys_+"_up",False,False)    ; h_p3_up.SetFillColor(0)
  h_p2_up = create1Dhisto(name_,t_mc_her_,wgt_+"*"+her2mg_,cuts_[2],c_jet_+"_1_mass",20,50.,250.,False,ROOT.kRed+1,1,"h_"+name_+"_p2_"+sys_+"_up",False,False)   ; h_p2_up.SetFillColor(0)
  h_p1_up = create1Dhisto(name_,t_mc_her_,wgt_+"*"+her2mg_,cuts_[3],c_jet_+"_1_mass",20,50.,250.,False,ROOT.kGreen-1,1,"h_"+name_+"_p1_"+sys_+"_up",False,False) ; h_p1_up.SetFillColor(0)

  h_p3_down = h_p3_up.Clone("h_p3_"+sys_+"_down"); h_p3_down.SetName("h_p3_"+sys_+"_down") 
  h_p2_down = h_p2_up.Clone("h_p2_"+sys_+"_down"); h_p2_down.SetName("h_p2_"+sys_+"_down") 
  h_p1_down = h_p1_up.Clone("h_p1_"+sys_+"_down"); h_p1_down.SetName("h_p1_"+sys_+"_down") 
  
  for i0 in range(0,h_p3_up.GetNbinsX()):
    h_p3_down.SetBinContent(i0, (h_p3_down.GetBinContent(i0)+2.*(h_p3.GetBinContent(i0)-h_p3_up.GetBinContent(i0))) )
    h_p2_down.SetBinContent(i0, (h_p2_down.GetBinContent(i0)+2.*(h_p2.GetBinContent(i0)-h_p2_up.GetBinContent(i0))) )
    h_p1_down.SetBinContent(i0, (h_p1_down.GetBinContent(i0)+2.*(h_p1.GetBinContent(i0)-h_p1_up.GetBinContent(i0))) )
 

  ## avoid zero bins in mc
  for ii in range(0,h_p3.GetNbinsX()):
    if (h_p3_up.GetBinContent(ii)<=0)   : h_p3_up.SetBinContent(ii,0.001);   h_p3_up.SetBinError(ii,0.001)
    if (h_p2_up.GetBinContent(ii)<=0)   : h_p2_up.SetBinContent(ii,0.001);   h_p2_up.SetBinError(ii,0.001)
    if (h_p1_up.GetBinContent(ii)<=0)   : h_p1_up.SetBinContent(ii,0.001);   h_p1_up.SetBinError(ii,0.001)
    if (h_p3_down.GetBinContent(ii)<=0) : h_p3_down.SetBinContent(ii,0.001); h_p3_down.SetBinError(ii,0.001)
    if (h_p2_down.GetBinContent(ii)<=0) : h_p2_down.SetBinContent(ii,0.001); h_p2_down.SetBinError(ii,0.001)
    if (h_p1_down.GetBinContent(ii)<=0) : h_p1_down.SetBinContent(ii,0.001); h_p1_down.SetBinError(ii,0.001)
 

  xname = "m_:SD} [GeV]"
  h_p3_up.GetXaxis().SetTitle(xname)
  h_p2_up.GetXaxis().SetTitle(xname)
  h_p1_up.GetXaxis().SetTitle(xname)
  h_p3_down.GetXaxis().SetTitle(xname)
  h_p2_down.GetXaxis().SetTitle(xname)
  h_p1_down.GetXaxis().SetTitle(xname)

  f_.cd()
  h_p3_up.Write("catp3_"+sys_+"Up")
  h_p2_up.Write("catp2_"+sys_+"Up")
  h_p1_up.Write("catp1_"+sys_+"Up")
  h_p3_down.Write("catp3_"+sys_+"Down")
  h_p2_down.Write("catp2_"+sys_+"Down")
  h_p1_down.Write("catp1_"+sys_+"Down")

def makeHistoLHEPDF(name_, path_, wgt_, cuts_, c_jet_, sys_, var_, f_) :

  ## nom
  f_mc_nom_ = ROOT.TFile.Open(path_+"/mc_nom/sm_tree.root","READONLY")
  t_mc_nom_ = f_mc_nom_.Get("Events")

  h_p3_up = create1Dhisto(name_,t_mc_nom_,wgt_,cuts_[1],c_jet_+"_1_mass",20,50.,250.,False,ROOT.kBlue,1,"h_"+name_+"_p3_"+sys_+"up",False,False)   ; h_p3_up.SetFillColor(0)
  h_p2_up = create1Dhisto(name_,t_mc_nom_,wgt_,cuts_[2],c_jet_+"_1_mass",20,50.,250.,False,ROOT.kRed+1,1,"h_"+name_+"_p2_"+sys_+"up",False,False)  ; h_p2_up.SetFillColor(0)
  h_p1_up = create1Dhisto(name_,t_mc_nom_,wgt_,cuts_[3],c_jet_+"_1_mass",20,50.,250.,False,ROOT.kGreen-1,1,"h_"+name_+"_p1_"+sys_+"up",False,False); h_p1_up.SetFillColor(0)
  h_p3_down = h_p3_up.Clone("h_"+name_+"_p3_"+sys_+"down")
  h_p2_down = h_p2_up.Clone("h_"+name_+"_p2_"+sys_+"down")
  h_p1_down = h_p1_up.Clone("h_"+name_+"_p1_"+sys_+"down")

  ## pdf
  f_mc_ = ROOT.TFile.Open(path_+"/mc_sys/LHEWeight/sm_tree.root","READONLY")
  t_mc_ = f_mc_.Get("Events")

  h_p3_v=[]
  h_p2_v=[]
  h_p1_v=[]

  for i in range(0,15):
    count = str(i) ## std::cout << i << " " << count << "\n"
    pdfwgt_ = "LHEPdfWeight["+count+"]*LHEPdfWeightNorm["+count+"]"
    h_p3_ = create1Dhisto(name_,t_mc_,wgt_+"*"+pdfwgt_,cuts_[1],c_jet_+"_1_mass",20,50.,250.,False,ROOT.kBlue,1,"h_"+name_+"_p3_"+sys_+var_+"_"+count,False,False)   ; h_p3_.SetFillColor(0)
    h_p2_ = create1Dhisto(name_,t_mc_,wgt_+"*"+pdfwgt_,cuts_[2],c_jet_+"_1_mass",20,50.,250.,False,ROOT.kRed+1,1,"h_"+name_+"_p2_"+sys_+var_+"_"+count,False,False)  ; h_p2_.SetFillColor(0)
    h_p1_ = create1Dhisto(name_,t_mc_,wgt_+"*"+pdfwgt_,cuts_[3],c_jet_+"_1_mass",20,50.,250.,False,ROOT.kGreen-1,1,"h_"+name_+"_p1_"+sys_+var_+"_"+count,False,False); h_p1_.SetFillColor(0)
    h_p3_v.append(h_p3_) 
    h_p2_v.append(h_p2_)
    h_p1_v.append(h_p1_)  
 
  ## get rms and sigma
  for ibin in range(0,h_p3_v[0].GetNbinsX()):
    mean_p3_  = 0.; mean_p2_  = 0.; mean_p1_  = 0. 
    rms_p3_   = 0.; rms_p2_   = 0.; rms_p1_   = 0.
    sigma_p3_ = 0.; sigma_p2_ = 0.; sigma_p1_ = 0.
    for ihisto in range(0,len(h_p3_v)):
      mean_p3_ += h_p3_v[ihisto].GetBinContent(ibin)                                         
      rms_p3_  += (h_p3_v[ihisto].GetBinContent(ibin))*(h_p3_v[ihisto].GetBinContent(ibin)) 
      mean_p2_ += h_p2_v[ihisto].GetBinContent(ibin)                                         
      rms_p2_  += (h_p2_v[ihisto].GetBinContent(ibin))*(h_p2_v[ihisto].GetBinContent(ibin)) 
      mean_p1_ += h_p1_v[ihisto].GetBinContent(ibin)                                         
      rms_p1_  += (h_p1_v[ihisto].GetBinContent(ibin))*(h_p1_v[ihisto].GetBinContent(ibin)) 
   
    mean_p3_ = mean_p3_/len(h_p3_v); rms_p3_ = np.sqrt(rms_p3_/len(h_p3_v)); sigma_p3_ = np.sqrt((rms_p3_*rms_p3_) - (mean_p3_*mean_p3_)) 
    mean_p2_ = mean_p2_/len(h_p2_v); rms_p2_ = np.sqrt(rms_p2_/len(h_p2_v)); sigma_p2_ = np.sqrt((rms_p2_*rms_p2_) - (mean_p2_*mean_p2_)) 
    mean_p1_ = mean_p1_/len(h_p1_v); rms_p1_ = np.sqrt(rms_p1_/len(h_p1_v)); sigma_p1_ = np.sqrt((rms_p1_*rms_p1_) - (mean_p1_*mean_p1_)) 

    h_p3_up.SetBinContent(ibin,h_p3_up.GetBinContent(ibin)+sigma_p3_); h_p3_down.SetBinContent(ibin,h_p3_down.GetBinContent(ibin)-sigma_p3_)
    h_p2_up.SetBinContent(ibin,h_p2_up.GetBinContent(ibin)+sigma_p2_); h_p2_down.SetBinContent(ibin,h_p2_down.GetBinContent(ibin)-sigma_p2_)
    h_p1_up.SetBinContent(ibin,h_p1_up.GetBinContent(ibin)+sigma_p1_); h_p1_down.SetBinContent(ibin,h_p1_down.GetBinContent(ibin)-sigma_p1_)
 
  

  ## avoid zero bins in mc
  for ii in range(0,h_p3_up.GetNbinsX()):
    if (h_p3_up.GetBinContent(ii)<=0)   : h_p3_up.SetBinContent(ii,0.001)  ; h_p3_up.SetBinError(ii,0.001)
    if (h_p2_up.GetBinContent(ii)<=0)   : h_p2_up.SetBinContent(ii,0.001)  ; h_p2_up.SetBinError(ii,0.001)
    if (h_p1_up.GetBinContent(ii)<=0)   : h_p1_up.SetBinContent(ii,0.001)  ; h_p1_up.SetBinError(ii,0.001)
    if (h_p3_down.GetBinContent(ii)<=0) : h_p3_down.SetBinContent(ii,0.001); h_p3_down.SetBinError(ii,0.001)
    if (h_p2_down.GetBinContent(ii)<=0) : h_p2_down.SetBinContent(ii,0.001); h_p2_down.SetBinError(ii,0.001)
    if (h_p1_down.GetBinContent(ii)<=0) : h_p1_down.SetBinContent(ii,0.001); h_p1_down.SetBinError(ii,0.001)
 
  xname = "m_:SD} [GeV]"
  h_p3_up.GetXaxis().SetTitle(xname)
  h_p2_up.GetXaxis().SetTitle(xname)
  h_p1_up.GetXaxis().SetTitle(xname)
  h_p3_down.GetXaxis().SetTitle(xname)
  h_p2_down.GetXaxis().SetTitle(xname)
  h_p1_down.GetXaxis().SetTitle(xname)

  f_.cd()
  h_p3_up.Write("catp3_"+sys_+"Up")
  h_p2_up.Write("catp2_"+sys_+"Up")
  h_p1_up.Write("catp1_"+sys_+"Up")
  h_p3_down.Write("catp3_"+sys_+"Down")
  h_p2_down.Write("catp2_"+sys_+"Down")
  h_p1_down.Write("catp1_"+sys_+"Down")

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