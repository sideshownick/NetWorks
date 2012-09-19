import os

def gp_init(filename='newgraph',xlabel='time',ylabel='Proportional uptake',args='notitle w p pt 7',extras=''):
	gp=os.popen('gnuplot -persist','w')
	print >>gp, 'set term postscript enhanced color eps 30'
	print >>gp, 'set out "'+filename+'.eps"'
	print >>gp, extras
	print >>gp, 'set xlabel "'+xlabel+'"; set ylabel "'+ylabel+'"; p "-" ', args
	return gp
	
def gp_plot(gp,data):
	#for line in data:
	#	print >>gp, line[0], line[1]
	print >>gp, data[0], data[1]
	gp.flush()
	
def gp_newline(gp):
	print >>gp, '\n'
	gp.flush()
	
def gp_end(gp, filename='newgraph'):
	print >>gp, 'end'
	gp.close()
	os.system('convert -density 200 -alpha Opaque '+filename+'.eps '+filename+'.png')
	
def get_cmap():
    from matplotlib.colors import LinearSegmentedColormap
    '''
    Label the 3 elements in each row in the cdict entry for a given color as
    (x, y0, y1).  Then for values of x between x[i] and x[i+1] the color
    value is interpolated between y1[i] and y0[i+1].
    '''
    cdict = {'red':   ((0.0, 0.0, 0.0),
                       (0.5, 0.0, 0.1),
                       (1.0, 1.0, 1.0)),

             'green': ((0.0, 0.0, 0.0),
                       (1.0, 0.0, 0.0)),

             'blue':  ((0.0, 0.0, 1.0),
                       (0.5, 0.1, 0.0),
                       (1.0, 0.0, 0.0))
             }

    colormap = LinearSegmentedColormap('newmap1', cdict)
    return colormap
