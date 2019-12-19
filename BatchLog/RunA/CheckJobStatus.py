import argparse
import os 
import glob

#Command line flags and arguments                                                                       
parser = argparse.ArgumentParser()
parser.add_argument('-d, --delComplete', dest='delComplete', action='store_true', help='delete completed jobs')
args = parser.parse_args()

delComplete = args.delComplete

allOutFile =  glob.glob('./*.out')
allOutFile.sort() # sort by name

jobsDone=[]
jobsNotDone=[]

for fileName in allOutFile:
  file = open(fileName,"r")


  lines = file.read()
  if "calcTopWSF::Done" in lines:
    jobsDone.append(fileName)
  else:
    jobsNotDone.append(fileName)

print "============================================"
print "                Jobs Done                   "
print "============================================"

for jobs in jobsDone:
  print jobs

print "============================================"
print "                Jobs Still Not Done         "
print "============================================"

for jobs in jobsNotDone:
  print jobs


print "========================================================"
print "                Checking last line of jobs  not done"
print "========================================================"

for jobs in jobsNotDone:
  print jobs 
  os.system('tail -n 1 ' + jobs)
  print "\n"


#
# Delete completed job directories
#
if delComplete:
  if len(jobsDone) == 0:
    print "No completed jobs to be deleted"
  else:
    for jobs in jobsDone:
      jobs=jobs[:-4]
      print "deleting %s"%(jobs)
      os.system('rm -rf %s.out'%jobs)
      os.system('rm -rf %s.err'%jobs)

