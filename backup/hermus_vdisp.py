import os
import scipy as sp
import numpy as np
import math as ma
import matplotlib.pyplot as py
import files as fi

#nbodyfile = raw_input("Enter nbody filename: ")
#orbfile = raw_input("Enter orbit filename: ")
#iterations = float(raw_input("How many files? "))

def vdisp(nbodyl,nbodyb,nbodyv,nbodyr,orbl,orbb,orbv,orbr):
  a = 0
  b = 0
  c = 0
  d = 0
  e = 0
  f = 0
  g = 0
  h = 0
  i = 0
  j = 0
  k = 0
  m = 0
  n = 0
  
  norbit = len(orbl)
  nnbody = len(nbodyl)
  orbarrlist = zip(orbl,orbb,orbv,orbr)
  orbarr = np.array(orbarrlist)
  lsearch = []
  vgsrsearch = []
  vgsrmodellist = []
  vgsrdevlist = []
  bsearch = []
  bmodellist = []
  bdevlist = []
  rsearch = []
  rmodellist = []
  rdevlist = []
  while i < nnbody:
    lsub = np.subtract(orbl[:],nbodyl[i])
    lsubplus =  [o for o in lsub if o > 0]
    lsubminus = [p for p in lsub if p < 0]
    lminplus = np.amin(lsubplus)
    lminminus = np.amax(lsubminus)
    lminus = np.add(lminminus,nbodyl[i])
    lplus = np.add(lminplus,nbodyl[i])
    lsearch.append(lminus)
    lsearch.append(lplus)
    i = i + 1
  larray = np.array(lsearch)
  while d < 2 * nnbody:
    bminustup = orbarr[np.where((orbarr[:,0] - larray[d]) == 0)]
    bplustup = orbarr[np.where((orbarr[:,0] - larray[d + 1]) == 0)]
    bplus = bplustup[0,1]
    bminus = bminustup[0,1]
    bsearch.append(bminus)
    bsearch.append(bplus)
    d = d + 2
  barray = np.array(bsearch)
  while a < 2 * nnbody:
    bintnum = np.subtract(barray[a+1],barray[a])
    bintdenom = np.subtract(larray[a+1],larray[a])
    bintsub = np.subtract(nbodyl[b],larray[a])
    bintquot = np.divide(bintnum,bintdenom)
    bintprod = np.multiply(bintquot,bintsub)
    bmodel = np.add(bintprod,barray[a])
    bmodellist.append(bmodel)
    a = a + 2
    b = b + 1
  bmodarray = np.array(bmodellist)
  while c < nnbody:
    bdev = np.subtract(bmodarray[c],nbodyb[c])
    bdevlist.append(bdev)
    c = c + 1
  bdevarr = np.array(bdevlist)
  #bdevmean = np.mean(bdevarr)
  #print bdevmean
  #bdevsub = np.subtract(bdevarr,bdevmean)
  bdevsq = np.power(bdevarr,2)
  bdevsum = np.sum(bdevsq)
  bdevquot = np.divide(bdevsum,len(nbodyl))
  bstdev = np.sqrt(bdevquot)
  while j < 2 * nnbody:
    vgsrminustup = orbarr[np.where((orbarr[:,0] - larray[j]) == 0)]
    vgsrplustup = orbarr[np.where((orbarr[:,0] - larray[j + 1]) == 0)]
    vgsrplus = vgsrplustup[0,2]
    vgsrminus = vgsrminustup[0,2]
    vgsrsearch.append(vgsrminus)
    vgsrsearch.append(vgsrplus)
    j = j + 2
  varray = np.array(vgsrsearch)
  while k < 2 * nnbody:
    vgsrintnum = np.subtract(varray[k+1],varray[k])
    vgsrintdenom = np.subtract(larray[k+1],larray[k])
    vgsrintsub = np.subtract(nbodyl[m],larray[k])
    vgsrintquot = np.divide(vgsrintnum,vgsrintdenom)
    vgsrintprod = np.multiply(vgsrintquot,vgsrintsub)
    vgsrmodel = np.add(vgsrintprod,varray[k])
    vgsrmodellist.append(vgsrmodel)
    k = k + 2
    m = m + 1
  vmodarray = np.array(vgsrmodellist)
  while n < nnbody:
    vgsrdev = np.subtract(vmodarray[n],nbodyv[n])
    vgsrdevlist.append(vgsrdev)
    n = n + 1
  vdevarr = np.array(vgsrdevlist)
  vdevsq = np.power(vdevarr,2)
  vdevsum = np.sum(vdevsq)
  vdevquot = np.divide(vdevsum,len(nbodyl))
  vstdev = np.sqrt(vdevquot)
  while e < 2 * nnbody:
    rminustup = orbarr[np.where((orbarr[:,0] - larray[e]) == 0)]
    rplustup = orbarr[np.where((orbarr[:,0] - larray[e + 1]) == 0)]
    rplus = rplustup[0,3]
    rminus = rminustup[0,3]
    rsearch.append(rminus)
    rsearch.append(rplus)
    e = e + 2
  rarray = np.array(rsearch)
  while f < 2 * nnbody:
    rintnum = np.subtract(rarray[f + 1],rarray[f])
    rintdenom = np.subtract(larray[f + 1],larray[f])
    rintsub = np.subtract(nbodyl[g],larray[f])
    rintquot = np.divide(rintnum,rintdenom)
    rintprod = np.multiply(rintquot,rintsub)
    rmodel = np.add(rintprod,rarray[f])
    rmodellist.append(rmodel)
    f = f + 2
    g = g + 1
  rmodarray = np.array(rmodellist)
  while h < nnbody:
    rdev = np.subtract(rmodarray[h],nbodyr[h])
    rdevlist.append(rdev)
    h = h + 1
  rdevarr = np.array(rdevlist)
  rdevsq = np.power(rdevarr,2)
  rdevsum = np.sum(rdevsq)
  rdevquot = np.divide(rdevsum,len(nbodyl))
  rstdev = np.sqrt(rdevquot)
  print str("b disp = " + str(bstdev))
  print str("v disp = " + str(vstdev))
  print str("r disp = " + str(rstdev))
  print str("N = " + str(nnbody))
  #print str("So far, so good, so what?!")


if __name__ == "__main__": 	
	index = 1
	iterations = 1
	while index < iterations + 1:
	  nbody = fi.read_file("hermus.1e6.40pc.orb76.4B.round2.polyfit.2deg", ",")
	  orbit = fi.read_file("hermustest76.combined.250M.csv.params.small", ",")
	  nbodyl = np.array(nbody[:,0]) #for Charles's polyfit files
	  nbodyb = np.array(nbody[:,1])
	  nbodyv = np.array(nbody[:,4])
	  nbodyr = np.array(nbody[:,3])
	  orbl = np.array(orbit[:,10])
	  orbb = np.array(orbit[:,11])
	  orbv = np.array(orbit[:,9])
	  orbr = np.array(orbit[:,8])
	  vdisp(nbodyl,nbodyb,nbodyv,nbodyr,orbl,orbb,orbv,orbr)
	  index = index + 1
