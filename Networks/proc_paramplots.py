import os, scipy

datfname='alldata.txt'
figname='fig_new'
figformat='png'
save_eps=True
xcol=1
ycol=2
zcol=3
zlabel='Average Uptake'
title=''
extras=''
infotext=''

def getPars(filename):
    exclusions=['scale0','fout','adopters','parameter\\\_values',\
    'Gmax','tag','hoststate','ex','takers','numup','avup','alpha',\
    'iftakers[i]>','states[int(n)]','numup+','a1','states','data','Asp',\
    'a[n]','b[n]','personal[n]','data','datavals','datavals','c[n]','scale[n]',\
    'thresh[n]','a','ft','fd','parameters[2][n]','ifdoublenumber','nhoods[line[0]]',\
    'parameters[3][n]','line[0]','line[6]','nh','parameters','pos','ifline[6]',\
    'scale','#get\\\_geoloc(nfile,xcol','#pos[i]','parameters[1][n]','pos[i]',\
    'nodes[i]','households[n]','c','pos[g+str(i)]','levels','line','nfile','gfile']
    par={}
    for line in file(filename):
    	line=line.replace("_","\\\_").replace(" ","").replace("'","").replace('"','').replace('\t','').replace('\n','').split('=')
    	if len(line)>1:
    	    if line[0] not in exclusions:
    		par[line[0]]=''
    		for value in line[1:]:
    			par[line[0]]+=value+' '
    infotext='{/=14 Network = '+par.pop('G')+'}\\n'
    if 'nodes' in par:
		if len(par['nodes'])!=3: 
			infotext+='{/=14 nodes = '+par.pop('nodes')+'}\\n'
		else: par.pop('nodes')
    if 'groups' in par: 
		if len(par['groups'])!=3:
			infotext+='{/=14 groups = '+par.pop('groups')+'}\\n'
		else: par.pop('groups')
    if 'nodes[n]' in par: infotext+='{/=14 nodes = '+par.pop('nodes[n]')+'}\\n'
    if 'nodes[%s%str(n)]' in par: infotext+='{/=14 nodes = '+par.pop('nodes[%s%str(n)]')+'}\\n'
    if 'groups[%s%str(n)]' in par: infotext+='{/=14 groups = '+par.pop('groups[%s%str(n)]')+'}\\n'
    if 'Mvals' in par: 
    	if len(par['Mvals'])!=3:
    		infotext+='{/=14 M = '+par.pop('Mvals')+'}\\n'
	else: par.pop('Mvals')  
    for pname in par:
		infotext+='{/=14 '+pname+' = '+par[pname]+'}\\n'
    return infotext


def triangle_plot(plotname='ternary_plot'):
	gp=os.popen('gnuplot','w')
	print >>gp, '''
		set terminal postscript eps enhanced color 20
		set output "'''+plotname+'''.eps"
		set bmargin 3
		set lmargin 3
		set rmargin 3
		set tmargin 3
		set size ratio 0.866
		set yrange [0:0.866]
		set xrange [0:1]
		set noborder
		set noxtics
		set noytics
		set label 101 "'''+infotext+'''" at -0.25,0.94
		set label 1 "'''+wlabel+''' = 0"   at 0.7,0.6 rotate by -55
		set label 2 "'''+xlabel+''' = 0"   at 0.4,-0.04	 
		set label 3 "'''+ylabel+''' = 0"   at 0.165,0.38 rotate by 55 
		set label 4 "(1,0,0)" at -0.05, -0.03 center
		set label 5 '(0,1,0)' at  0.5,   0.9  center
		set label 6 '(0,0,1)' at  1.05, -0.03 center
		set palette rgbformulae 30,31,32 negative
		set palette maxcolors 25
		set colorbox horizontal
		set colorbox user origin 0.1,0.9 size 0.8,0.05
		set title "'''+zlabel+'''" 0.0,1.0
		set xlabel "{/=24 ('''+wlabel+','+xlabel+','+ylabel+''')}" 0,-1.3
		set style line 1 lt 1 lw 3 pt -1 ps 1
		set style line 2 lt 5 lw 1 pt -1 ps 1
		set arrow 1 from 0,0 to 1, 0.0 nohead front linestyle 1
		set arrow 2 from 0.1,0 to 0.55, 0.779 nohead front lt 1 lc rgb'cyan'  lw 1.5
		set arrow 3 from 0.2,0 to 0.60, 0.693 nohead front lt 1 lc rgb'cyan'  lw 1.5
		set arrow 4 from 0.3,0 to 0.65, 0.606 nohead front lt 1 lc rgb'cyan'  lw 1.5
		set arrow 5 from 0.4,0 to 0.70, 0.520 nohead front lt 1 lc rgb'cyan'  lw 1.5
		set arrow 6 from 0.5,0 to 0.75, 0.433 nohead front lt 1 lc rgb'cyan'  lw 1.5
		set arrow 7 from 0.6,0 to 0.80, 0.346 nohead front lt 1 lc rgb'cyan'  lw 1.5
		set arrow 8 from 0.7,0 to 0.85, 0.260 nohead front lt 1 lc rgb'cyan'  lw 1.5
		set arrow 9 from 0.8,0 to 0.90, 0.173 nohead front lt 1 lc rgb'cyan'  lw 1.5
		set arrow 10 from 0.9,0 to 0.95, 0.0866 nohead front lt 1 lc rgb'cyan'  lw 1.5
		set arrow 11 from 1, 0 to 0.50, 0.866 nohead front linestyle 1
		set arrow 12 from 0.95, 0.0866 to 0.05, 0.0866 nohead front lt 1 lc rgb'cyan'  lw 1.5
		set arrow 13 from 0.90, 0.173 to 0.10, 0.173 nohead front lt 1 lc rgb'cyan'  lw 1.5
		set arrow 14 from 0.85, 0.260 to 0.15, 0.260 nohead front lt 1 lc rgb'cyan'  lw 1.5
		set arrow 15 from 0.80, 0.346 to 0.20, 0.346 nohead front lt 1 lc rgb'cyan'  lw 1.5
		set arrow 16 from 0.75, 0.433 to 0.25, 0.433 nohead front lt 1 lc rgb'cyan'  lw 1.5
		set arrow 17 from 0.70, 0.520 to 0.30, 0.520 nohead front lt 1 lc rgb'cyan'  lw 1.5
		set arrow 18 from 0.65, 0.606 to 0.35, 0.606 nohead front lt 1 lc rgb'cyan'  lw 1.5
		set arrow 19 from 0.60, 0.693 to 0.40, 0.693 nohead front lt 1 lc rgb'cyan'  lw 1.5
		set arrow 20 from 0.55, 0.779 to 0.45, 0.779 nohead front lt 1 lc rgb'cyan'  lw 1.5
		set arrow 21 from 0.50, 0.866 to 0,0 nohead front linestyle 1
		set arrow 22 from 0.05, 0.0866 to 0.1,0 nohead front lt 1 lc rgb'cyan'  lw 1.5
		set arrow 23 from 0.10, 0.173 to 0.2,0 nohead front lt 1 lc rgb'cyan'  lw 1.5
		set arrow 24 from 0.15, 0.260 to 0.3,0 nohead front lt 1 lc rgb'cyan'  lw 1.5
		set arrow 25 from 0.20, 0.346 to 0.4,0 nohead front lt 1 lc rgb'cyan'  lw 1.5
		set arrow 26 from 0.25, 0.433 to 0.5,0 nohead front lt 1 lc rgb'cyan'  lw 1.5
		set arrow 27 from 0.30, 0.520 to 0.6,0 nohead front lt 1 lc rgb'cyan'  lw 1.5
		set arrow 28 from 0.35, 0.606 to 0.7,0 nohead front lt 1 lc rgb'cyan'  lw 1.5
		set arrow 29 from 0.40, 0.693 to 0.8,0 nohead front lt 1 lc rgb'cyan'  lw 1.5
		set arrow 30 from 0.45, 0.779 to 0.9,0 nohead front lt 1 lc rgb'cyan'  lw 1.5
		plot [0:1] [-0.001:1] "-" u \
		(($1+2*$2)/(2*($1+(1.-$1-$2)+$2))):\
		(sqrt(3)*$1/(2*($1+(1.-$1-$2)+$2))):\
		3 notitle w p palette pt 13 ps 1.6'''
	for line in file(datfname):
		vals=map(float,line.split())
		if vals[0]+vals[1]<=1:
			print >>gp, vals[0], vals[1], vals[2]
	print >>gp, 'end'
	gp.close()
	os.system('convert -density 400 -alpha Opaque '+plotname+'.eps '+plotname+'.png')
    	if save_eps==False:
    		os.remove(plotname+'.eps')

#plot "<awk '{print ((1.-$1-$2)+2*$2)/(2*((1.-$1-$2)+$1+$2)), sqrt(3)*(1.-$1-$2)/(2*((1.-$1-$2)+$1+$2)), $3}' alldata.txt" w p palette pt 13

















