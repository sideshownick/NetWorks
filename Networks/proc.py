import os, scipy
from parameters import *

datfname='alldata.txt'
figname='fig_new'
figformat='png'
save_eps=True
xcol=1
ycol=2
zcol=3
zlabel='Average Uptake'
par0='alpha'
par1='beta'
par3='gamma'
wlabel=par0
xlabel=par1
ylabel=par2
title=''
extras=''
param_key='({/Symbol a, b, g})'
fontsize=10
pointsize=1.8

def process():
    data={}
    contents=os.listdir('FinishedResults')
    for filename in contents:
	##par1,par2=filename.replace('.txt','').split('_')
	for line in file('FinishedResults/'+filename):
	    if len(line)>0:
	    	line=line.split()
	    	#rounder0=len(line[0]); rounder1=len(line[1])
		#line=map(float, line)
	    	#line[0]=round(line[0],rounder0); line[1]=round(line[1],rounder1)
		data[line[0],line[1]]=line

    fout=open(datfname,'w')		
    for p1 in scipy.arange(par1min,par1max,par1step):
	for p2 in scipy.arange(par2min,par2max,par2step):
		print >>fout, p1, p2,
		if (str(p1),str(p2)) in data:
		    for val in data[str(p1),str(p2)][2:]:
			print >>fout, val,
		else:
		    for i in range(len(line)-2):
			print >>fout, 0.0,
		print >>fout, ''	
    fout.close()

def plot():
    gp=os.popen('gnuplot','w')
    print >>gp, '''set terminal postscript eps size 600/72.,300/72. enhanced color font '''+str(fontsize*2)+'''
    		   set palette maxcolors 25
    		   set size square; set view map
    		   set palette rgbformulae 30,31,32 negative
    		   set out "'''+figname+'''.eps"
    		   set title "'''+title+'''"
    		   set xlabel "'''+ylabel+'''"
    		   set ylabel "'''+xlabel+'''"
    		   set cblabel "'''+zlabel+'''"
    		   splot "'''+datfname+'''" u ($%d):($%d):($%d) notitle w image'''%(ycol,xcol,zcol)
    gp.close()
    os.system('convert -density 1200 -alpha Opaque -geometry 600 '+figname+'.eps '+figname+'.'+figformat)
    if save_eps==False:
    	os.remove(figname+'.eps')


def triangle_plot(plotname='ternary_plot'):
	gp=os.popen('gnuplot','w')
	print >>gp, '''
		set terminal postscript eps size 600/72.,300/72. enhanced color font '''+str(fontsize*2)+'''
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
		set cbrange[0:1]
		set label 1 "'''+wlabel+''' = 0"   at 0.62,0.75 rotate by -56
		set label 2 "'''+xlabel+''' = 0"   at 0.2,-0.04	 
		set label 3 "'''+ylabel+''' = 0"   at 0.05,0.175 rotate by 56
		set label 4 "(1,0,0)" at -0.05, -0.03 center
		set label 5 '(0,1,0)' at  0.5,   0.9  center
		set label 6 '(0,0,1)' at  1.05, -0.03 center
		set palette rgbformulae 30,31,32 negative
		set palette maxcolors 25
		set colorbox horizontal
		set colorbox user origin 0.1,0.9 size 0.8,0.05
		set title "'''+zlabel+'''" 0.0,1.0
		set label "{/='''+str(fontsize*2)+''' parameters: '''+param_key+'''}" at screen 0.1,0.8
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
		3 notitle w p palette pt 13 ps %f'''%pointsize
	for line in file(datfname):
		vals=map(float,line.split())
		if vals[0]+vals[1]<=1:
			print >>gp, vals[0], vals[1], vals[2]
	print >>gp, 'end'
	gp.close()
	os.system('convert -density 1200 -alpha Opaque -geometry 600 '+plotname+'.eps '+plotname+'.png')
    	if save_eps==False:
    		os.remove(plotname+'.eps')

#plot "<awk '{print ((1.-$1-$2)+2*$2)/(2*((1.-$1-$2)+$1+$2)), sqrt(3)*(1.-$1-$2)/(2*((1.-$1-$2)+$1+$2)), $3}' alldata.txt" w p palette pt 13

















