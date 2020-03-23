#!/bin/bash

###############
## arguments ##
###############
# object :: {T, W}
# year :: {2016, 2017, 2018}
# workdir0 :: working folder name: {hrtsf_2016, hrtsf_2017, hrtsf_2018} 
# ptranges :: W: {incl, low, lowmed, med}, T: {incl, low, lowmed, med, medhi}
# algos :: W: {deepak8, sdtau21}, T: {deepak8, sdtau32}
# mist_rates :: {0p1, 0p5, 1p0, 5p0}

objects=${1}
years=${2}
workdir0=${3}
ptranges=${4}
algos=${5}
mist_rates=${6}
syst="tot"

if [[ ! -d ${workdir0} ]]; 
then mkdir ${workdir0}
fi

declare -a algos
declare -a ptranges
declare -a WPs_mist_rate_0p1
declare -a WPs_mist_rate_0p5
declare -a WPs_mist_rate_1p0
declare -a WPs_mist_rate_5p0
declare -a WPs_mist_rate
declare -a mist_rates

################################
### get WP for Top/W-tagging ###
################################

for object in "${objects[@]}";
do
  for year in "${years[@]}";
  do
    ## Top-tagging ##
    if [ ${object} == "T" ];
    then
      
      if [ ${year} == 2016 ];
      then
        WPs_mist_rate_0p1=(0.989966 0.864515 0.8927 0.466789)     # 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top
        WPs_mist_rate_0p5=(0.937122 0.621402 0.688459 0.219164)   # 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top
        WPs_mist_rate_1p0=(0.852861 0.436951 0.534739 0.13735)    # 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top
        WPs_mist_rate_5p0=(0.245148 0.0669528 0.107193 0.0274599) # 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top
      elif [ ${year} == 2017 ];
      then
        WPs_mist_rate_0p1=(0.985738 0.842546 0.817421 0.315268)     # 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top
        WPs_mist_rate_0p5=(0.894945 0.57765 0.497896 0.12387)       # 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top
        WPs_mist_rate_1p0=(0.74501 0.391455 0.310047 0.0737485)     # 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top
        WPs_mist_rate_5p0=(0.0931942 0.0542414 0.0275957 0.0138089) # 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top    
      elif [ ${year} == 2018 ];
      then
        WPs_mist_rate_0p1=(0.986217 0.844952 0.831612 0.333162)   # 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top
        WPs_mist_rate_0p5=(0.898277 0.559342 0.523792 0.126772 )  # 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top
        WPs_mist_rate_1p0=(0.75146 0.36306 0.334927 0.0732553)    # 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top
        WPs_mist_rate_5p0=(0.102426 0.045428 0.0342551 0.0130718) # 0: ak8_1_DeepAK8_TvsQCD, 1: ak8_1_DeepAK8MD_TvsQCD, 2: ak8_1_DeepAK8_Top, 3: ak8_1_DeepAK8MD_Top    
      fi

    ## W-tagging ##
    elif [ ${object} == "W" ];
    then

      if [ ${year} == 2016 ];
      then
        WPs_mist_rate_0p1=(0.993694 0.910292 0.854871 0.620627) # 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W
        WPs_mist_rate_0p5=(0.972569 0.759349 0.76604 0.471379)  # 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W
        WPs_mist_rate_1p0=(0.941254 0.631961 0.688198 0.383825) # 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W
        WPs_mist_rate_5p0=(0.526229 0.183695 0.255735 0.129108) # 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W
      elif [ ${year} == 2017 ];
      then
        WPs_mist_rate_0p1=(0.998032 0.960866 0.908412 0.733628) # 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W
        WPs_mist_rate_0p5=(0.991407 0.884424 0.851776 0.616956) # 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W
        WPs_mist_rate_1p0=(0.981299 0.802331 0.801854 0.5366)   # 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W
        WPs_mist_rate_5p0=(0.778869 0.313254 0.436723 0.220494) # 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W
      elif [ ${year} == 2018 ];
      then
        WPs_mist_rate_0p1=(0.997201 0.952358 0.894613 0.71532)  # 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W
        WPs_mist_rate_0p5=(0.987834 0.859153 0.829094 0.591239) # 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W
        WPs_mist_rate_1p0=(0.973452 0.766602 0.772662 0.507302) # 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W
        WPs_mist_rate_5p0=(0.706981 0.274176 0.378693 0.197519) # 0: ak8_1_DeepAK8_WvsQCD, 1: ak8_1_DeepAK8MD_WvsQCD, 2: ak8_1_DeepAK8_W, 3: ak8_1_DeepAK8MD_W
      fi
    fi

    #########################
    ## loop over the algos ##
    #########################
    for mistRate in "${mist_rates[@]}";
    do
      unset WPs_mist_rate

      ## Mistag rate: 0.1% ##
      if [ ${mistRate} == "0p1" ];
      then              
        for element in "${WPs_mist_rate_0p1[@]}"
        do  
          WPs_mist_rate+=("${element}")
        done

        WP_binarized=${WPs_mist_rate[0]}
        WP_binarizedMD=${WPs_mist_rate[1]}
        WP_raw=${WPs_mist_rate[2]}
        WP_rawMD=${WPs_mist_rate[3]}
      
      ## Mistag rate: 0.5% ##
      elif  [ ${mistRate} == "0p5" ];
      then
        for element in "${WPs_mist_rate_0p5[@]}"
        do
          WPs_mist_rate+=("${element}")
        done

        WP_binarized=${WPs_mist_rate[0]}
        WP_binarizedMD=${WPs_mist_rate[1]}
        WP_raw=${WPs_mist_rate[2]}
        WP_rawMD=${WPs_mist_rate[3]}   

      ## Mistag rate: 1.0%##
      elif  [ ${mistRate} == "1p0" ];
      then
        for element in "${WPs_mist_rate_1p0[@]}"
        do
          WPs_mist_rate+=("${element}")
        done

        WP_binarized=${WPs_mist_rate[0]}
        WP_binarizedMD=${WPs_mist_rate[1]}
        WP_raw=${WPs_mist_rate[2]}
        WP_rawMD=${WPs_mist_rate[3]}

      ## Mistag rate: 5.0% ##
      elif  [ ${mistRate} == "5p0" ];
      then
        for element in "${WPs_mist_rate_5p0[@]}"
        do
          WPs_mist_rate+=("${element}")
        done          

        WP_binarized=${WPs_mist_rate[0]}
        WP_binarizedMD=${WPs_mist_rate[1]}
        WP_raw=${WPs_mist_rate[2]}
        WP_rawMD=${WPs_mist_rate[3]}
      fi
      
      ## Loop over algos ##
      for algo in "${algos[@]}";
      do
        workdir=${workdir0}"/"${object}"_"${algo}"_"${syst}"_mist_rate_"${mistRate}
        eosdir="/eos/user/s/ssyedoma/JMARWTag/TempFit/"${workdir}
        if [[ ! -d ${workdir} ]]; 
        then mkdir ${workdir}
        fi
        if [[ ! -d ${eosdir} ]]; 
        then mkdir ${eosdir} 
        fi        

        ## Loop over the working points ##
        for wp in "JMAR"
        do  
          ## Loop over the pt bins ##
          for ptrange in "${ptranges[@]}";
          do  
            start=$SECONDS
          
            # 2nd step ::
            #############################################################
            cd ${workdir}
            inputname=${object}"_"${algo}"_"${wp}"_"${ptrange}
            
            ## make datacard ##
            # echo " :: making datacard . . ."
            # cp ../../makeSFDatacard.C .      
            # cmdmakedatacard=$(echo 'makeSFDatacard.C("'${inputname}'",'${year}')')
            # root -l -b -q ${cmdmakedatacard} > sf"_"datacard"_"${inputname}".txt"
            # sed -n -i '3,$ p' sf"_"datacard"_"${inputname}".txt"
            # rm makeSFDatacard.C

            ## do the tag and probe ##
            # echo " :: running the tag and probe . . ."
            # if [ ${object} == "T" ];
            # then
            #   text2workspace.py -m 125 -P HiggsAnalysis.CombinedLimit.TagAndProbeExtended:tagAndProbe sf.txt --PO categories=catp3,catp2,catp1
            # elif [ ${object} == "W" ];
            # then
            #   text2workspace.py -m 125 -P HiggsAnalysis.CombinedLimit.TagAndProbeExtended:tagAndProbe sf"_"datacard"_"${inputname}".txt" --PO categories=catp2,catp3,catp1

            # fi
            # mv sf"_"datacard"_"${inputname}".root" sf"_"${inputname}".root"

            # echo "Do the MultiDimFit"
            # combine -M MultiDimFit -m 125 sf"_"${inputname}".root" --algo=singles --robustFit 1 --cminDefaultMinimizerTolerance 5.
           
            # echo "Run the FitDiagnostics"    
            # combine -M FitDiagnostics -n "_"${inputname} -m 125 sf"_"${inputname}".root" --saveShapes --saveWithUncertainties --robustFit 1 --cminDefaultMinimizerTolerance 5.
            
            # mv fitDiagnostics"_"${inputname}.root sf"_"fitDiagnostics"_"${inputname}".root"
        
            # combineTool.py -M Impacts -d sf"_"${inputname}.root -m 125 --doInitialFit --robustFit 1
            # combineTool.py -M Impacts -d sf"_"${inputname}.root -m 125 --robustFit 1 --doFits --parallel 60
            # combineTool.py -M Impacts -d sf"_"${inputname}.root -m 125 -o impacts"_"${inputname}.json --robustFit 1 
            # plotImpacts.py -i impacts"_"${inputname}.json -o impacts"_"${inputname}

            # cp impacts"_"${inputname}.pdf ${eosdir}

            # rm higgsCombine_paramFit_*  

            # make data/mc plots ##          
            cd ../../
            
            cmdmake=$(echo 'makePlots.C("'${workdir}'","'${inputname}'","'${wp}'","'${ptrange}'",'50.','250.','20',"mass","'${object}'","'${wp}'","'${mistRate}'","'${year}'")')
            root -l -b -q ${cmdmake}
            # echo "copying plots_datamc to EOS"
            # mkdir ${eosdir}"/"plots_datamc 
            # cp -r ${workdir}"/"plots_datamc ${eosdir}

            # duration=$(( SECONDS - start ))
            # echo ""
            # echo "calcSF.sh (${object}, ${mistRate}, ${ptrange}, ${algo}, ${year}) DONE in ${duration} s"
            
          done
        done
      done
      ## make SF plots ##          
      # cd ../../
      # pwd
      # wp="JMAR"
      # cmdmake=$(echo 'makePlots.C("'${workdir}'","'${inputname}'","'${wp}'","'${ptranges}'",'50.','250.','20',"mass","'${object}'","'${wp}'","'${mistRate}'","'${year}'")')
      # root -l -q -b ${cmdmake}
      # echo "copying plots_datamc to EOS"
      # mkdir ${eosdir}"/"plots_datamc 
      # cp -r ${workdir}"/"plots_datamc ${eosdir}
    done
  done
done
duration=$(( SECONDS - start ))
echo ""
echo "calcSF.sh DONE in ${duration} s"