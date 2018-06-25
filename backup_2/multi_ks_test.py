import files as fi
import numpy as np
import scipy as sc
import matplotlib.pyplot as py
import matplotlib.mlab as mlab
import scipy.stats as stats
from pylab import *
import random

	
def Vgsr_sim(vgsr1,dist1,deltab,vgsr2,dist2):


	'''
	#UNCOMMENT FOR SINGLE RUN
	N=len(dist1)

	v=[]
	mu, sigma = 0, 120 # mean and standard deviation
	while (N>0):
		test = np.random.normal(mu, sigma, N)
		for m in range(len(test)):
			if (test[m]<300 and test[m]>-300): 
				v.append(test[m])
				N=N-1
			else: np.delete(test, m)
			
	N=len(dist1)
	'''

	
	

	#Hermus Stream stars distances 10 < D < 25
	#now setting it up to run M number of times and save the best p-vales for each run to a list
	bestdist=[]
	bestv=[]	
	low_p=1.5
	count=0
	pvalues=[]	
	Best_p_values=[]
	Best_dist_range=[]
	Best_dist_values=[]
	Best_v_values=[]
	
	
	#Number of runs:M
	M=15000
	r=0
	while (r<M):
		N=len(dist1)

		v=[]
		
		mu, sigma = 0, 120 # mean and standard deviation
		while (N>0):
			test = np.random.normal(mu, sigma, N)
			for m in range(len(test)):
				if (test[m]<300 and test[m]>-300): 
					v.append(test[m])
					N=N-1
			else: np.delete(test, m)
		

		#v = np.random.choice(vgsr2, N,replace=False)
		
		low_p=1.0
		count=0
		for i in range(13,27):
			for j in range(i+2,29):
				newdist=[]
				newv=[]
				for k in range(len(dist1)):
					if dist1[k]>i and dist1[k]<j:
						newdist.append(dist1[k])
						newv.append(v[k])
						#newv.append(vgsr1[k])
				D2,p2=sc.stats.kstest(newv, 'norm', args=(0, 120))
				#print p2
				if (p2<low_p): 
					low_p=p2
					bestdist=newdist
					bestv=newv
					bestmin=i
					bestmax=j
				count=count+1

		pvalues.append(low_p)
		
		r=r+1
		print r

	print low_p
	print count
	print len(bestdist)
	print bestmin, bestmax
	#print pvalues

		
		
	'''
	#print low_p
	#print count
	#print len(bestdist)
	#print bestmin, bestmax
	#print pvalues
	'''
	p005=0.0
	p004=0.0
	p003=0.0
	p002=0.0
	p001=0.0
	for y in range(len(pvalues)):
		if pvalues[y]<0.005:
			p005=p005+1
			if pvalues[y]<0.004:
				p004=p004+1
				if pvalues[y]<0.003:
					p003=p003+1
					if pvalues[y]<0.002:
						p002=p002+1
						if pvalues[y]<0.0013:
							p001=p001+1
	
	print p005, p004, p003, p002, p001			
	
	
if __name__ == "__main__": 
	#data1=fi.read_file("HAC_BHB_mid_sim.csv", ",")
	data1=fi.read_file("hyllus_pm2ra_111617.csv", ",") #Original for the paper
	#data1=fi.read_file("Hermus_051016_3to6.csv", ",")
	#data1=fi.read_file("Hermus_lgt40.csv", ",")
	#data1=fi.read_file("Hermus_off_lgt40.csv", ",")
	data2=fi.read_file("hyllus_on_off.csv", ",")

	
	#vgsr1=data1[:,23]
	#dist1=data1[:,25]

	deltab=data1[:,3]
	vgsr1=data1[:,4]
	dist1=data1[:,5]
	
	vgsr2=data2[:,4]
	dist2=data2[:,5]

	Vgsr_sim(vgsr1,dist1,deltab,vgsr2,dist2)