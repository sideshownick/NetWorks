import networkx as nx
import scipy as sp

##assign weights to links
##version 1: retain links with probability P
def assign_linkweights(G,edges,P):
	for e in edges:
		if sp.random.random() > P:
			G.edge[e[0]][e[1]]['weight'] = 0.0

	
def scale_sizes(G, nodes, groups, works, node_ps, group_ps, link_lw):
	for g in list(groups):
		G.node['g%s'%g]['size'] *= group_ps/100.0
		
	for w in works:
		G.node['w%s'%w]['size'] *= group_ps/100.0
	
	for n in list(nodes):
		G.node[n]['size'] *= node_ps/100.0

	for e in G.edges():
		G.edge[e[0]][e[1]]['weight'] *= link_lw/100.0

##clear work nodes
def remove_works(Gs,W):
	grouplist=[]
	for w in range(0,W):
		grouplist.append('w%d'%w)
		
	Gs.remove_nodes_from(grouplist)
	
	
##clear inter-personal ties	
def remove_ties(Gs,G0):
	for g in range(1,G0+1):
		for e in nx.ego_graph(Gs,'g%d'%g).edges():
			try: Gs.remove_edge(e[0].replace('g',''),e[1].replace('g',''))
			except: pass

##clear group nodes
def remove_groups_from(Gs,groups):
	grouplist=[]
	for g in list(groups):
		grouplist.append('g%s'%g)
		
	#for w in works:
	#	grouplist.append('w%s'%w)
		
	Gs.remove_nodes_from(grouplist)
	
	
##clear inter-personal ties	
def remove_ties_from(Gs,groups):
	for g in list(groups):
		for e in nx.ego_graph(Gs,'g%s'%g).edges():
			try: Gs.remove_edge(e[0].replace('g',''),e[1].replace('g',''))
			except: pass






##make basic geographic society graph based on data
def geo_sparse(nodes,groups,M='',P=5,radius='',G=0,assign_groups=True,make_friends=True,random_seed='',node_points=100,group_points=100,link_width=100,works=range(0,20),directed=True):
	#N=number of nodes; G0=number of groups; M=membership number (groups per person)
	#P=partners per group; PO=number_of_potential_group_links.probability_of_link
	try: sp.random.seed(random_seed)
	except: pass
	
	##set node list
	nodestrings=list(nodes)
	N=len(nodestrings)
	
	##create groups
	grouplist=[]
	for g in list(groups):
		grouplist.append('g%s'%g)
	G0=len(grouplist)

	if G==0:
		##initialise graph
		if directed==True: Gs=nx.DiGraph()
		else: Gs=nx.Graph()
	  
		for n in nodestrings:
			Gs.add_node(n, state=0.0, colour="red", size=node_points*0.2,
					nodetype="house", xloc=int(nodes[n][1]), yloc=int(nodes[n][2]))
	
		for g in list(groups):		
			Gs.add_node('g%s'%g, state=0.0, colour="green", size=group_points*0.5, 
					nodetype="group", xloc=int(groups[g][1]), yloc=int(groups[g][2])) 
	else: Gs=G
	
	##PROTOTYPE: assign people to one of W random workplaces
	for w in works:
		Gs.add_node('w%s'%w, state=1.0, colour="blue", size=group_points*0.8, nodetype="work", 
		     xloc=int(425000+8000*sp.random.random()), yloc=int(432000+5000*sp.random.random()))
	if len(works) > 0:
	    for n in nodestrings:
	      if nodes[n][0]['work']==1:
		w=int(len(works)*sp.random.random())
		Gs.add_edge('w%s'%w,n)
		Gs.add_edge(n,'w%s'%w)
		
	#quit()
		
	##assign them to P others at work
	for w in works:
		Size=len(Gs['w%s'%w])
		members=list(Gs['w%s'%w])	
		a=members
		gdeg={}
		for n in a: gdeg[n]=0
		while len(a)>0:
    			n=a.pop(sp.random.random_integers(0,len(a)-1))
    			b=list(sp.copy(a))
    			while gdeg[n]<P:#Gs.degree(n)<P:
				if len(a) > 0: 
					nn=a.pop(sp.random.random_integers(0,len(a)-1))
					#Gs.add_edge(n,nn)#do other way for digraph(see below)
					Gs.add_edge(nn,n,weight=float(nodes[n][0]['t_wrk']))
					Gs.add_edge(n,nn,weight=float(nodes[nn][0]['t_wrk']))
					gdeg[n]+=1
					gdeg[nn]+=1
				else: break
    			for n in b:
    				if gdeg[n]==P: b.remove(n)#Gs.degree(n)==P: b.remove(n)
    			a=b

	'''
		Size=len(Gs['w%s'%w])
		members=list(Gs['w%s'%w])
	    	ntemp1={}
	    	for n in members:
			##make an array keeping count of individual's remaining connections
			ntemp1[n]=P
	
	    	for n in list(ntemp1):##for future use, in case use individual data
			if ntemp1[n]==0:##if individual has no connections
				ntemp1.pop(n)##remove them from array
				
	    	while len(ntemp1) > 1:		
			##get a random member of the array
			n1=ntemp1.keys()[sp.random.random_integers(0,len(ntemp1)-1)]
			kn1=ntemp1.pop(n1)##pop out the value for the number of connections
	
			##pick a random member of the remaining (temporary) array
			n2=ntemp1.keys()[sp.random.random_integers(0,len(ntemp1)-1)]
			ntemp1[n2]-=1 ##remove one from the number (in temp 1) of connections it still needs
			##pop n2 out if now complete
			if ntemp1[n2]==0: ntemp1.pop(n2)
			
			##return n1 to array if it still has spare links
			if kn1 > 1: ntemp1[n1]=kn1-1

			##connect the two nodes	
			Gs.add_edge(n2,n1,weight=float(nodes[n1][0]['t_wrk']))
			Gs.add_edge(n1,n2,weight=float(nodes[n2][0]['t_wrk']))	
    	for i in range(len(Gs)):
		print len(Gs[i])
	quit()
	'''
	if assign_groups==True and len(grouplist)>0:
		rad=radius #5000
		##make each node a member of M random groups
		for n in nodestrings:
			#if n in map(int,['56','93','133','137','630','670']): 
	      		#	print nodes[n]
			##get x,y coords of node
			xn=Gs.node[n]['xloc']
			yn=Gs.node[n]['yloc']
			
			##get distances to each group
			group_dist=[]	
			for g in grouplist:
				xg=Gs.node[g]['xloc']
				yg=Gs.node[g]['yloc']
				distance=sp.sqrt((xn-xg)**2+(yn-yg)**2)
				if radius!='':
					if distance <= rad:
						group_dist.append((g,radius*sp.random.random()))
					else: group_dist.append((g,distance))
				else: group_dist.append((g,distance))
				##could also set all within min radius to same dist, to add randomness
			##get array, sorted according to node-group distance
			gd=sp.sort(sp.array(group_dist,[('group','S10'),('dist',float)]),order='dist')
			
			if M!='':
				r1=sp.random.random()
				cumM=0.0
			##assign to number of groups according to probability distribution
			##this assigns starting with closest group upwards (note above about min dist)
				for m in range(0,len(M)):
					cumM+=M[m]
					if r1 > cumM:
						Gs.add_edge(gd[m][0],n)
						Gs.add_edge(n,gd[m][0])	
			else:
				##assigns to a number of groups based on data, closest first
				for m in range(int(nodes[n][0]['grp'])):
					Gs.add_edge(gd[m][0],n)
					Gs.add_edge(n,gd[m][0])

	##connect each member randomly to P other members of each group
	for group in grouplist:
			Size=len(Gs[group])
			members=list(Gs[group])
			a=members
			gdeg={}
			for n in a: gdeg[n]=0
			while len(a)>0:
    				n=a.pop(sp.random.random_integers(0,len(a)-1))
    				b=list(sp.copy(a))
    				while gdeg[n]<P:#Gs.degree(n)<P:
					if len(a) > 0: 
						nn=a.pop(sp.random.random_integers(0,len(a)-1))
						#Gs.add_edge(n,nn)
						Gs.add_edge(nn,n,weight=float(nodes[n][0]['t_grp']))						
						Gs.add_edge(n,nn,weight=float(nodes[nn][0]['t_grp']))
						gdeg[n]+=1
						gdeg[nn]+=1
					else: break
    				for n in b:
    					if gdeg[n]==P: b.remove(n)#Gs.degree(n)==P: b.remove(n)
    				a=b
	'''
		Size=len(Gs[group])
		members=list(Gs[group])
	    	ntemp1={}
	    	for n in members:
			##make an array keeping count of individual's remaining connections
			ntemp1[n]=P
	
	    	for n in list(ntemp1):##for future use, in case use individual data
			if ntemp1[n]==0:##if individual has no connections
				ntemp1.pop(n)##remove them from array
				
	    	while len(ntemp1) > 1:		
			##get a random member of the array
			n1=ntemp1.keys()[sp.random.random_integers(0,len(ntemp1)-1)]
			kn1=ntemp1.pop(n1)##pop out n1 and get the number of its connections
			
			##pick a random member of the remaining (temporary) array
			n2=ntemp1.keys()[sp.random.random_integers(0,len(ntemp1)-1)]
			ntemp1[n2]-=1 ##remove one from the number (in temp 1) of connections it still needs
			##pop n2 out if now complete
			if ntemp1[n2]==0: ntemp1.pop(n2)
			
			##return n1 to array if it still has spare links
			if kn1 > 1: ntemp1[n1]=kn1-1
	
			##connect the two nodes
			Gs.add_edge(n2,n1,weight=float(nodes[n1][0]['t_grp']))
			Gs.add_edge(n1,n2,weight=float(nodes[n2][0]['t_grp']))	
	'''
	if make_friends==True:
	    ##connect to random depending on data
	    ntemp1={}
	    for n in nodes:
		##make an array of number of each individual's long-dist (random) connections
		ntemp1[n]=int(nodes[n][0]['ind'])
	    for n in list(ntemp1):
		if ntemp1[n]==0:##if individual has no connections
			ntemp1.pop(n)##remove them from array
	    while len(ntemp1) > 1:		
		##get a random member of the array
		n1=ntemp1.keys()[sp.random.random_integers(0,len(ntemp1)-1)]
		kn1=ntemp1.pop(n1)##pop out the value for the number of connections

		##pick a random member of the remaining (temporary) array
		n2=ntemp1.keys()[sp.random.random_integers(0,len(ntemp1)-1)]
		ntemp1[n2]-=1 ##remove one from the number (in temp 1) of connections it still needs		
		##pop n2 out if now complete
		if ntemp1[n2]==0: ntemp1.pop(n2)
		
		##return n1 to array if it still has spare links
		if kn1 > 1: ntemp1[n1]=kn1-1	
			
		#Gs.add_edge(n2,n1)
		Gs.add_edge(n2,n1,weight=float(nodes[n1][0]['t_ind']))##connect the two nodes
		Gs.add_edge(n1,n2,weight=float(nodes[n2][0]['t_ind']))
	
	##remove self-edges
	Gs.remove_edges_from(Gs.selfloop_edges())
	
	return Gs

def nearnei_random(N,k,radius0):
  G=nx.Graph()
  for n in range(0,N):
	G.add_node(n, state=1.0, xloc=n, yloc=0)
	
  for n in range(0,N):
	n1=n
	nvals=[n]
	escape=0
	while len(G.edge[n]) < k and escape==0:
	    count=0
	    while(n1 in nvals) and escape==0:
	        count+=1
		n1=int(sp.mod(n+2*radius0*(sp.random.random()-0.5),N))
		if len(G.edge[n1]) >= k: n1=n
		if count == 100: escape=1
	    nvals.append(n1)
	    G.add_edge(n,n1,weight=1.0)
  return G
  
def nearnei_regular(N,nnei,dnei):
  G=nx.Graph()
  for n in range(0,N):
	G.add_node(n, state=1.0, xloc=n, yloc=0)
	
  for n in range(0,N):
  	for j in range(1,nnei+1):
		G.add_edge(n,sp.mod(n+dnei*j,N),weight=1.0)
  return G


def watts_2D(Nh, Nv, pr):
	Gw=nx.grid_2d_graph(Nh, Nv, periodic=False)
	
	nx.double_edge_swap(Gw, nswap=pr*Nh*Nv*4, max_tries=100)
	
	Gs=nx.Graph()
	Gs.add_nodes_from(Gw.nodes(),state=1.0)
	Gs.add_edges_from(Gw.edges(),weight=1.0)
	##remove self-edges
	Gs.remove_edges_from(Gs.selfloop_edges())
	
	return Gs
	

def pl_cluster_new(n, m, p, random_seed=None):
	Gw=nx.powerlaw_cluster_graph(n, m, p, seed=random_seed)
	
	Gs=nx.Graph()
	Gs.add_nodes_from(Gw.nodes(),state=1.0)
	Gs.add_edges_from(Gw.edges(),weight=1.0)
	##remove self-edges
	Gs.remove_edges_from(Gs.selfloop_edges())
	
	return Gs

##make watts network
def watts_new(n,nb,pr,double_swap=False):

	Gs=nx.Graph()
	if double_swap==False:
		Gw=nx.watts_strogatz_graph(n, nb, pr)
	else:
		Gw=nx.watts_strogatz_graph(n, nb, 0.0)
		nx.double_edge_swap(Gw, nswap=int(pr*n*nb/2.), max_tries=10000)
		
	Gs.add_nodes_from(Gw.nodes(),state=1.0,parameters={})
	
	Gs.add_edges_from(Gw.edges(),weight=1.0)
	
	##remove self-edges
	Gs.remove_edges_from(Gs.selfloop_edges())
	
	return Gs

##make hexagonal watts 
def watts_hex(Ny,Nx,pr=0.5):
	Gs=nx.Graph()
	Gs.add_nodes_from(range(0,Nx*Ny),state=1.0)
	for iy in range(0,Ny):
	    for ix in range(0,Nx):
	    	ni = iy*Nx+ix
	    	nj1 = iy*Nx+sp.mod(ix+1,Nx)
	    	nj2 = sp.mod(iy+1,Ny)*Nx+ix
	    	nj3 = sp.mod(iy+1,Ny)*Nx+sp.mod(ix+1,Nx)
		Gs.add_edges_from(((ni,nj1),(ni,nj2),(ni,nj3)),weight=1.0)

	nx.double_edge_swap(Gs, nswap=int(pr*Nx*Ny*3), max_tries=10000)

	##remove self-edges
	Gs.remove_edges_from(Gs.selfloop_edges())
	
	return Gs
	
	
##make 8-star watts 
def watts_truss(Ny,Nx,pr=0.1,double_swap=True):
	#,tri_swap=False):
	Gs=nx.Graph()
	for iy in range(0,Ny):
	    for ix in range(0,Nx):
		Gs.add_node(iy*Nx+ix,state=1.0,xloc=ix,yloc=iy)
	for iy in range(0,Ny):
	    for ix in range(0,Nx):
	    	ni = iy*Nx+ix
	    	nj1 = iy*Nx+sp.mod(ix+1,Nx)
	    	nj2 = sp.mod(iy+1,Ny)*Nx+ix
	    	nj3 = sp.mod(iy+1,Ny)*Nx+sp.mod(ix+1,Nx)
		Gs.add_edges_from(((ni,nj1),(ni,nj2),(ni,nj3),(nj1,nj2)),weight=1.0)

	#if tri_swap==True:
	#	triad_swap(Gs, nswap=int(pr*Nx*Ny*4))
	if double_swap==True:
		nx.double_edge_swap(Gs, nswap=int(pr*Nx*Ny*4), max_tries=10000)	
	
	else:
		nodes=list(Gs)
		for sw in range(int(pr*Nx*Ny*4)):
			edges=Gs.edges()
			re=int(len(edges)*sp.random.random())
			Gs.remove_edge(edges[re][0],edges[re][1])
			nodes=list(Gs)
			n1=int(len(nodes)*sp.random.random())
			for tries in range(0,int(1e6)):
				n2=int(len(nodes)*sp.random.random())
				if n2!=n1 and (n1,n2) not in edges and (n2,n1) not in edges: break
			Gs.add_edge(n1,n2,weight=1.0)

	##remove self-edges
	Gs.remove_edges_from(Gs.selfloop_edges())
	
	return Gs

def random_new(n,nb,random_seed=None):

	p=1.0*nb/n
	
	Gr=nx.fast_gnp_random_graph(n, p, seed=random_seed)
	Gs=nx.Graph()
	
	Gs.add_nodes_from(Gr.nodes(),state=1.0)
	
	Gs.add_edges_from(Gr.edges(),weight=1.0)
	
	##remove self-edges
	Gs.remove_edges_from(Gs.selfloop_edges())
	
	return Gs



def BA_new(n,m,random_seed=None):
	
	Gr=nx.barabasi_albert_graph(n, m, seed=random_seed)
	Gs=nx.Graph()
	
	Gs.add_nodes_from(Gr.nodes(),state=1.0)
	
	Gs.add_edges_from(Gr.edges(),weight=1.0)
	
	##remove self-edges
	Gs.remove_edges_from(Gs.selfloop_edges())
	
	return Gs


	
	
	
####
