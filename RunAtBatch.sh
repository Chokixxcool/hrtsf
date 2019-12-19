#!/bin/bash

cd /afs/cern.ch/user/s/ssyedoma/work/JMARWTag/TempFit/CMSSW_10_2_13/src/
eval `scramv1 runtime -sh`
cd /afs/cern.ch/user/ss/syedoma/work/JMARWTag/TempFit/CMSSW_10_2_13/src/hrtsf/

OBJECT=${1}
YEAR=${2}
WORKDIR=${3}
PTBIN=${4}
ALGO=${5}
MISTRATES=${6}

./calcTopWSF_Fikri.sh ${OBJECT} ${YEAR} ${WORKDIR} ${PTBIN} ${ALGO} ${MISTRATES}

echo "calcTopWSF::Done"
