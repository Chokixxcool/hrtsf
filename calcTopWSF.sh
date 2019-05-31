#!/bin/bash
## arguments object = "T" or "W"
object=$1
syst="tot"

declare -a algos
declare -a ptranges

if [ ${object} == "T" ];
then
    #algos=("sdtau32" "sdtau32btag" "ecftoptag" "hotvr" "best" "imagetop" "imagetopmd" "deepak8" "deepak8md")
    #ptranges=("low" "lowmed" "med" "medhi")
    algos=("hotvr")
    ptranges=("med")
elif [ ${object} == "W" ];
then
    #algos=("sdtau21" "sdn2" "sdn2ddt" "best" "deepak8" "deepak8md")
    #ptranges=("low" "lowmed" "med")
    algos=("sdn2")
    ptranges=("low")
fi

## loop over the algos
for algo in "${algos[@]}";
do

    workdir=${object}"_"${algo}"_"${syst}
    mkdir ${workdir}

    ## loop over the working points
    for wp in "JMAR"
    do

        ## loop over the pt bins
	for ptrange in "${ptranges[@]}";
	do

            ## get nominal sf
	    #echo "get nominal sf"
	    #getsf=$(echo 'getsf.C("'${object}'","'${ptrange}'","'${wp}'","'${algo}'")')
	    #readsf=$(root -l -q ${getsf})
	    #root -l -q ${getsf} 
	    #readsf=( $(<readsf.txt) )
	    #echo "print sf"
	    #echo ${readsf}
	    		
	    ##make templates
	    echo "make templates"
	    cmdpass=$(echo 'makeSFTemplates.C("'${object}'","'${algo}'","'${wp}'","'${ptrange}'","'${syst}'",true)')
	    cmdfail=$(echo 'makeSFTemplates.C("'${object}'","'${algo}'","'${wp}'","'${ptrange}'","'${syst}'",false)')
	    root -l -q ${cmdpass}
	    root -l -q ${cmdfail}
 
            ## make datacard
	    echo "make datacard"
	    echo " "
	    cd ${workdir}
	    inputname=${object}"_"${algo}"_"${wp}"_"${ptrange}
	    cp ../makeSFDatacard.C .
	    cmdmakedatacard=$(echo 'makeSFDatacard.C("'${inputname}'")')
	    root -l -q ${cmdmakedatacard} > sf.txt
	    sed -n -i '3,$ p' sf.txt
	    
            ## do the tag and probe
	    echo "run the tag an probe"
	    if [ ${object} == "T" ];
            then
		text2workspace.py -m 125 -P HiggsAnalysis.CombinedLimit.TagAndProbeExtended:tagAndProbe sf.txt --PO categories=catp3,catp2,catp1
	    elif [ ${object} == "W" ];
            then	
		text2workspace.py -m 125 -P HiggsAnalysis.CombinedLimit.TagAndProbeExtended:tagAndProbe sf.txt --PO categories=catp2,catp3,catp1
	    fi
	    mv sf.root sf"_"${inputname}".root"
	    echo "Do the MultiDimFit"
	    combine -M MultiDimFit -m 125 sf"_"${inputname}.root --algo=singles --robustFit=1 --cminDefaultMinimizerTolerance 5.
	    echo "Run the FitDiagnostics"    
	    combine -M FitDiagnostics -m 125 sf"_"${inputname}.root --saveShapes --saveWithUncertainties --robustFit=1 --cminDefaultMinimizerTolerance 5.
	    mv fitDiagnostics.root sf"_"fitDiagnostics"_"${inputname}".root"
	    mv sf.txt sf"_"datacard"_"${inputname}".txt"
	    cd ../
	    cmdmake=$(echo 'makePlots.C("'${workdir}'","'${inputname}'","'${wp}'","'${ptrange}'",'50.','250.','20',"mass")')
	    root -l -q ${cmdmake}
	done
    done
done
