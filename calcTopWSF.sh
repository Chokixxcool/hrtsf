#!/bin/bash
## arguments object = "T" or "W", year = 2016 or 2017 or 2018, folder_name
object=$1
year=$2
workdir0=$3

syst="tot"

declare -a algos
declare -a ptranges
declare -a WPs_mist_rate_0p1
declare -a WPs_mist_rate_0p5
declare -a WPs_mist_rate_1p0
declare -a WPs_mist_rate_5p0
declare -a WPs_mist_rate
declare -a mist_rates

#declare WP_Top_binarzied
#workdir0="V4_Top_2016"
mkdir ${workdir0}

if [ ${object} == "T" ];
then
    #algos=("sdtau32" "sdtau32btag" "ecftoptag" "hotvr" "best" "imagetop" "imagetopmd" "deepak8" "deepak8md")
    ptranges=("low" "lowmed" "med" "medhi")
    algos=("deepak8" "deepak8md" "deepak8_raw" "deepak8md_raw")
    #algos=("deepak8")
    #ptranges=("medhi")

    mist_rates=("0p1" "0p5" "1p0" "5p0")
    #mist_rates=("0p5")
    
    if [ ${year} == 2016 ];
    then
	    WPs_mist_rate_0p1=(0.989966 0.864515 0.8927 0.466789) # 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top
	    WPs_mist_rate_0p5=(0.937122 0.621402 0.688459 0.219164) # 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top
	    WPs_mist_rate_1p0=(0.852861 0.436951 0.534739 0.13735) # 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top
	    WPs_mist_rate_5p0=(0.245148 0.0669528 0.107193 0.0274599) # 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top
    elif [ ${year} == 2017 ];
    then
            WPs_mist_rate_0p1=(0.985738 0.842546 0.817421 0.315268) # 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top
            WPs_mist_rate_0p5=(0.894945 0.57765 0.497896 0.12387) # 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top
            WPs_mist_rate_1p0=(0.74501 0.391455 0.310047 0.0737485) # 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top
            WPs_mist_rate_5p0=(0.0931942 0.0542414 0.0275957 0.0138089) # 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top    
    elif [ ${year} == 2018 ];
    then
            WPs_mist_rate_0p1=(0.986217 0.844952 0.831612 0.333162) # 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top
            WPs_mist_rate_0p5=(0.898277 0.559342 0.523792 0.126772 ) # 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top
            WPs_mist_rate_1p0=(0.75146 0.36306 0.334927 0.0732553) # 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top
            WPs_mist_rate_5p0=(0.102426 0.045428 0.0342551 0.0130718) # 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top    
    fi

    #echo ${WPs_mist_rate_0p1[1]}

elif [ ${object} == "W" ];
then
    #algos=("sdtau21" "sdn2" "sdn2ddt" "best" "deepak8" "deepak8md")
    algos=( "deepak8" "deepak8md" "deepak8_raw" "deepak8md_raw") 
    ptranges=("low" "lowmed" "med")
    #algos=("sdn2")
    #ptranges=("low")

    mist_rates=("0p1" "0p5" "1p0" "5p0")

    if [ ${year} == 2016 ];
    then
	    WPs_mist_rate_0p1=(0.993694 0.910292 0.854871 0.620627) # 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W
	    WPs_mist_rate_0p5=(0.972569 0.759349 0.76604 0.471379) # 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W
	    WPs_mist_rate_1p0=(0.941254 0.631961 0.688198 0.383825) # 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W
	    WPs_mist_rate_5p0=(0.526229 0.183695 0.255735 0.129108) # 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W
    elif [ ${year} == 2017 ];
    then
            WPs_mist_rate_0p1=(0.998032 0.960866 0.908412 0.733628) # 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W
            WPs_mist_rate_0p5=(0.991407 0.884424 0.851776 0.616956) # 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W
            WPs_mist_rate_1p0=(0.981299 0.802331 0.801854 0.5366) # 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W
            WPs_mist_rate_5p0=(0.778869 0.313254 0.436723 0.220494) # 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W
    elif [ ${year} == 2018 ];
    then
            WPs_mist_rate_0p1=(0.997201 0.952358 0.894613 0.71532) # 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W
            WPs_mist_rate_0p5=(0.987834 0.859153 0.829094 0.591239) # 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W
            WPs_mist_rate_1p0=(0.973452 0.766602 0.772662 0.507302) # 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W
            WPs_mist_rate_5p0=(0.706981 0.274176 0.378693 0.197519) # 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W
    fi
fi

## loop over the algos
 
for mistRate in "${mist_rates[@]}";
do
 	unset WPs_mist_rate

        if [ ${mistRate} == "0p1" ];
        then              
		for element in "${WPs_mist_rate_0p1[@]}"
                do	
	        	WPs_mist_rate+=("${element}")
                done

		WP_Top_binarized=${WPs_mist_rate[0]}
                WP_Top_binarizedMD=${WPs_mist_rate[1]}
                WP_Top_raw=${WPs_mist_rate[2]}
                WP_Top_rawMD=${WPs_mist_rate[3]}
                
                #echo ${WPs_mist_rate[@]}             

                #echo ${WP_Top_binarized} 
                #echo ${WP_Top_binarizedMD}
                #echo ${WP_Top_raw} 
                #echo ${WP_Top_rawMD} 

        elif  [ ${mistRate} == "0p5" ];
        then
                for element in "${WPs_mist_rate_0p5[@]}"
                do
                        WPs_mist_rate+=("${element}")
                done

                WP_Top_binarized=${WPs_mist_rate[0]}
                WP_Top_binarizedMD=${WPs_mist_rate[1]}
                WP_Top_raw=${WPs_mist_rate[2]}
                WP_Top_rawMD=${WPs_mist_rate[3]}

                
        elif  [ ${mistRate} == "1p0" ];
        then
                for element in "${WPs_mist_rate_1p0[@]}"
                do
                        WPs_mist_rate+=("${element}")
                done

                WP_Top_binarized=${WPs_mist_rate[0]}
                WP_Top_binarizedMD=${WPs_mist_rate[1]}
                WP_Top_raw=${WPs_mist_rate[2]}
                WP_Top_rawMD=${WPs_mist_rate[3]}

                
        elif  [ ${mistRate} == "5p0" ];
        then
                for element in "${WPs_mist_rate_5p0[@]}"
                do
                        WPs_mist_rate+=("${element}")
                done          

                WP_Top_binarized=${WPs_mist_rate[0]}
                WP_Top_binarizedMD=${WPs_mist_rate[1]}
                WP_Top_raw=${WPs_mist_rate[2]}
                WP_Top_rawMD=${WPs_mist_rate[3]}
      
        fi
		 
	for algo in "${algos[@]}";
	do

	    workdir=${workdir0}"/"${object}"_"${algo}"_"${syst}"_mist_rate_"${mistRate}
	    mkdir ${workdir}

	    ## loop over the working points
	    for wp in "JMAR"
	    do

		## loop over the pt bins
		for ptrange in "${ptranges[@]}";
		do
				
		    ##make templates
		    echo "make templates"
		    cmdpass=$(echo 'makeSFTemplates.C("'${object}'","'${algo}'","'${wp}'","'${ptrange}'","'${syst}'",true,"'${mistRate}'",'${WP_Top_binarized}','${WP_Top_binarizedMD}','${WP_Top_raw}','${WP_Top_rawMD}','${year}',"'${workdir0}'")') 
                    cmdfail=$(echo 'makeSFTemplates.C("'${object}'","'${algo}'","'${wp}'","'${ptrange}'","'${syst}'",false,"'${mistRate}'",'${WP_Top_binarized}','${WP_Top_binarizedMD}','${WP_Top_raw}','${WP_Top_rawMD}','${year}',"'${workdir0}'")')              
		    root -l -q ${cmdpass}
		    root -l -q ${cmdfail}
	 
		    ## make datacard
		    echo "make datacard"
		    echo " "
		    cd ${workdir}
		    inputname=${object}"_"${algo}"_"${wp}"_"${ptrange}
                    if [ ${year} == 2016 ];
                    then
			cp ../../makeSFDatacard.C .
                    elif [ ${year} == 2017 ] || [ ${year} == 2018 ];
                    then
                         cp ../../makeSFDatacard_2017.C .
                    fi
                    cp ../../combineTool.py .
                    cp ../../plotImpacts.py .  

                    if [ ${year} == 2016 ];
                    then
		         cmdmakedatacard=$(echo 'makeSFDatacard.C("'${inputname}'")')
                    elif [ ${year} == 2017 ] || [ ${year} == 2018 ];
                    then 
                         cmdmakedatacard=$(echo 'makeSFDatacard_2017.C("'${inputname}'")')
                    fi
 

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
  		    #combine -M MultiDimFit -m 125 sf"_"${inputname}.root --algo=singles --robustFit 1 --cminDefaultMinimizerStrategy 0 	
		    echo "Run the FitDiagnostics"    
		    combine -M FitDiagnostics -m 125 sf"_"${inputname}.root --saveShapes --saveWithUncertainties --robustFit=1 --cminDefaultMinimizerTolerance 5.
	 	    #combine -M FitDiagnostics -m 125 sf"_"${inputname}.root --saveShapes --saveWithUncertainties --robustFit 1 --cminDefaultMinimizerStrategy 0 
		    mv fitDiagnostics.root sf"_"fitDiagnostics"_"${inputname}".root"
                    
                    python combineTool.py -M Impacts -d sf"_"${inputname}.root -m 125 --doInitialFit --robustFit 1
		    python combineTool.py -M Impacts -d sf"_"${inputname}.root -m 125 --robustFit 1 --doFits --parallel 60
		    python combineTool.py -M Impacts -d sf"_"${inputname}.root -m 125 -o impacts.json
                    python plotImpacts.py -i impacts.json -o impacts		

                    mv impacts.pdf impacts"_"${inputname}.pdf
 
                    rm higgsCombine_paramFit_*  
                    rm combineTool.py
                    rm plotImpacts.py
                    rm impacts.json
                       
		    mv sf.txt sf"_"datacard"_"${inputname}".txt"
		    cd ../../
		    cmdmake=$(echo 'makePlots.C("'${workdir}'","'${inputname}'","'${wp}'","'${ptrange}'",'50.','250.','20',"mass")')
		    root -l -q ${cmdmake}
		done
	    done
	done
done
