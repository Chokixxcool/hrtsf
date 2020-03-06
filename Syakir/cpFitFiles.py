import os, sys, glob

# for algo in ["deepak8","sdtau21"]:
# 	for mr in ["0p1","0p5","1p0","5p0"]:
# 		os.system('mkdir W_%s_tot/%s'%(algo,mr))

files=glob.glob("hrtsf*/*/sf_fitDiagnostics_*")
for algo in ["deepak8", "sdtau21"]:
	for mr in ["0p1","0p5","1p0","5p0"]:
		f=[x for x in files if mr in x and algo in x]
		for fit in f:
			os.system('cp %s W_%s_tot/%s'%(fit,algo,mr))