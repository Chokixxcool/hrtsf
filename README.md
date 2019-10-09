# HRTSF

Code to calculate SF using templates and combine [PRELIMINARY -- work in progress]


(I) setup

-> setup combine from here:
https://github.com/nucleosynthesis/HiggsAnalysis-CombinedLimit/wiki/gettingstarted#for-end-users-that-dont-need-to-commit-or-do-any-development

-> get the SF code:
git clone ssh://git@gitlab.cern.ch:7999/gouskos/hrtsf.git

-> run:
cd hrtsf
mv TagAndProbeExtended.py $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/python/
scram b -j4


(II) brief instructions

-> run the SF code:
./calcTopWSF.sh "object" "year" "folder_name"
where object [for now] is "T" or "W" year= 2016, 2017, 2018 folder_name=directory you want to store the files. A few things are currently hardcoded, tailored to the Heavy Reasonance Tagging paper needs. We are working on improving the fuctionality. 

The templates and the datacards are produced with makeSFTemplates.C and makeSFDatacard.C scripts. Simple examples for now.

Pre/Post fit plots are produced while running this step. The actual code is in makePlots.C. 

-> In makePlots.C one can find more useful functions: (a) read the scale factors from the root files produced by combine, (b) calculate working points, etc..

