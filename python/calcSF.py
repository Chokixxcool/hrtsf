import glob, sys, os
from makeSFTemplates import *

objects     =[sys.argv[1]]
years       =[sys.argv[2]]
workdir0    =[sys.argv[3]]
ptranges    =[sys.argv[4]]
algos       =[sys.argv[5]]
mist_rates  =[sys.argv[6]]
syst="tot"


EOSUSER="root://eosuser.cern.ch/"
USER="s/ssyedoma"
TEMPDIR="/eos/user/"+USER+"/JMARWTag/TempFit/SFtemplates"
DCDIR="/eos/user/"+USER+"/JMARWTag/TempFit/SFdatacards"
FDDIR="/eos/user/"+USER+"/JMARWTag/TempFit/SFfitdiags"
PLTDIR="/eos/user/"+USER+"/JMARWTag/TempFit/plots"

DIRLIST=[TEMPDIR, DCDIR, FDDIR, PLTDIR]
for d in DIRLIST:
  if not os.path.exists(d):
    os.makedirs(d)

def main():
  timerMain = ROOT.TStopwatch()
  timerMain.Start()
  for year in years:
    for obj in objects:
      [WPs_mist_rate_0p1, WPs_mist_rate_0p5, WPs_mist_rate_1p0, WPs_mist_rate_5p0] = defmistrate(obj, year) 
      mistRateElem={"0p1":WPs_mist_rate_0p1, "0p5":WPs_mist_rate_0p5, "1p0":WPs_mist_rate_1p0, "5p0":WPs_mist_rate_5p0}      
      for mistRate in mist_rates:
        [WP_binarized, WP_binarizedMD, WP_raw, WP_rawMD] = mistRateElem[mistRate]
        for algo in algos:
          if algo=="sdtau21" and not mistRate=="0p1": continue
          for wp in ["JMAR"]:
            for ptrange in ptranges:
              ### make templates #############################################
              # makeSFTemp()
              
              mistRateN={"sdtau21":"","deepak8":"_"+mistRate}
              inputname = year+"_"+obj+"_"+algo+"_"+wp+"_"+ptrange+mistRateN[algo]
              ### make datacards #############################################
              makeSFDatacard(inputname,year)

              ### do tag and probe #############################################
              print " :: run tag and probe for %s" %inputname
              if obj=="W": os.system("text2workspace.py -m 125 -P HiggsAnalysis.CombinedLimit.TagAndProbeExtended:tagAndProbe {}/sf_datacard_{}.txt --PO categories=catp2,catp3,catp1".format(DCDIR,inputname))

              # print "Do MultiDimFit"
              # os.system("combine -M MultiDimFit -n _{} -m 125 {}/sf_datacard_{}.root --algo=singles --robustFit 1 --cminDefaultMinimizerTolerance 5.".format(inputname,DCDIR,inputname))

              print "Run FitDiagnostics"
              os.system("combine -M FitDiagnostics -n _{} -m 125 {}/sf_datacard_{}.root --saveShapes --saveWithUncertainties --robustFit 1 --cminDefaultMinimizerTolerance 5.".format(inputname,DCDIR,inputname))
              os.system("mv fitDiagnostics_{}.root {}/".format(inputname,FDDIR))
              os.system("mv higgsCombine_{}.FitDiagnostics.mH125.root {}/".format(inputname,FDDIR))

              # os.system("combineTool.py -M Impacts -d {}/sf_datacard_{}.root -m 125 --doInitialFit --robustFit 1".format(DCDIR,inputname))
              # os.system("combineTool.py -M Impacts -d {}/sf_datacard_{}.root -m 125 --robustFit 1 --doFits --parallel 60".format(DCDIR,inputname))
              # os.system("combineTool.py -M Impacts -d {}/sf_datacard_{}.root -m 125 -o impacts_{}.json --robustFit 1 ".format(DCDIR,inputname,inputname))
              
              # os.system("plotImpacts.py -i impacts_{}.json -o impacts_{}".format(inputname,inputname))

              # os.system("cp impacts_{}.pdf {}".format(inputname,eosdir))
              # os.system("rm higgsCombine_paramFit_*")

              ### make plots #############################################
              
            #   os.cd("../../")
            #   cmdmake="makePlots.C({},{},{},{},{},{},{},{},{},{})".format(workdir,inputname,wp,ptrange,'50.','250.','20',"mass",obj,wp)
            #   os.system("root -l -q {})".format(cmdmake))
            #   print "copying plots_datamc to EOS"
            #   os.mkdir("{}/plots_datamc".format(eosdir))
            #   os.system("cp -r {}/plots_datamc {}".format(workdir,eosdir))
  timerMain.Print()

def makeSFTemp():
  print " :: make templates . . ."
  print "*********** pass ***********"
  makeSFTemplates(obj,algo,wp,ptrange,syst,True,mistRate,WP_binarized,WP_binarizedMD,WP_raw,WP_rawMD,year,TEMPDIR)
  print "*********** fail ***********"
  makeSFTemplates(obj,algo,wp,ptrange,syst,False,mistRate,WP_binarized,WP_binarizedMD,WP_raw,WP_rawMD,year,TEMPDIR)

def defmistrate(obj,year):
  # Top-Tagging #
  if obj=="T":
    if year=="2016":
      WPs_mist_rate_0p1=[0.989966, 0.864515, 0.8927, 0.466789] #, 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top
      WPs_mist_rate_0p5=[0.937122, 0.621402, 0.688459, 0.219164] #, 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top
      WPs_mist_rate_1p0=[0.852861, 0.436951, 0.534739, 0.13735] #, 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top
      WPs_mist_rate_5p0=[0.245148, 0.0669528, 0.107193, 0.0274599] #, 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top
    elif year=="2017":
      WPs_mist_rate_0p1=[0.985738, 0.842546, 0.817421, 0.315268]     #, 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top
      WPs_mist_rate_0p5=[0.894945, 0.57765, 0.497896, 0.12387]       #, 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top
      WPs_mist_rate_1p0=[0.74501, 0.391455, 0.310047, 0.0737485]     #, 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top
      WPs_mist_rate_5p0=[0.0931942, 0.0542414, 0.0275957, 0.0138089] #, 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top    
    elif year=="2018":
      WPs_mist_rate_0p1=[0.986217, 0.844952, 0.831612, 0.333162]   #, 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top
      WPs_mist_rate_0p5=[0.898277, 0.559342, 0.523792, 0.126772]  #, 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top
      WPs_mist_rate_1p0=[0.75146, 0.36306, 0.334927, 0.0732553]    #, 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top
      WPs_mist_rate_5p0=[0.102426, 0.045428, 0.0342551, 0.0130718] #, 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top

  # W-Tagging #
  if obj=="W":
    if year=="2016":
      WPs_mist_rate_0p1=[0.993694, 0.910292, 0.854871, 0.620627] #, 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W
      WPs_mist_rate_0p5=[0.972569, 0.759349, 0.76604, 0.471379]  #, 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W
      WPs_mist_rate_1p0=[0.941254, 0.631961, 0.688198, 0.383825] #, 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W
      WPs_mist_rate_5p0=[0.526229, 0.183695, 0.255735, 0.129108] #, 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W
    elif year=="2017":
      WPs_mist_rate_0p1=[0.998032, 0.960866, 0.908412, 0.733628] #, 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W
      WPs_mist_rate_0p5=[0.991407, 0.884424, 0.851776, 0.616956] #, 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W
      WPs_mist_rate_1p0=[0.981299, 0.802331, 0.801854, 0.5366]   #, 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W
      WPs_mist_rate_5p0=[0.778869, 0.313254, 0.436723, 0.220494] #, 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W
    elif year=="2018":
      WPs_mist_rate_0p1=[0.997201, 0.952358, 0.894613, 0.71532]  #, 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W
      WPs_mist_rate_0p5=[0.987834, 0.859153, 0.829094, 0.591239] #, 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W
      WPs_mist_rate_1p0=[0.973452, 0.766602, 0.772662, 0.507302] #, 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W
      WPs_mist_rate_5p0=[0.706981, 0.274176, 0.378693, 0.197519] #, 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W
  
  return WPs_mist_rate_0p1, WPs_mist_rate_0p5, WPs_mist_rate_1p0, WPs_mist_rate_5p0

def makeSFDatacard(inputname, year):
  print " :: make datacard for %s" %inputname
  fpass=ROOT.TFile.Open(TEMPDIR+"/"+inputname+"_pass.root","READONLY")
  ffail=ROOT.TFile.Open(TEMPDIR+"/"+inputname+"_fail.root","READONLY")
  h_obs_pass=fpass.Get("data_obs")
  h_obs_fail=ffail.Get("data_obs")
  h_catp3_pass = fpass.Get("catp3")
  h_catp3_fail = ffail.Get("catp3")
  h_catp2_pass = fpass.Get("catp2")
  h_catp2_fail = ffail.Get("catp2")
  h_catp1_pass = fpass.Get("catp1")
  h_catp1_fail = ffail.Get("catp1")
  
  dcname="sf_datacard_"+inputname+".txt"
  dc=open(DCDIR+"/"+dcname, "w+")

  dc.write( "imax 2  number of channels\n")
  dc.write( "jmax *  number of backgrounds\n")
  dc.write( "kmax *  number of nuisance parameters (sources of systematical uncertainties)\n")
  dc.write( "------------\n")
  dc.write( "shapes  *  pass   " + TEMPDIR+"/"+inputname + "_pass.root  $PROCESS $PROCESS_$SYSTEMATIC\n")
  dc.write( "shapes  *  fail   " + TEMPDIR+"/"+inputname + "_fail.root  $PROCESS $PROCESS_$SYSTEMATIC\n")
  dc.write( "------------\n")
  dc.write( "# we have just one channel, in which we observe 0 events\n")
  dc.write( "bin             pass    fail\n")
  dc.write( "observation      " + str(h_obs_pass.Integral(1,h_obs_pass.GetNbinsX())) + "  " +  str(h_obs_fail.Integral(1,h_obs_fail.GetNbinsX()))  + "\n")
  dc.write( "------------\n")
  dc.write( "# now we list the expected events for signal and all backgrounds in that bin\n")
  dc.write( "# the second 'process' line must have a positive number for backgrounds, and 0 for signal\n")
  dc.write( "# then we list the independent sources of uncertainties, and give their effect (syst. error)\n")
  dc.write( "# on each process and bin\n")
  dc.write( "bin             pass    pass   pass       fail   fail   fail\n")
  dc.write( "process         catp2   catp3   catp1    catp2   catp3   catp1\n"  )
  dc.write( "process            -1     -2      3       -1     -2       3\n")
  dc.write( "rate            " 
      + str(h_catp2_pass.Integral(1,h_catp2_pass.GetNbinsX())) + " " + str(h_catp3_pass.Integral(1,h_catp3_pass.GetNbinsX())) + " " + str(h_catp1_pass.Integral(1,h_catp1_pass.GetNbinsX())) + " "
      + str(h_catp2_fail.Integral(1,h_catp2_fail.GetNbinsX())) + " " + str(h_catp3_fail.Integral(1,h_catp3_fail.GetNbinsX())) + " " + str(h_catp1_fail.Integral(1,h_catp1_fail.GetNbinsX())) + "\n"
  )
  dc.write( "------------\n")
  dc.write( "lumi    lnN     1.025  1.025  1.025  1.025  1.025  1.025\n")
  dc.write( "pu      shape     1      1      1      1      1      1  \n")
  dc.write( "jer     shape     1      1      1      1      1      1  \n")
  dc.write( "jes     shape     1      1      1      1      1      1  \n")
  dc.write( "met     shape     1      1      1      1      1      1  \n")
  if (year=="2016"): dc.write( "herwig      shape     1      1      1      1      1      1  \n")
  dc.write( "lhescalemuf shape     1      1      1      1      1      1  \n")
  dc.write( "lhescalemur shape     1      1      1      1      1      1  \n")
  dc.write( "lhepdf      shape     1      1      1      1      1      1  \n")
  dc.write( "*  autoMCStats  0 \n")
  dc.close()

if __name__ == '__main__':
  main()