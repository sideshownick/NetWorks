import scipy as sp
from scipy import sparse
import networkx as nx
#from scipy import zeros, random, sparse, shape, ones
#from scipy import weave as wv

def update_rule(Asp,states0,parameters,scale=0.0):
	thresh,personal,a,b,c,scale0=parameters #ignore scale ( = 0 )
	states=sp.copy(states0)
	#states is a list of states for all N individuals
	
	nei_sum=Asp*states
	degrees=Asp*sp.ones(len(states))
	
	##get average of all neighbours, i.e. s
	nei_av=[]
	for i in range(0,len(nei_sum)):
		if degrees[i]>0: nei_av.append(nei_sum[i]/degrees[i])
		else: nei_av.append(0.0)
	
	totav=sum(states)/len(states) #this is m
	
	for n in range(0,len(states)): #len means length, i.e. number of individuals
		
		utility=a[n]*personal[n]+b[n]*nei_av[n]+c[n]*totav
		if states[n] < 1.0: #if state == 0
			if utility <= thresh[n]: 
				states[n]=0.0#scale*utility ##i.e. zero if scale=0
			else:
				states[n]=1.0	
	return states
	
	
	
def three_level(Gx):#,parameters):
	
	#thresh,personal,a,b,c,scale=parameters

	avg={}
	for n in Gx.nodes():
		avg[n] = 0.0
		
	data=nx.get_node_attributes(Gx,'state')
	parameters=nx.get_node_attributes(Gx,'parameters')
	
	##count individuals' neighbours' average
	for n,nbrs in Gx.adjacency_iter():
		avg[n]=0.0
		wsum=0.0
		for nbr in nbrs:
			#avg[n]+=Gx[n][nbr]['weight']*data[nbr] #weight is edge weight (default=1.0)
			avg[n]+=data[nbr] ###NOTE WEIGHTS ASSUMED 1 FOR SPEED (use above otherwise)
			wsum+=1.#Gx[n][nbr]['weight']
		try: avg[n]=avg[n]/wsum
		except: pass ##in case of division by zero
	datavals=[]
	for node in Gx.nodes():
		datavals.append(data[node])

	##system average value
	totav=sum(datavals)/len(datavals)
	
	##test utility against threshold, adopt if above threshold or take average value otherwise
	for n in Gx.nodes():
	    a,b,c,thresh,personal,scale=parameters[n]
	    utility=a*personal+b*avg[n]+c*totav

	    #utility=a[n]*personal[n]+b[n]*avg[n]+c[n]*totav
	    if data[n] < 1.0: 
		if utility < thresh: 
			Gx.node[n]['state']=scale*utility
			#if random.random() < 0.01: #thresh[n]:
			#	data[n] =  1.0
		else:
			#if random.random() > thresh[n]:
			Gx.node[n]['state']=1.0	
			
			
			
			
			
			
			
			
