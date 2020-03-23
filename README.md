# HRTSF

Code to calculate SF using templates and combine [PRELIMINARY -- work in progress]
// original by Loukas Gouskos

# I. setup
```
mkdir WTag
cd WTag
```
-> setup combine from here:
```
cmsrel CMSSW_10_2_13
cd CMSSW_10_2_13/src
cmsenv
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit
git fetch origin
git checkout v8.0.1
scramv1 b clean; scramv1 b -j8 # always make a clean build
cd ../../
git clone https://github.com/cms-analysis/CombineHarvester.git CombineHarvester
scram b -j8
```
-> get the SF code:
```
git clone git@github.com:Chokixxcool/hrtsf.git
```
-> run:
```
cd hrtsf
cp TagAndProbeExtended.py $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/python/
scram b -j8
```

# II. brief instructions

-> run the SF code:
```
./calcSF.sh {object} {year} {workdir0} {ptranges} {algos} {mist_rates}
```
where
 object :: {T, W} 
 year :: {2016, 2017, 2018}
 workdir0 :: working folder name: {hrtsf_2016, hrtsf_2017, hrtsf_2018} 
 ptranges :: W: {incl, low, lowmed, med}, T: {incl, low, lowmed, med, medhi}
 algos :: W: {deepak8, sdtau21}, T: {deepak8, sdtau32}
 mist_rates :: {0p1, 0p5, 1p0, 5p0}
 
A few things are currently hardcoded, tailored to the Heavy Reasonance Tagging paper needs. We are working on improving the fuctionality. 

The templates and the datacards are produced with makeSFTemplates.C and makeSFDatacard.C scripts.

Pre/Post fit plots are produced while running this step. The actual code is in makePlots.C. 

In makePlots.C one can find more useful functions: (a) read the scale factors from the root files produced by combine, (b) calculate working points, etc..

