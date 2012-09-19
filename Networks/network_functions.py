import scipy as sp
from scipy import sparse
import sys
sys.path.append('PythonLibs/lib/python2.7/site-packages/')
import networkx as nx
import my_networks as mynet

##activate a random group
def seed_random_group(G,groups,seed_group):
	##pick random groups
	for i in range(seed_group):
		group='g%s'%(str(int(len(groups)*sp.random.random())))
		members=list(G[group])
		print members
		for n in members:
			G.node[n]['state']=1.0
		
##activate a random workgroup
def seed_random_works(G,works,seed_works):
	##pick random work groups
	for i in range(seed_works):
		work='w%s'%(str(int(len(works)*sp.random.random())))	
		members=list(G[str(work)])
		print members
		for n in members:
			G.node[n]['state']=1.0	
			
##get geographic locations
def get_geoloc(filename,xcol=2,ycol=3):
	data={}
	i=0
	for line in file(filename):
		vals=line.split()
		data[i]=vals[1],vals[xcol],vals[ycol]
		i+=1
	return data

##define the load_network function, if random generates totally random connections (directed)
def load_network(N=10,k=6,network='Random'):

    	netdata=[]
	if network!='Random':
		for line in file(network):
	    		if line[0]!='#':
				line=line.split()
			if len(line)==3:
				netdata.append(line)
		data_array=sp.array(netdata)
		N=max(max(map(int,data_array[:,0])),max(map(int,data_array[:,1])))
	else:
		for n1 in range(N):
			for nei in range(k):
				n2=n1
				nvals=[n1]
				while n2 in nvals: 
					n2=int(sp.ceil(N*sp.random.random()))
				nvals.append(n2)
				netdata.append([n1,n2,1.0])
		data_array=sp.array(netdata)
	A_matrix=sp.mat(sp.zeros((int(N),int(N))))
	for row in data_array:
		A_matrix[int(row[0])-1,int(row[1])-1]=float(row[2])
	return A_matrix 
	

