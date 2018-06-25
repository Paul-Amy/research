import files as fi
import numpy as np
import scipy as sc
import matplotlib.pyplot as py
import matplotlib.patches as mp
from pylab import *
from numpy import random

def Hermus_XYZ(X2,Y2,Z2,X3raw,Y3raw,Z3raw,X4,Y4,Z4,X5,Y5,Z5):
	#Create XYZ positional plots for Hermus results
	#Inputs:X[:,0], Y[:,1], Z[:,2]
	#Files: hermustest27.forward.0.25B.params, hermustest27.back.0.25B.params
	#Saved as:
	sample_list = []
	i = 0
	while i < len(X3raw):
	  test_val=np.random.random_sample()
	  if test_val < 0.1: 
	    sample_list.append(data3[i,:])
	    i = i + 1
	  else:
	    i = i + 1
	samp_arr = np.array(sample_list)
	
	X3 = samp_arr[:,0]
	Y3 = samp_arr[:,1]
	Z3 = samp_arr[:,2]
	py.subplots_adjust(wspace=0.3, hspace=0.3)	
	ax1=py.subplot(221)
	ax2=py.subplot(222)
	ax3=py.subplot(223)

	#ax1.scatter(X1,Z1, s=1)
	#ax2.scatter(Y1,Z1, s=1)
	#ax3.scatter(X1,Y1, s=1)

	#ax1.scatter(X2,Z2, s=12,edgecolors='none')
	#ax2.scatter(Y2,Z2, s=12,edgecolors='none')
	#ax3.scatter(X2,Y2, s=12,edgecolors='none')
	
	ax1.scatter(X3,Z3,s=0.1,c='k',marker=',',alpha=0.005)
	ax2.scatter(Y3,Z3,s=0.1,c='k',marker=',',alpha=0.005)
	ax3.scatter(X3,Y3,s=0.1,c='k',marker=',',alpha=0.005)
	
	ax1.plot(X5,Z5,'k',linewidth=1)
	ax2.plot(Y5,Z5,'k',linewidth=1)
	ax3.plot(X5,Y5,'k',linewidth=1)

	ax1.plot(X4,Z4,'k',linewidth=1)
	ax2.plot(Y4,Z4,'k',linewidth=1)
	ax3.plot(X4,Y4,'k',linewidth=1)
	

	ax1.axis([-16,16,-16,16])
	ax2.axis([-16,16,-16,16])
	ax3.axis([-16,16,-16,16])
	
	
	nbins = len(ax2.get_xticklabels()) 	
	#ax1.yaxis.set_major_locator(MaxNLocator(nbins+2))
	#ax2.yaxis.set_major_locator(MaxNLocator(nbins, prune='upper'))
	#ax3.yaxis.set_major_locator(MaxNLocator(nbins, prune='upper'))
	#setp(ax1.xaxis.get_ticklabels(), visible=False)
	#setp(ax2.yaxis.get_ticklabels(), visible=False)
	
	#ax1.legend()
	#ax2.legend()
	#ax3.legend()

	ax1.set_ylabel('Z (kpc)', fontsize=16)
	ax2.set_ylabel('Z (kpc)', fontsize=16)
	ax3.set_ylabel('Y (kpc)', fontsize=16)
	ax1.set_xlabel('X (kpc)', fontsize=16)
	ax2.set_xlabel('Y (kpc)', fontsize=16)
	ax3.set_xlabel('X (kpc)', fontsize=16)

	#ax1.legend(loc=4)
	#ax2.legend(loc=4)
	#ax3.legend(loc=4)
	
	py.savefig('50_orb_xyz_triple.pdf', format='pdf', dpi=600)

if __name__ == "__main__": 

	#Hermus forwrad and back orbit
	#16 stars that were used to fit the orbit that was in the submitted paper
	#data2=fi.read_file("Hermus_orbit_stars_16.csv", ",")
	
	#data3=fi.read_file("hermus3.back.250M.params", ",")
	#data4=fi.read_file("hermus3.forward.250M.params", ",")	

	#Hermus OLD Orbit using Orbital fitting
	#data3=fi.read_file("hermustest11.back.0.25B.params", ",")
	#data4=fi.read_file("hermustest11.forward.0.25B.params

	#Hermus FINAL Orbit using Orbital fitting (chisquared=1.614)
	#data3=fi.read_file("hermusfinal.back.0.25B.params", ",")
	#data4=fi.read_file("hermusfinal.forward.0.25B.params", ",")

	#Hermus FINAL Orbit using Orbital fitting (chisquared=1.606)
	#data3=fi.read_file("hermusfinal2.back.0.25B.params", ",")
	#data4=fi.read_file("hermusfinal2.forward.0.25B.params", ",")



	#13 Hermus stars used to fit this new orbit
	#data2=fi.read_file("Hermus_pm2_15stars.csv", ",")
	data2=fi.read_file("hermus_pm2_10stars_091616.csv", ",")

	#Hermus orbit fit using 13 stars within 2degrees of the Hermus 3rd order polynomial with b>40 (chisquared=1.297)
	#data3=fi.read_file("hermustest30.back.0.25B.params", ",")
	#data4=fi.read_file("hermustest30.forward.0.25B.params", ",")

	#data3=fi.read_file("hermustest31.back.0.25B.params", ",")
	#data4=fi.read_file("hermustest31.forward.0.25B.params", ",")

	#data3=fi.read_file("hermustest61.back.250M.params", ",")
	#data4=fi.read_file("hermustest61.forward.250M.params", ",")
		
	#Hermustest64 average orbit for 50 optimized runs
	data3=fi.read_file("50_orbits_vary_data.csv", ",")
	data4=fi.read_file("hermustest64.forward.100M.csv.params", ",")
	data5=fi.read_file("hermustest64.back.100M.csv.params",",")


	#X1=data1[:,0]
	#Y1=data1[:,1]
	#Z1=data1[:,2]

	l=data2[:,2]
	b=data2[:,3]
	r=data2[:,4]
		

	X2=r*np.cos(l*(np.pi/180.0))*np.cos(b*(np.pi/180.0))-8.0
	Y2=r*np.sin(l*(np.pi/180.0))*np.cos(b*(np.pi/180.0))
	Z2=r*sin(b*(np.pi/180.0))
	
	X3raw=data3[:,0]
	Y3raw=data3[:,1]
	Z3raw=data3[:,2]
	#sample_list = []

	#while i < len(X3raw):
	  #test_val=np.random.random_sample()
	  #if test_val < 0.2: 
	    #sample_list.append(data3[i,:])
	    #i = i + 1
	  #else:
	    #i = i + 1
	#samp_arr = np.array(sample_list)
	
	#X3 = samp_arr[:,0]
	#Y3 = samp_arr[:,1]
	#Z3 = samp_arr[:,2]
	#print X3
	#print len(X3raw)
	#print len(X3)
	X4=data4[:,0]
	Y4=data4[:,1]
	Z4=data4[:,2]
	
	X5=data5[:,0]
	Y5=data5[:,1]
	Z5=data5[:,2]

	Hermus_XYZ(X2,Y2,Z2,X3raw,Y3raw,Z3raw,X4,Y4,Z4,X5,Y5,Z5)