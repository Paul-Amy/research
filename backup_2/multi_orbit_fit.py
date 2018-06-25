import math as ma
import scipy as sp
import numpy as np
import files as fi
import os
import itertools
import scipy.stats
from scipy import optimize
import random
from datetime import datetime
import re

niter = 0
#NEMO parameters
pot = "mpn"
potpars = "0,5.0,0.26,329751.696,0.33,85024.6529,114.0,1.0,12.0"
orbsteps = 5000
orbtimestep = 0.000016

#Chi-squared parameters

nparams = 5

os.system("touch orbit_var_data")
opt_output = open("orbit_var_data", "a+")

def MakeOrbit(x):
  os.system("touch bdev")
  os.system("touch vdev")
  os.system("touch rdev")
  bdev = open("bdev","r+")
  vdev = open("vdev","r+")
  rdev = open("rdev","r+")
  
  data = fi.read_file("orbit.input", " ")
  l_in = data[:,0]
  b_in = data[:,1]
  r_in = data[:,2]
  vgsr_in = data[:,3]

  npoints = len(l_in)
  ndata = 3*npoints

  b, r, vx, vy, vz = x
  deg2rad = np.pi/180.0
  rad2deg = 180.0/np.pi
  l = 47
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
  
  db = list(itertools.repeat(berror,len(l1)))
  dvgsr = list(itertools.repeat(vgsrerror,len(l1)))
  dr = list(itertools.repeat(rerror,len(l1)))

  os.system("touch orbit.1.fit")
  params1=open('orbit.1.fit','r+')
  j=0
  for j in range(len(x1)):
		  print >>params1, l1[j], b1[j], r1[j], vgsr1[j]

  params1.close()

  os.system("rm orbit.1.tab")

  obsdata = np.genfromtxt("orbit.input")
  testdata1 = np.genfromtxt("orbit.1.fit")
  
  # To do the chi-square test, we first need to search the orbit data for two 
  #points on opposite sides of each of the observed points. We'll do a 
  #single-variable search in l. First, we make the lists and indices.

  lindex = 0 
  bindex = 0
  vgsrindex = 0
  rindex = 0
  lsearch = []
  bsearch = []
  vgsrsearch = []
  rsearch = []

  #This searches through the test orbit by l and gets the two values of l that are 
  #closest to and on the opposite side of the data point.

  while lindex < npoints:
    lsub = np.subtract(testdata1[:,0],obsdata[lindex,0])
    lsubplus =  [m for m in lsub if m > 0]
    lsubminus = [n for n in lsub if n < 0]
    lminplus = np.amin(lsubplus)
    lminminus = np.amax(lsubminus)

    lminus = np.add(lminminus,obsdata[lindex,0])
    lplus = np.add(lminplus,obsdata[lindex,0])
    lsearch.append(lminus)
    lsearch.append(lplus)
    lindex = lindex + 1

  #Write the list of l values to an array
  larray = np.asarray(lsearch)

  #This searches through the test orbit for the b values corresponding to the 
  #closest l values from above.

  while bindex < 2 * npoints:
    bminustup = testdata1[np.where((testdata1[:,0] - larray[bindex]) == 0)]
    bplustup = testdata1[np.where((testdata1[:,0] - larray[bindex + 1]) == 0)]
    bplus = bplustup[0,1]
    bminus = bminustup[0,1]
    bsearch.append(bminus)
    bsearch.append(bplus)
    bindex = bindex + 2
    
  #Ditto, except for vgsr.

  while vgsrindex < 2 * npoints:
    vgsrminustup = testdata1[np.where((testdata1[:,0] - larray[vgsrindex]) == 0)]
    vgsrplustup = testdata1[np.where((testdata1[:,0] - larray[vgsrindex + 1]) == 0)]
    vgsrplus = vgsrplustup[0,3]
    vgsrminus = vgsrminustup[0,3]
    vgsrsearch.append(vgsrminus)
    vgsrsearch.append(vgsrplus)
    vgsrindex = vgsrindex + 2
    
  ##One more time, for r.

  while rindex < 2 * npoints:
    rplustup = testdata1[np.where((testdata1[:,0] - larray[rindex]) == 0)]
    rminustup = testdata1[np.where((testdata1[:,0] - larray[rindex + 1]) == 0)]
    rplus = rplustup[0,2]
    rminus = rminustup[0,2]
    rsearch.append(rminus)
    rsearch.append(rplus)
    rindex = rindex + 2
    
  os.system("rm orbit.1.fit")


  #Now write the fit parameter lists to an array:

  barray = np.asarray(bsearch)
  vgsrarray = np.asarray(vgsrsearch)
  rarray = np.asarray(rsearch)
  lindex2 = 0
  lindex3 = 0
  lindex4 = 0
  bindex2 = 0
  vgsrindex2 = 0
  rindex2 = 0
  lcoll = []
  lcoll = obsdata[:,0]
  lcol = np.array(lcoll)
  bmodellist = []
  vgsrmodellist = []
  rmodellist = []
  
  #We begin the chi-squared part. We first interpolate the orbit using the fit 
  #parameters.

  while bindex2 < 2 * npoints:
    bintnum = np.subtract(barray[bindex2+1],barray[bindex2])
    bintdenom = np.subtract(larray[bindex2+1],larray[bindex2])
    bintsub = np.subtract(lcoll[lindex2],larray[bindex2])
    bintquot = np.divide(bintnum,bintdenom)
    bintprod = np.multiply(bintquot,bintsub)
    bmodel = np.add(bintprod,barray[bindex2])
    bmodellist.append(bmodel)
    bindex2 = bindex2 + 2
    lindex2 = lindex2 + 1

  while vgsrindex2 < 2 * npoints:
    vgsrintnum = np.subtract(vgsrarray[vgsrindex2+1],vgsrarray[vgsrindex2])
    vgsrintdenom = np.subtract(larray[vgsrindex2+1],larray[vgsrindex2])
    vgsrintsub = np.subtract(lcol[lindex3],larray[vgsrindex2])
    vgsrintquot = np.divide(vgsrintnum,vgsrintdenom)
    vgsrintprod = np.multiply(vgsrintquot,vgsrintsub)
    vgsrmodel = np.add(vgsrintprod,vgsrarray[vgsrindex2])
    vgsrmodellist.append(vgsrmodel)
    vgsrindex2 = vgsrindex2 + 2
    lindex3 = lindex3 + 1
    
  while rindex2 < 2 * npoints:
    rintnum = np.subtract(rarray[rindex2+1],rarray[rindex2])
    rintdenom = np.subtract(larray[rindex2+1],larray[rindex2])
    rintsub = np.subtract(lcol[lindex4],larray[rindex2])
    rintquot = np.divide(rintnum,rintdenom)
    rintprod = np.multiply(rintquot,rintsub)
    rmodel = np.add(rintprod,rarray[rindex2])
    rmodellist.append(rmodel)
    rindex2 = rindex2 + 2
    lindex4 = lindex4 + 1

  bmodelarray = np.array(bmodellist)
  vgsrmodelarray = np.array(vgsrmodellist)
  rmodelarray = np.array(rmodellist)
  
  #Now, let's calculate the chi-squareds for each fit variable. Each calculated 
  #chi-squared value is fed into an array, which is then summed to get a final 
  #chi-square for the variable.

  chibindex = 0
  chivgsrindex = 0
  chirindex = 0

  chibind = np.empty([npoints,1])
  chivgsrind = np.empty([npoints,1])
  chirind = np.empty([npoints,1])
  
  while chibindex < npoints:
    chibnum = np.subtract(bmodelarray[chibindex],obsdata[chibindex,1])
    chibdenom = berror
    chibfrac = np.divide(chibnum,chibdenom)
    chibind[chibindex] = np.power(chibfrac,2)
    bdev.write(str(chibnum) + "\n")
    #bdev.write(str(obsdata[chibindex,0]) + "\n")
    chibindex = chibindex + 1
    
  chisqb = np.sum(chibind)
  
  while chivgsrindex < npoints:
    chivgsrnum = np.subtract(vgsrmodelarray[chivgsrindex],obsdata[chivgsrindex,3])
    chivgsrdenom = vgsrerror
    chivgsrfrac = np.divide(chivgsrnum,chivgsrdenom)
    chivgsrind[chivgsrindex] = np.power(chivgsrfrac,2)
    vdev.write(str(chivgsrnum) + "\n")
    chivgsrindex = chivgsrindex + 1
  
  chisqvgsr = np.sum(chivgsrind)
  
  while chirindex < npoints:
    chirnum = np.subtract(rmodelarray[chirindex],obsdata[chirindex,2])
    chirdenom = rerror
    chirfrac = np.divide(chirnum,chirdenom)
    chirind[chirindex] = np.power(chirfrac,2)
    rdev.write(str(chirnum) + "\n")
    chirindex = chirindex + 1

  chisqr = np.sum(chirind)

  #Now that we have the chi-squareds for the three fit variables, we combine them
  #into a goodness of fit value for the stream as a whole:
  eta = float(ndata - nparams - 1)
  chisqstrcoeff = float(1 / eta)
  chisqsum = chisqb + chisqvgsr + chisqr
  chisqstr = chisqstrcoeff * chisqsum
  print chisqstr
  return chisqstr
  bdev.close()
  vdev.close()
  rdev.close()
 
while niter < 100:
  chisqlist = []
  x0 = np.asarray((42,16,-100,100,0))
  berror = 1
  vgsrerror = 15
  rerror = 1
  #First, we need to generate the orbit.input file for the first optimization:
  rawdata = fi.read_file("hyllus_pm2_14to18_140to220_6stars_021618.csv", ",")
  lraw=rawdata[:,2]
  braw=rawdata[:,3]
  rstart=rawdata[:,4]
  vstart = rawdata[:,5]
  randvlist = []
  randrlist = []
  randv_low_lim = np.subtract(vstart,10)
  randv_upper_lim = np.add(vstart,10)
  randr_low_lim = np.subtract(rstart,1)
  randr_upper_lim = np.add(rstart,1)
  randviter = 0
  randriter = 0
  #Create random vgsr values for each datapoint by choosing randomly within +/- 10 km/s of each point
  while randviter < len(lraw): 
    randv = random.uniform(randv_low_lim[randviter],randv_upper_lim[randviter])
    randvlist.append(randv)
    randviter = randviter + 1
  #Similarly in r, choose randomly within +/- 1 kpc of each point
  while randriter < len(lraw): 
    randr = random.uniform(randr_low_lim[randriter],randr_upper_lim[randriter])
    randrlist.append(randr)
    randriter = randriter + 1
  #Create arrays of the random values and create the orbit.input file for the optimization in NEMO
  rraw = np.array(randrlist)
  vgsrraw = np.array(randvlist)
  os.system("touch orbit.input")
  inputfile=open('orbit.input','r+')
  j=0
  for j in range(len(lraw)):
    print >>inputfile, lraw[j], braw[j], rraw[j], vgsrraw[j]
  inputfile.close()
  #Now that we've created the orbit.input file, we can perform the first optimization.
  x0 = [42,16,-100,100,0]
  out1 = optimize.fmin_cg(MakeOrbit, x0, gtol = 1e-05, epsilon = 1e-02)
  os.system("rm rdev vdev bdev")
  MakeOrbit(out1)
  #Here we read in the deviation files from the single run of MakeOrbit using the output of the first optimization. This allows us to find the standard deviations of b, vgsr, and r:
  data1 = fi.read_file("bdev")
  data2 = fi.read_file("vdev")
  data3 = fi.read_file("rdev")
  b = data1[:]
  v = data2[:]
  r = data3[:]
  Ndev = len(b)
  bsq = np.power(b,2)
  bquot = np.divide(bsq,Ndev)
  bsum = np.sum(bquot)
  berror = np.sqrt(bsum)
  vsq = np.power(v,2)
  vquot = np.divide(vsq,Ndev)
  vsum = np.sum(vquot)
  verror = np.sqrt(vsum)
  rsq = np.power(r,2)
  rquot = np.divide(rsq,Ndev)
  rsum = np.sum(rquot)
  rerror = np.sqrt(rsum)
  chisq1 = MakeOrbit(out1)
  print chisq1
  chisqlist.append(chisq1)
  print("FIRST OPTIMIZATION COMPLETED")
  #Repeat the optimization with new errors and the output of the previous one:
  out2 = optimize.fmin_cg(MakeOrbit, out1, gtol = 1e-05, epsilon = 1e-02)
  os.system("rm rdev vdev bdev")
  MakeOrbit(out2)
  #New errors from 2nd optimization:
  data1 = fi.read_file("bdev")
  data2 = fi.read_file("vdev")
  data3 = fi.read_file("rdev")
  b = data1[:]
  v = data2[:]
  r = data3[:]
  Ndev = len(b)
  bsq = np.power(b,2)
  bquot = np.divide(bsq,Ndev)
  bsum = np.sum(bquot)
  berror = np.sqrt(bsum)
  vsq = np.power(v,2)
  vquot = np.divide(vsq,Ndev)
  vsum = np.sum(vquot)
  verror = np.sqrt(vsum)
  rsq = np.power(r,2)
  rquot = np.divide(rsq,Ndev)
  rsum = np.sum(rquot)
  rerror = np.sqrt(rsum)
  chisq2 = MakeOrbit(out2)
  print chisq2
  chisqlist.append(chisq2)
  chisqdiff = np.subtract(chisq2,chisq1)
  chisq_abs = np.absolute(chisqdiff)
  if chisq_abs > 0.0001:
    print("SECOND OPTIMIZATION COMPLETED")
    out3 = optimize.fmin_cg(MakeOrbit, out2, gtol = 1e-05, epsilon = 1e-02)
    os.system("rm rdev vdev bdev")
    MakeOrbit(out3)
    data1 = fi.read_file("bdev")
    data2 = fi.read_file("vdev")
    data3 = fi.read_file("rdev")
    b = data1[:]
    v = data2[:]
    r = data3[:]
    Ndev = len(b)
    bsq = np.power(b,2)
    bquot = np.divide(bsq,Ndev)
    bsum = np.sum(bquot)
    berror = np.sqrt(bsum)
    vsq = np.power(v,2)
    vquot = np.divide(vsq,Ndev)
    vsum = np.sum(vquot)
    verror = np.sqrt(vsum)
    rsq = np.power(r,2)
    rquot = np.divide(rsq,Ndev)
    rsum = np.sum(rquot)
    rerror = np.sqrt(rsum)
    chisq3 = MakeOrbit(out3)
    print chisq3
    chisqlist.append(chisq3)
    chisqdiff2 = np.subtract(chisq3,chisq2)
    chisq_abs2 = np.absolute(chisqdiff2)
    if chisq_abs2 > 0.0001:
      out4 = optimize.fmin_cg(MakeOrbit, out3, gtol = 1e-05, epsilon = 1e-02)
      os.system("rm rdev vdev bdev")
      MakeOrbit(out4)
      data1 = fi.read_file("bdev")
      data2 = fi.read_file("vdev")
      data3 = fi.read_file("rdev")
      b = data1[:]
      v = data2[:]
      r = data3[:]
      Ndev = len(b)
      bsq = np.power(b,2)
      bquot = np.divide(bsq,Ndev)
      bsum = np.sum(bquot)
      berror = np.sqrt(bsum)
      vsq = np.power(v,2)
      vquot = np.divide(vsq,Ndev)
      vsum = np.sum(vquot)
      verror = np.sqrt(vsum)
      rsq = np.power(r,2)
      rquot = np.divide(rsq,Ndev)
      rsum = np.sum(rquot)
      rerror = np.sqrt(rsum)
      chisq4 = MakeOrbit(out4)
      print chisq4
      chisqlist.append(chisq4)
      chisqdiff3 = np.subtract(chisq4,chisq3)
      chisq_abs3 = np.absolute(chisqdiff3)
      print chisq_abs3
      if chisq_abs3 > 0.0001:
	out5 = optimize.fmin_cg(MakeOrbit, out4, gtol = 1e-05, epsilon = 1e-02)
	os.system("rm rdev vdev bdev")
	MakeOrbit(out5)
	data1 = fi.read_file("bdev")
	data2 = fi.read_file("vdev")
	data3 = fi.read_file("rdev")
	b = data1[:]
	v = data2[:]
	r = data3[:]
	Ndev = len(b)
	bsq = np.power(b,2)
	bquot = np.divide(bsq,Ndev)
	bsum = np.sum(bquot)
	berror = np.sqrt(bsum)
	vsq = np.power(v,2)
	vquot = np.divide(vsq,Ndev)
	vsum = np.sum(vquot)
	verror = np.sqrt(vsum)
	rsq = np.power(r,2)
	rquot = np.divide(rsq,Ndev)
	rsum = np.sum(rquot)
	rerror = np.sqrt(rsum)
	chisq5 = MakeOrbit(out5)
	print chisq5
	chisqlist.append(chisq5)
	chisqdiff4 = np.subtract(chisq5,chisq4)
	chisq_abs4 = np.absolute(chisqdiff4)
	print chisq_abs4
	if chisq_abs4 > 0.0001:
	  print("DIFFERENCE NOT LESS THAN TOLERANCE AFTER FIFTH OPTIMIZATION. STOP CURRENT AND RUN NEXT ITERATION.")
	  niter = niter + 1
	  os.system("rm orbit.input")
	else:
	  print("DIFFERENCE LESS THAN TOLERANCE ON FIFTH OPTIMIZATION. NEXT ITERATION.")
	  chisqout5 = MakeOrbit(out5)
	  opt_output.write(str(out5) + "," + str(chisqout5) + "\n")
	  niter = niter + 1
	  os.system("rm orbit.input")
      else:
	print("DIFFERENCE LESS THAN TOERANCE ON FOURTH OPTIMIZATION. NEXT ITERATION.")
	chisqout4 = MakeOrbit(out4)
	opt_output.write(str(out4) + "," + str(chisqout4) +  "\n")
	niter = niter + 1
	os.system("rm orbit.input")
    else:
      print("DIFFERENCE LESS THAN TOLERANCE ON THIRD OPTIMIZATION. NEXT ITERATION.")
      chisqout3 = MakeOrbit(out3)
      opt_output.write(str(out3) + "," + str(chisqout3) +  "\n")
      niter = niter + 1
      os.system("rm orbit.input")
  else:
    print("DIFFERENCE LESS THAN TOLERANCE ON SECOND OPTIMIZATION. NEXT ITERATION.")
    chisqout2 = MakeOrbit(out2)
    opt_output.write(str(out2) + "," + str(chisqout2) +  "\n")
    niter = niter + 1
    os.system("rm orbit.input")
  #while chisqlist[index] - chisqlist[index-1] > 0.00005:
    #out = optimize.fmin_cg(MakeOrbit, output_list[index], gtol = 1e-05, epsilon = 1e-02)