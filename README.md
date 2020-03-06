# HRTSF

Code to calculate SF using templates and combine [PRELIMINARY -- work in progress]
// original by Loukas Gouskos

# I. setup

-> setup combine from here:
https://github.com/nucleosynthesis/HiggsAnalysis-CombinedLimit/wiki/gettingstarted#for-end-users-that-dont-need-to-commit-or-do-any-development

-> get the SF code:
```
git clone ssh://git@gitlab.cern.ch:7999/gouskos/hrtsf.git
```
-> run:
```
cd hrtsf
mv TagAndProbeExtended.py $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/python/
scram b -j4
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

