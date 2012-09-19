#!python
import scipy as sp
from scipy import random as sprand
import random as rand
from scipy import sparse
from MyPython.Networks.dynamics import *
from MyPython.Networks.network_functions import *
from MyPython.Networks.functions import *
from MyPython.Networks.plotters import *
import MyPython.Networks.my_networks as mynets
#sys.path.append('/home/amt6/matnjm/RemoteCalcs/PythonLibs/lib/python2.7/site-packages/')
import networkx as nx
import NetworkModel as nm

alpha=0.0
beta=1.0
gamma=0.0

Mvals=''
framedir='Frames'
spring_layout=True

random_thresholds=False
set_thresholds=False

from parameters import *

pos={}
nodes={}
nhoods={}
households={}
groups={}
G=set()
mean=0.0
var=0.0
trans=0.0
clust=0.0
trav=0.0
clav=0.0
transvals=[]
clustvals=[]


def get_house_data():
	Npars=0
	for line in file(paramfile): Npars+=1
	if N == 0: nm.N=Npars			
	levels={1.0: thresh_top, 0.75: thresh_hig, 0.5: thresh_mid, 0.25: thresh_low, 0.0: thresh_bot}	
	nm.pos={}
	if nfile!='':
	 	for n,line in enumerate(file(nfile)):
			line=line.split()
			nm.nhoods[line[0]]=line[1],line[4],line[5]
	else:
	 	for n in range(0,N):
	 		nm.nhoods[n]='n%s'%str(n), 10000*sp.random.random(), 2000*sp.random.random()
	 	
	if gfile!='':	
	 	#for i,line in enumerate(file(gfile)):
		#	line=line.split()
		#	nm.pos['g'+str(i)]=[float(line[4]),float(line[5])]
	 	nm.groups=get_geoloc(gfile,xcol=4,ycol=5)
	else:
	 	nm.groups={}
		for n in range(0,nm.Ng):
			nm.groups['%s'%str(n)]='g%s'%str(n), 10000*sp.random.random(), 500+1000*sp.random.random()
	
	number=0
	n=-1
	count=0
	randloc=0
	while len(nm.households) < nm.N:
	    if nfile=='' or random_locations==1 or len(nm.households)==Npars: randloc=1
	    if set_thresholds==True: 
	    	threshdist=threshold_distribution(N,thresh_distvals, prob_threshvals)
	    for line in file(paramfile):
		line=line.split()
		if len(line)==7:#11:
			if line[6]=='-2': line[6]=rand.choice(nm.nhoods.keys())
			if randloc==1: 
				line[0]=str(int(n)+1)
				line[6]=rand.choice(nm.nhoods.keys())
			if fixed_associations==True:
				line[3]=nm.ind_num
				line[4]=nm.grp_num
				line[5]=nm.work_num
			n=line[0]	
			if random_thresholds==True:
				node_threshold=sp.random.random() ###this may need changing to a different distribution...
			elif set_thresholds==True:
				tv1=int(len(threshdist)*sp.random.random())
				node_threshold=threshdist.pop(tv1)
			else:
				node_threshold=levels[float(line[1])]
			nm.households[n]={'ID':n,
			 	   'thresh':node_threshold,
			 	   	'p':p0,#*2*float(line[2]), 
			 	      'ind':int(line[3]), 
			 	      'grp':int(line[4]), 
			 	     'work':int(line[5]), 
			 	    'llsoa':int(line[6]), 
			 	      'red':1.0,#line[7], 
			 	    't_ind':1.0,#line[8], 
			 	    't_grp':1.0,#line[9], 
			 	    't_wrk':1.0,#line[10], 
			 	      'pos':[float(nm.nhoods[line[6]][1]),float(nm.nhoods[line[6]][2])]}
			if line[1]=='1':number+=1
			count+=1
		if count >= N: break
	if output_to_terminal!=False:
		print len(nm.households), number, 1.0-1.0*number/len(nm.households)



def build_network(is_dir=True):

	 #nodes={}
	 for i,n in enumerate(nm.households):
	 	nh=len(nm.nhoods) 
		#nm.pos[i]=[float(nm.nhoods[nm.nhoods.keys()[sp.mod(i,nh)]][1]),float(nm.nhoods[nm.nhoods.keys()[sp.mod(i,nh)]][2])]
		nm.pos[i]=nm.households[n]['pos'] ##SOMETHING HERE
		nm.nodes[i]=(nm.households[n],nm.pos[i][0],nm.pos[i][1]) ##SOMETHING HERE
	 nm.N=len(nm.nodes)
	 workgroups=range(0,nm.Works)

	 #for i in workgroups:
	 #	nm.pos['w'+str(i)]=[430000+sp.random.random(),430000+sp.random.random()]
	 G=mynets.geo_sparse(nm.nodes, nm.groups, nm.Mvals, k_gp, works=workgroups,directed=is_dir)   
	 return G




def run_net_model():	 
	  nm.transvals=[]
	  nm.clustvals=[]
	  workgroups=range(0,nm.Works)
	  get_house_data()

	  if save_frames==True:
		try: os.mkdir(framedir)
		except: 
			rnum=sprand.random_integers(10000)
			print 'Directory "'+framedir+'" exists, moving to "'+framedir+str(rnum)+'"'
			os.rename(framedir,framedir+str(rnum))
			os.mkdir(framedir)

	  #icdata=open('initial-final_vals.dat','w')

	  averages=[]

	  filename=nametag
	  
	  if seed_group==0 and seed_works==0 and randomise_network==False:
		nm.G=build_network(is_dir=False)
		mynets.remove_groups_from(nm.G,nm.groups)
	 	mynets.remove_works(nm.G,len(workgroups))
	 	
	 	#nm.trans=nx.transitivity(nx.Graph(G))
	    	#nm.clust=nx.average_clustering(nx.Graph(G))
	    	nm.trans=nx.transitivity(G)
	    	nm.clust=nx.average_clustering(G)
	    	nm.transvals.append(nm.trans)
	    	nm.clustvals.append(nm.clust)
	 	
	 	#nx.draw_networkx(G, pos=nm.pos); py.show(); quit()

	  
	  #plot1=gp_init(filename, extras='set yrange[0:1]; set xrange[0:'+str(max_time)+']', args='notitle w l, 0.48 notitle w l lt 3')
	  if save_frames==True:
	  	totfile=open(totals_file,'w')
	  ##randomise initial adopters
	  for run in range(0,nruns):
	    if output_to_terminal!=False:
	    	print v_val, 'run', run
	      
	    if seed_group>0 or seed_works>0 or randomise_network==True:
	    	nm.G=build_network(is_dir=False)
	    	if seed_group>0:
	  		seed_random_group(nm.G,nm.groups,seed_group)
	    	if seed_works>0:
	    		seed_random_works(nm.G,workgroups,seed_works)
	    
	    	mynets.remove_groups_from(nm.G,nm.groups)
	    	mynets.remove_works(nm.G,len(workgroups))
	    	nm.trans=nx.transitivity(G)
	    	nm.clust=nx.average_clustering(G)
	    	#nm.trans=nx.transitivity(nx.Graph(G))
	    	#nm.clust=nx.average_clustering(nx.Graph(G))   
	    		
	    	nm.transvals.append(nm.trans)
	    	nm.clustvals.append(nm.clust)
	    	
	    	#G.remove_node(56)
		#nx.draw(G); py.show(); quit()
	    	ic_binary(nm.G,m0)
	    	#Asp=nx.to_scipy_sparse_matrix(G)
	    	states=nx.get_node_attributes(nm.G,'state').values()
	    else:
	    	ic_binary(nm.G,m0)
	    	states=nx.get_node_attributes(nm.G,'state').values()
	    	#states=random_states(N,m0)
	    	
	    ##re-randomise parameters at every realisation
	    #parameters=parameter_dist(N,p0,atypes,P)
	    set_parameter_dist(nm.G,p0,atypes,P)
	    	
	    for n in range(len(nm.G)):#range(len(parameters[0])):
		#parameters[0][n]=households[households.keys()[n]]['thresh']
		#parameters[1][n]=households[households.keys()[n]]['p']
		nm.G.node[n]['parameters'][3]=nm.households[nm.households.keys()[n]]['thresh']
		nm.G.node[n]['parameters'][4]=nm.households[nm.households.keys()[n]]['p']
	    if save_frames==True:
	    	print >>totfile, int(sum(states))
	    #for val in states:
	    #	print >>icdata, val,
	    #print >>icdata, ''
	    #data=[states]
	    
	    if save_frames==True and run==0:
	    	import pylab as py
	    	if spring_layout==True:
	    		nm.pos=nx.spring_layout(nm.G)
	    	colormap=get_cmap()
	    	nx.draw_networkx(nx.Graph(nm.G), nm.pos, with_labels=False, 
				node_size=50.0, width=0.5,	
				node_color=states, vmin=0.0, vmax=1.0, cmap=colormap)
	    	py.savefig(framedir+'/timestep%.2d.png'%0)
	    if save_frames==True:
	    	print >>totfile, int(sum(states))

	    #gp_plot(plot1,(0,1.0*sum(states)/N))
	    for time in range(1,max_time+1):		
		#states=update_rule(Asp,states,parameters)
		#print sum(states)
		three_level(nm.G)
		states=nx.get_node_attributes(nm.G,'state').values()
		#print count_adopters(G)
		#quit()
		
		if save_frames==True and run==0:
			import pylab as py
			#states=nx.get_node_attributes(G,'state').values()
			py.clf()	
			nx.draw_networkx(nx.Graph(nm.G), nm.pos, with_labels=False, 
				node_size=50.0, width=0.5,	
				node_color=states, vmin=0.0, vmax=1.0, cmap=colormap)
			py.savefig(framedir+'/timestep%.2d.png'%time)
		if save_frames==True:
			print >>totfile, int(sum(states))
		#gp_plot(plot1,(time,1.0*sum(states)/N))
			
	    averages.append(1.0*sum(states)/N)
	    if output_to_terminal!=False:
	    	print int(sum(states)), nm.trans, nm.clust
	    if save_frames==True:
	    	print >>totfile, '\n'
	    #gp_newline(plot1)
	    #for val in states:
	    #	print >>icdata, val,
	    #print >>icdata, '\n'
	  meanav=sp.mean(averages)
	  nm.var=sp.var(averages)
	  nm.trav=sp.mean(nm.transvals)
	  nm.clav=sp.mean(nm.clustvals)
	  if output_to_terminal!=False:
	  	print meanav
	  #gp_end(plot1,filename)
	  if save_frames==True:
	  	totfile.close()
	  nm.mean=meanav

	  return meanav
