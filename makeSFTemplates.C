#include "setTDRStyle.h"
#include <sstream>
#include <fstream>
#include "TTree.h"
#include "TFile.h"
#include "TH1.h"
#include "TH1D.h"
#include <vector>
#include "Rtypes.h"
#include "TColor.h"
#include "TVectorF.h"
#include <cstdlib>

TH1D *create1Dhisto(TString sample, TTree *tree,TString intLumi,TString cuts,TString branch,int bins,float xmin,float xmax,
		    bool useLog,int color, int style,TString name,bool norm,bool data);
void setTDRStyle();

void makeSFTemplates(TString object, TString algo, TString wp, TString ptrange, bool pass) {

  TString passstr = "pass"; if (pass) { passstr = "pass"; } else { passstr = "fail"; }
  TString name = object+"_"+algo+"_"+wp+"_"+ptrange+"_"+passstr;

  setTDRStyle();
  gROOT->SetBatch(true);
  gStyle->SetOptStat(0);
  gStyle->SetOptFit(1);
  gStyle->SetPalette(1);
  TH1::SetDefaultSumw2(kTRUE);

  //TFile *f_mc   = TFile::Open("/eos/uscms/store/user/lpcjme/JPilotOutputs/HRTTrees/top_tree.root"  , "READONLY" );
  //TFile *f_data = TFile::Open("/eos/uscms/store/user/lpcjme/JPilotOutputs/HRTTrees/data_tree.root" , "READONLY" );
  TFile *f_mc   = TFile::Open("/eos/uscms/store/user/lpcjme/LGOutputs/hrt_muon_20190225/sm.root"            , "READONLY" );
  TFile *f_data = TFile::Open("/eos/uscms/store/user/lpcjme/LGOutputs/hrt_muon_20190225/singlemu_tree.root" , "READONLY" );
  TTree *t_mc   = (TTree*)f_mc->Get("Events");
  TTree *t_data = (TTree*)f_data->Get("Events");
  
  std::vector<TTree *> samples; samples.clear();
  samples.push_back(t_mc);
  samples.push_back(t_data);

  float intLumi     = 36.8;
  ostringstream tmpLumi;
  tmpLumi << intLumi;
  TString lumi = tmpLumi.str();


  // baseline selection
  TString c_base = "(n_ak8>=1 && n_ca15>=1)";

  // selection on algo
  TString c_algo_wp;
  TString c_jet, c_r;
  if (algo == "sdtau32") { 
    c_jet = "ak8"; c_r = "0.8";
    if (wp == "JMAR") { c_algo_wp = "(("+c_jet+"_1_tau3/"+c_jet+"_1_tau2)<0.52)"; }
  }

  if (algo == "sdtau32btag") { 
    c_jet = "ak8"; c_r = "0.8";
    if (wp == "JMAR") { c_algo_wp = "(("+c_jet+"_1_tau3/"+c_jet+"_1_tau2)<0.52 && max("+c_jet+"_1_sj1_btagCSVV2,"+c_jet+"_1_sj2_btagCSVV2)>0.5426)"; }
  }

  if (algo == "ecftoptag") { 
    c_jet = "ca15"; c_r = "1.5";
    if (wp == "JMAR") { c_algo_wp = "( ca15_1_ecfTopTagBDT>-1. && (0.5+0.5*ca15_1_ecfTopTagBDT)>0.87)"; }
  }

  if (algo == "sdtau21") { 
    c_jet = "ak8"; c_r = "0.8";
    if (wp == "JMAR") { c_algo_wp = "(("+c_jet+"_1_tau2/"+c_jet+"_1_tau1)<0.68)"; }
  }

  if (algo == "sdn2") { 
    c_jet = "ak8"; c_r = "0.8";
    if (wp == "JMAR") { c_algo_wp = "("+c_jet+"_1_n2b1<0.74)"; }
  }

  if (algo == "sdn2ddt") { 
    c_jet = "ak8"; c_r = "0.8";
    if (wp == "JMAR") { c_algo_wp = "("+c_jet+"_1_n2b1ddt<0.91)"; }
  }

  if (algo == "hotvr") { 
    c_jet = "hotvr"; c_r = "1.5";
    if (wp == "JMAR") { c_algo_wp = "( && hotvr_1_fpt<0.8 && hotvr_1_nsubjets>=3 && hotvr_1_mmin>=50. && (1-hotvr_1_tau32)>0.57)"; }
  }
  
  if (algo == "best") { 
    c_jet = "ak8"; c_r = "0.8";
    if (wp == "JMAR" && object=="T") { c_algo_wp = "("+c_jet+"_1_best_"+(TString)object+"vsQCD>0.94)"; }
    if (wp == "JMAR" && object=="W") { c_algo_wp = "("+c_jet+"_1_best_"+(TString)object+"vsQCD>0.77)"; } 
    if (wp == "L")    { c_algo_wp = "("+c_jet+"_1_best_"+(TString)object+"vsQCD>0.1883)"; }
    if (wp == "M")    { c_algo_wp = "("+c_jet+"_1_best_"+(TString)object+"vsQCD>0.8511)"; }
    if (wp == "T")    { c_algo_wp = "("+c_jet+"_1_best_"+(TString)object+"vsQCD>0.9377)"; }
    if (wp == "VT")   { c_algo_wp = "("+c_jet+"_1_best_"+(TString)object+"vsQCD>0.9897)"; }
  }

  if (algo == "imagetop") { 
    c_jet = "ak8"; c_r = "0.8";
    if (wp == "JMAR" && object=="T") { c_algo_wp = "("+c_jet+"_1_image_top>0.98)"; }
  }

  if (algo == "imagetopmd") { 
    c_jet = "ak8"; c_r = "0.8";
    if (wp == "JMAR" && object=="T") { c_algo_wp = "("+c_jet+"_1_image_top>0.98)"; }
  }

  if (algo == "deepak8") { 
    c_jet = "ak8"; c_r = "0.8";
    if (wp == "JMAR" && object=="T") { c_algo_wp = "("+c_jet+"_1_DeepAK8_"+(TString)object+"vsQCD>0.98)"; }
    if (wp == "JMAR" && object=="W") { c_algo_wp = "("+c_jet+"_1_DeepAK8_"+(TString)object+"vsQCD>0.94)"; }
    if (wp == "L")    { c_algo_wp = "("+c_jet+"_1_DeepAK8_"+(TString)object+"vsQCD>0.1883)"; }
    if (wp == "M")    { c_algo_wp = "("+c_jet+"_1_DeepAK8_"+(TString)object+"vsQCD>0.8511)"; }
    if (wp == "T")    { c_algo_wp = "("+c_jet+"_1_DeepAK8_"+(TString)object+"vsQCD>0.9377)"; }
    if (wp == "VT")   { c_algo_wp = "("+c_jet+"_1_DeepAK8_"+(TString)object+"vsQCD>0.9897)"; }
  }

  if (algo == "deepak8md") { 
    c_jet = "ak8"; c_r = "0.8";
    if (wp == "JMAR" && object=="T") { c_algo_wp = "("+c_jet+"_1_DeepAK8MD_"+(TString)object+"vsQCD>0.80)"; }
    if (wp == "JMAR" && object=="W") { c_algo_wp = "("+c_jet+"_1_DeepAK8MD_"+(TString)object+"vsQCD>0.56)"; }
    if (wp == "L")    { c_algo_wp = "("+c_jet+"_1_DeepAK8MD_"+(TString)object+"vsQCD>0.1883)"; }
    if (wp == "M")    { c_algo_wp = "("+c_jet+"_1_DeepAK8MD_"+(TString)object+"vsQCD>0.8511)"; }
    if (wp == "T")    { c_algo_wp = "("+c_jet+"_1_DeepAK8MD_"+(TString)object+"vsQCD>0.9377)"; }
    if (wp == "VT")   { c_algo_wp = "("+c_jet+"_1_DeepAK8MD_"+(TString)object+"vsQCD>0.9897)"; }
  }

  // mass selection
  TString c_mass = "("+c_jet+"_1_mass>50. && "+c_jet+"_1_mass<250.)"; 
  
  // pt range
  TString c_ptrange;
  if ( ((TString)object=="T") && (ptrange == "incl") )   { c_ptrange = "("+c_jet+"_1_pt>300.)"; }
  if ( ((TString)object=="T") && (ptrange == "low") )    { c_ptrange = "("+c_jet+"_1_pt>300. && "+c_jet+"_1_pt<=400.)";  }
  if ( ((TString)object=="T") && (ptrange == "lowmed") ) { c_ptrange = "("+c_jet+"_1_pt>400. && "+c_jet+"_1_pt<=480.)";  }
  if ( ((TString)object=="T") && (ptrange == "med") )    { c_ptrange = "("+c_jet+"_1_pt>480. && "+c_jet+"_1_pt<=600.)";  }
  if ( ((TString)object=="T") && (ptrange == "medhi") )  { c_ptrange = "("+c_jet+"_1_pt>600. && "+c_jet+"_1_pt<=1200.)"; }

  if ( ((TString)object=="W") && (ptrange == "incl") )   { c_ptrange = "("+c_jet+"_1_pt>200.)"; }
  if ( ((TString)object=="W") && (ptrange == "low") )    { c_ptrange = "("+c_jet+"_1_pt>200. && "+c_jet+"_1_pt<=300.)";  }
  if ( ((TString)object=="W") && (ptrange == "lowmed") ) { c_ptrange = "("+c_jet+"_1_pt>300. && "+c_jet+"_1_pt<=400.)";  }
  if ( ((TString)object=="W") && (ptrange == "med") )    { c_ptrange = "("+c_jet+"_1_pt>400. && "+c_jet+"_1_pt<=800.)";  }

  // pass or fail tagging score
  if (pass) { c_algo_wp = "("+c_algo_wp+")";  }
  else      { c_algo_wp = "!("+c_algo_wp+")"; }

  // mtaching definition
  TString c_p3 = "( ("+c_jet+"_1_dr_fj_top_wqmax<"+c_r+") && ("+c_jet+"_1_dr_fj_top_b<"+c_r+") )";
  TString c_p2 = "( (!"+c_p3+") && ("+c_jet+"_1_dr_fj_top_wqmax<"+c_r+") && ("+c_jet+"_1_dr_fj_top_b>"+c_r+") )";
  TString c_p1 = "(!("+c_p3+" || "+c_p2+"))";
  //TString c_p3 = "("+c_jet+"_1_isFullyMerged)"; // && ak8_1_topSize>-1. && ak8_1_topSize<0.8 
  //TString c_p2 = "("+c_jet+"_1_isSemiMerged)";
  //TString c_p1 = "(!("+c_p3+" || "+c_p2+"))";

  // final set of cuts
  TString cut = c_base+" && "+c_algo_wp+" && "+c_mass+" && "+c_ptrange; std::cout << cut << "\n";
  std::vector<TString> cuts; cuts.clear();
  cuts.push_back(cut);
  cuts.push_back(cut+" && "+c_p3);
  cuts.push_back(cut+" && "+c_p2);
  cuts.push_back(cut+" && "+c_p1);

  std::vector<TString> leg_sample; leg_sample.clear();
  leg_sample.push_back("t-matched");
  leg_sample.push_back("W-matched");
  leg_sample.push_back("unmatched");
  leg_sample.push_back("Data");

  // create histos
  TH1D *h_incl = create1Dhisto(name,samples[0],lumi,cuts[0],c_jet+"_1_mass",20,50.,250.,false,1,1,"h_"+name+"_incl",false,false);      h_incl->SetFillColor(0);
  TH1D *h_p3   = create1Dhisto(name,samples[0],lumi,cuts[1],c_jet+"_1_mass",20,50.,250.,false,kBlue,1,"h_"+name+"_p3",false,false);    h_p3->SetFillColor(0);
  TH1D *h_p2   = create1Dhisto(name,samples[0],lumi,cuts[2],c_jet+"_1_mass",20,50.,250.,false,kRed+1,1,"h_"+name+"_p2",false,false);   h_p2->SetFillColor(0);
  TH1D *h_p1   = create1Dhisto(name,samples[0],lumi,cuts[3],c_jet+"_1_mass",20,50.,250.,false,kGreen-1,1,"h_"+name+"_p1",false,false); h_p1->SetFillColor(0);

  TH1D *h_data = create1Dhisto(name,samples[1],lumi,cuts[0],c_jet+"_1_mass",20,50.,250.,false,1,1,"h_"+name+"_data",false,true); h_data->SetFillColor(0);
  h_data->SetMarkerColor(1); h_data->SetMarkerSize(1.2); h_data->SetMarkerStyle(20);
  h_data->SetLineWidth(1);

  // pileup syst
  TH1D *h_p3_puup = create1Dhisto(name,samples[0],lumi,cuts[1],c_jet+"_1_mass",20,50.,250.,false,kBlue,1,"h_"+name+"_p3_puup",false,false);    h_p3_puup->SetFillColor(0);
  TH1D *h_p2_puup = create1Dhisto(name,samples[0],lumi,cuts[2],c_jet+"_1_mass",20,50.,250.,false,kRed+1,1,"h_"+name+"_p2_puup",false,false);   h_p2_puup->SetFillColor(0);
  TH1D *h_p1_puup = create1Dhisto(name,samples[0],lumi,cuts[3],c_jet+"_1_mass",20,50.,250.,false,kGreen-1,1,"h_"+name+"_p1_puup",false,false); h_p1_puup->SetFillColor(0);

  TH1D *h_p3_pudn = create1Dhisto(name,samples[0],lumi,cuts[1],c_jet+"_1_mass",20,50.,250.,false,kBlue,1,"h_"+name+"_p3_pudn",false,false);    h_p3_pudn->SetFillColor(0);
  TH1D *h_p2_pudn = create1Dhisto(name,samples[0],lumi,cuts[2],c_jet+"_1_mass",20,50.,250.,false,kRed+1,1,"h_"+name+"_p2_pudn",false,false);   h_p2_pudn->SetFillColor(0);
  TH1D *h_p1_pudn = create1Dhisto(name,samples[0],lumi,cuts[3],c_jet+"_1_mass",20,50.,250.,false,kGreen-1,1,"h_"+name+"_p1_pudn",false,false); h_p1_pudn->SetFillColor(0);
  

  // avoid zero bins in mc
  for (unsigned int ii=0; ii<h_p3->GetNbinsX(); ++ii) {
    if (h_p3->GetBinContent(ii)<=0) { h_p3->SetBinContent(ii,0.001); h_p3->SetBinError(ii,0.001); }
    if (h_p2->GetBinContent(ii)<=0) { h_p2->SetBinContent(ii,0.001); h_p2->SetBinError(ii,0.001); }
    if (h_p1->GetBinContent(ii)<=0) { h_p1->SetBinContent(ii,0.001); h_p1->SetBinError(ii,0.001); }
    /*if (h_herwig_p3_Up->GetBinContent(ii)<=0) { h_herwig_p3_Up->SetBinContent(ii,0.001); h_herwig_p3_Up->SetBinError(ii,0.001); }
    if (h_herwig_p2_Up->GetBinContent(ii)<=0) { h_herwig_p2_Up->SetBinContent(ii,0.001); h_herwig_p2_Up->SetBinError(ii,0.001); }
    if (h_herwig_p1_Up->GetBinContent(ii)<=0) { h_herwig_p1_Up->SetBinContent(ii,0.001); h_herwig_p1_Up->SetBinError(ii,0.001); }
    if (h_herwig_p3_Down->GetBinContent(ii)<=0) { h_herwig_p3_Down->SetBinContent(ii,0.001); h_herwig_p3_Down->SetBinError(ii,0.001); }
    if (h_herwig_p2_Down->GetBinContent(ii)<=0) { h_herwig_p2_Down->SetBinContent(ii,0.001); h_herwig_p2_Down->SetBinError(ii,0.001); }
    if (h_herwig_p1_Down->GetBinContent(ii)<=0) { h_herwig_p1_Down->SetBinContent(ii,0.001); h_herwig_p1_Down->SetBinError(ii,0.001); }*/
    if (h_p3_puup->GetBinContent(ii)<=0) { h_p3_puup->SetBinContent(ii,0.001); h_p3_puup->SetBinError(ii,0.001); }
    if (h_p2_puup->GetBinContent(ii)<=0) { h_p2_puup->SetBinContent(ii,0.001); h_p2_puup->SetBinError(ii,0.001); }
    if (h_p1_puup->GetBinContent(ii)<=0) { h_p1_puup->SetBinContent(ii,0.001); h_p1_puup->SetBinError(ii,0.001); }
    if (h_p3_pudn->GetBinContent(ii)<=0) { h_p3_pudn->SetBinContent(ii,0.001); h_p3_pudn->SetBinError(ii,0.001); }
    if (h_p2_pudn->GetBinContent(ii)<=0) { h_p2_pudn->SetBinContent(ii,0.001); h_p2_pudn->SetBinError(ii,0.001); }
    if (h_p1_pudn->GetBinContent(ii)<=0) { h_p1_pudn->SetBinContent(ii,0.001); h_p1_pudn->SetBinError(ii,0.001); }
  }

  TString xname = "m_{SD} [GeV]";
  h_p3->GetXaxis()->SetTitle(xname);
  h_p2->GetXaxis()->SetTitle(xname);
  h_p1->GetXaxis()->SetTitle(xname);
  h_data->GetXaxis()->SetTitle(xname);
  /*h_herwig_p3_Up->GetXaxis()->SetTitle((TString)xname);
  h_herwig_p2_Up->GetXaxis()->SetTitle((TString)xname);
  h_herwig_p1_Up->GetXaxis()->SetTitle((TString)xname);
  h_herwig_p3_Down->GetXaxis()->SetTitle((TString)xname);
  h_herwig_p2_Down->GetXaxis()->SetTitle((TString)xname);
  h_herwig_p1_Down->GetXaxis()->SetTitle((TString)xname);*/
  h_p3_puup->GetXaxis()->SetTitle((TString)xname);
  h_p2_puup->GetXaxis()->SetTitle((TString)xname);
  h_p1_puup->GetXaxis()->SetTitle((TString)xname);
  h_p3_pudn->GetXaxis()->SetTitle((TString)xname);
  h_p2_pudn->GetXaxis()->SetTitle((TString)xname);
  h_p1_pudn->GetXaxis()->SetTitle((TString)xname);

  
  // make dir
  TString dirname1 = object+"_"+algo;
  const int dir_err = system("mkdir -p ./"+dirname1);
  if (-1 == dir_err) { printf("Error creating directory!n"); exit(1); }

  TString nameoutfile = name+".root"; 
  TFile *fout = new TFile("./"+dirname1+"/"+nameoutfile,"RECREATE");

  h_p3->Write("catp3");
  h_p2->Write("catp2");
  h_p1->Write("catp1");
  h_data->Write("data_obs");
  /*h_herwig_p3_Up->Write("flvC_herwigUp");
  h_herwig_p2_Up->Write("flvB_herwigUp");
  h_herwig_p1_Up->Write("flvL_herwigUp");
  h_herwig_p3_Down->Write("flvC_herwigDown");
  h_herwig_p2_Down->Write("flvB_herwigDown");
  h_herwig_p1_Down->Write("flvL_herwigDown");*/
  /*flvC_her->Write("flvC_her");
  flvB_her->Write("flvB_her");
  flvL_her->Write("flvL_her");*/
  h_p3_puup->Write("catp3_puUp");
  h_p2_puup->Write("catp2_puUp");
  h_p1_puup->Write("catp1_puUp");
  h_p3_pudn->Write("catp3_puDown");
  h_p2_pudn->Write("catp2_puDown");
  h_p1_pudn->Write("catp1_puDown");
  fout->Close();
  std::cout << "\n\n";
}


TH1D *create1Dhisto(TString sample,TTree *tree,TString intLumi,TString cuts,TString branch,int bins,float xmin,float xmax,
		    bool useLog,int color, int style,TString name,bool norm,bool data) {
  TH1::SetDefaultSumw2(kTRUE);

  TString cut;
  //  if (data) { cut ="(passMuTrig && "+cuts+")"; } 
  if (data) { cut ="("+cuts+")"; } 
  else {
    if      (name.Contains("puup")) { cut ="(xsecWeight*puWeightUp*"+intLumi+")*("+cuts+")"; }
    else if (name.Contains("pudn")) { cut ="(xsecWeight*puWeightDown*"+intLumi+")*("+cuts+")"; }
    else if (name.Contains("herw")) { cut ="(xsecWeight*puWeight*"+intLumi+")*("+cuts+")"; }
    else                            { cut ="(xsecWeight*puWeight*"+intLumi+")*("+cuts+")"; }
  }
  
  std::cout << "cut = " << cut << "\n";

  TH1D *hTemp = new TH1D(name,name,bins,xmin,xmax); //hTemp->SetName(name);
  tree->Project(name,branch,cut);

  hTemp->SetLineWidth(3);
  hTemp->SetMarkerSize(0);
  hTemp->SetLineColor(color);
  hTemp->SetFillColor(color);
  hTemp->SetLineStyle(style);

  // ad overflow bin             
  double error =0.; double integral = hTemp->IntegralAndError(bins,bins+1,error);
  hTemp->SetBinContent(bins,integral);
  hTemp->SetBinError(bins,error);

  if (norm) { hTemp->Scale(1./(hTemp->Integral())); }

  return hTemp;
} //~ end of create1Dhisto
