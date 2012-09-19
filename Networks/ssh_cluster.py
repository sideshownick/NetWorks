import sys, os, time
import scipy as sp
from commands import getoutput as gop
from run_CPUfarm import *


os.system("rm *.lock")

host = []
hoststate = []
for h in [1,2,3,4,5,6,7,9,10,11,12,15,16,17,19]:
	host.append("edlin"+str(h))
	hoststate.append(0)
	#try: 	os.system('ssh edlin'+str(h)+' "hostname; top -b -n1 | grep matnjm | grep -c python" &')
		#os.system('ssh edlin'+str(h)+' top -b -n1 | grep matnjm | grep -c python > edlin'+str(h)+'.stat &')
	os.system('ssh edlin'+str(h)+' killall python &')
	#except: pass	

	os.system("echo 0 > edlin"+str(h)+".stat")
	
	
#host.append("math-njm")
#hoststate.append(0)
#os.system("echo 0 > "+host[h]+".stat")

H = len(host)

betamin=0.0
betamax=1.0
betastep=.01

gammamin=0.0
gammamax=1.0
gammastep=.01

h1=h=0

for exnum in experiment_numbers:
 ##renew host job status files
 for h in range(0,len(host)):
 	os.system('ssh '+host[h]+' top -b -n1 | grep matnjm | grep -c python > '+host[h]+'.stat &')
 	
 #os.system('echo "'+str(time.time())+'" > time'+str(exnum)+'_start.txt')
 os.mkdir('FinishedResults'+str(exnum))	
 for beta in sp.arange(betamax,betamin,-betastep):
  gmax=1.-beta
  for gamma in sp.arange(gammamin,gmax,gammastep):
   success=0
   while success==0:
     if h1==(H-1): h1=0
     else: h1=h
     for h in range(h1,H):     
       try:
       	#os.system('ssh '+host[h]+' top -b -n1 | grep matnjm | grep -c python > '+host[h]+'.stat &')
       	#time.sleep(1.0)
        hoststate[h]=int(gop("cat "+host[h]+".stat"))
	print "["+str(h+1)+"]  "+host[h]+" \t:", hoststate[h]
	time.sleep(0.1)
	if hoststate[h] >= 1: 
		print "skipping "+host[h]
		time.sleep(0.1)
	else:
		#while os.path.isfile(host[h]+".lock"):
		#	continue
		#open(host[h]+".lock", 'w').close()
		#os.system('ssh '+host[h]+' top -b -n1 | grep matnjm | grep -c python > '+host[h]+'.stat &')
		#time.sleep(1.0)
		hoststate[h]=int(gop("cat "+host[h]+".stat"))
		os.system("echo %d > %s.stat"%(hoststate[h]+1,host[h]))
		#os.remove(host[h]+".lock")
		
		tag='b%.3f_g%.3f'%(beta,gamma)#sp.random.random()
		runfilename='ParamRuns/runfile'+str(tag)
		runfile=open(runfilename,'w')
		print >>runfile, "import sys; sys.path.append('PythonLibs/lib/python2.7/site-packages/')\n\
beta = %f; gamma=%f; host='%s'; hstate=%d"%(beta,gamma,host[h],hoststate[h]+1)
		runfile.close()
		
		os.system('cat run_parameters'+str(exnum)+'.py >> '+runfilename)
		
		success=1
			
		try: os.system('ssh '+host[h]+' "cd Remote_Calcs; nice -n 10 python '+runfilename+'" &')
		except: success=0
    		time.sleep(0.1)
    		break
       except:
      	print "\tno connection"
      	time.sleep(0.1)
    
  

    
    
    
    
    
    
    
    
    
###
