import scipy as sp
#from parameters import *
import networkx as nx
from scipy import random


################################
### initial condition generators
##################################

##0 or 1 at a defined fraction
def ic_binary(G,fr):
	data={}
	for n in G.nodes():
		rval=random.random()
		if rval <= fr:
			G.node[n]['state']=1.0
			data[n]=1.0
		else: 
			data[n] = 0.0
			G.node[n]['state']=0.0
	return data



#initial condition, initially only node 1 has the tech.	
def random_states(N,m0):	
	states=sp.zeros(N)
	for  i in range(N):
		if sp.random.random() < m0:
			states[i]=1
	return states
	
##assign parameters
def set_homogeneous_parameters(G,parameter_values):
	for n in G.nodes():
		G.node[n]['parameters']=parameter_values


##count number of any value in a data array
def countval(data,val):
	count=0
	for i in data:
		if i==val:
			count+=1
	return count 
	
	
##count adopters
def count_adopters(G,statename='state',value=1.0):
	data=nx.get_node_attributes(G,statename)	
    	datavals=[]
	for n in data:
		datavals.append(data[n])
	adopters=countval(datavals,value)
	return adopters
	
	
def load_parameters(N, pfile='households.dat'):
	thresh=sp.zeros(N)
	personal=sp.zeros(N)
	a=sp.zeros(N)
	b=sp.zeros(N)
	c=sp.zeros(N)
	scale=sp.zeros(N)
	
	for m,line in enumerate(file(pfile)):
	    	#if m > 0:
	    	#	n=m-1
		vals=line.split()
		thresh[n],personal[n],a[n],b[n],c[n],scale[n]=vals
	
	##ensure parameters are normalised:
	norm=sp.array(a)+sp.array(b)+sp.array(c)
	a=sp.array(a)/norm
	b=sp.array(b)/norm
	c=sp.array(c)/norm
	
	parameters=thresh,personal,a,b,c,scale
	return parameters

def threshold_distribution(N,thvals,Pth):
	threshdist=[]
	j=0
	cum=Pth[j]
	for i in range(N):
		if 1.*i/N >= cum:
			j+=1
			cum+=Pth[j]
		threshdist.append(thvals[j])
	return threshdist

def parameter_dist(N=500,p0=0.5,atypes='random',P='random'):
	parf=open('params.tmp','w')
	thresh=sp.zeros(N); personal=sp.zeros(N); scale=sp.zeros(N)
	a,b,c=sp.zeros((3,N))#; b=sp.zeros(N); c=sp.zeros(N)
	
	##generate list of values to select from
	vals=[]
	j=0
	cum=P[j]
	for i in range(N):
	    if atypes != 'random':
		if 1.*i/N >= cum:
			j+=1
			cum+=P[j]
		vals.append(atypes[j])
	    else:
	    	b1,c1=sp.random.random(2)
	    	if b1+c1 > 1.:
	    		b2,c2 = 1.-c1,1.-b1
	    	else: b2=b1; c2=c1
	    	a2=1.-b2-c2
	    	vals.append((a2,b2,c2))
	    	print >>parf, a2, b2,c2
	parf.close()	
	##randomly assign values (according to distribution)
	N1=N
	for i in range(N):
		v1=int(len(vals)*sp.random.random())
		a[i],b[i],c[i]=vals.pop(v1) 
		thresh[i]=0.25 #sp.random.random() ##NEED NONUNIFORM HERE
		personal[i]=p0
		scale[i]=0.0
	parameters=thresh,personal,a,b,c,scale
	return parameters
	
def set_parameter_dist(G,p0,atypes,P):
	N=len(G)
	thresh,personal,a,b,c,scale=parameter_dist(N,p0,atypes,P)

	for i,n in enumerate(G.nodes()):
		G.node[n]['parameters']=[a[i],b[i],c[i],thresh[i],personal[i],scale[i]]
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	 
