import sys, os, time
import scipy as sp
from commands import getoutput as gop
from parameters import *

hostnumbers=[1,2,3,4,5,6,7,9,10,11,12,17,18,19]

os.system("rm *.lock *.stat")


##kill all old processes
host = []
hoststate = []
for h in hostnumbers:
	host.append("edlin"+str(h))
	hoststate.append(0)
	#os.system('ssh edlin'+str(h)+' killall python &')
	os.system("echo 0 > edlin"+str(h)+".stat")
	
H = len(host)
#quit()



h1=h=0

workingdir=os.getcwd()

##renew host job status files
for h in range(0,len(host)):
 	os.system('ssh '+host[h]+' top -b -n1 | grep matnjm | grep -c python > '+host[h]+'.stat &')
 	

for p1 in sp.arange(par1min,par1max,par1step):
  for p2 in sp.arange(par2min,par2max,par2step):
   success=0
   while success==0:
     if h1==(H-1): h1=0
     else: h1=h
     for h in range(h1,H):     
       try:
        hoststate[h]=int(gop("cat "+host[h]+".stat"))
	#print "["+str(h+1)+"]  "+host[h]+" \t:", hoststate[h]
	time.sleep(0.1)
	if hoststate[h] >= 1: 
		#print "skipping "+host[h]
		time.sleep(0.1)
	else:
		print "["+str(h+1)+"] "+str(p1)+","+str(p2)+" \t"+host[h]+" \t:", hoststate[h]
		hoststate[h]=int(gop("cat "+host[h]+".stat"))
		os.system("echo %d > %s.stat"%(hoststate[h]+1,host[h]))		
		runfilename='ParamRuns/runfile_%.3f_%.3f'%(p1,p2)
		runfile=open(runfilename,'w')
		print >>runfile, "import os; import sys; sys.path.append('/home/amt6/matnjm/RemoteCalcs/PythonLibs/lib/python2.7/site-packages/');"
		print >>runfile, "os.chdir('"+workingdir+"')"
		print >>runfile, "import MyPython.Networks.NetworkModel as nm"
		print >>runfile, "nm."+par1+"="+str(p1)+"; nm."+par2+"="+str(p2)+"; host='%s'; hstate=%d"%(host[h],hoststate[h]+1)
		print >>runfile, extras+"; nm.run_net_model()"
		print >>runfile, "fout=open('FinishedResults/%.3f_%.3f.txt','w')"%(p1,p2)
		print >>runfile, "print >>fout, nm.%s, nm.%s, nm.mean, nm.var, nm.trav, nm.clav; fout.close()"%(par1,par2)
		print >>runfile, "os.remove('"+runfilename+"')"	
		print >>runfile, "from commands import getoutput as gop"
		print >>runfile, 'hoststate=int(gop("cat "+host+".stat"))'
		print >>runfile, 'os.system("echo %d > %s.stat"%(hoststate-1,host))'
		runfile.close()		
		success=1
			
		try: os.system('ssh '+host[h]+' "cd '+workingdir+'; nice -n 10 python '+runfilename+'" &')
		except: success=0
    		time.sleep(0.1)
    		break
       except:
      	print "\tno connection"
      	time.sleep(0.1)
    
  

    
    
    
    
    
    
    
    
    
###
