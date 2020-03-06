import ROOT, os, glob

INDIR="/eos/user/s/ssyedoma/JMARWTag/TempFit/plots/"
years=["2018"]
wp=["0p1","0p5","1p0","5p0"]
taggers=["sdtau21","deepak8"]

def main():
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
 	main()