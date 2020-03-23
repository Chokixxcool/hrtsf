import glob, sys, os

objects=sys.argv[1]
years=sys.argv[2]
workdir0=sys.argv[3]
ptranges=sys.argv[4]
algos=sys.argv[5]
mist_rates=sys.argv[6]
syst="tot"

def main():
  for obj in objects:
  	for year in years:
      [WPs_mist_rate_0p1, WPs_mist_rate_0p5, WPs_mist_rate_1p0, WPs_mist_rate_5p0] = defmistrate(obj, year) 
  		
    	# loop over algos
    	for mistRate in mist_rates:
    		WPs_mist_rate=mistRateElem(mistRate)
        WP_binarized=WPs_mist_rate[0]
        WP_binarizedMD=WPs_mist_rate[1]
        WP_raw=WPs_mist_rate[2]
        WP_rawMD=WPs_mist_rate[3]

    		# loop over algos #
    		for algo in algos:
    			workdir=workdir0+"/"+obj+"_"+algo+"_"+syst+"_mist_rate_"+mistRate
    			eosdir="/eos/user/s/ssyedoma/JMARWTag/TempFit/"+workdir
    			if not os.path.exists(workdir): os.mkdir(workdir)
          if not os.path.exists(eosdir): os.mkdir(eosdir)

    			# loop over WPs #
    			for wp in ["JMAR"]:
    				for ptrange in ptranges:
    					# make templates #
    					print " :: make templates . . ."
    					cmdpass="makeSFTemplates({},{},{},{},{},{},{},{},{},{},{},{},{})".format(obj,algo,wp,ptrange,syst,True,mistRate,WP_binarized,WP_binarizedMD,WP_raw,WP_rawMD,year,workdir0)
    					cmdfail="makeSFTemplates({},{},{},{},{},{},{},{},{},{},{},{},{})".format(obj,algo,wp,ptrange,syst,False,mistRate,WP_binarized,WP_binarizedMD,WP_raw,WP_rawMD,year,workdir0)
    					print "*********** pass ***********"
              os.system("root -l -b -q %s"%cmdpass)
              print "*********** fail ***********"
              os.system("root -l -b -q %s"%cmdfail)

              # make datacard #
          		os.system("cd %s"%workdir)
          		inputname=obj+"_"+algo+"_"+wp+"_"+ptrange
          		print " :: make datacard . . ."
          		os.system("cp ../../makeSFDatacard.py .")

          		cmdmakedatacard="makeSFDatacard.C({},{})".format(inputname,year)
          		os.system("root -l -b -q {} > sf_datacard_{}.txt".format(cmdmakedatacard,inputname))
          		os.system("sed -n -i '3,$ p' sf_datacard_{}.txt".format(inputname))

          		# do tag and probe #
          		print " :: run tag and probe . . . "
          		if obj=="T": os.system("text2workspace.py -m 125 -P HiggsAnalysis.CombinedLimit.TagAndProbeExtended:tagAndProbe sf.txt --PO categories=catp3,catp2,catp1")
          		elif obj=="W": os.system("text2workspace.py -m 125 -P HiggsAnalysis.CombinedLimit.TagAndProbeExtended:tagAndProbe sf_datacard_{}.txt --PO categories=catp2,catp3,catp1".format(inputname))

          		os.system("mv sf_datacard_{}.root sf_{}.root".format(inputname,inputname))

          		print "Do MultiDimFit"
          		os.system("combine -M MultiDimFit -m 125 sf_{}.root --algo=singles --robustFit 1 --cminDefaultMinimizerTolerance 5.".format(inputname))

          		print "Run FitDiagnostics"
          		os.system("combine -M FitDiagnostics -n _{} -m 125 sf_{}.root --saveShapes --saveWithUncertainties --robustFit 1 --cminDefaultMinimizerTolerance 5.".format(inputname,inputname))

          		os.system("mv fitDiagnostics_{}.root sf_fitDiagnostics_{}.root".format(inputname,inputname))
          		os.system("combineTool.py -M Impacts -d sf_{}.root -m 125 --doInitialFit --robustFit 1".format(inputname))
              os.system("combineTool.py -M Impacts -d sf_{}.root -m 125 --robustFit 1 --doFits --parallel 60".format(inputname))
              os.system("combineTool.py -M Impacts -d sf_{}.root -m 125 -o impacts_{}.json --robustFit 1 ".format(inputname,inputname))
              os.system("plotImpacts.py -i impacts_{}.json -o impacts_{}".format(inputname,inputname))

              os.system("cp impacts_{}.pdf {}".format(inputname,eosdir))
              os.system("rm higgsCombine_paramFit_*")

              # make plots #
              os.cd("../../")
              cmdmake="makePlots.C({},{},{},{},{},{},{},{},{},{})".format(workdir,inputname,wp,ptrange,'50.','250.','20',"mass",obj,wp)
              os.system("root -l -q {})".format(cmdmake))
              print "copying plots_datamc to EOS"
              os.mkdir("{}/plots_datamc".format(eosdir))
              os.system("cp -r {}/plots_datamc {}".format(workdir,eosdir))

def defmistrate(obj,year):
  # Top-Tagging #
  if obj=="T":
    if year==2016:
      WPs_mist_rate_0p1=[0.989966, 0.864515, 0.8927, 0.466789] #, 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top
      WPs_mist_rate_0p5=[0.937122, 0.621402, 0.688459, 0.219164] #, 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top
      WPs_mist_rate_1p0=[0.852861, 0.436951, 0.534739, 0.13735] #, 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top
      WPs_mist_rate_5p0=[0.245148, 0.0669528, 0.107193, 0.0274599] #, 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top
    elif year==2017:
      WPs_mist_rate_0p1=[0.985738, 0.842546, 0.817421, 0.315268]     #, 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top
      WPs_mist_rate_0p5=[0.894945, 0.57765, 0.497896, 0.12387]       #, 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top
      WPs_mist_rate_1p0=[0.74501, 0.391455, 0.310047, 0.0737485]     #, 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top
      WPs_mist_rate_5p0=[0.0931942, 0.0542414, 0.0275957, 0.0138089] #, 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top    
    elif year==2018:
      WPs_mist_rate_0p1=[0.986217, 0.844952, 0.831612, 0.333162]   #, 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top
      WPs_mist_rate_0p5=[0.898277, 0.559342, 0.523792, 0.126772]  #, 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top
      WPs_mist_rate_1p0=[0.75146, 0.36306, 0.334927, 0.0732553]    #, 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top
      WPs_mist_rate_5p0=[0.102426, 0.045428, 0.0342551, 0.0130718] #, 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top

  # W-Tagging #
  if obj=="W":
    if year==2016:
      WPs_mist_rate_0p1=[0.993694, 0.910292, 0.854871, 0.620627] #, 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W
      WPs_mist_rate_0p5=[0.972569, 0.759349, 0.76604, 0.471379]  #, 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W
      WPs_mist_rate_1p0=[0.941254, 0.631961, 0.688198, 0.383825] #, 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W
      WPs_mist_rate_5p0=[0.526229, 0.183695, 0.255735, 0.129108] #, 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W
    elif year==2017:
      WPs_mist_rate_0p1=[0.998032, 0.960866, 0.908412, 0.733628] #, 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W
      WPs_mist_rate_0p5=[0.991407, 0.884424, 0.851776, 0.616956] #, 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W
      WPs_mist_rate_1p0=[0.981299, 0.802331, 0.801854, 0.5366]   #, 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W
      WPs_mist_rate_5p0=[0.778869, 0.313254, 0.436723, 0.220494] #, 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W
    elif year==2018:
      WPs_mist_rate_0p1=[0.997201, 0.952358, 0.894613, 0.71532]  #, 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W
      WPs_mist_rate_0p5=[0.987834, 0.859153, 0.829094, 0.591239] #, 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W
      WPs_mist_rate_1p0=[0.973452, 0.766602, 0.772662, 0.507302] #, 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W
      WPs_mist_rate_5p0=[0.706981, 0.274176, 0.378693, 0.197519] #, 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W

  return WPs_mist_rate_0p1, WPs_mist_rate_0p5, WPs_mist_rate_1p0, WPs_mist_rate_5p0

def mistRateElem(mistRate):
  WPs_mist_rate=[]
  if mistRate=="0p1":
    for element in WPs_mist_rate_0p1:
      WPs_mist_rate+=element
      
  elif mistRate=="0p5":
    for element in WPs_mist_rate_0p5:
      WPs_mist_rate+=element

  elif mistRate=="1p0":
    for element in WPs_mist_rate_1p0:
      WPs_mist_rate+=element

  elif mistRate=="5p0":
    for element in WPs_mist_rate_5p0:
      WPs_mist_rate+=element

  return WPs_mist_rate

def makeSFDatacard(inputname, year):
  fpass=ROOT.TFile.Open(inputname+"_pass.root","READONLY")
  ffail=ROOT.TFile.Open(inputname+"_fail.root","READONLY")
  h_obs_pass=fpass.Get("data_obs")
  h_obs_fail=ffail.Get("data_obs")
  h_catp3_pass = fpass.Get("catp3")
  h_catp3_fail = ffail.Get("catp3")
  h_catp2_pass = fpass.Get("catp2")
  h_catp2_fail = ffail.Get("catp2")
  h_catp1_pass = fpass.Get("catp1")
  h_catp1_fail = ffail.Get("catp1")
  
  dc=open(DCDIR+dcname, "w+")

  dc.write( "imax 2  number of channels\n")
  dc.write( "jmax 2  number of backgrounds\n")
  dc.write( "kmax *  number of nuisance parameters (sources of systematical uncertainties)\n")
  dc.write( "------------\n")
  dc.write( "shapes  *  pass   " << inputname << "_pass.root  $PROCESS $PROCESS_$SYSTEMATIC\n")
  dc.write( "shapes  *  fail   " << inputname << "_fail.root  $PROCESS $PROCESS_$SYSTEMATIC\n")
  dc.write( "------------\n")
  dc.write( "# we have just one channel, in which we observe 0 events\n")
  dc.write( "bin             pass    fail\n")
  dc.write( "observation      " << h_obs_pass->Integral(1,h_obs_pass->GetNbinsX()) << "  " <<  h_obs_fail->Integral(1,h_obs_fail->GetNbinsX())  << "\n")
  dc.write( "------------\n")
  dc.write( "# now we list the expected events for signal and all backgrounds in that bin\n")
  dc.write( "# the second 'process' line must have a positive number for backgrounds, and 0 for signal\n")
  dc.write( "# then we list the independent sources of uncertainties, and give their effect (syst. error)\n")
  dc.write( "# on each process and bin\n")
  dc.write( "bin             pass    pass   pass       fail   fail   fail\n")
  dc.write( "process         catp2   catp3   catp1    catp2   catp3   catp1\n"  )
  dc.write( "process            -1     -2      3       -1     -2       3\n")
  dc.write( "rate            " 
      << h_catp2_pass->Integral(1,h_catp2_pass->GetNbinsX()) << " " << h_catp3_pass->Integral(1,h_catp3_pass->GetNbinsX()) << " " << h_catp1_pass->Integral(1,h_catp1_pass->GetNbinsX()) << " "
      << h_catp2_fail->Integral(1,h_catp2_fail->GetNbinsX()) << " " << h_catp3_fail->Integral(1,h_catp3_fail->GetNbinsX()) << " " << h_catp1_fail->Integral(1,h_catp1_fail->GetNbinsX()) << "\n"
  )
  dc.write( "------------\n")
  dc.write( "lumi    lnN     1.025  1.025  1.025  1.025  1.025  1.025\n")
  dc.write( "pu      shape     1      1      1      1      1      1  \n")
  dc.write( "jer     shape     1      1      1      1      1      1  \n")
  dc.write( "jes     shape     1      1      1      1      1      1  \n")
  dc.write( "met     shape     1      1      1      1      1      1  \n")
  dc.close()

if __name__ == '__main__':
  main()