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
#include <math.h>
#include <string>
#include <cstring>
#include <TArray.h>

void makeHistoHerwig(TString name_, TString path_, TString wgt_, std::vector<TString> cuts_, TString c_jet_, TString sys_, TFile *f_);
void makeHistoLHEPDF(TString name_, TString path_, TString wgt_, std::vector<TString> cuts_, TString c_jet_, TString sys_, TString var_, TFile *f_);
void makeHisto(TString name_, TString path_, TString wgt_, std::vector<TString> cuts_, TString c_jet_, TString sys_, TString var_, TFile *f_);
TH1D *create1Dhisto(TString sample, TTree *tree,TString intLumi,TString cuts,TString branch,int bins,float xmin,float xmax,
		    bool useLog,int color, int style,TString name,bool norm,bool data);
void setTDRStyle();

void makeSFTemplates(TString object, TString algo, TString wp, TString ptrange, TString syst, bool pass, TString mistRate, float WP_Top_binarized, float WP_Top_binarizedMD, float WP_Top_raw, float WP_Top_rawMD, int year, TString workdir) {

  TString passstr = "pass"; if (pass) { passstr = "pass"; } else { passstr = "fail"; }
  TString name = object+"_"+algo+"_"+wp+"_"+ptrange+"_"+passstr;

  setTDRStyle();
  gROOT->SetBatch(true);
  gStyle->SetOptStat(0);
  gStyle->SetOptFit(1);
  gStyle->SetPalette(1);
  TH1::SetDefaultSumw2(kTRUE);

  float intLumi;
 
  if (year == 2016){
       intLumi = 36.8;
  }
  else if(year == 2017){
       intLumi = 41.53;
  }
  else if(year == 2018){
       intLumi = 59.74;
  }

  ostringstream tmpLumi;
  tmpLumi << intLumi;
  TString lumi = tmpLumi.str();


  // baseline selection
  TString c_base;
  if (year == 2016){    
       c_base = "(n_ak8>=1 && n_ca15>=1)";
  }
  else if (year == 2017 || year == 2018){
       c_base = "(n_ak8>=1)";
  }


  // selection on algo
  TString c_algo_wp;
  TString c_jet, c_r;
  
  if (algo == "sdtau32") { 
    c_jet = "ak8"; c_r = "0.8";
    if (wp == "JMAR") { c_algo_wp = "((1-"+c_jet+"_1_tau3/"+c_jet+"_1_tau2)>0.4422)"; }
  }
  if (algo == "sdtau32btag") { 
    c_jet = "ak8"; c_r = "0.8";
    if (wp == "JMAR") { c_algo_wp = "((1-"+c_jet+"_1_tau3/"+c_jet+"_1_tau2)>0.3973 && max("+c_jet+"_1_sj1_btagCSVV2,"+c_jet+"_1_sj2_btagCSVV2)>0.5426)"; }
  }

  if (algo == "ecftoptag") { 
    c_jet = "ca15"; c_r = "1.5";
    if (wp == "JMAR") { c_algo_wp = "( ca15_1_ecfTopTagBDT>-1. && (0.5+0.5*ca15_1_ecfTopTagBDT)>0.5988)"; }
  }

  if (algo == "sdtau21") { 
    c_jet = "ak8"; c_r = "0.8";
    if (wp == "JMAR") { c_algo_wp = "((1-"+c_jet+"_1_tau2/"+c_jet+"_1_tau1)>0.6514)"; }
  }

  if (algo == "sdn2") { 
    c_jet = "ak8"; c_r = "0.8";
    //    if (wp == "JMAR") { c_algo_wp = "((1-"+c_jet+"_1_n2b1)>0.7339)"; }
    if (wp == "JMAR") { c_algo_wp = "((1-"+c_jet+"_1_n2b1)>0.7939)"; }
  }

  if (algo == "sdn2ddt") { 
    c_jet = "ak8"; c_r = "0.8";
    if (wp == "JMAR") { c_algo_wp = "((0.5-0.5*"+c_jet+"_1_n2b1ddt)>0.4767)"; }
  }

  if (algo == "hotvr") { 
    c_jet = "hotvr"; c_r = "1.5";
    if (wp == "JMAR") { c_algo_wp = "( hotvr_1_fpt<0.8 && hotvr_1_nsubjets>=3 && hotvr_1_mmin>=50. && (1-hotvr_1_tau32)>0.4504)"; }
  }
  
  if (algo == "best") { 
    c_jet = "ak8"; c_r = "0.8";
    if (wp == "JMAR" && object=="T") { c_algo_wp = "("+c_jet+"_1_best_"+(TString)object+"vsQCD>0.9119)"; }
    if (wp == "JMAR" && object=="W") { c_algo_wp = "("+c_jet+"_1_best_"+(TString)object+"vsQCD>0.8759)"; } 
    if (wp == "L")    { c_algo_wp = "("+c_jet+"_1_best_"+(TString)object+"vsQCD>0.1883)"; }
    if (wp == "M")    { c_algo_wp = "("+c_jet+"_1_best_"+(TString)object+"vsQCD>0.8511)"; }
    if (wp == "T")    { c_algo_wp = "("+c_jet+"_1_best_"+(TString)object+"vsQCD>0.9377)"; }
    if (wp == "VT")   { c_algo_wp = "("+c_jet+"_1_best_"+(TString)object+"vsQCD>0.9897)"; }
  }

  if (algo == "imagetop") { 
    c_jet = "ak8"; c_r = "0.8";
    if (wp == "JMAR" && object=="T") { c_algo_wp = "("+c_jet+"_1_image_top>0.9669)"; }
  }

  if (algo == "imagetopmd") { 
    c_jet = "ak8"; c_r = "0.8";
    if (wp == "JMAR" && object=="T") { c_algo_wp = "("+c_jet+"_1_image_top>0.9603)"; }
  }

  if (algo == "deepak8") { 
    c_jet = "ak8"; c_r = "0.8";
    //if (wp == "JMAR" && object=="T") { c_algo_wp = "("+c_jet+"_1_DeepAK8_"+(TString)object+"vsQCD>0.852861)"; }
    if (wp == "JMAR" && object=="T") { c_algo_wp = "("+c_jet+"_1_DeepAK8_"+(TString)object+"vsQCD>"+to_string(WP_Top_binarized)+")"; }
    if (wp == "JMAR" && object=="W") { c_algo_wp = "("+c_jet+"_1_DeepAK8_"+(TString)object+"vsQCD>"+to_string(WP_Top_binarized)+")"; }
    if (wp == "L")    { c_algo_wp = "("+c_jet+"_1_DeepAK8_"+(TString)object+"vsQCD>0.1883)"; }
    if (wp == "M")    { c_algo_wp = "("+c_jet+"_1_DeepAK8_"+(TString)object+"vsQCD>0.8511)"; }
    if (wp == "T")    { c_algo_wp = "("+c_jet+"_1_DeepAK8_"+(TString)object+"vsQCD>0.9377)"; }
    if (wp == "VT")   { c_algo_wp = "("+c_jet+"_1_DeepAK8_"+(TString)object+"vsQCD>0.9897)"; }
  }

  if (algo == "deepak8md") {
    c_jet = "ak8"; c_r = "0.8";
    //if (wp == "JMAR" && object=="T") { c_algo_wp = "("+c_jet+"_1_DeepAK8MD_"+(TString)object+"vsQCD>0.436951)"; }
    if (wp == "JMAR" && object=="T") { c_algo_wp = "("+c_jet+"_1_DeepAK8MD_"+(TString)object+"vsQCD>"+to_string(WP_Top_binarizedMD)+")"; }
    if (wp == "JMAR" && object=="W") { c_algo_wp = "("+c_jet+"_1_DeepAK8MD_"+(TString)object+"vsQCD>"+to_string(WP_Top_binarizedMD)+")"; }
    if (wp == "L")    { c_algo_wp = "("+c_jet+"_1_DeepAK8MD_"+(TString)object+"vsQCD>0.1883)"; }
    if (wp == "M")    { c_algo_wp = "("+c_jet+"_1_DeepAK8MD_"+(TString)object+"vsQCD>0.8511)"; }
    if (wp == "T")    { c_algo_wp = "("+c_jet+"_1_DeepAK8MD_"+(TString)object+"vsQCD>0.9377)"; }
    if (wp == "VT")   { c_algo_wp = "("+c_jet+"_1_DeepAK8MD_"+(TString)object+"vsQCD>0.9897)"; }
  }

  //
  if (algo == "deepak8_raw"){
     c_jet = "ak8"; c_r = "0.8";
     //if (wp == "JMAR" && object=="T") { c_algo_wp = "("+c_jet+"_1_DeepAK8_Top > 0.4)"; }
     if (wp == "JMAR" && object=="T") { c_algo_wp = "("+c_jet+"_1_DeepAK8_Top >"+to_string(WP_Top_raw)+")"; }
     if (wp == "JMAR" && object=="W") { c_algo_wp = "("+c_jet+"_1_DeepAK8_W >"+to_string(WP_Top_raw)+")"; }

  }

  if (algo == "deepak8md_raw"){
     c_jet = "ak8"; c_r = "0.8";
     //if (wp == "JMAR" && object=="T") { c_algo_wp = "("+c_jet+"_1_DeepAK8MD_Top > 0.0138089)"; }
     if (wp == "JMAR" && object=="T") { c_algo_wp = "("+c_jet+"_1_DeepAK8MD_Top > "+to_string(WP_Top_rawMD)+")"; }
     if (wp == "JMAR" && object=="W") { c_algo_wp = "("+c_jet+"_1_DeepAK8MD_W > "+to_string(WP_Top_rawMD)+")"; }

  }

  /////////////////


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

  // matching definition
  TString c_p3 = "( ("+c_jet+"_1_dr_fj_top_wqmax<("+c_r+")) && ("+c_jet+"_1_dr_fj_top_b<("+c_r+")) )";
  TString c_p2 = "( (!"+c_p3+") && ("+c_jet+"_1_dr_fj_top_wqmax<"+c_r+") && ("+c_jet+"_1_dr_fj_top_b>"+c_r+") )";
  TString c_p1 = "(!("+c_p3+" || "+c_p2+"))";
  //TString c_p3 = "("+c_jet+"_1_isFullyMerged)"; // && ak8_1_topSize>-1. && ak8_1_topSize<0.8 
  //TString c_p2 = "("+c_jet+"_1_isSemiMerged)";
  //TString c_p1 = "(!("+c_p3+" || "+c_p2+"))";

  // final set of cuts
  TString cut = c_base+" && "+c_algo_wp+" && "+c_mass+" && "+c_ptrange;  std::cout << cut << "\n";
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

  TString EOSCMS="root://eoscms.cern.ch/";
  //TString path = "/eos/uscms/store/group/lpcjme/noreplica/NanoHRT/Trees/Apr08/muon/";
  TString path; 
  if(year==2016){
      path = EOSCMS;
      path += "/eos/cms/store/group/phys_jetmet/nbinnorj/WTopTagging/ntuples_HRTSF/2016/";
  }
  else if(year==2017){
      path = EOSCMS;
      path += "/eos/cms/store/group/phys_jetmet/nbinnorj/WTopTagging/ntuples_HRTSF/29July/";
  }  
  else if(year==2018){
      //path = "/eos/uscms/store/user/pakontax/2018_Samples_From_Sicheng_For_Copy_V2/";
      path = EOSCMS;
      path += "/eos/cms/store/group/phys_jetmet/nbinnorj/WTopTagging/ntuples_HRTSF/3Oct_For_Copy/";
  }

  TFile *f_mc = TFile::Open(path+"/mc_nom/sm_tree.root" , "READONLY" );
  cout<<"path: "<<path<<endl;
  TFile *f_data = TFile::Open(path+"/data/singlemu_tree.root" , "READONLY" );
  TTree *t_mc   = (TTree*)f_mc->Get("Events");
  TTree *t_data = (TTree*)f_data->Get("Events");

  // inclusive distributions -- get overall normalization factor
  TString cut_incl  = c_base+" && "+c_mass+" && "+c_ptrange; // init 20,50.,250.
  TH1D *h_mc_incl   = create1Dhisto(name,t_mc,lumi,cut_incl,c_jet+"_1_mass",20,50.,250.,false,1,1,"h_"+name+"_mc_incl",false,false); h_mc_incl->SetFillColor(0);
  TH1D *h_data_incl = create1Dhisto(name,t_data,lumi,cut_incl,c_jet+"_1_mass",20,50.,250.,false,1,1,"h_"+name+"_data_incl",false,true); h_data_incl->SetFillColor(0);
  float scalemc2data = h_data_incl->Integral()/h_mc_incl->Integral(); std::cout << h_data_incl->Integral() << " " << h_mc_incl->Integral() << " overall norm = " << scalemc2data << "\n";
  ostringstream tmpscalemc2data;
  tmpscalemc2data << scalemc2data;
  TString scalemc2datastr = tmpscalemc2data.str(); std::cout << scalemc2datastr << "\n";
  
  TH1D *h_data = create1Dhisto(name,t_data,lumi,cuts[0],c_jet+"_1_mass",20,50.,250.,false,1,1,"h_"+name+"_data",false,true); h_data->SetFillColor(0);
  h_data->SetMarkerColor(1); h_data->SetMarkerSize(1.2); h_data->SetMarkerStyle(20);
  h_data->SetLineWidth(1);

  // make dir
  TString dirname1 = workdir+"/"+object+"_"+algo+"_"+syst+"_mist_rate_"+mistRate;
  const int dir_err = system("mkdir -p ./"+dirname1);
  if (-1 == dir_err) { printf("Error creating directory!n"); exit(1); }

  TString nameoutfile = name+".root"; 
  TFile *fout = new TFile("./"+dirname1+"/"+nameoutfile,"RECREATE");
  h_data->Write("data_obs");

  makeHisto(name, path,lumi+"*"+scalemc2datastr,cuts,c_jet,"nom","nom",fout);
  makeHisto(name, path,lumi+"*"+scalemc2datastr,cuts,c_jet,"pu","up",fout);
  makeHisto(name, path,lumi+"*"+scalemc2datastr,cuts,c_jet,"pu","down",fout);
  makeHisto(name, path,lumi+"*"+scalemc2datastr,cuts,c_jet,"jer","up",fout);
  makeHisto(name, path,lumi+"*"+scalemc2datastr,cuts,c_jet,"jer","down",fout);
  makeHisto(name, path,lumi+"*"+scalemc2datastr,cuts,c_jet,"jes","up",fout);
  makeHisto(name, path,lumi+"*"+scalemc2datastr,cuts,c_jet,"jes","down",fout);
  makeHisto(name, path,lumi+"*"+scalemc2datastr,cuts,c_jet,"met","up",fout);
  makeHisto(name, path,lumi+"*"+scalemc2datastr,cuts,c_jet,"met","down",fout);
  makeHisto(name, path,lumi+"*"+scalemc2datastr+"*LHEScaleWeight[5]*LHEScaleWeightNorm[5]",cuts,c_jet,"lhescalemuf","up",fout);
  makeHisto(name, path,lumi+"*"+scalemc2datastr+"*LHEScaleWeight[3]*LHEScaleWeightNorm[3]",cuts,c_jet,"lhescalemuf","down",fout);
  makeHisto(name, path,lumi+"*"+scalemc2datastr+"*LHEScaleWeight[7]*LHEScaleWeightNorm[7]",cuts,c_jet,"lhescalemur","up",fout);
  makeHisto(name, path,lumi+"*"+scalemc2datastr+"*LHEScaleWeight[1]*LHEScaleWeightNorm[1]",cuts,c_jet,"lhescalemur","down",fout);
  makeHistoLHEPDF(name,path,lumi+"*"+scalemc2datastr,cuts,c_jet,"lhepdf","def",fout);
  if(year==2016){
      makeHistoHerwig(name,path,lumi+"*"+scalemc2datastr,cuts,c_jet,"herwig",fout);
  }

  fout->Close();
  std::cout << "\n\n";
}


void makeHisto(TString name_, TString path_, TString wgt_, std::vector<TString> cuts_, TString c_jet_, TString sys_, TString var_, TFile *f_) {

  TFile *f_mc_; 
  if ((sys_=="nom") || (sys_=="pu")) { f_mc_ = TFile::Open(path_+"/mc_nom/sm_tree.root","READONLY"); }
  else if (sys_.Contains("lhe"))     { f_mc_ = TFile::Open(path_+"/mc_sys/LHEWeight/sm_tree.root","READONLY"); }
  else                               { f_mc_ = TFile::Open(path_+"/mc_sys/"+sys_+"_"+var_+"/sm_tree.root","READONLY"); }
  TTree *t_mc_ = (TTree*)f_mc_->Get("Events");

  // create histos
  TH1D *h_p3 = create1Dhisto(name_,t_mc_,wgt_,cuts_[1],c_jet_+"_1_mass",20,50.,250.,false,kBlue,1,"h_"+name_+"_p3_"+sys_+var_,false,false);    h_p3->SetFillColor(0);
  TH1D *h_p2 = create1Dhisto(name_,t_mc_,wgt_,cuts_[2],c_jet_+"_1_mass",20,50.,250.,false,kRed+1,1,"h_"+name_+"_p2_"+sys_+var_,false,false);   h_p2->SetFillColor(0);
  TH1D *h_p1 = create1Dhisto(name_,t_mc_,wgt_,cuts_[3],c_jet_+"_1_mass",20,50.,250.,false,kGreen-1,1,"h_"+name_+"_p1_"+sys_+var_,false,false); h_p1->SetFillColor(0);

  // avoid zero bins in mc
  for (unsigned int ii=0; ii<h_p3->GetNbinsX(); ++ii) {
    if (h_p3->GetBinContent(ii)<=0) { h_p3->SetBinContent(ii,0.001); h_p3->SetBinError(ii,0.001); }
    if (h_p2->GetBinContent(ii)<=0) { h_p2->SetBinContent(ii,0.001); h_p2->SetBinError(ii,0.001); }
    if (h_p1->GetBinContent(ii)<=0) { h_p1->SetBinContent(ii,0.001); h_p1->SetBinError(ii,0.001); }
  }

  TString xname = "m_{SD} [GeV]";
  h_p3->GetXaxis()->SetTitle(xname);
  h_p2->GetXaxis()->SetTitle(xname);
  h_p1->GetXaxis()->SetTitle(xname);

  TString var_f; if (var_=="up") { var_f = "Up"; } else { var_f = "Down"; } 
  f_->cd();
  if (sys_=="nom") {
    h_p3->Write("catp3");
    h_p2->Write("catp2");
    h_p1->Write("catp1");
  }
  else {
    h_p3->Write("catp3_"+sys_+var_f);
    h_p2->Write("catp2_"+sys_+var_f);
    h_p1->Write("catp1_"+sys_+var_f);
  }

}

void makeHistoHerwig(TString name_, TString path_, TString wgt_, std::vector<TString> cuts_, TString c_jet_, TString sys_, TFile *f_) {

  TFile *f_mc_     = TFile::Open(path_+"/mc_nom/sm_tree.root","READONLY");
  TFile *f_mc_her_ = TFile::Open(path_+"/mc_nom/sm_herwig_tree.root","READONLY");

  TTree *t_mc_     = (TTree*)f_mc_->Get("Events");
  TTree *t_mc_her_ = (TTree*)f_mc_her_->Get("Events");

  // fix normalization of incl sm and sm_her
  TH1D *h_incl     = create1Dhisto(name_,t_mc_,wgt_,cuts_[0],c_jet_+"_1_mass",20,50.,250.,false,kBlue,1,"h_"+name_+"_incl_"+sys_,false,false);    
  TH1D *h_incl_her = create1Dhisto(name_,t_mc_her_,wgt_,cuts_[0],c_jet_+"_1_mass",20,50.,250.,false,kBlue,1,"h_"+name_+"_incl_her_"+sys_,false,false);    
  float her2mg = 1.; her2mg = (h_incl->Integral())/(h_incl_her->Integral());
  ostringstream tmpher2mg;
  tmpher2mg << her2mg;
  TString her2mg_ = tmpher2mg.str();

  // create histos
  TH1D *h_p3 = create1Dhisto(name_,t_mc_,wgt_,cuts_[1],c_jet_+"_1_mass",20,50.,250.,false,kBlue,1,"h_"+name_+"_p3_"+sys_+"_nom",false,false);    h_p3->SetFillColor(0);
  TH1D *h_p2 = create1Dhisto(name_,t_mc_,wgt_,cuts_[2],c_jet_+"_1_mass",20,50.,250.,false,kRed+1,1,"h_"+name_+"_p2_"+sys_+"_nom",false,false);   h_p2->SetFillColor(0);
  TH1D *h_p1 = create1Dhisto(name_,t_mc_,wgt_,cuts_[3],c_jet_+"_1_mass",20,50.,250.,false,kGreen-1,1,"h_"+name_+"_p1_"+sys_+"_nom",false,false); h_p1->SetFillColor(0);

  TH1D *h_p3_up = create1Dhisto(name_,t_mc_her_,wgt_+"*"+her2mg_,cuts_[1],c_jet_+"_1_mass",20,50.,250.,false,kBlue,1,"h_"+name_+"_p3_"+sys_+"_up",false,false);    h_p3_up->SetFillColor(0);
  TH1D *h_p2_up = create1Dhisto(name_,t_mc_her_,wgt_+"*"+her2mg_,cuts_[2],c_jet_+"_1_mass",20,50.,250.,false,kRed+1,1,"h_"+name_+"_p2_"+sys_+"_up",false,false);   h_p2_up->SetFillColor(0);
  TH1D *h_p1_up = create1Dhisto(name_,t_mc_her_,wgt_+"*"+her2mg_,cuts_[3],c_jet_+"_1_mass",20,50.,250.,false,kGreen-1,1,"h_"+name_+"_p1_"+sys_+"_up",false,false); h_p1_up->SetFillColor(0);

  TH1D *h_p3_down = (TH1D*)h_p3_up->Clone("h_p3_"+sys_+"_down"); h_p3_down->SetName("h_p3_"+sys_+"_down"); 
  TH1D *h_p2_down = (TH1D*)h_p2_up->Clone("h_p2_"+sys_+"_down"); h_p2_down->SetName("h_p2_"+sys_+"_down"); 
  TH1D *h_p1_down = (TH1D*)h_p1_up->Clone("h_p1_"+sys_+"_down"); h_p1_down->SetName("h_p1_"+sys_+"_down"); 
  
  for (unsigned int i0=0; i0<h_p3_up->GetNbinsX(); ++i0) {
    h_p3_down->SetBinContent(i0, (h_p3_down->GetBinContent(i0)+2.*(h_p3->GetBinContent(i0)-h_p3_up->GetBinContent(i0))) );
    h_p2_down->SetBinContent(i0, (h_p2_down->GetBinContent(i0)+2.*(h_p2->GetBinContent(i0)-h_p2_up->GetBinContent(i0))) );
    h_p1_down->SetBinContent(i0, (h_p1_down->GetBinContent(i0)+2.*(h_p1->GetBinContent(i0)-h_p1_up->GetBinContent(i0))) );
  }

  // avoid zero bins in mc
  for (unsigned int ii=0; ii<h_p3->GetNbinsX(); ++ii) {
    if (h_p3_up->GetBinContent(ii)<=0) { h_p3_up->SetBinContent(ii,0.001); h_p3_up->SetBinError(ii,0.001); }
    if (h_p2_up->GetBinContent(ii)<=0) { h_p2_up->SetBinContent(ii,0.001); h_p2_up->SetBinError(ii,0.001); }
    if (h_p1_up->GetBinContent(ii)<=0) { h_p1_up->SetBinContent(ii,0.001); h_p1_up->SetBinError(ii,0.001); }
    if (h_p3_down->GetBinContent(ii)<=0) { h_p3_down->SetBinContent(ii,0.001); h_p3_down->SetBinError(ii,0.001); }
    if (h_p2_down->GetBinContent(ii)<=0) { h_p2_down->SetBinContent(ii,0.001); h_p2_down->SetBinError(ii,0.001); }
    if (h_p1_down->GetBinContent(ii)<=0) { h_p1_down->SetBinContent(ii,0.001); h_p1_down->SetBinError(ii,0.001); }
  }

  TString xname = "m_{SD} [GeV]";
  h_p3_up->GetXaxis()->SetTitle(xname);
  h_p2_up->GetXaxis()->SetTitle(xname);
  h_p1_up->GetXaxis()->SetTitle(xname);
  h_p3_down->GetXaxis()->SetTitle(xname);
  h_p2_down->GetXaxis()->SetTitle(xname);
  h_p1_down->GetXaxis()->SetTitle(xname);

  f_->cd();
  h_p3_up->Write("catp3_"+sys_+"Up");
  h_p2_up->Write("catp2_"+sys_+"Up");
  h_p1_up->Write("catp1_"+sys_+"Up");
  h_p3_down->Write("catp3_"+sys_+"Down");
  h_p2_down->Write("catp2_"+sys_+"Down");
  h_p1_down->Write("catp1_"+sys_+"Down");

}


void makeHistoLHEPDF(TString name_, TString path_, TString wgt_, std::vector<TString> cuts_, TString c_jet_, TString sys_, TString var_, TFile *f_) {

  // nom
  TFile *f_mc_nom_ = TFile::Open(path_+"/mc_nom/sm_tree.root","READONLY");
  TTree *t_mc_nom_ = (TTree*)f_mc_nom_->Get("Events");

  TH1D *h_p3_up = create1Dhisto(name_,t_mc_nom_,wgt_,cuts_[1],c_jet_+"_1_mass",20,50.,250.,false,kBlue,1,"h_"+name_+"_p3_"+sys_+"up",false,false);    h_p3_up->SetFillColor(0);
  TH1D *h_p2_up = create1Dhisto(name_,t_mc_nom_,wgt_,cuts_[2],c_jet_+"_1_mass",20,50.,250.,false,kRed+1,1,"h_"+name_+"_p2_"+sys_+"up",false,false);   h_p2_up->SetFillColor(0);
  TH1D *h_p1_up = create1Dhisto(name_,t_mc_nom_,wgt_,cuts_[3],c_jet_+"_1_mass",20,50.,250.,false,kGreen-1,1,"h_"+name_+"_p1_"+sys_+"up",false,false); h_p1_up->SetFillColor(0);
  TH1D *h_p3_down = (TH1D*)h_p3_up->Clone("h_"+name_+"_p3_"+sys_+"down");
  TH1D *h_p2_down = (TH1D*)h_p2_up->Clone("h_"+name_+"_p2_"+sys_+"down");
  TH1D *h_p1_down = (TH1D*)h_p1_up->Clone("h_"+name_+"_p1_"+sys_+"down");

  // pdf
  TFile *f_mc_ = TFile::Open(path_+"/mc_sys/LHEWeight/sm_tree.root","READONLY");
  TTree *t_mc_ = (TTree*)f_mc_->Get("Events");

  std::vector<TH1D*> h_p3_v; h_p3_v.clear();
  std::vector<TH1D*> h_p2_v; h_p2_v.clear();
  std::vector<TH1D*> h_p1_v; h_p1_v.clear();

  for (unsigned i=0; i<15; ++i){
    TString count = std::to_string(i); //std::cout << i << " " << count << "\n";
    TString pdfwgt_ = "LHEPdfWeight["+count+"]*LHEPdfWeightNorm["+count+"]";
    TH1D *h_p3_ = create1Dhisto(name_,t_mc_,wgt_+"*"+pdfwgt_,cuts_[1],c_jet_+"_1_mass",20,50.,250.,false,kBlue,1,"h_"+name_+"_p3_"+sys_+var_+"_"+count,false,false);    h_p3_->SetFillColor(0);
    TH1D *h_p2_ = create1Dhisto(name_,t_mc_,wgt_+"*"+pdfwgt_,cuts_[2],c_jet_+"_1_mass",20,50.,250.,false,kRed+1,1,"h_"+name_+"_p2_"+sys_+var_+"_"+count,false,false);   h_p2_->SetFillColor(0);
    TH1D *h_p1_ = create1Dhisto(name_,t_mc_,wgt_+"*"+pdfwgt_,cuts_[3],c_jet_+"_1_mass",20,50.,250.,false,kGreen-1,1,"h_"+name_+"_p1_"+sys_+var_+"_"+count,false,false); h_p1_->SetFillColor(0);
    h_p3_v.push_back(h_p3_); 
    h_p2_v.push_back(h_p2_);
    h_p1_v.push_back(h_p1_);  
  }

  // get rms and sigma
  for (unsigned int ibin=0; ibin<h_p3_v[0]->GetNbinsX(); ++ibin) {
    float mean_p3_  = 0.; float mean_p2_  = 0.; float mean_p1_  = 0.; 
    float rms_p3_   = 0.; float rms_p2_   = 0.; float rms_p1_   = 0.;
    float sigma_p3_ = 0.; float sigma_p2_ = 0.; float sigma_p1_ = 0.;
    for (unsigned int ihisto=0; ihisto<h_p3_v.size(); ++ihisto) {
      mean_p3_ += h_p3_v[ihisto]->GetBinContent(ibin);                                         
      rms_p3_  += (h_p3_v[ihisto]->GetBinContent(ibin))*(h_p3_v[ihisto]->GetBinContent(ibin)); 
      mean_p2_ += h_p2_v[ihisto]->GetBinContent(ibin);                                         
      rms_p2_  += (h_p2_v[ihisto]->GetBinContent(ibin))*(h_p2_v[ihisto]->GetBinContent(ibin)); 
      mean_p1_ += h_p1_v[ihisto]->GetBinContent(ibin);                                         
      rms_p1_  += (h_p1_v[ihisto]->GetBinContent(ibin))*(h_p1_v[ihisto]->GetBinContent(ibin)); 
    }
    mean_p3_ = mean_p3_/h_p3_v.size(); rms_p3_ = sqrt(rms_p3_/h_p3_v.size()); sigma_p3_ = sqrt((rms_p3_*rms_p3_) - (mean_p3_*mean_p3_)); 
    mean_p2_ = mean_p2_/h_p2_v.size(); rms_p2_ = sqrt(rms_p2_/h_p2_v.size()); sigma_p2_ = sqrt((rms_p2_*rms_p2_) - (mean_p2_*mean_p2_)); 
    mean_p1_ = mean_p1_/h_p1_v.size(); rms_p1_ = sqrt(rms_p1_/h_p1_v.size()); sigma_p1_ = sqrt((rms_p1_*rms_p1_) - (mean_p1_*mean_p1_)); 

    h_p3_up->SetBinContent(ibin,h_p3_up->GetBinContent(ibin)+sigma_p3_); h_p3_down->SetBinContent(ibin,h_p3_down->GetBinContent(ibin)-sigma_p3_);
    h_p2_up->SetBinContent(ibin,h_p2_up->GetBinContent(ibin)+sigma_p2_); h_p2_down->SetBinContent(ibin,h_p2_down->GetBinContent(ibin)-sigma_p2_);
    h_p1_up->SetBinContent(ibin,h_p1_up->GetBinContent(ibin)+sigma_p1_); h_p1_down->SetBinContent(ibin,h_p1_down->GetBinContent(ibin)-sigma_p1_);
  }
  

  // avoid zero bins in mc
  for (unsigned int ii=0; ii<h_p3_up->GetNbinsX(); ++ii) {
    if (h_p3_up->GetBinContent(ii)<=0) { h_p3_up->SetBinContent(ii,0.001); h_p3_up->SetBinError(ii,0.001); }
    if (h_p2_up->GetBinContent(ii)<=0) { h_p2_up->SetBinContent(ii,0.001); h_p2_up->SetBinError(ii,0.001); }
    if (h_p1_up->GetBinContent(ii)<=0) { h_p1_up->SetBinContent(ii,0.001); h_p1_up->SetBinError(ii,0.001); }
    if (h_p3_down->GetBinContent(ii)<=0) { h_p3_down->SetBinContent(ii,0.001); h_p3_down->SetBinError(ii,0.001); }
    if (h_p2_down->GetBinContent(ii)<=0) { h_p2_down->SetBinContent(ii,0.001); h_p2_down->SetBinError(ii,0.001); }
    if (h_p1_down->GetBinContent(ii)<=0) { h_p1_down->SetBinContent(ii,0.001); h_p1_down->SetBinError(ii,0.001); }
  }

  TString xname = "m_{SD} [GeV]";
  h_p3_up->GetXaxis()->SetTitle(xname);
  h_p2_up->GetXaxis()->SetTitle(xname);
  h_p1_up->GetXaxis()->SetTitle(xname);
  h_p3_down->GetXaxis()->SetTitle(xname);
  h_p2_down->GetXaxis()->SetTitle(xname);
  h_p1_down->GetXaxis()->SetTitle(xname);

  f_->cd();
  h_p3_up->Write("catp3_"+sys_+"Up");
  h_p2_up->Write("catp2_"+sys_+"Up");
  h_p1_up->Write("catp1_"+sys_+"Up");
  h_p3_down->Write("catp3_"+sys_+"Down");
  h_p2_down->Write("catp2_"+sys_+"Down");
  h_p1_down->Write("catp1_"+sys_+"Down");
  
}


TH1D *create1Dhisto(TString sample,TTree *tree,TString intLumi,TString cuts,TString branch,int bins,float xmin,float xmax,
		    bool useLog,int color, int style,TString name,bool norm,bool data) {
  TH1::SetDefaultSumw2(kTRUE);

  TString cut;
  //  if (data) { cut ="(passMuTrig && "+cuts+")"; } 
  if (data) { cut ="("+cuts+")"; } 
  else {
    if      (name.Contains("puUp"))   { cut ="(xsecWeight*puWeightUp*genWeight*"+intLumi+")*("+cuts+")"; }
    else if (name.Contains("puDown")) { cut ="(xsecWeight*puWeightDown*genWeight*"+intLumi+")*("+cuts+")"; }
    //else if (name.Contains("herw"))   { cut ="(xsecWeight*puWeight*"+intLumi+")*("+cuts+")"; }
    else                              { cut ="(xsecWeight*puWeight*genWeight*"+intLumi+")*("+cuts+")"; }
  }
  
  // std::cout << "cut = " << cut << "\n";
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
