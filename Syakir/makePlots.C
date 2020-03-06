#include "setTDRStyle.h"
#include <sstream>
#include <fstream>
#include "TTree.h"
#include "TFile.h"
#include "TH1D.h"
#include <vector>
#include "Rtypes.h"
#include "TColor.h"
#include "TVectorF.h"
#include <cstdlib>
//////////////////////// predefine
void getMistag(TString object, TString wp, TString year, TString mistrate);
void rescaleXaxis(TGraphAsymmErrors *inputhisto, double xmin, double scale);
void setTDRStyle();
void makeDataMCPlotsFromCombine(TString path2file, TString filename, TString score, TString ptrange, TString category, float xmin, float xmax, int nbins,TString xaxisname, bool log);
void getdiscvalmistag(float eff, TString algo, TString algosvar, TString jettype, TString object, TString cut);
void getSFSummarySources(TString object, TString wp, TString path2file, TString mistrate);
void getSFSummary(TString object, TString wp, TString path2file);
void makeMatchingEffPlots(TString obj_, TString year);
double median(std::vector<TString> vec);
TH1F *rescaleXaxis(TH1F *inputhisto, float xmin, float xmax);
TH1F *getDataMCratio(TGraphAsymmErrors *indata, TH1F *inMC);
TH1D *create1Dhisto(TString sample, TTree *tree,TString intLumi,TString cuts,TString branch,int bins,float xmin,float xmax, bool useLog,int color, int style,TString name,bool norm,bool data);
TGraphAsymmErrors *getSFGraph(TString object, TString algo, TString wp, std::vector<TString> ptrange, int ialgo, int nalgos, int color, TString mistrate);
TGraphAsymmErrors *getSFGraphSyst(TString object, TString algo, TString wp, std::vector<TString> ptrange, int ialgo, int nalgos, int color, TString extra, TGraphAsymmErrors *gr_nom);
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
TString EOSDIR="/eos/user/s/ssyedoma/JMARWTag/TempFit/plots/";
void makePlots(TString path2file, TString filename, TString score, TString ptrange, float xmin, float xmax, int nbins, TString xaxis, TString object, TString wp, TString mistrate, TString year) {
  TH1::SetDefaultSumw2(kTRUE);
  setTDRStyle();
  gROOT->SetBatch(false);
  gStyle->SetOptStat(0);
  gStyle->SetOptFit(1);
  gStyle->SetPalette(1);
  gStyle->SetOptTitle(0);
  TH1::SetDefaultSumw2(kTRUE);
  
  // make pre/post fit plots
  // makeDataMCPlotsFromCombine(path2file,filename,score,ptrange,"pass",xmin,xmax,nbins,xaxis,false);
  // makeDataMCPlotsFromCombine(path2file,filename,score,ptrange,"fail",xmin,xmax,nbins,xaxis,false);

  // make matching efficiency plots
  // cout << "running makeMatchingEffPlots . . ." << endl;
  // makeMatchingEffPlots("w",year);

  // make data & MC efficiency plots
  cout << "running getMistag plots . . ." << endl;
  cout << ":: "+object+" "+mistrate+" "+year << endl;
  getMistag(object, wp, year, mistrate);

  // make SF plots
  // cout << "running getSFSummarySources . . ." << endl;
  // getSFSummarySources(object, wp, path2file, mistrate);
}

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

void makeDataMCPlotsFromCombine(TString path2file, TString filename, TString score, TString ptrange, TString category, float xmin, float xmax, int nbins,TString xaxisname, bool log) {

  setTDRStyle();
  gROOT->SetBatch(true);
  gStyle->SetOptStat(0);
  gStyle->SetOptFit(0);
  gStyle->SetPalette(1);
  TH1::SetDefaultSumw2(kTRUE);

  if (xaxisname == "mass") { xaxisname = "m(jet) [GeV]"; }

  std::cout << "Making plots_datamc directory" << "\n";
  const int dir_err = system("mkdir -p ./"+(TString)path2file+"/plots_datamc");
  if (-1 == dir_err) { printf("Error creating directory!n"); exit(1); }
  TFile *fdiag = TFile::Open("./"+path2file+"/sf_fitDiagnostics_"+filename+".root", "READONLY" );

  // get prefit histograms
  TString prefitstr = "shapes_prefit";
  TH1F *h_prefit_catp3_ = (TH1F*)fdiag->Get(prefitstr+"/"+category+"/catp3"); h_prefit_catp3_->SetName("h_catp3_");
  TH1F *h_prefit_catp2_ = (TH1F*)fdiag->Get(prefitstr+"/"+category+"/catp2"); h_prefit_catp2_->SetName("h_catp2_");
  TH1F *h_prefit_catp1_ = (TH1F*)fdiag->Get(prefitstr+"/"+category+"/catp1"); h_prefit_catp1_->SetName("h_catp1_");
  TH1F *h_prefit_total_ = (TH1F*)fdiag->Get(prefitstr+"/"+category+"/total"); h_prefit_total_->SetName("h_total_");
  TH1F *h_prefit_catp3 = rescaleXaxis(h_prefit_catp3_,xmin,xmax); h_prefit_catp3->SetName("h_catp3");
  TH1F *h_prefit_catp2 = rescaleXaxis(h_prefit_catp2_,xmin,xmax); h_prefit_catp2->SetName("h_catp2");
  TH1F *h_prefit_catp1 = rescaleXaxis(h_prefit_catp1_,xmin,xmax); h_prefit_catp1->SetName("h_catp1");
  TH1F *h_prefit_total = rescaleXaxis(h_prefit_total_,xmin,xmax); h_prefit_total->SetName("h_total");
  
  // get postfit histograms
  TTree *tree = (TTree*)fdiag->Get("tree_fit_sb");
  TH1F *h_fit_status = new TH1F("h_fit_status_","h_fit_status_",20,-10.,10.); 
  tree->Project("h_fit_status_","fit_status");
  TString postfitstr = "shapes_fit_s"; if (h_fit_status->GetMean()<0.) { postfitstr = "shapes_prefit"; }
  TH1F *h_postfit_catp3_ = (TH1F*)fdiag->Get(postfitstr+"/"+category+"/catp3"); h_postfit_catp3_->SetName("h_catp3_");
  TH1F *h_postfit_catp2_ = (TH1F*)fdiag->Get(postfitstr+"/"+category+"/catp2"); h_postfit_catp2_->SetName("h_catp2_");
  TH1F *h_postfit_catp1_ = (TH1F*)fdiag->Get(postfitstr+"/"+category+"/catp1"); h_postfit_catp1_->SetName("h_catp1_");
  TH1F *h_postfit_total_ = (TH1F*)fdiag->Get(postfitstr+"/"+category+"/total"); h_postfit_total_->SetName("h_total_");
  TH1F *h_postfit_catp3 = rescaleXaxis(h_postfit_catp3_,xmin,xmax); h_postfit_catp3->SetName("h_catp3");
  TH1F *h_postfit_catp2 = rescaleXaxis(h_postfit_catp2_,xmin,xmax); h_postfit_catp2->SetName("h_catp2");
  TH1F *h_postfit_catp1 = rescaleXaxis(h_postfit_catp1_,xmin,xmax); h_postfit_catp1->SetName("h_catp1");
  TH1F *h_postfit_total = rescaleXaxis(h_postfit_total_,xmin,xmax); h_postfit_total->SetName("h_total");
  
  // get data
  TGraphAsymmErrors *h_data = (TGraphAsymmErrors*)fdiag->Get("shapes_prefit/"+category+"/data"); h_data->SetName("h_data_");
  std::cout << h_data->GetN() << "\n";
  rescaleXaxis(h_data, xmin, (xmax-xmin)/(float)nbins); 
  
  //cosmetics
  h_prefit_catp3->SetLineColor(4);       h_prefit_catp3->SetLineStyle(2); h_prefit_catp3->SetLineWidth(3); h_prefit_catp3->SetMarkerSize(0);
  h_prefit_catp2->SetLineColor(633);     h_prefit_catp2->SetLineStyle(2); h_prefit_catp2->SetLineWidth(3); h_prefit_catp2->SetMarkerSize(0);
  h_prefit_catp1->SetLineColor(415);     h_prefit_catp1->SetLineStyle(2); h_prefit_catp1->SetLineWidth(3); h_prefit_catp1->SetMarkerSize(0);
  h_prefit_total->SetLineColor(kBlue+2); h_prefit_total->SetLineStyle(2); h_prefit_total->SetLineWidth(3); h_prefit_total->SetMarkerSize(0);
  
  h_postfit_catp3->SetLineColor(4);       h_postfit_catp3->SetLineStyle(1); h_postfit_catp3->SetLineWidth(4); h_postfit_catp3->SetMarkerSize(0);
  h_postfit_catp2->SetLineColor(633);     h_postfit_catp2->SetLineStyle(1); h_postfit_catp2->SetLineWidth(4); h_postfit_catp2->SetMarkerSize(0);
  h_postfit_catp1->SetLineColor(415);     h_postfit_catp1->SetLineStyle(1); h_postfit_catp1->SetLineWidth(4); h_postfit_catp1->SetMarkerSize(0);
  h_postfit_total->SetLineColor(kBlue+2); h_postfit_total->SetLineStyle(1); h_postfit_total->SetLineWidth(4); h_postfit_total->SetMarkerSize(0);
  
  h_data->SetLineColor(1); h_data->SetLineWidth(3); 
  h_data->SetMarkerColor(1); h_data->SetMarkerStyle(20); h_data->SetMarkerSize(1.2); 
  
  //TGraphAsymmErrors *h_r_prefit = h_data->Clone("h_r_prefit"); h_r_prefit->Divide(h_data,h_prefit_total);
  TH1F *h_r_prefit = getDataMCratio(h_data,h_prefit_total); h_r_prefit->SetName("h_r_prefit_");
  h_r_prefit->SetMarkerSize(0); h_r_prefit->SetLineColor(kMagenta); h_r_prefit->SetLineStyle(2);
  
  TH1F *h_r_postfit = getDataMCratio(h_data,h_postfit_total); h_r_postfit->SetName("h_r_postfit_");
  h_r_postfit->SetMarkerColor(1); h_r_postfit->SetLineColor(1);
  
  TLegend* leg = new TLegend(0.60,0.55,0.94,0.86);
  leg->SetFillStyle(0);
  leg->SetFillColor(0);
  leg->SetLineWidth(0);
  leg->AddEntry(h_postfit_catp3,"top matched","L");
  leg->AddEntry(h_postfit_catp2,"W matched","L");
  leg->AddEntry(h_postfit_catp1,"unmatched","L");
  leg->AddEntry(h_postfit_total,"Total SM","L");
  leg->AddEntry(h_data,"Data","P");
  
  TLegend* legfit = new TLegend(0.4,0.7,0.65,0.86);
  legfit->SetFillStyle(0);
  legfit->SetFillColor(0);
  legfit->SetLineWidth(0);
  legfit->AddEntry(h_prefit_total,"Pre-fit","L");
  legfit->AddEntry(h_postfit_total,"Post-fit","L");
  
  TLegend* legfitr = new TLegend(0.35,0.80,0.55,0.93);
  legfitr->SetFillStyle(0);
  legfitr->SetFillColor(0);
  legfitr->SetLineWidth(0);
  legfitr->AddEntry(h_r_prefit,"Pre-fit","L");
  legfitr->AddEntry(h_r_postfit,"Post-fit","L");

  TPaveText *pt_cms = new TPaveText(0.11,0.77,0.4,0.9,"NDC");
  pt_cms->SetFillStyle(0);
  pt_cms->SetFillColor(0);
  pt_cms->SetLineWidth(0);
  pt_cms->AddText("CMS");
  pt_cms->SetTextSize(0.08);

  TPaveText *pt_preliminary = new TPaveText(0.2,0.63,0.4,0.9,"NDC");
  pt_preliminary->SetFillStyle(0);
  pt_preliminary->SetFillColor(0);
  pt_preliminary->SetLineWidth(0);
  pt_preliminary->AddText("Preliminary");
  pt_preliminary->SetTextFont(52);
  pt_preliminary->SetTextSize(0.06);

  TLatex pt_lumi;
  const char *longstring = "35.9 fb^{-1} (13 TeV)";
  pt_lumi.SetTextSize(0.07);
  pt_lumi.SetTextFont(42);
  
  TString logstr = "lin"; if (log) { logstr = "log"; } 
  TCanvas *c = new TCanvas("c_"+category+"_"+score+"_"+ptrange+"_"+logstr,"c_"+category+"_"+score+"_"+ptrange+"_"+logstr,600,600); 
  c->SetName("c_"+category+"_"+score+"_"+ptrange+"_"+logstr);
  
  TPad *pMain  = new TPad("pMain_"+category+"_"+score+"_"+ptrange+"_"+logstr,"pMain+"+category+"_"+score+"_"+ptrange+"_"+logstr,0.0,0.35,1.0,1.0);
  pMain->SetRightMargin(0.05);
  pMain->SetLeftMargin(0.17);
  pMain->SetBottomMargin(0.02);
  pMain->SetTopMargin(0.1);
  
  TPad *pRatio = new TPad("pRatio_"+category+"_"+score+"_"+ptrange+"_"+logstr,"pRatio_"+category+"_"+score+"_"+ptrange+"_"+logstr,0.0,0.0,1.0,0.35);
  pRatio->SetRightMargin(0.05);
  pRatio->SetLeftMargin(0.17);
  pRatio->SetTopMargin(0.02);
  pRatio->SetBottomMargin(0.4);
  pMain->Draw();
  pRatio->Draw();
  
  pMain->cd();
  
  float maxyld = h_postfit_total->GetMaximum(); 
  if (h_prefit_total->GetMaximum()>h_postfit_total->GetMaximum()) { maxyld = h_prefit_total->GetMaximum(); }
  if (log) { gPad->SetLogy(); h_prefit_total->GetYaxis()->SetRangeUser(0.1,10.*maxyld); } else { h_prefit_total->GetYaxis()->SetRangeUser(0.,1.8*maxyld); }
  h_prefit_total->GetXaxis()->SetLabelSize(0.);
  h_prefit_total->GetYaxis()->SetTitle("Events / bin");
  h_prefit_total->GetXaxis()->SetTitle(xaxisname);
  h_prefit_total->Draw("HIST E0");
  h_prefit_catp3->Draw("HIST E0 sames");
  h_prefit_catp2->Draw("HIST E0 sames");
  h_prefit_catp1->Draw("HIST E0 sames");
  h_postfit_catp3->Draw("HIST E0 sames");
  h_postfit_catp2->Draw("HIST E0 sames");
  h_postfit_catp1->Draw("HIST E0 sames");
  h_postfit_total->Draw("HIST E0 sames");
  h_data->Draw("P sames");
  leg->Draw("sames");
  pt_cms->Draw("sames");
  pt_preliminary->Draw("sames");
  pt_lumi.DrawLatexNDC(0.64,0.93,longstring);
  c->RedrawAxis();
  
  pRatio->cd();
  gPad->SetBottomMargin(0.2);
  h_r_postfit->GetYaxis()->SetTitleOffset(0.75);
  h_r_postfit->GetYaxis()->SetTitleSize(0.1);
  h_r_postfit->GetYaxis()->SetLabelSize(0.08);
  h_r_postfit->GetXaxis()->SetTitleSize(0.1);
  h_r_postfit->GetXaxis()->SetLabelSize(0.08);
  h_r_postfit->GetXaxis()->SetTitle(xaxisname);
  h_r_postfit->GetYaxis()->SetTitle("Data / Post-fit");
  h_r_postfit->GetYaxis()->SetRangeUser(0.01,1.99);
  h_r_postfit->Draw("P E0");
  //  h_r_prefit->Draw("HIST sames");
  c->RedrawAxis();
  
  if (log) {
    c->Print(path2file+"/plots_datamc/"+category+"_"+score+"_"+ptrange+"_log.pdf");
    c->Print(path2file+"/plots_datamc/"+category+"_"+score+"_"+ptrange+"_log.png");
  } 
  else {
    c->Print(path2file+"/plots_datamc/"+category+"_"+score+"_"+ptrange+"_lin.pdf");
    c->Print(path2file+"/plots_datamc/"+category+"_"+score+"_"+ptrange+"_lin.png");
  }
  //c->Delete();
} // end of makeDataMCPlotsFromCombine

void getSFSummary(TString object, TString wp, TString path2file) {
  
  setTDRStyle();
  gROOT->SetBatch(false);
  gStyle->SetOptStat(0);
  gStyle->SetOptFit(1);
  gStyle->SetPalette(1);
  TH1::SetDefaultSumw2(kTRUE);
  
  std::vector<TString> algos;    algos.clear();
  std::vector<TString> legnames; legnames.clear();
  std::vector<TString> ptrange;  ptrange.clear();
  std::vector<int> colors; colors.clear();
  
  if (object=="T") {
    algos.push_back("sdtau32");     legnames.push_back("m_{SD}+#tau_{32}");       colors.push_back(800);
    algos.push_back("sdtau32btag"); legnames.push_back("m_{SD}+#tau_{32}+b-tag"); colors.push_back(632);
    //algos.push_back("hotvr");       legnames.push_back("HOTVR");                  colors.push_back(812);
    algos.push_back("ecftoptag");   legnames.push_back("CA15-ECF");               colors.push_back(419);
    algos.push_back("best");        legnames.push_back("BEST");                   colors.push_back(882);
    algos.push_back("imagetop");    legnames.push_back("ImageTop");               colors.push_back(603);
    algos.push_back("imagetopmd");  legnames.push_back("ImageTop-MD");            colors.push_back(600);
    algos.push_back("deepak8");     legnames.push_back("DeepAK8");                colors.push_back(866);
    algos.push_back("deepak8md");   legnames.push_back("DeepAK8-MD");             colors.push_back(616);
    
    ptrange.push_back("low");
    ptrange.push_back("lowmed");
    ptrange.push_back("med");
    ptrange.push_back("medhi");
  }

  if (object=="W") {
    // algos.push_back("sdtau21");     legnames.push_back("m_{SD}+#tau_{21}");   colors.push_back(800);
    // algos.push_back("sdn2");        legnames.push_back("m_{SD}+N_{2}");       colors.push_back(408);
    // algos.push_back("sdn2ddt");     legnames.push_back("m_{SD}+N_{2}^{DDT}"); colors.push_back(419);
    // algos.push_back("best");        legnames.push_back("BEST");               colors.push_back(882);
    algos.push_back("deepak8");     legnames.push_back("DeepAK8");            colors.push_back(866);
    // algos.push_back("deepak8md");   legnames.push_back("DeepAK8-MD");         colors.push_back(616);
    
    ptrange.push_back("low");
    ptrange.push_back("lowmed");
    ptrange.push_back("med");
  }
 

  std::string names[100];
  TH1F *h_dummy; int nbins; int xmax;
  if (object=="T") { names[0] = "300-400"; names[1] = "400-480"; names[2] = "480-600"; names[3] = "600-1200"; nbins = 4, xmax = 4.; }
  if (object=="W") { names[0] = "200-300"; names[1] = "300-400"; names[2] = "400-800";  nbins = 3, xmax = 3.; }
  h_dummy = new TH1F("h_dummy","h_dummy",nbins,0.,xmax);
  for (unsigned int i1=0; i1<h_dummy->GetNbinsX(); ++i1) { h_dummy->GetXaxis()->SetBinLabel(i1+1,names[i1].c_str()); }

  std::vector<TGraphAsymmErrors*> gr_sf;
  for (unsigned int ialgo=0; ialgo<algos.size(); ++ialgo) {

    double xval[20], xvalerr[20];
    double yval[20], yvalerrlo[20], yvalerrhi[20];
    
    for (unsigned int iptrange=0; iptrange<ptrange.size(); ++iptrange) {
      // TFile *fdiag = TFile::Open("./"+object+"_"+algos[ialgo]+"/sf_fitDiagnostics_"+object+"_"+algos[ialgo]+"_"+wp+"_"+ptrange[iptrange]+".root", "READONLY" );
      TFile *fdiag = TFile::Open("./"+path2file+"/sf_fitDiagnostics_"+object+"_"+algos[ialgo]+"_"+wp+"_"+ptrange[iptrange]+".root", "READONLY" );

      TTree *t_   = (TTree*)fdiag->Get("tree_fit_sb");

      TString strCat, strCatLoErr, strCatHiErr;   
      if (object=="T") { strCat = "SF_catp3"; strCatLoErr = "SF_catp3LoErr"; strCatHiErr = "SF_catp3HiErr"; }
      if (object=="W") { strCat = "SF_catp2"; strCatLoErr = "SF_catp2LoErr"; strCatHiErr = "SF_catp2HiErr"; }
      TH1F *h_sf_cat      = new TH1F("h_sf_cat"      , "h_sf_cat"      , 10000,0.,10.);
      TH1F *h_sf_catLoErr = new TH1F("h_sf_catLoErr" , "h_sf_catLoErr" , 10000,0.,10.);
      TH1F *h_sf_catHiErr = new TH1F("h_sf_catHiErr" , "h_sf_catHiErr" , 10000,0.,10.);
      t_->Draw(strCat+" >> h_sf_cat");
      t_->Draw(strCatLoErr+" >> h_sf_catLoErr");
      t_->Draw(strCatHiErr+" >> h_sf_catHiErr");

      xval[iptrange]    = (iptrange+0.5) + 0.03*(ialgo - 1.*(algos.size()-2));
      xvalerr[iptrange] = 0.;
      yval[iptrange]    = h_sf_cat->GetMean();
      yvalerrlo[iptrange] = h_sf_catLoErr->GetMean();
      yvalerrhi[iptrange] = h_sf_catHiErr->GetMean();
      if (algos[ialgo]=="sdtau21" && ptrange[iptrange]=="low") { yvalerrlo[iptrange] = 0.01; yvalerrhi[iptrange] = 0.01; }

      h_sf_cat->Delete();
      h_sf_catLoErr->Delete();
      h_sf_catHiErr->Delete();

    } // end looping over the pt bins

    TGraphAsymmErrors *gr_sf_tmp = new TGraphAsymmErrors(ptrange.size(),xval,yval,xvalerr,xvalerr,yvalerrlo,yvalerrhi);
    gr_sf_tmp->SetLineColor(colors[ialgo]);
    gr_sf_tmp->SetMarkerColor(colors[ialgo]);
    gr_sf.push_back(gr_sf_tmp);

  } // end looping over files

  TLegend* leg;
  if (object=="T") { leg = new TLegend(0.75,0.46,0.92,0.89); }
  if (object=="W") { leg = new TLegend(0.75,0.66,0.92,0.89); }
  leg->SetFillStyle(0);
  leg->SetFillColor(0);
  leg->SetLineWidth(0);

  TPaveText *pt_cms = new TPaveText(0.01,0.77,0.4,0.9,"NDC");
  pt_cms->SetFillStyle(0);
  pt_cms->SetFillColor(0);
  pt_cms->SetLineWidth(0);
  pt_cms->AddText("CMS");
  pt_cms->SetTextSize(0.08);

  TPaveText *pt_preliminary = new TPaveText(0.06,0.63,0.4,0.9,"NDC");
  pt_preliminary->SetFillStyle(0);
  pt_preliminary->SetFillColor(0);
  pt_preliminary->SetLineWidth(0);
  pt_preliminary->AddText("Preliminary");
  pt_preliminary->SetTextFont(52);
  pt_preliminary->SetTextSize(0.06);

  TLatex pt_lumi;
  const char *longstring = "35.9 fb^{-1} (13 TeV)";
  pt_lumi.SetTextSize(0.07);
  pt_lumi.SetTextFont(42);

  TCanvas *c_sf = new TCanvas("c_sf","c_sf",700,500);
  gPad->SetLeftMargin(0.1);
  gPad->SetBottomMargin(0.13);
  gPad->SetTopMargin(1.02);
  //  gPad->SetGridy();
  h_dummy->GetYaxis()->SetRangeUser(0.5,2.);
  h_dummy->GetYaxis()->SetTitleOffset(0.8);
  h_dummy->GetYaxis()->SetTitle("#epsilon_{DATA} / #epsilon_{MC}");
  h_dummy->GetXaxis()->SetLabelSize(0.06);
  h_dummy->GetXaxis()->SetTitle("p_{T} (jet) [GeV]");
  h_dummy->Draw("HIST");
  for (unsigned int i0=0; i0<gr_sf.size(); ++i0) {
    gr_sf[i0]->Draw("P sames");
    leg->AddEntry(gr_sf[i0],legnames[i0],"PL");
    for (unsigned int igr = 0; igr<gr_sf[i0]->GetN(); ++igr) {
      double x_, y_;
      gr_sf[i0]->GetPoint(igr,x_,y_);
      std::cout << std::fixed;
      std::cout << std::setprecision(2);
      if (igr < (gr_sf[i0]->GetN()-1)) { std::cout << " & " << y_ << "$^{+" << gr_sf[i0]->GetErrorYhigh(igr) << "}_{-" << gr_sf[i0]->GetErrorYlow(igr) << "}$"; }
      else                             { std::cout << " & " << y_ << "$^{+" << gr_sf[i0]->GetErrorYhigh(igr) << "}_{-" << gr_sf[i0]->GetErrorYlow(igr) << "}$ \\\\ \n"; }
    }
  }
  leg->Draw("sames");
  pt_cms->Draw("sames");
  pt_preliminary->Draw("sames");
  pt_lumi.DrawLatexNDC(0.58,0.93,longstring);
  c_sf->Print("sf_"+object+"_"+wp+".png");
}

void getSFSummarySources(TString object, TString wp, TString path2file, TString mistrate) {
  
  setTDRStyle();
  gROOT->SetBatch(false);
  gStyle->SetOptStat(0);
  gStyle->SetOptFit(1);
  gStyle->SetPalette(1);
  TH1::SetDefaultSumw2(kTRUE);
  
  std::vector<TString> algos;    algos.clear();
  std::vector<TString> legnames; legnames.clear();
  std::vector<TString> ptrange;  ptrange.clear();
  std::vector<int> colors; colors.clear();
  
  if (object=="T") {
    algos.push_back("sdtau32");     legnames.push_back("m_{SD}+#tau_{32}");       colors.push_back(800);
    algos.push_back("sdtau32btag"); legnames.push_back("m_{SD}+#tau_{32}+b-tag"); colors.push_back(632);
    algos.push_back("hotvr");       legnames.push_back("HOTVR");                  colors.push_back(812);
    algos.push_back("ecftoptag");   legnames.push_back("CA15-ECF");               colors.push_back(419);
    algos.push_back("best");        legnames.push_back("BEST");                   colors.push_back(882);
    algos.push_back("imagetop");    legnames.push_back("ImageTop");               colors.push_back(603);
    algos.push_back("imagetopmd");  legnames.push_back("ImageTop-MD");            colors.push_back(600);
    algos.push_back("deepak8");     legnames.push_back("DeepAK8");                colors.push_back(866);
    algos.push_back("deepak8md");   legnames.push_back("DeepAK8-MD");             colors.push_back(616);
    
    ptrange.push_back("low");
    ptrange.push_back("lowmed");
    ptrange.push_back("med");
    ptrange.push_back("medhi");
  }

  if (object=="W") {
    algos.push_back("sdtau21");     legnames.push_back("m_{SD}+#tau_{21}");   colors.push_back(800);
    // algos.push_back("sdn2");        legnames.push_back("m_{SD}+N_{2}");       colors.push_back(408);
    // algos.push_back("sdn2ddt");     legnames.push_back("m_{SD}+N_{2}^{DDT}"); colors.push_back(419);
    // algos.push_back("best");        legnames.push_back("BEST");               colors.push_back(882);
    algos.push_back("deepak8");     legnames.push_back("DeepAK8");            colors.push_back(866);
    // algos.push_back("deepak8md");   legnames.push_back("DeepAK8-MD");         colors.push_back(616);
    
    ptrange.push_back("low");
    ptrange.push_back("lowmed");
    ptrange.push_back("med");
  }
 

  std::string names[100];
  TH1F *h_dummy; int nbins; int xmax;
  if (object=="T") { names[0] = "300-400"; names[1] = "400-480"; names[2] = "480-600"; names[3] = "600-1200"; nbins = 4, xmax = 4.; }
  if (object=="W") { names[0] = "200-300"; names[1] = "300-400"; names[2] = "400-800";  nbins = 3, xmax = 3.; }
  h_dummy = new TH1F("h_dummy","h_dummy",nbins,0.,xmax);
  for (unsigned int i1=0; i1<h_dummy->GetNbinsX(); ++i1) { h_dummy->GetXaxis()->SetBinLabel(i1+1,names[i1].c_str()); }

  std::vector<TGraphAsymmErrors*> gr_sf;
  std::vector<TGraphAsymmErrors*> gr_sf_stat;
  for (unsigned int ialgo=0; ialgo<algos.size(); ++ialgo) {
    cout<<"getting SF for "<<algos[ialgo]<<" . . ."<<endl;
    TGraphAsymmErrors *gr_tot  = getSFGraph(object,algos[ialgo],wp,ptrange,ialgo,algos.size(),colors[ialgo],mistrate); gr_tot->SetName("gr_tot_"+algos[ialgo]);
    // TGraphAsymmErrors *gr_stat = getSFGraphSyst(object,algos[ialgo],wp,ptrange,ialgo,algos.size(),colors[ialgo],"stat",gr_tot); gr_stat->SetName("gr_stat_"+algos[ialgo]);

    gr_tot->SetFillColor(colors[ialgo]);  gr_tot->SetFillStyle(3002); gr_tot->SetLineColor(colors[ialgo]); 
    // gr_stat->SetLineWidth(1); gr_stat->SetLineColor(colors[ialgo]); gr_stat->SetFillColor(0); gr_stat->SetFillStyle(0); gr_stat->SetMarkerSize(1);

    gr_sf.push_back(gr_tot);
    // gr_sf_stat.push_back(gr_stat);

  } // end looping over files
  cout<<"end looping over files"<<endl<<endl;
  TLegend* leg;
  if (object=="T") { leg = new TLegend(0.75,0.46,0.92,0.89); }
  if (object=="W") { leg = new TLegend(0.75,0.66,0.92,0.89); }
  leg->SetFillStyle(0);
  leg->SetFillColor(0);
  leg->SetLineWidth(0);

  TPaveText *pt_cms = new TPaveText(0.01,0.77,0.4,0.9,"NDC");
  pt_cms->SetFillStyle(0);
  pt_cms->SetFillColor(0);
  pt_cms->SetLineWidth(0);
  pt_cms->AddText("CMS");
  pt_cms->SetTextSize(0.08);

  TPaveText *pt_preliminary = new TPaveText(0.06,0.63,0.4,0.9,"NDC");
  pt_preliminary->SetFillStyle(0);
  pt_preliminary->SetFillColor(0);
  pt_preliminary->SetLineWidth(0);
  pt_preliminary->AddText("Preliminary");
  pt_preliminary->SetTextFont(52);
  pt_preliminary->SetTextSize(0.06);

  TLatex pt_lumi;
  const char *longstring = "35.9 fb^{-1} (13 TeV)";
  pt_lumi.SetTextSize(0.07);
  pt_lumi.SetTextFont(42);

  TCanvas *c_sf = new TCanvas("c_sf","c_sf",700,500);
  gPad->SetLeftMargin(0.1);
  gPad->SetBottomMargin(0.13);
  gPad->SetTopMargin(1.02);
  //  gPad->SetGridy();
  h_dummy->GetYaxis()->SetRangeUser(0.5,2.);
  h_dummy->GetYaxis()->SetTitleOffset(0.8);
  h_dummy->GetYaxis()->SetTitle("#epsilon_{DATA} / #epsilon_{MC}");
  h_dummy->GetXaxis()->SetLabelSize(0.06);
  h_dummy->GetXaxis()->SetTitle("p_{T} (jet) [GeV]");

  h_dummy->Draw("HIST");

  for (unsigned int i0=0; i0<gr_sf.size(); ++i0) {
    gr_sf[i0]->Draw("E2 sames");
    leg->AddEntry(gr_sf[i0],legnames[i0],"PL");
    // gr_sf_stat[i0]->Draw("P E1 sames");
    // leg->AddEntry(gr_sf_stat[i0],legnames[i0],"L");
  }

  leg->Draw("sames");
  pt_cms->Draw("sames");
  pt_preliminary->Draw("sames");
  pt_lumi.DrawLatexNDC(0.58,0.93,longstring);
  c_sf->Print("sf_"+object+"_"+wp+"_"+mistrate+".png");
  cout<<"end"<<endl;
}

TGraphAsymmErrors *getSFGraph(TString object, TString algo, TString wp, std::vector<TString> ptrange, int ialgo, int nalgos, int color, TString mistrate) {
  
  double xval[20], xvalerr[20];
  double yval[20], yvalerrlo[20], yvalerrhi[20];
  
  for (unsigned int iptrange=0; iptrange<ptrange.size(); ++iptrange) {
    TFile *fdiag = TFile::Open("./"+object+"_"+algo+"_tot/"+mistrate+"/sf_fitDiagnostics_"+object+"_"+algo+"_"+wp+"_"+ptrange[iptrange]+".root", "READONLY" );
    // TFile *fdiag = TFile::Open("./"+path2file+"/sf_fitDiagnostics_"+object+"_"+algo+"_"+wp+"_"+ptrange[iptrange]+".root", "READONLY" );
    TTree *t_   = (TTree*)fdiag->Get("tree_fit_sb");
    TString strCat, strCatLoErr, strCatHiErr;   
    if (object=="T") { strCat = "SF_catp3"; strCatLoErr = "SF_catp3LoErr"; strCatHiErr = "SF_catp3HiErr"; }
    if (object=="W") { strCat = "SF_catp2"; strCatLoErr = "SF_catp2LoErr"; strCatHiErr = "SF_catp2HiErr"; }
    TH1F *h_sf_cat      = new TH1F("h_sf_cat"      , "h_sf_cat"      , 10000,0.,10.);
    TH1F *h_sf_catLoErr = new TH1F("h_sf_catLoErr" , "h_sf_catLoErr" , 10000,0.,10.);
    TH1F *h_sf_catHiErr = new TH1F("h_sf_catHiErr" , "h_sf_catHiErr" , 10000,0.,10.);
    t_->Project("h_sf_cat",strCat);
    t_->Project("h_sf_catLoErr",strCatLoErr);
    t_->Project("h_sf_catHiErr",strCatHiErr);
    
    xval[iptrange]    = (iptrange+0.7) + 0.07*(ialgo - 1.*(nalgos-2));
    xvalerr[iptrange] = 0.03;
    yval[iptrange]    = h_sf_cat->GetMean();
    yvalerrlo[iptrange] = h_sf_catLoErr->GetMean();
    yvalerrhi[iptrange] = h_sf_catHiErr->GetMean();
    //   if (algos[ialgo]=="sdtau21" && ptrange[iptrange]=="low") { yvalerrlo[iptrange] = 0.01; yvalerrhi[iptrange] = 0.01; }
    
    h_sf_cat->Delete();
    h_sf_catLoErr->Delete();
    h_sf_catHiErr->Delete();
    
  } // end looping over the pt bins
  
  TGraphAsymmErrors *gr_sf_tmp = new TGraphAsymmErrors(ptrange.size(),xval,yval,xvalerr,xvalerr,yvalerrlo,yvalerrhi); 
  gr_sf_tmp->SetLineColor(color);
  gr_sf_tmp->SetMarkerColor(color);
  return gr_sf_tmp;
}


TGraphAsymmErrors *getSFGraphSyst(TString object, TString algo, TString wp, std::vector<TString> ptrange, int ialgo, int nalgos, int color, TString extra, TGraphAsymmErrors *gr_nom) {
  
  double xval[20], xvalerr[20];
  double yval[20], yvalerrlo[20], yvalerrhi[20];
  
  for (unsigned int iptrange=0; iptrange<ptrange.size(); ++iptrange) {
    TFile *fdiag = TFile::Open("./"+object+"_"+algo+"_"+extra+"/sf_fitDiagnostics_"+object+"_"+algo+"_"+wp+"_"+ptrange[iptrange]+".root", "READONLY" );
    TTree *t_   = (TTree*)fdiag->Get("tree_fit_sb");
    
    TString strCat, strCatLoErr, strCatHiErr;   
    if (object=="T") { strCat = "SF_catp3"; strCatLoErr = "SF_catp3LoErr"; strCatHiErr = "SF_catp3HiErr"; }
    if (object=="W") { strCat = "SF_catp2"; strCatLoErr = "SF_catp2LoErr"; strCatHiErr = "SF_catp2HiErr"; }
    TH1F *h_sf_cat      = new TH1F("h_sf_cat"      , "h_sf_cat"      , 10000,0.,10.);
    TH1F *h_sf_catLoErr = new TH1F("h_sf_catLoErr" , "h_sf_catLoErr" , 10000,0.,10.);
    TH1F *h_sf_catHiErr = new TH1F("h_sf_catHiErr" , "h_sf_catHiErr" , 10000,0.,10.);
    t_->Project("h_sf_cat",strCat);
    t_->Project("h_sf_catLoErr",strCatLoErr);
    t_->Project("h_sf_catHiErr",strCatHiErr);
    double nom_x = 0; double nom_y = 0; gr_nom->GetPoint(iptrange,nom_x,nom_y); 
    xval[iptrange]    = (iptrange+0.7) + 0.07*(ialgo - 1.*(nalgos-2));
    xvalerr[iptrange] = 0.;
    yval[iptrange]    = nom_y; 
    float yvalerrlo_ = (h_sf_catLoErr->GetMean()/h_sf_cat->GetMean())*(nom_y); if (yvalerrlo_>gr_nom->GetErrorYlow(iptrange))  { yvalerrlo_ = gr_nom->GetErrorYlow(iptrange); }
    float yvalerrhi_ = (h_sf_catHiErr->GetMean()/h_sf_cat->GetMean())*(nom_y); if (yvalerrhi_>gr_nom->GetErrorYhigh(iptrange)) { yvalerrhi_ = gr_nom->GetErrorYhigh(iptrange); }
    yvalerrlo[iptrange] = yvalerrlo_;
    yvalerrhi[iptrange] = yvalerrhi_;
    //   if (algos[ialgo]=="sdtau21" && ptrange[iptrange]=="low") { yvalerrlo[iptrange] = 0.01; yvalerrhi[iptrange] = 0.01; }
    
    h_sf_cat->Delete();
    h_sf_catLoErr->Delete();
    h_sf_catHiErr->Delete();
    
  } // end looping over the pt bins
  
  TGraphAsymmErrors *gr_sf_tmp = new TGraphAsymmErrors(ptrange.size(),xval,yval,xvalerr,xvalerr,yvalerrlo,yvalerrhi); 
  gr_sf_tmp->SetLineColor(color);
  gr_sf_tmp->SetMarkerColor(color);
  return gr_sf_tmp;
}

void getdiscval(float sigeff, TString algo, TString object, TString cut="(0==0)") {

  //TFile *f_sig = TFile::Open("/eos/uscms/store/user/lpcjme/LGOutputs/hrt_muon_20190225/qcd-mg_tree.root" , "READONLY" );
  TFile *f_sig = TFile::Open("/eos/uscms/store/group/lpcjme/noreplica/NanoHRT/Trees/Apr08/qcd/mc_nom/qcd-mg_tree.root" , "READONLY" );
  TTree *t_sig = (TTree*)f_sig->Get("Events");


  int nbins = 4000;
  TString cut_final; int start = 1; int end = nbins+1; 
  TH1F *h_sig = new TH1F("h_sig_"+algo,"h_sig_"+algo,nbins,0.,1.);
  if (algo=="sdtau32") { 
    if (object=="T") { cut_final = "(xsecWeight*puWeight)*("+cut+" && ak8_1_pt>500. && ((ak8_1_dr_fj_top_wqmax<0.8) && (ak8_1_dr_fj_top_b<0.8)) && (ak8_1_mass>0 && ak8_1_mass<210000.))"; }
    t_sig->Project("h_sig_"+algo,"1-ak8_1_tau3/ak8_1_tau2",cut_final); 
  }

  if (algo=="sdtau32btag") { 
    if (object=="T") { cut_final = "(xsecWeight*puWeight)*("+cut+" && ak8_1_pt>500. && ((ak8_1_dr_fj_top_wqmax<0.8) && (ak8_1_dr_fj_top_b<0.8)) && (ak8_1_mass>0 && ak8_1_mass<210000.) && max(ak8_1_sj1_btagCSVV2,ak8_1_sj2_btagCSVV2)>0.5426 )"; }
    t_sig->Project("h_sig_"+algo,"1-ak8_1_tau3/ak8_1_tau2",cut_final); 
  }

  if (algo=="sdtau21") { 
    if (object=="W") { cut_final = "(xsecWeight*puWeight)*("+cut+" && ak8_1_pt>500. && (!((ak8_1_dr_fj_top_wqmax<0.8) && (ak8_1_dr_fj_top_b<0.8))) && ((ak8_1_dr_fj_top_wqmax<0.8) && (ak8_1_dr_fj_top_b>0.8)) && (ak8_1_mass>0 && ak8_1_mass<1050000.) )"; }
    t_sig->Project("h_sig_"+algo,"1-ak8_1_tau2/ak8_1_tau1",cut_final); 
  }

  if (algo=="sdn2") { 
    if (object=="W") { cut_final = "(xsecWeight*puWeight)*("+cut+" && ak8_1_pt>500. && (!((ak8_1_dr_fj_top_wqmax<0.8) && (ak8_1_dr_fj_top_b<0.8))) && ((ak8_1_dr_fj_top_wqmax<0.8) && (ak8_1_dr_fj_top_b>0.8)) && (ak8_1_mass>0 && ak8_1_mass<10500000.) )"; }
    t_sig->Project("h_sig_"+algo,"1-ak8_1_n2b1",cut_final); 
  }

  if (algo=="sdn2ddt") { 
    if (object=="W") { cut_final = "(xsecWeight*puWeight)*("+cut+" && ak8_1_pt>500. && (!((ak8_1_dr_fj_top_wqmax<0.8) && (ak8_1_dr_fj_top_b<0.8))) && ((ak8_1_dr_fj_top_wqmax<0.8) && (ak8_1_dr_fj_top_b>0.8)) && (ak8_1_mass>0 && ak8_1_mass<1050000.) )"; }
    t_sig->Project("h_sig_"+algo,"(0.5-0.5*ak8_1_n2b1ddt)",cut_final); 
  }

  if (algo=="ecftoptag") {  // transformation: 0.5+0.5*ca15_ecfTopTagBDT
    if (object=="T") { cut_final = "(xsecWeight*puWeight)*("+cut+" && ca15_1_pt>500. && ((ca15_1_dr_fj_top_wqmax<0.8) && (ca15_1_dr_fj_top_b<0.8)) && (ca15_1_mass>0 && ca15_1_mass<210000.) && ca15_1_ecfTopTagBDT>-1. )"; }
    t_sig->Project("h_sig_"+algo,"(0.5+0.5*ca15_1_ecfTopTagBDT)",cut_final); 
  }

  if (algo=="hotvr") {  
    if (object=="T") { cut_final = "(xsecWeight*puWeight)*("+cut+" && hotvr_1_pt>500. && ((hotvr_1_dr_fj_top_wqmax<0.8) && (hotvr_1_dr_fj_top_b<0.8)) && (hotvr_1_mass>0 && hotvr_1_mass<2200000.) && hotvr_1_fpt<0.8 && hotvr_1_nsubjets>=3 && hotvr_1_mmin>=50. )"; }
    t_sig->Project("h_sig_"+algo,"(1-hotvr_1_tau32)",cut_final); 
  }

  if (algo=="best") { 
    if (object=="T") { cut_final = "(xsecWeight*puWeight)*("+cut+" && ak8_1_pt>500. && ((ak8_1_dr_fj_top_wqmax<0.8) && (ak8_1_dr_fj_top_b<0.8)))"; }
    if (object=="W") { cut_final = "(xsecWeight*puWeight)*("+cut+" && ak8_1_pt>500. && (!((ak8_1_dr_fj_top_wqmax<0.8) && (ak8_1_dr_fj_top_b<0.8))) && ((ak8_1_dr_fj_top_wqmax<0.8) && (ak8_1_dr_fj_top_b>0.8)))"; }
    t_sig->Project("h_sig_"+algo,"ak8_1_best_"+object+"vsQCD",cut_final); 
  }

  if (algo=="imagetop") { 
    if (object=="T") { cut_final = "(xsecWeight*puWeight)*("+cut+" && ak8_1_pt>500. && ((ak8_1_dr_fj_top_wqmax<0.8) && (ak8_1_dr_fj_top_b<0.8)))"; }
    t_sig->Project("h_sig_"+algo,"ak8_1_image_top",cut_final); 
  }

  if (algo=="imagetopmd") { 
    if (object=="T") { cut_final = "(xsecWeight*puWeight)*("+cut+" && ak8_1_pt>500. && ((ak8_1_dr_fj_top_wqmax<0.8) && (ak8_1_dr_fj_top_b<0.8)))"; }
    t_sig->Project("h_sig_"+algo,"ak8_1_image_top_md",cut_final); 
  }

  if (algo=="deepak8") { 
    if (object=="T") { cut_final = "(xsecWeight*puWeight)*("+cut+" && ak8_1_pt>500. && ((ak8_1_dr_fj_top_wqmax<0.8) && (ak8_1_dr_fj_top_b<0.8)))"; }
    //    if (object=="W") { cut_final = "(xsecWeight*puWeight)*("+cut+" && ak8_1_pt>200. && ((!((ak8_1_dr_fj_top_wqmax<0.8) && (ak8_1_dr_fj_top_b<0.8))) && ((ak8_1_dr_fj_top_wqmax<0.8) && (ak8_1_dr_fj_top_b>0.8))))"; }
    if (object=="W") { cut_final = "(xsecWeight*puWeight)*("+cut+" && ak8_1_pt>500. )"; }
    t_sig->Project("h_sig_"+algo,"ak8_1_DeepAK8_"+object+"vsQCD",cut_final); 
  }

  if (algo=="deepak8md") { 
    if (object=="T") { cut_final = "(xsecWeight*puWeight)*("+cut+" && ak8_1_pt>500. && ((ak8_1_dr_fj_top_wqmax<0.8) && (ak8_1_dr_fj_top_b<0.8)))"; }
    if (object=="W") { cut_final = "(xsecWeight*puWeight)*("+cut+" && ak8_1_pt>500. && (!((ak8_1_dr_fj_top_wqmax<0.8) && (ak8_1_dr_fj_top_b<0.8))) && ((ak8_1_dr_fj_top_wqmax<0.8) && (ak8_1_dr_fj_top_b>0.8)))"; }
    t_sig->Project("h_sig_"+algo,"ak8_1_DeepAK8MD_"+object+"vsQCD",cut_final); 
  }


  float ntot_sig = h_sig->Integral(0,nbins+1);
  for (unsigned int i0=start; i0<end; ++i0) {
    float tmp_sig = h_sig->Integral(i0,nbins+1);
    if ( (tmp_sig/ntot_sig)<sigeff && (tmp_sig/ntot_sig)>0. ) { std::cout << tmp_sig/ntot_sig << " " << h_sig->GetBinCenter(i0) << "\n"; break;  }
  } 
}

TH1F *rescaleXaxis(TH1F *inputhisto, float xmin, float xmax) {
  TH1::SetDefaultSumw2(kTRUE);

  int nbins = inputhisto->GetNbinsX();
  TString name = inputhisto->GetName();
  TH1F *outputhisto = new TH1F(name,name,nbins,xmin,xmax);

  for (unsigned int i0=0; i0<nbins; ++i0) {
    outputhisto->SetBinContent(i0+1,inputhisto->GetBinContent(i0+1));
    outputhisto->SetBinError(i0+1,inputhisto->GetBinError(i0+1));
  }

  return outputhisto;
}

void rescaleXaxis(TGraphAsymmErrors *g, double xmin, double scaleX) {
  TH1::SetDefaultSumw2(kTRUE);

  int N=g->GetN();
  double *x=g->GetX();
  double *xerrh=g->GetEXhigh();
  double *xerrl=g->GetEXlow();
  int i=0; while(i<N) {
    x[i]=xmin+x[i]*scaleX;
    xerrh[i]=0.;
    xerrl[i]=0.;
    i=i+1;
  }
  g->GetHistogram()->Delete();
  g->SetHistogram(0);
}


TGraphAsymmErrors *getTGraphAsymmErrorsFromHisto(TH1 *input) {
  TH1::SetDefaultSumw2(kTRUE);

  int nbins = input->GetNbinsX();
  double x[nbins], y[nbins], exl[nbins], exh[nbins], eyl[nbins], eyh[nbins];
  for (unsigned int i0=0; i0<nbins; ++i0) {
    x[i0] = input->GetBinCenter(i0+1); 
    exl[i0] = 0.;
    exh[i0] = 0.;
    y[i0] = input->GetBinContent(i0+1);
    eyl[i0] = input->GetBinError(i0+1);
    eyh[i0] = input->GetBinError(i0+1);
  }
  TGraphAsymmErrors *gr = new TGraphAsymmErrors(nbins,x,y,exl,exh,eyl,eyh);

  return gr;
}


TH1F *getDataMCratio(TGraphAsymmErrors *indata, TH1F *inMC) {
  TH1::SetDefaultSumw2(kTRUE);

  TH1F *h_data = (TH1F*)inMC->Clone("h_data"); h_data->SetName("h_data");
  for (unsigned int i0=0; i0<inMC->GetNbinsX(); ++i0) {
    h_data->SetBinContent(i0+1, indata->GetY()[i0]);
    h_data->SetBinError(i0+1, (indata->GetEYlow()[i0]+indata->GetEYhigh()[i0])/2.);
  }

  TH1F *h_ratio = (TH1F*)h_data->Clone("h_ratio");
  h_ratio->Divide(h_data,inMC);
  h_ratio->SetMarkerStyle(20); h_ratio->SetMarkerSize(1);
  h_ratio->SetLineWidth(2); h_ratio->SetLineStyle(1);

  return h_ratio;
}

void makeMatchingEffPlots(TString obj_, TString year) {
  TH1::SetDefaultSumw2(kTRUE);

  setTDRStyle();
  gROOT->SetBatch(false);
  gStyle->SetOptStat(0);
  gStyle->SetOptFit(1);
  gStyle->SetPalette(1);
  gStyle->SetOptTitle(0);
  TH1::SetDefaultSumw2(kTRUE);


  TFile *f_;
  TString intLumi;
  TString EOSCMS="root://eoscms.cern.ch/";
  TString path=EOSCMS+"/eos/cms/store/group/phys_jetmet/nbinnorj/WTopTagging/ntuples_HRTSF/";
  if (obj_ == "top") { f_ = TFile::Open("/eos/uscms/store/group/lpcjme/noreplica/NanoHRT/Trees/Apr08/drplots/zprime_tt.root" , "READONLY" ); }
  // if (obj_ == "w") { f_ = TFile::Open("/eos/uscms/store/group/lpcjme/noreplica/NanoHRT/Trees/Apr08/drplots/zprime_ww.root"   , "READONLY" ); }
  if (obj_ == "w") { 
    if      (year == "2016") { f_ = TFile::Open(path+"2016/mc_nom/sm_tree.root" , "READONLY" ); intLumi="36.8"; }
    else if (year == "2017") { f_ = TFile::Open(path+"29July/mc_nom/sm_tree.root" , "READONLY" ); intLumi="41.53"; }
    else if (year == "2018") { f_ = TFile::Open(path+"3Oct_For_Copy/mc_nom/sm_tree.root" , "READONLY" ); intLumi="59.74"; }
  }
  TTree *t_ = (TTree*)f_->Get("Events");


  TString c_had_ak8;
  TString c_had_ak8_dr0p6; 
  TString c_had_ak8_dr0p6_q; 
  TString c_had_ca15; 
  TString c_had_ca15_dr1p2; 
  TString c_had_ca15_dr1p2_q; 
  // if (obj_ == "top") {
  //   c_had_ak8         = "(ak8_1_is_"+obj_+"==1 && ak8_1_pt>200 && abs(ak8_1_eta)<2.4 && ak8_1_dr_fj_"+obj_+"<3.)"; 
  //   c_had_ak8_dr0p6   = "(ak8_1_is_"+obj_+"==1 && ak8_1_pt>200 && ak8_1_dr_fj_"+obj_+"<0.6 && abs(ak8_1_eta)<2.4)"; 
  //   c_had_ak8_dr0p6_q = "(ak8_1_is_"+obj_+"==1 && ak8_1_pt>200 && ak8_1_dr_fj_"+obj_+"<0.6 && (ak8_1_dr_fj_top_wqmax<0.6) && (ak8_1_dr_fj_top_b<0.6) && abs(ak8_1_eta)<2.4)"; 
  //   c_had_ca15         = "(ca15_1_is_"+obj_+"==1 && ca15_1_pt>200 && abs(ca15_1_eta)<2.4 && ca15_1_dr_fj_"+obj_+"<3.)"; 
  //   c_had_ca15_dr1p2   = "(ca15_1_is_"+obj_+"==1 && ca15_1_pt>200 && ca15_1_dr_fj_"+obj_+"<1.2  && abs(ca15_1_eta)<2.4)"; 
  //   c_had_ca15_dr1p2_q = "(ak8_1_is_"+obj_+"==1 && ca15_1_pt>200 && ca15_1_dr_fj_"+obj_+"<1.2 && (ca15_1_dr_fj_top_wqmax<1.2) && (ca15_1_dr_fj_top_b<1.2) && abs(ca15_1_eta)<2.4)"; 
  // }

  if (obj_ == "w") {
    // c_had_ak8         = "(ak8_1_is_"+obj_+"==1 && ak8_1_pt>200 && abs(ak8_1_eta)<2.4 && ak8_1_dr_fj_"+obj_+"<3.)"; 
    // c_had_ak8_dr0p6   = "(ak8_1_is_"+obj_+"==1 && ak8_1_pt>200 && ak8_1_dr_fj_"+obj_+"<0.6 && abs(ak8_1_eta)<2.4)"; 
    // c_had_ak8_dr0p6_q = "(ak8_1_is_"+obj_+"==1 && ak8_1_pt>200 && ak8_1_dr_fj_"+obj_+"<0.6 && (ak8_1_dr_fj_top_wqmax<0.6) && abs(ak8_1_eta)<2.4)"; 
    // c_had_ca15         = "(ca15_1_is_"+obj_+"==1 && ca15_1_pt>200 && abs(ca15_1_eta)<2.4 && ca15_1_dr_fj_"+obj_+"<3.)"; 
    // c_had_ca15_dr1p2   = "(ca15_1_is_"+obj_+"==1 && ca15_1_dr_fj_"+obj_+"<1.2  && abs(ca15_1_eta)<2.4)"; 
    // c_had_ca15_dr1p2_q = "(ak8_1_is_"+obj_+"==1 &&  ca15_1_pt>200 && ca15_1_dr_fj_"+obj_+"<1.2 && (ca15_1_dr_fj_top_wqmax<1.2) && abs(ca15_1_eta)<2.4)"; 
    
    c_had_ak8          = "(ak8_1_pt>100 && abs(ak8_1_eta)<2.4)";
    // c_had_ak8_dr0p6_q  = "(ak8_1_pt>200 && abs(ak8_1_eta)<2.4)"; 
    // c_had_ak8_dr0p6    = "(ak8_1_pt>100 && abs(ak8_1_eta)<2.4 && ak8_1_dr_fj_"+obj_+"<0.6)"; 
    c_had_ak8_dr0p6_q  = "(ak8_1_pt>100 && abs(ak8_1_eta)<2.4 && ak8_1_dr_fj_top_wqmax<0.6)"; 
    // c_had_ca15         = "(ca15_1_pt>200 && abs(ca15_1_eta)<2.4 && ca15_1_dr_fj_"+obj_+"<3.)"; 
    // c_had_ca15_dr1p2   = "(ca15_1_dr_fj_"+obj_+"<1.2  && abs(ca15_1_eta)<2.4)"; 
    // c_had_ca15_dr1p2_q = "(ca15_1_pt>200 && ca15_1_dr_fj_"+obj_+"<1.2 && (ca15_1_dr_fj_top_wqmax<1.2) && abs(ca15_1_eta)<2.4)"; 
  }

  int bins; float xmin, xmax;
  if (obj_ == "top") { bins = 18; xmin = 100.; xmax = 1000.; }
  if (obj_ == "w") { bins = 10; xmin = 100.; xmax = 600.; }
  // TH1D* h_pt_ak8   = (TH1D*)create1Dhisto("sample",t_,"1",c_had_ak8,"ak8_1_gen"+obj_+"pt",bins,xmin,xmax,false,1,1,"h_pt",false,false);             
  TH1D* h_pt_ak8   = (TH1D*)create1Dhisto("sample",t_,intLumi,c_had_ak8,"leptonicW_pt",bins,xmin,xmax,false,1,1,"h_pt",false,false);             
  // TH1D* h_pt_dr0p6 = (TH1D*)create1Dhisto("sample",t_,"1",c_had_ak8_dr0p6,"ak8_1_gen"+obj_+"pt",bins,xmin,xmax,false,2,1,"h_pt_dr0p6",false,false); 
  // TH1D* h_pt_dr0p6_q = (TH1D*)create1Dhisto("sample",t_,"1",c_had_ak8_dr0p6_q,"ak8_1_gen"+obj_+"pt",bins,xmin,xmax,false,2,1,"h_pt_dr0p6_q",false,false);
  // TH1D* h_pt_dr0p6 = (TH1D*)create1Dhisto("sample",t_,"1",c_had_ak8_dr0p6,"ak8_1_pt",bins,xmin,xmax,false,2,1,"h_pt_dr0p6",false,false);
  TH1D* h_pt_dr0p6_q = (TH1D*)create1Dhisto("sample",t_,intLumi,c_had_ak8_dr0p6_q,"leptonicW_pt",bins,xmin,xmax,false,2,1,"h_pt_dr0p6_q",false,false);  
  // TH1D* h_pt_ca15  = (TH1D*)create1Dhisto("sample",t_,"1",c_had_ca15,"ca15_1_gen"+obj_+"pt",bins,xmin,xmax,false,1,1,"h_pt",false,false);             
  // TH1D* h_pt_dr1p2 = (TH1D*)create1Dhisto("sample",t_,"1",c_had_ca15_dr1p2,"ca15_1_gen"+obj_+"pt",bins,xmin,xmax,false,1,1,"h_pt_dr1p2",false,false);
  // TH1D* h_pt_dr1p2_q = (TH1D*)create1Dhisto("sample",t_,"1",c_had_ca15_dr1p2_q,"ca15_1_gen"+obj_+"pt",bins,xmin,xmax,false,1,1,"h_pt_dr1p2_q",false,false);
  

  // cosmetiscs
  h_pt_ak8->SetFillColor(0); h_pt_ak8->SetMarkerColor(1); h_pt_ak8->SetMarkerStyle(20); h_pt_ak8->SetMarkerSize(1.);
  // h_pt_dr0p6->SetFillColor(0); h_pt_dr0p6->SetMarkerColor(2); h_pt_dr0p6->SetMarkerStyle(20); h_pt_dr0p6->SetMarkerSize(1.);
  h_pt_dr0p6_q->SetFillColor(0); h_pt_dr0p6_q->SetMarkerColor(2); h_pt_dr0p6_q->SetMarkerStyle(24); h_pt_dr0p6_q->SetMarkerSize(1.);
  // h_pt_ca15->SetFillColor(0); h_pt_ca15->SetMarkerColor(1); h_pt_ca15->SetMarkerStyle(20); h_pt_ca15->SetMarkerSize(1.);
  // h_pt_dr1p2->SetFillColor(0); h_pt_dr1p2->SetMarkerColor(1); h_pt_dr1p2->SetMarkerStyle(21); h_pt_dr1p2->SetMarkerSize(1.);
  // h_pt_dr1p2_q->SetFillColor(0); h_pt_dr1p2_q->SetMarkerColor(1); h_pt_dr1p2_q->SetMarkerStyle(25); h_pt_dr1p2_q->SetMarkerSize(1.);
  
  // TH1D* h_pt_dr0p6_r   = (TH1D*)h_pt_dr0p6->Clone("h_pt_dr0p6_r"); h_pt_dr0p6_r->Divide(h_pt_dr0p6,h_pt_ak8);
  TH1D* h_pt_dr0p6_q_r = (TH1D*)h_pt_dr0p6_q->Clone("h_pt_dr0p6_q_r"); h_pt_dr0p6_q_r->Divide(h_pt_dr0p6_q,h_pt_ak8);
  // TH1D* h_pt_dr1p2_r   = (TH1D*)h_pt_dr1p2->Clone("h_pt_dr1p2_r"); h_pt_dr1p2_r->Divide(h_pt_dr1p2,h_pt_ca15);
  // TH1D* h_pt_dr1p2_q_r = (TH1D*)h_pt_dr1p2_q->Clone("h_pt_dr1p2_q_r"); h_pt_dr1p2_q_r->Divide(h_pt_dr1p2_q,h_pt_ca15);


  TPaveText *pt_cms = new TPaveText(0.11,0.77,0.4,0.9,"NDC");
  pt_cms->SetFillStyle(0);
  pt_cms->SetFillColor(0);
  pt_cms->SetLineWidth(0);
  pt_cms->AddText("CMS");
  pt_cms->SetTextSize(0.08);

  TPaveText *pt_preliminary = new TPaveText(0.2,0.63,0.42,0.9,"NDC");
  pt_preliminary->SetFillStyle(0);
  pt_preliminary->SetFillColor(0);
  pt_preliminary->SetLineWidth(0);
  pt_preliminary->AddText("Preliminary");
  pt_preliminary->SetTextFont(52);
  pt_preliminary->SetTextSize(0.06);

  TLatex pt_lumi;
  // const char *longstring ="35.9 fb^{-1} (13 TeV)";
  const char *longstring ="";
  if (year == "2016") {longstring ="36.8 fb^{-1} (13 TeV)";}
  else if (year == "2017") {longstring ="41.53 fb^{-1} (13 TeV)";}
  else if (year == "2018") {longstring ="59.74 fb^{-1} (13 TeV)";}
  pt_lumi.SetTextSize(0.05);
  pt_lumi.SetTextFont(42);

  TLegend* leg = new TLegend(0.55,0.68,0.92,0.9);
  leg->SetFillStyle(0);
  leg->SetFillColor(0);
  leg->SetLineWidth(0);
  TString objb_; if (obj_ == "top") { objb_ = "t"; } else {  objb_ = "W"; }
  // leg->AddEntry(h_pt_dr0p6_r,"#DeltaR(AK8,"+objb_+")<0.6","P");
  // leg->AddEntry(h_pt_dr1p2_r,"#DeltaR(CA15,"+objb_+")<1.2","P");
  leg->AddEntry(h_pt_dr0p6_q_r,"max#DeltaR(AK8,q)<0.6","P");
  // leg->AddEntry(h_pt_dr1p2_q_r,"max#DeltaR(CA15,q)<1.2","P");

  TCanvas *c_dr = new TCanvas("c_dr","c_dr",500,500);
  gPad->SetRightMargin(0.05);
  gPad->SetLeftMargin(0.13);
  gPad->SetBottomMargin(0.15);
  gPad->SetTopMargin(0.09);
  h_pt_dr0p6_q_r->GetYaxis()->SetRangeUser(0.,1.5);
  h_pt_dr0p6_q_r->GetYaxis()->SetTitle("Reconstruction efficiency");
  if (obj_== "top") { h_pt_dr0p6_q_r->GetXaxis()->SetTitle("t quark p_{T} [GeV]"); } 
  else  { h_pt_dr0p6_q_r->GetXaxis()->SetTitle("W boson p_{T} [GeV]"); } 
  h_pt_dr0p6_q_r->GetYaxis()->SetTitleOffset(1.08);
  h_pt_dr0p6_q_r->GetXaxis()->SetTitleOffset(1.1);
  h_pt_dr0p6_q_r->Draw("P");
  // h_pt_dr0p6_r->Draw("P sames");
  // h_pt_dr1p2_r->Draw("P sames");
  // h_pt_dr1p2_q_r->Draw("P sames");
  pt_cms->Draw("same");
  pt_preliminary->Draw("same");
  pt_lumi.DrawLatexNDC(0.55,0.93,longstring);
  leg->Draw("same");

  c_dr->Print("eff_"+obj_+year+".png");

  leg->Clear();

  leg->SetFillStyle(0);
  leg->SetFillColor(0);
  leg->SetLineWidth(0);
  leg->AddEntry(h_pt_dr0p6_q,"max#DeltaR(AK8,q)<0.6","P");
  leg->AddEntry(h_pt_ak8,"None","P");

  TCanvas *d_dr = new TCanvas("d_dr","d_dr",500,500);
  gPad->SetRightMargin(0.05);
  gPad->SetLeftMargin(0.13);
  gPad->SetBottomMargin(0.15);
  gPad->SetTopMargin(0.09);
  h_pt_dr0p6_q->GetYaxis()->SetTitle("Number of events");
  if (obj_== "top") { h_pt_dr0p6_q->GetXaxis()->SetTitle("t quark p_{T} [GeV]"); } 
  else  { h_pt_dr0p6_q->GetXaxis()->SetTitle("W boson p_{T} [GeV]"); } 
  h_pt_dr0p6_q->GetYaxis()->SetTitleOffset(1.08);
  h_pt_dr0p6_q->GetXaxis()->SetTitleOffset(1.1);
  h_pt_dr0p6_q->Draw("P");
  
  leg->Draw("same");

  d_dr->Print("evt_"+obj_+year+".png");
}

void getMistag(TString object, TString wp, TString year, TString mistrate) {
  setTDRStyle();
  gROOT->SetBatch(false);
  gStyle->SetOptStat(0);
  gStyle->SetOptFit(1);
  gStyle->SetPalette(1);
  TH1::SetDefaultSumw2(kTRUE);

  const char *intLumi;
  TFile *f_mc; TFile *f_data;
  TString EOSCMS="root://eoscms.cern.ch/";
  TString path=EOSCMS+"/eos/cms/store/group/phys_jetmet/nbinnorj/WTopTagging/ntuples_HRTSF/";
  if (object == "W") { 
    if      (year == "2016") { f_mc = TFile::Open(path+"2016/mc_nom/sm_tree.root" , "READONLY" ); 
                               f_data = TFile::Open(path+"2016/data/singlemu_tree.root", "READONLY"); 
                               intLumi="36.8"; }
    else if (year == "2017") { f_mc = TFile::Open(path+"29July/mc_nom/sm_tree.root" , "READONLY" ); 
                               f_data = TFile::Open(path+"29July/data/singlemu_tree.root", "READONLY"); 
                               intLumi="41.53"; }
    else if (year == "2018") { f_mc = TFile::Open(path+"3Oct_For_Copy/mc_nom/sm_tree.root" , "READONLY" ); 
                               f_data = TFile::Open(path+"3Oct_For_Copy/data/singlemu_tree.root", "READONLY"); 
                               intLumi="59.74"; }
  }
  TTree *t_mc   = (TTree*)f_mc->Get("Events");
  TTree *t_data = (TTree*)f_data->Get("Events");

  std::vector<TString> algos;    algos.clear();
  std::vector<TString> legnames; legnames.clear();
  std::vector<TString> ptrange;  ptrange.clear();
  std::vector<int>     colors;   colors.clear();
    
  if (object=="W") {
    // algos.push_back("sdtau21");     legnames.push_back("m_{SD}+#tau_{21}");   colors.push_back(800);
    algos.push_back("deepak8");     legnames.push_back("DeepAK8");            colors.push_back(866);
  }
  // baseline selection
  TString c_base;
  // c_base = "(ht>1000 && n_ak8>=1 && n_ca15>=1)";
  // c_base = "(n_ak8>=1 && n_ca15>=1)";
  c_base = "(n_ak8>=1 || n_ca15>=1)";
  TString cut_incl = c_base;
  
  int bins; float xmin, xmax;
  // xbins={200.0, 250.0, 350.0, 400.0, 500.0, 600.0, 800.0}
  if (object=="W") { bins = 20; xmin = 200.; xmax = 800.; }

  float getmed = median(algos);
  std::vector<TH1D*> eff_mc; eff_mc.clear();
  std::vector<TH1D*> eff_data; eff_data.clear();
  std::vector<TH1D*> sf; sf.clear();

  for (unsigned int ialgo=0; ialgo<algos.size(); ++ialgo) {
    
    TFile rootfile(EOSDIR+"mistag_"+year+"_"+algos[ialgo]+".root","RECREATE");
    
    TString c_algo_wp, c_jet;
    if (algos[ialgo] == "sdtau21")     { c_jet = "ak8";   if (wp == "JMAR") { c_algo_wp = "((1-"+c_jet+"_1_tau2/"+c_jet+"_1_tau1)>0.6781)"; } }
    if (algos[ialgo] == "deepak8")     { c_jet = "ak8";   if (wp == "JMAR" && object=="W") { c_algo_wp = "("+c_jet+"_1_DeepAK8_"+(TString)object+"vsQCD>0.9383)"; }
    }

    TString c_mass;
    if (object=="W") { c_mass = "("+c_jet+"_1_mass>65. && "+c_jet+"_1_mass<105.)"; }
    //TString c_mass = "("+c_jet+"_1_mass>0.)";

    xmin = xmin - (2.*(getmed)) + (2.*ialgo);
    xmax = xmax - (2.*(getmed)) + (2.*ialgo);
    const char *lumi = intLumi;

    TH1D *h_incl_mc   = create1Dhisto("sample",t_mc,lumi,cut_incl,c_jet+"_1_pt",bins,xmin,xmax,false,1,1,"h_incl_mc",false,false);     h_incl_mc->SetFillColor(0);  
    TH1D *h_num_mc = create1Dhisto("sample",t_mc,lumi,cut_incl+" && "+c_algo_wp+" && "+c_mass,c_jet+"_1_pt",bins,xmin,xmax,false,colors[ialgo],1,"h_num_mc_"+algos[ialgo],false,false); 
    TH1D *h_mc_r   = (TH1D*)h_num_mc->Clone("h_mc_r_"+algos[ialgo]); 
    h_mc_r->Divide(h_num_mc,h_incl_mc,1.,1.,"B");
    h_mc_r->Write("MC");

    TH1D *h_incl_data = create1Dhisto("sample",t_data,lumi,cut_incl,c_jet+"_1_pt",bins,xmin,xmax,false,1,1,"h_incl_data",false,true); h_incl_data->SetFillColor(0);
    TH1D *h_num_data = create1Dhisto("sample",t_data,lumi,cut_incl+" && "+c_algo_wp+" && "+c_mass,c_jet+"_1_pt",bins,xmin,xmax,false,colors[ialgo],1,"h_num_data_"+algos[ialgo],false,true);
    TH1D *h_data_r = (TH1D*)h_num_data->Clone("h_data_r_"+algos[ialgo]); 
    h_data_r->Divide(h_num_data,h_incl_data,1.,1.,"B");
    h_data_r->Write("Data");

    TH1D *h_sf = (TH1D*)h_mc_r->Clone("h_sf_"+algos[ialgo]); 
    h_sf->Divide(h_data_r,h_mc_r);
    h_sf->SetLineColor(colors[ialgo]); h_sf->SetMarkerColor(colors[ialgo]); h_sf->SetFillColor(0);
    h_sf->SetMarkerSize(1.);
    h_sf->Write("SF");

    eff_mc.push_back(h_mc_r);
    eff_data.push_back(h_data_r);
    sf.push_back(h_sf);
    
    h_incl_mc->Delete(); h_incl_data->Delete(); 
  } // end of looping over the algos

  TLegend* leg;
  if (object=="W") { leg = new TLegend(0.75,0.66,0.92,0.89); }
  leg->SetFillStyle(0);
  leg->SetFillColor(0);
  leg->SetLineWidth(0);

  TPaveText *pt_cms = new TPaveText(0.10,0.77,0.4,0.9,"NDC");
  pt_cms->SetFillStyle(0);
  pt_cms->SetFillColor(0);
  pt_cms->SetLineWidth(0);
  pt_cms->AddText("CMS");
  pt_cms->SetTextSize(0.08);

  TPaveText *pt_preliminary = new TPaveText(0.18,0.63,0.4,0.9,"NDC");
  pt_preliminary->SetFillStyle(0);
  pt_preliminary->SetFillColor(0);
  pt_preliminary->SetLineWidth(0);
  pt_preliminary->AddText("Preliminary");
  pt_preliminary->SetTextFont(52);
  pt_preliminary->SetTextSize(0.06);
  
  TPaveText *pt_lumi = new TPaveText(0.8,0.9,0.9,1.0,"NDC");
  pt_lumi->SetFillStyle(0);
  pt_lumi->SetFillColor(0);
  pt_lumi->SetLineWidth(0);
  if (year == "2016") {pt_lumi->AddText("36.8 fb^{-1} (13 TeV)");}
  else if (year == "2017") {pt_lumi->AddText("41.53 fb^{-1} (13 TeV)");}
  else if (year == "2018") {pt_lumi->AddText("59.74 fb^{-1} (13 TeV)");}
  pt_lumi->SetTextFont(52);
  pt_lumi->SetTextSize(0.06);

  // TLatex pt_lumi;
  // const char *longstring = "";
  // if (year == "2016") {longstring ="36.8 fb^{-1} (13 TeV)";}
  // else if (year == "2017") {longstring ="41.53 fb^{-1} (13 TeV)";}
  // else if (year == "2018") {longstring ="59.74 fb^{-1} (13 TeV)";}
  // pt_lumi.SetTextSize(0.07);
  // pt_lumi.SetTextFont(42);

  // TCanvas *c_sf = new TCanvas("c_sf","c_sf",700,500);
  // gStyle->SetErrorX(0.);
  // gPad->SetLeftMargin(0.1);
  // gPad->SetBottomMargin(0.13);
  // gPad->SetTopMargin(1.02);
  // sf[getmed]->GetYaxis()->SetRangeUser(0.5,2.);
  // sf[getmed]->GetYaxis()->SetTitleOffset(0.8);
  // sf[getmed]->GetYaxis()->SetTitle("#epsilon_{DATA} / #epsilon_{MC}");
  // sf[getmed]->GetXaxis()->SetLabelSize(0.06);
  // sf[getmed]->GetXaxis()->SetTitle("p_{T} (jet) [GeV]");
  // sf[getmed]->Draw("P E0");
  // for (unsigned int i0=0; i0<sf.size(); ++i0) { leg->AddEntry(sf[i0],legnames[i0],"PL"); if (i0!=getmed) { sf[i0]->Draw("P E0 sames"); } }
  // leg->Draw("sames");
  // pt_cms->Draw("sames");
  // pt_preliminary->Draw("sames");
  // pt_lumi.DrawLatexNDC(0.58,0.93,longstring);
  // c_sf->Print("sf_"+year+".png");
  // leg->Clear();

  TCanvas *c_mistag = new TCanvas("c_mistag","c_mistag",1200 , 1200);
  c_mistag->Divide(1,2);

  c_mistag->cd(1);
  for (unsigned int i0=0; i0<eff_mc.size(); ++i0) { 
    if (i0==0) { eff_mc[i0]->GetYaxis()->SetRangeUser(0.0,1.0);
                 eff_mc[i0]->GetYaxis()->SetTitleOffset(0.8);
                 eff_mc[i0]->GetYaxis()->SetTitle("#epsilon_{MC}");
                 eff_mc[i0]->GetXaxis()->SetLabelSize(0.06);
                 eff_mc[i0]->GetXaxis()->SetTitle("p_{T} (jet) [GeV]");
                 eff_mc[i0]->Draw("P E0"); }               
    else       { eff_mc[i0]->Draw("P E0 sames"); }
    leg->AddEntry(eff_mc[i0],legnames[i0],"LP");
  }
  leg->Draw("sames");
  pt_cms->Draw("sames");
  pt_preliminary->Draw("sames");
  pt_lumi->Draw("sames");
  // pt_lumi.DrawLatexNDC(0.58,1.0,longstring);
  leg->Clear();

  c_mistag->cd(2);
  for (unsigned int i0=0; i0<eff_data.size(); ++i0) { 
    if (i0==0) { eff_data[i0]->GetYaxis()->SetRangeUser(0.0,1.0);
                 eff_data[i0]->GetYaxis()->SetTitleOffset(0.8);
                 eff_data[i0]->GetYaxis()->SetTitle("#epsilon_{Data}");
                 eff_data[i0]->GetXaxis()->SetLabelSize(0.06);
                 eff_data[i0]->GetXaxis()->SetTitle("p_{T} (jet) [GeV]");
                 eff_data[i0]->Draw("P E0"); } 
    else       { eff_data[i0]->Draw("P E0 sames"); }
    leg->AddEntry(eff_data[i0],legnames[i0],"LP");
  }
  leg->Draw("sames");
  pt_cms->Draw("sames");
  pt_preliminary->Draw("sames");
  pt_lumi->Draw("sames");
  // pt_lumi.DrawLatexNDC(0.58,1.0,longstring);

  c_mistag->Print(EOSDIR+"mistag_"+year+"_"+mistrate+".pdf");
  c_mistag->Print(EOSDIR+"mistag_"+year+"_"+mistrate+".png");
}

void drawMistag(TString) {}

void getMisTagRates(TString sample, TString object, TString wp) {
  // sample: photon qcd  
  setTDRStyle();
  gROOT->SetBatch(false);
  gStyle->SetOptStat(0);
  gStyle->SetOptFit(1);
  gStyle->SetPalette(1);
  TH1::SetDefaultSumw2(kTRUE);

  float intLumi     = 36.8;
  ostringstream tmpLumi;
  tmpLumi << intLumi;
  TString lumi = tmpLumi.str();


  TFile *f_mc; TFile *f_mc_b; TFile *f_data;
  if (sample == "photon") {
    TString path = "/eos/uscms/store/group/lpcjme/noreplica/NanoHRT/Trees/Apr08/"+sample+"/";
    f_mc = TFile::Open(path+"/mc_nom/sm.root" , "READONLY" );
    //f_mc = TFile::Open(path+"/mc_nom/photon_tree.root" , "READONLY" );
    f_mc_b = TFile::Open(path+"/mc_nom/sm.root" , "READONLY" );
    f_data = TFile::Open(path+"/data/singlephoton_tree.root" , "READONLY" );
  }

  if (sample == "qcd") {
    TString path = "/eos/uscms/store/group/lpcjme/noreplica/NanoHRT/Trees/Apr08/"+sample+"/";
    //f_mc = TFile::Open(path+"/mc_nom/qcd-mg_tree.root" , "READONLY" );
    f_mc = TFile::Open(path+"/mc_nom/qcd-herwig_tree.root" , "READONLY" );
    f_mc_b = TFile::Open(path+"/mc_nom/sm_noqcd.root" , "READONLY" );
    f_data = TFile::Open(path+"/data/jetht_tree.root" , "READONLY" );
  }
  TTree *t_mc   = (TTree*)f_mc->Get("Events");
  TTree *t_mc_b = (TTree*)f_mc_b->Get("Events");
  TTree *t_data = (TTree*)f_data->Get("Events");

  std::vector<TString> algos;    algos.clear();
  std::vector<TString> algo;     algos.clear();
  std::vector<TString> legnames; legnames.clear();
  std::vector<TString> ptrange;  ptrange.clear();
  std::vector<int>     colors;   colors.clear();
  
  if (object=="T") {
    algos.push_back("sdtau32");     legnames.push_back("m_{SD}+#tau_{32}");       colors.push_back(800);
    algos.push_back("sdtau32btag"); legnames.push_back("m_{SD}+#tau_{32}+b-tag"); colors.push_back(632);
    //algos.push_back("hotvr");       legnames.push_back("HOTVR");                  colors.push_back(812);
    algos.push_back("ecftoptag");   legnames.push_back("CA15-ECF");               colors.push_back(419);
    algos.push_back("best");        legnames.push_back("BEST");                   colors.push_back(882);
    algos.push_back("imagetop");    legnames.push_back("ImageTop");               colors.push_back(603);
    algos.push_back("imagetopmd");  legnames.push_back("ImageTop-MD");            colors.push_back(600);
    algos.push_back("deepak8");     legnames.push_back("DeepAK8");                colors.push_back(866);
    algos.push_back("deepak8md");   legnames.push_back("DeepAK8-MD");             colors.push_back(616);
  }

  if (object=="W") {
    algos.push_back("sdtau21");     legnames.push_back("m_{SD}+#tau_{21}");   colors.push_back(800);
    algos.push_back("sdn2");        legnames.push_back("m_{SD}+N_{2}");       colors.push_back(408);
    algos.push_back("sdn2ddt");     legnames.push_back("m_{SD}+N_{2}^{DDT}"); colors.push_back(419);
    algos.push_back("best");        legnames.push_back("BEST");               colors.push_back(882);
    algos.push_back("deepak8");     legnames.push_back("DeepAK8");            colors.push_back(866);
    algos.push_back("deepak8md");   legnames.push_back("DeepAK8-MD");         colors.push_back(616);
  }

  // baseline selection
  TString c_base;
  if (sample == "photon") { c_base = "(passPhoton165_HE10 && n_ak8>=1 && n_ca15>=1 && nphotons>=1 && pho_1_pt>200.)"; }
  if (sample == "qcd")    { c_base = "(ht>1000 && n_ak8>=1 && n_ca15>=1)"; }
  TString cut_incl = c_base;
  
  int bins; float xmin, xmax;
  if (sample == "photon") {
    if (object=="T") { bins = 7; xmin = 300.; xmax = 1000.; }
    if (object=="W") { bins = 8; xmin = 200.; xmax = 1000.; }
  }
  if (sample == "qcd")    { 
    if (object=="T") { bins = 12; xmin = 300.; xmax = 1500.; }
    if (object=="W") { bins = 13; xmin = 200.; xmax = 1500.; }
  }

  float getmed = median(algos);
  std::vector<TH1D*> eff_mc; eff_mc.clear();
  std::vector<TH1D*> eff_data; eff_data.clear();
  std::vector<TH1D*> sf; sf.clear();
  for (unsigned int ialgo=0; ialgo<algos.size(); ++ialgo) {
    TString c_algo_wp, c_jet;
    if (algos[ialgo] == "sdtau32")     { c_jet = "ak8";   if (wp == "JMAR") { c_algo_wp = "((1-"+c_jet+"_1_tau3/"+c_jet+"_1_tau2)>0.4909)"; } }
    if (algos[ialgo] == "sdtau32btag") { c_jet = "ak8";   if (wp == "JMAR") { c_algo_wp = "((1-"+c_jet+"_1_tau3/"+c_jet+"_1_tau2)>0.3881 && max("+c_jet+"_1_sj1_btagCSVV2,"+c_jet+"_1_sj2_btagCSVV2)>0.5426)"; } }
    if (algos[ialgo] == "ecftoptag")   { c_jet = "ca15";  if (wp == "JMAR") { c_algo_wp = "( "+c_jet+"_1_ecfTopTagBDT>-1. && (0.5+0.5*"+c_jet+"_1_ecfTopTagBDT)>0.7831)"; } }
    if (algos[ialgo] == "sdtau21")     { c_jet = "ak8";   if (wp == "JMAR") { c_algo_wp = "((1-"+c_jet+"_1_tau2/"+c_jet+"_1_tau1)>0.6781)"; } }
    if (algos[ialgo] == "sdn2")        { c_jet = "ak8";   if (wp == "JMAR") { c_algo_wp = "((1-"+c_jet+"_1_n2b1)>0.7643)"; } }
    if (algos[ialgo] == "sdn2ddt")     { c_jet = "ak8";   if (wp == "JMAR") { c_algo_wp = "((0.5-0.5*"+c_jet+"_1_n2b1ddt)>0.4891)"; } }
    if (algos[ialgo] == "hotvr")       { c_jet = "hotvr"; if (wp == "JMAR") { c_algo_wp = "( && hotvr_1_fpt<0.8 && hotvr_1_nsubjets>=3 && hotvr_1_mmin>=50. && (1-hotvr_1_tau32)>0.4504)"; } }
    if (algos[ialgo] == "best")        { c_jet = "ak8";   
      if (wp == "JMAR" && object=="T") { c_algo_wp = "("+c_jet+"_1_best_"+(TString)object+"vsQCD>0.8563)"; } 
      if (wp == "JMAR" && object=="W") { c_algo_wp = "("+c_jet+"_1_best_"+(TString)object+"vsQCD>0.9001)"; }
    }
    if (algos[ialgo] == "imagetop")    { c_jet = "ak8";   if (wp == "JMAR") { c_algo_wp = "("+c_jet+"_1_image_top>0.8021)"; } }
    if (algos[ialgo] == "imagetopmd")  { c_jet = "ak8";   if (wp == "JMAR") { c_algo_wp = "("+c_jet+"_1_image_top>0.7485)"; } }
    if (algos[ialgo] == "deepak8")     { c_jet = "ak8"; 
      if (wp == "JMAR" && object=="T") { c_algo_wp = "("+c_jet+"_1_DeepAK8_"+(TString)object+"vsQCD>0.8537)"; } 
      if (wp == "JMAR" && object=="W") { c_algo_wp = "("+c_jet+"_1_DeepAK8_"+(TString)object+"vsQCD>0.9383)"; }
    }
    if (algos[ialgo] == "deepak8md")   { c_jet = "ak8";
      if (wp == "JMAR" && object=="T") { c_algo_wp = "("+c_jet+"_1_DeepAK8MD_"+(TString)object+"vsQCD>0.4285)"; }
      if (wp == "JMAR" && object=="W") { c_algo_wp = "("+c_jet+"_1_DeepAK8MD_"+(TString)object+"vsQCD>0.6231)"; }
    }

    TString c_mass;
    if (object=="T") { c_mass = "("+c_jet+"_1_mass>105. && "+c_jet+"_1_mass<210.)"; }
    if (object=="W") { c_mass = "("+c_jet+"_1_mass>65. && "+c_jet+"_1_mass<105.)"; }
    //TString c_mass = "("+c_jet+"_1_mass>0.)";

    xmin = xmin - (2.*(getmed)) + (2.*ialgo);
    xmax = xmax - (2.*(getmed)) + (2.*ialgo);
    
    TH1D *h_incl_mc   = create1Dhisto(sample,t_mc,lumi,cut_incl,c_jet+"_1_pt",bins,xmin,xmax,false,1,1,"h_incl_mc",false,false);     h_incl_mc->SetFillColor(0);  
    TH1D *h_num_mc = create1Dhisto(sample,t_mc,lumi,cut_incl+" && "+c_algo_wp+" && "+c_mass,c_jet+"_1_pt",bins,xmin,xmax,false,colors[ialgo],1,"h_num_mc_"+algos[ialgo],false,false); 
    TH1D *h_mc_r   = (TH1D*)h_num_mc->Clone("h_mc_r_"+algos[ialgo]); h_mc_r->Divide(h_num_mc,h_incl_mc,1.,1.,"B");
    
    TH1D *h_incl_data;
    if (sample == "qcd") {
      TH1D *h_incl_mc_b = create1Dhisto(sample,t_mc_b,lumi,cut_incl,c_jet+"_1_pt",bins,xmin,xmax,false,1,1,"h_incl_mc_b",false,false); h_incl_mc_b->SetFillColor(0);  
      TH1D *h_incl_data_0 = create1Dhisto(sample,t_data,lumi,cut_incl,c_jet+"_1_pt",bins,xmin,xmax,false,1,1,"h_incl_data_0",false,true); h_incl_data_0->SetFillColor(0);  
      h_incl_data = (TH1D*)h_incl_data_0->Clone("h_incl_data"); h_incl_data->Add(h_incl_mc_b,-1.);
      h_incl_mc_b->Delete(); h_incl_data_0->Delete();
    }
    else { h_incl_data = create1Dhisto(sample,t_data,lumi,cut_incl,c_jet+"_1_pt",bins,xmin,xmax,false,1,1,"h_incl_data",false,true); h_incl_data->SetFillColor(0); }

    TH1D *h_num_data;
    if (sample == "qcd") {
      TH1D *h_num_mc_b = create1Dhisto(sample,t_mc_b,lumi,cut_incl+" && "+c_algo_wp+" && "+c_mass,c_jet+"_1_pt",bins,xmin,xmax,false,colors[ialgo],1,"h_num_mc_b_"+algos[ialgo],false,false); 
      TH1D *h_num_data_0 = create1Dhisto(sample,t_data,lumi,cut_incl+" && "+c_algo_wp+" && "+c_mass,c_jet+"_1_pt",bins,xmin,xmax,false,colors[ialgo],1,"h_num_data_0_"+algos[ialgo],false,true); 
      h_num_data = (TH1D*)h_num_data_0->Clone("h_num_data"); h_num_data->Add(h_num_mc_b,-1.);
      h_num_mc_b->Delete(); h_num_data_0->Delete();
    }
    else { h_num_data = create1Dhisto(sample,t_data,lumi,cut_incl+" && "+c_algo_wp+" && "+c_mass,c_jet+"_1_pt",bins,xmin,xmax,false,colors[ialgo],1,"h_num_data_"+algos[ialgo],false,true); }
    TH1D *h_data_r = (TH1D*)h_num_data->Clone("h_data_r_"+algos[ialgo]); h_data_r->Divide(h_num_data,h_incl_data,1.,1.,"B");

    TH1D *h_sf = (TH1D*)h_mc_r->Clone("h_sf_"+algos[ialgo]); h_sf->Divide(h_data_r,h_mc_r);
    h_sf->SetLineColor(colors[ialgo]); h_sf->SetMarkerColor(colors[ialgo]); h_sf->SetFillColor(0);
    h_sf->SetMarkerSize(1.);
    //eff_mc.push_back(h_mc_r);
    //eff_data.push_back(h_data_r);
    sf.push_back(h_sf);
    
    h_incl_mc->Delete(); h_incl_data->Delete(); 
  } // end of looping over the algos

  TLegend* leg;
  if (object=="T") { leg = new TLegend(0.75,0.46,0.92,0.89); }
  if (object=="W") { leg = new TLegend(0.75,0.66,0.92,0.89); }
  leg->SetFillStyle(0);
  leg->SetFillColor(0);
  leg->SetLineWidth(0);

  TPaveText *pt_cms = new TPaveText(0.01,0.77,0.4,0.9,"NDC");
  pt_cms->SetFillStyle(0);
  pt_cms->SetFillColor(0);
  pt_cms->SetLineWidth(0);
  pt_cms->AddText("CMS");
  pt_cms->SetTextSize(0.08);

  TPaveText *pt_preliminary = new TPaveText(0.06,0.63,0.4,0.9,"NDC");
  pt_preliminary->SetFillStyle(0);
  pt_preliminary->SetFillColor(0);
  pt_preliminary->SetLineWidth(0);
  pt_preliminary->AddText("Preliminary");
  pt_preliminary->SetTextFont(52);
  pt_preliminary->SetTextSize(0.06);

  TLatex pt_lumi;
  const char *longstring = "35.9 fb^{-1} (13 TeV)";
  pt_lumi.SetTextSize(0.07);
  pt_lumi.SetTextFont(42);

  TCanvas *c_sf = new TCanvas("c_sf","c_sf",700,500);
  gStyle->SetErrorX(0.);
  gPad->SetLeftMargin(0.1);
  gPad->SetBottomMargin(0.13);
  gPad->SetTopMargin(1.02);
  sf[getmed]->GetYaxis()->SetRangeUser(0.5,2.);
  sf[getmed]->GetYaxis()->SetTitleOffset(0.8);
  sf[getmed]->GetYaxis()->SetTitle("#epsilon_{DATA} / #epsilon_{MC}");
  sf[getmed]->GetXaxis()->SetLabelSize(0.06);
  sf[getmed]->GetXaxis()->SetTitle("p_{T} (jet) [GeV]");
  sf[getmed]->Draw("P E0");
  for (unsigned int i0=0; i0<sf.size(); ++i0) { leg->AddEntry(sf[i0],legnames[i0],"PL"); if (i0!=getmed) { sf[i0]->Draw("P E0 sames"); } }
  //  for (unsigned int i0=0; i0<sf.size(); ++i0) {   }
  leg->Draw("sames");
  pt_cms->Draw("sames");
  pt_preliminary->Draw("sames");
  pt_lumi.DrawLatexNDC(0.58,0.93,longstring);

  TCanvas *c_eff_mc = new TCanvas("c_eff_mc","c_eff_mc",700,500);
  for (unsigned int i0=0; i0<eff_mc.size(); ++i0) { 
    if (i0==0) { eff_mc[i0]->Draw("P E0"); } 
    else       { eff_mc[i0]->Draw("P E0 sames"); }
  }

  TCanvas *c_eff_data = new TCanvas("c_eff_data","c_eff_data",700,500);
  for (unsigned int i0=0; i0<eff_data.size(); ++i0) { 
    if (i0==0) { eff_data[i0]->Draw("P E0"); } 
    else       { eff_data[i0]->Draw("P E0 sames"); }
  }
}


double median(std::vector<TString> vecb) {

  std::vector<int> vec;
  int counter = 0;
  for (unsigned int i0=0; i0<vecb.size(); ++i0) { vec.push_back(counter); ++counter; }
  typedef vector<int>::size_type vec_sz;

  vec_sz size = vec.size();
  if (size == 0) { throw domain_error("median of an empty vector"); }
  sort(vec.begin(), vec.end());
  vec_sz mid = size/2;
  return size % 2 == 0 ? (vec[mid] + vec[mid-1]) / 2 : vec[mid];
}

TH1D *create1Dhisto(TString sample,TTree *tree,TString intLumi,TString cuts,TString branch,int bins,float xmin,float xmax, bool useLog,int color, int style,TString name,bool norm,bool data) {
  TH1::SetDefaultSumw2(kTRUE);

  TString cut;
  if (data) { cut ="("+cuts+")"; }
  else {
    if      (name.Contains("puUp"))   { cut ="(xsecWeight*puWeightUp*genWeight*"+intLumi+")*("+cuts+")"; }
    else if (name.Contains("puDown")) { cut ="(xsecWeight*puWeightDown*genWeight*"+intLumi+")*("+cuts+")"; }
    //else if (name.Contains("herw"))   { cut ="(xsecWeight*puWeight*"+intLumi+")*("+cuts+")"; }
    //else                              { cut ="(xsecWeight*puWeight*genWeight*"+intLumi+")*("+cuts+")"; }
    else                              { cut ="(puWeight*genWeight*"+intLumi+")*("+cuts+")"; }
  }


  TH1D *hTemp = new TH1D(name,name,bins,xmin,xmax);
  tree->Project(name,branch,cut);

  hTemp->SetLineWidth(3);
  hTemp->SetMarkerSize(0);
  hTemp->SetLineColor(color);
  hTemp->SetFillColor(color);
  hTemp->SetLineStyle(style);

  // ad overflow bin
  double error =0.; double integral = hTemp->IntegralAndError(bins,bins+1,error);
  //hTemp->SetBinContent(bins,integral);
  //hTemp->SetBinError(bins,error);

  if (norm) { hTemp->Scale(1./(hTemp->Integral())); }

  return hTemp;
} 

void getMisTagList() {

  float eff = 0.01;
  /*getdiscvalmistag(eff,"sdtau32"     ,"(1-(ak8_1_tau3/ak8_1_tau2))","ak8","T","0==0");
  getdiscvalmistag(eff,"sdtau32btag" ,"(1-(ak8_1_tau3/ak8_1_tau2))","ak8","T","max(ak8_1_sj1_btagCSVV2,ak8_1_sj2_btagCSVV2)>0.5426");
  getdiscvalmistag(eff,"ecftoptag"   ,"(0.5+0.5*ca15_1_ecfTopTagBDT)","ca15","T","0==0");*/
  //  getdiscvalmistag(eff,"hotvr","","ak8","T","0==0");
  /*getdiscvalmistag(eff,"sdtau21"     ,"(1-(ak8_1_tau2/ak8_1_tau1))","ak8","W","0==0");
  getdiscvalmistag(eff,"sdn2"        ,"(1-ak8_1_n2b1)","ak8","W","0==0");
  getdiscvalmistag(eff,"sdn2ddt"     ,"(0.5-0.5*ak8_1_n2b1ddt)","ak8","W","0==0");
  getdiscvalmistag(eff,"best"        ,"(ak8_1_best_TvsQCD)","ak8","T","0==0");*/
  getdiscvalmistag(eff,"best"        ,"ak8_1_best_WvsQCD","ak8","W","0==0");
  /*getdiscvalmistag(eff,"imagetop"    ,"ak8_1_image_top","ak8","T","0==0");
  getdiscvalmistag(eff,"imagetopmd"  ,"ak8_1_image_top_md","ak8","T","0==0");*/
  //getdiscvalmistag(eff,"deepak8"     ,"ak8_1_DeepAK8_TvsQCD","ak8","T","0==0");
  getdiscvalmistag(eff,"deepak8"     ,"ak8_1_DeepAK8_WvsQCD","ak8","W","0==0");
  //getdiscvalmistag(eff,"deepak8md"   ,"ak8_1_DeepAK8MD_TvsQCD","ak8","T","0==0");
  getdiscvalmistag(eff,"deepak8md"   ,"ak8_1_DeepAK8MD_WvsQCD","ak8","W","0==0");
}

void getdiscvalmistag(float eff, TString algo, TString algosvar, TString jettype, TString object, TString cut) {
  TH1::SetDefaultSumw2(kTRUE);
  //  TFile *f_ = TFile::Open("/eos/uscms/store/group/lpcjme/noreplica/NanoHRT/Trees/Apr08/drplots/zprime_tt.root" , "READONLY" ); 
  TFile *f_ = TFile::Open("/eos/uscms/store/group/lpcjme/noreplica/NanoHRT/Trees/Apr08/qcd/mc_nom/qcd-mg_tree.root" , "READONLY" );
  TTree *t_ = (TTree*)f_->Get("Events");

  // selection
  TString c_r; if (jettype=="ak8") { c_r = "0.6"; } if (jettype=="ca15") { c_r = "1.2"; }
  TString c_match = "("+jettype+"_1_pt>500)";
  TString c_mass; 
  if (object=="T") { c_mass = "("+jettype+"_1_mass>105. && "+jettype+"_1_mass<210.)"; }
  if (object=="W") { c_mass = "("+jettype+"_1_mass>65. && "+jettype+"_1_mass<105.)"; }
  //  if (object=="T") { c_match = "("+jettype+"_1_dr_fj_top_wqmax<"+c_r+") && ("+jettype+"_1_dr_fj_top_b<"+c_r+")"; }

  // get efficiencies
  TString cut_init = "(xsecWeight*puWeight)*("+c_match+")";
  TString cut_final = "(xsecWeight*puWeight)*("+c_match+" && "+cut+" && "+c_mass+")";
  int nbins = 100000; int start = 1; int end = nbins+1;
  TH1F *h_init = new TH1F("h_"+algo+"_init","h_"+algo+"_init",nbins,-10.,10.);
  t_->Project("h_"+algo+"_init",algosvar,cut_init);
  TH1F *h_ = new TH1F("h_"+algo,"h_"+algo,nbins,-10.,10.);
  t_->Project("h_"+algo,algosvar,cut_final);

  float discval_; 
  float ntot = h_init->Integral(0,nbins+1);
  for (unsigned int i0=start; i0<end; ++i0) {
    float tmp_eff = h_->Integral(i0,nbins+1);
    if ( (tmp_eff/ntot)<eff && (tmp_eff/ntot)>0. ) { discval_ = h_->GetBinCenter(i0); break;  }
  } 

  std::cout << algo <<  " " <<  discval_ << "\n";
}

