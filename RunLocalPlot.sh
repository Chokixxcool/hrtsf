#!/bin/bash
# run this after making SF templates & comment out SF templates production lines in calcTopWSF_Fikri.sh #
OBJECT=W
YEAR=("2016" "2017" "2018")
# WORKDIR=("hrtsf_2016" "hrtsf_2017" "hrtsf_2018")
PTBIN=("incl" "low" "lowmed" "med")
ALGO=("deepak8" "sdtau21")
MISTRATE=("0p1" "0p5" "1p0" "5p0")

for year in "${YEAR[@]}";
	do
	if [ ${year} == "2016" ]; then workdir="hrtsf_2016";
	elif [ ${year} == "2017" ]; then workdir="hrtsf_2017";
	elif [ ${year} == "2018" ]; then workdir="hrtsf_2018";
	fi

	for ptbin in "${PTBIN[@]}";
		do

		for algo in "${ALGO[@]}";
			do

			for mistrate in "${MISTRATE[@]}";
			do
			./calcTopWSF_Fikri.sh ${OBJECT} ${year} ${workdir} ${ptbin} ${algo} ${mistrate}
			done
		done
	done
done
