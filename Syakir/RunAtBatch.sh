#!/bin/bash
cd /afs/cern.ch/user/s/ssyedoma/work/JMARWTag/TempFit/CMSSW_10_2_13/src/
source /afs/cern.ch/user/s/ssyedoma/root6.18.sh
eval `scramv1 runtime -sh`
cd /afs/cern.ch/user/s/ssyedoma/work/JMARWTag/TempFit/CMSSW_10_2_13/src/hrtsf/Syakir/

OBJECT=${1}
YEAR=${2}
WORKDIR=${3}
PTBIN=${4}
ALGO=${5}
MISTRATES=${6}

./calcSF.sh ${OBJECT} ${YEAR} ${WORKDIR} ${PTBIN} ${ALGO} ${MISTRATES}

echo "calcTopWSF::Done"
