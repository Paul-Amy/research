import math as ma
import scipy as sp
import numpy as np
import files as fi
import os
from scipy import optimize

#THIS PROGRAM DOES THE STUPID FUCKING LIKELIHOOD METHOD THAT SOME REFEREE PULLED OUT OF HIS ASS AND THUS I HAD TO CHECK HIS BULLSHIT METHOD.

#NEMO parameters
pot = "mpn"
potpars = "0,5.0,0.26,329751.696,0.33,85024.6529,114.0,1.0,12.0"
orbsteps = 5000
orbtimestep = 0.000016

#Chi-squared parameters
lerror = 1
berror = 1 #0.52
vgsrerror = 24.01 #10.12
rerror = 1.47 #0.84
nparams = 5

def fit_params(lraw,braw,rraw,vgsrraw):
	os.system("touch orbit.input")
	inputfile=open('orbit.input','r+')
	j=0
	for j in range(len(lraw)):
		print >>inputfile, lraw[j], braw[j], vgsrraw[j], rraw[j]

	inputfile.close()

if __name__ == "__main__": 	
	rawdata=fi.read_file("hermus_pm2_11stars_021017.csv", ",")
	lraw=rawdata[:,2] #pulls out a single column (note: i=0,1,2,3...)
	braw=rawdata[:,3]
	rraw=rawdata[:,4]
	vgsrraw=rawdata[:,5]
	fit_params(lraw,braw,rraw,vgsrraw)

def chi_sq(x):
  b, r, vx, vy, vz = x
  deg2rad = np.pi/180.0
  rad2deg = 180.0/np.pi
  l = 45
  sinlinit = np.sin(l*deg2rad)
  coslinit = np.cos(l*deg2rad)
  sinbinit = np.sin(b*deg2rad)
  cosbinit = np.cos(b*deg2rad)
  xinit = r*coslinit*cosbinit - 8.0
  yinit = r*sinlinit*cosbinit
  zinit = r*sinbinit
  vxinit = vx
  vyinit = vy
  vzinit = vz
  
  #Call NEMO functions to make first orbit, integrate it back and forwards in 
  #time, convert the orbit files to snapshots, and stack the snapshots together 
  #before printing them out in ASCII form.
  
  os.system("mkorbit out=orbit1.temp x=" + str(xinit) + " y=" + str(yinit) + " z=" + str(zinit) + " vx=" + str(vxinit) + " vy=" + str(vyinit) + " vz=" + str(vzinit) + " potname=" + str(pot) + 
" potpars=" + str(potpars))
  os.system("orbint in=orbit1.temp out=orbit1.for.temp nsteps=" + str(orbsteps) + " dt=" + str(orbtimestep) + " potname=" + str(pot) + " potpars=" + str(potpars))
  os.system("orbint in=orbit1.temp out=orbit1.back.temp nsteps=" + str(orbsteps) + " dt=-" + str(orbtimestep) + " potname=" + str(pot) + " potpars=" + str(potpars))
  os.system("otos in=orbit1.for.temp out=orbit.1.for.snap.temp")
  os.system("otos in=orbit1.back.temp out=orbit.1.back.snap.temp")
  os.system("snapstack in1=orbit.1.for.snap.temp in2=orbit.1.back.snap.temp out=orbit.1.total.snap.temp")
  os.system("snapprint in=orbit.1.total.snap.temp tab=orbit.1.tab csv=t")

  #Remove temporary orbit files, leaving just the ASCII file

  os.system("rm *.temp") 

  #Get the output data file, convert coordinates, and write to a new file

  data1 = fi.read_file("orbit.1.tab", ",")
  x1 = data1[:,0]
  y1 = data1[:,1]
  z1 = data1[:,2]
  vx1 = data1[:,3]
  vy1 = data1[:,4]
  vz1 = data1[:,5]

  e = 0
  a = 0
  xsol = np.add(x1,float(8))
  l1rad = np.arctan2(y1,xsol)
  l1 = np.multiply(l1rad,rad2deg)
  for e in range(len(l1)):
    if (l1[e] < 0):
      l1[e] = l1[e] + 360
  r1x = np.power(xsol,2)
  r1y = np.power(y1,2)
  r1z = np.power(z1,2)
  r1sum = np.add(r1x,r1y)
  r1sqrt = np.add(r1sum,r1z)
  r1 = np.sqrt(r1sqrt)
  b1arg = np.divide(z1,r1)
  b1rad = np.arcsin(b1arg)
  b1 = np.multiply(b1rad,rad2deg)
  vgsr1x = np.multiply(xsol,vx1)
  vgsr1y = np.multiply(y1,vy1)
  vgsr1z = np.multiply(z1,vz1)
  vgsr1numpart = np.add(vgsr1x,vgsr1y)
  vgsr1num = np.add(vgsr1numpart,vgsr1z)
  vgsr1 = np.divide(vgsr1num, r1)
  
  os.system("touch orbit.1.fit")
  
  params1=open('orbit.1.fit','r+')
  j=0
  for j in range(len(x1)):
		  print >>params1, l1[j], b1[j], vgsr1[j], r1[j]

  params1.close()

  os.system("rm orbit.1.tab")

  obsdata = np.genfromtxt("orbit.input")
  testdata1 = np.genfromtxt("orbit.1.fit")
  os.system("rm orbit.1.fit")
 
  stoparr = testdata1[:,0]
  stop = len(stoparr)
  runsarr = obsdata[:,0]
  npoints = len(runsarr)
  nruns = 0
  ldenomsq = np.power(lerror,2)
  bdenomsq = np.power(berror,2)
  vdenomsq = np.power(vgsrerror,2)
  rdenomsq = np.power(rerror,2)
  ldenom = 2*ldenomsq
  bdenom = 2*bdenomsq 
  vdenom = 2*vdenomsq
  rdenom = 2*rdenomsq
  chisqlist = []
  while nruns < npoints:
    sum_index = 0
    sumlist = []
    while sum_index < stop:
      arglist = []
      lsub = np.subtract(testdata1[sum_index,0],obsdata[nruns,0])
      lsubsq = np.power(lsub,2)
      lsubquot = np.divide(lsubsq,ldenom)
      arglist.append(lsubquot)

      bsub = np.subtract(testdata1[sum_index,1],obsdata[nruns,1])
      bsubsq = np.power(bsub,2)
      bsubquot = np.divide(bsubsq,bdenom)
      arglist.append(bsubquot)

      vsub = np.subtract(testdata1[sum_index,2],obsdata[nruns,2])
      vsubsq = np.power(vsub,2)
      vsubquot = np.divide(vsubsq,vdenom)
      arglist.append(vsubquot)

      rsub = np.subtract(testdata1[sum_index,3],obsdata[nruns,3])
      rsubsq = np.power(rsub,2)
      rsubquot = np.divide(rsubsq,rdenom)
      arglist.append(rsubquot)
      
      argarr = np.array(arglist)
      argsum = np.sum(argarr)
      argval = np.multiply(argsum,-0.5)
      argexp = np.exp(argval)
      sumlist.append(argexp)
      sum_index = sum_index + 1
    
    sumarr = np.array(sumlist)

    sum_res = np.sum(sumarr)
    chisq = np.log(sum_res)
    chisqlist.append(chisq)
    nruns = nruns + 1
  chisqarr = np.array(chisqlist)
  chisqtot = np.sum(chisqarr)
  chisqfin = np.multiply(chisqtot,-1)
  print chisqfin
  return chisqfin




x0 = np.asarray((46.91,12.40,-95.99,137.64,66.84))
res1 = optimize.fmin_cg(chi_sq, x0, gtol = 1e-05, epsilon = 1e-02)
print res1
#chi_sq(x0)