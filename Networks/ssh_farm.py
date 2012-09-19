import sys, os, time
import scipy as sp
from commands import getoutput as gop
new_jobs='' ##leave blank here and put name of one new master-level runfile in job-level parameters file if continuation is required
import parameters
reload(parameters)
from parameters import *

hostnumbers=[1,2,3,4,5,6,7,9,10,12,17,18]
hosts=['edlin%d'%(i) for i in hostnumbers]
maxjobs=1



def set_params():
    paramvals=[]
    for p1 in sp.arange(par1min,par1max,par1step):
	for p2 in sp.arange(par2min,par2max,par2step):
		paramvals.append((p1,p2))
    return paramvals

def purge_jobs(hosts=hosts):
	for host in hosts:
		os.system('ssh '+host+' killall -u matnjm python &')


###the base script to run in each job ### needs liberating!
def gen_script(runfilename,par1,p1,par2,p2,host):
	workingdir=os.getcwd()
	runfile=open(runfilename,'w')
	print >>runfile, "import os; import sys; sys.path.append('/home/amt6/matnjm/RemoteCalcs/PythonLibs/lib/python2.7/site-packages/');"
	print >>runfile, "os.chdir('"+workingdir+"')"
	print >>runfile, "import MyPython.Networks.NetworkModel as nm"
	print >>runfile, "nm."+par1+"="+str(p1)+"; nm."+par2+"="+str(p2)+"; host='%s'"%(host)
	print >>runfile, "runnm=True; "+extras
	print >>runfile, "if runnm==True: nm.run_net_model()"
	print >>runfile, "if runnm==True: fout=open('FinishedResults/%.3f_%.3f.txt','w')"%(p1,p2)
	print >>runfile, "if runnm==True: print >>fout, nm.%s, nm.%s, nm.mean, nm.var, nm.trav, nm.clav; fout.close()"%(par1,par2)
	print >>runfile, "os.remove('"+runfilename+"')"	
	runfile.close()	



###the gubbins
def job_sow(): 	
    workingdir=os.getcwd()
    hi=0
    paramvals=set_params()
    while len(paramvals)>0:
        ##look if host has max jobs from me
 	oput=gop('ssh -o NumberOfPasswordPrompts=0 -f '+hosts[hi]+' "hostname; top -b -n1 | grep matnjm | grep -c python"').split()
 	if len(oput)==2 and int(oput[1])<maxjobs:
 	    p1,p2=paramvals.pop(0)
 	    #print p1,p2
 	    host=oput[0]
 	    runfilename='ParamRuns/runfile_%.3f_%.3f'%(p1,p2)
 	    gen_script(runfilename,par1,p1,par2,p2,host)
 	    time.sleep(0.1)
 	    print p1, p2, host
 	    os.system('ssh -o NumberOfPasswordPrompts=0 -f '+host+' "cd '+workingdir+'; nice -n 10 python '+runfilename+'" &')
 	    #print 'running'
 	hi=(hi+1)%len(hosts) ##cycle through hosts
    if len(new_jobs)>0:
    	os.chdir('..')
    	os.system('python '+new_jobs+' &')


def make_dirs():
    try: 
	os.mkdir('FinishedResults')	
	os.mkdir('ParamRuns')
    except: 
        nowtime=time.asctime()
    	os.mkdir(nowtime)
    	os.rename('FinishedResults',nowtime+'/FinishedResults')
    	os.rename('ParamRuns',nowtime+'/ParamRuns')
    	os.mkdir('FinishedResults')	
	os.mkdir('ParamRuns')
  

    
    
    
    
    
    
    
    
    
###
