import scipy as sp
import numpy as np
import os

pi = float(np.pi)
#iterations = float(raw_input("How many simulations to run? "))
#mkplum parameters
plumname = raw_input("Name of Plummer sphere file: ")
nbody = float(raw_input("Number of bodies: "))
plumr = float(raw_input("Scale radius in kpc: "))
plummass = float(raw_input("Mass in structural units: "))
#snapshift parameters
xinit = float(raw_input("Initial x in kpc: "))
yinit = float(raw_input("Initial y in kpc: "))
zinit = float(raw_input("Initial z in kpc: "))
vxinit = float(raw_input("Initial vx in km/s: "))
vyinit = float(raw_input("Initial vy in km/s: "))
vzinit = float(raw_input("Initial vz in km/s: "))
#gyrfalcON parameters
accname = raw_input("Potential to use: ")
#potquery = str(raw_input("Do you want to use the standard potential parameters? y/n: "))
potquery = int(raw_input("Press 1 for Law 2005 potential parameters or 2 for Dumas 2015 potential parameters: "))
if potquery == '1' or potquery:
  accpars = str("0,6.5,0.26,4.45865888E5,0.7,1.52954402E5,73,1.0,12.0")
  omega = 0.0
  a = 6.5
  b = 0.26
  miya_mass = 4.45865888E5
  plummer_rc = 0.7
  plummer_mass = 1.52954402E5
  vhalo = 73.0
  q = 1.0
  d = 12.0
if potquery == '2' or potquery:
  omega = 0.0
  a = 5.0
  b = 0.26
  miya_mass = 329751.696
  plummer_rc = 0.33
  plummer_mass = 85024.6529
  vhalo = 114.0
  q = 1.0
  d = 12.0
else:
  print("Invalid input.")
tstepfracnum = float(4*pi*np.power(plumr,3))
tstepfracdenom = float(3*plummass)
tstepsqrtarg = np.divide(tstepfracnum,tstepfracdenom)
tstepsqrt = np.sqrt(tstepsqrtarg)
tstep = np.multiply(0.01,tstepsqrt)
kmaxnum = np.log(tstep)
kmaxdenom = np.log(0.5)
kmax = np.divide(kmaxnum,kmaxdenom)
epssqrt = np.sqrt(nbody)
eps = np.divide(plumr,epssqrt)
tstop = raw_input("Time to run the nbody in Gyr: ")
startout = raw_input("Initial position to output (T/F): ")
lastout = raw_input("Final position to output (T/F): ")
step = raw_input("Interval for output: ")
#i = 1

#os.system("mkplum out=" + str(plumname) + "." + str(i) +  " nbody=" + str(nbody) + " r_s=" + str(plumr) + " mass=" + str(plummass))
os.system("snapshift in=" + str(plumname) + " out=" + str(plumname) + "." + "shift rshift=" + str(xinit) + "," + str(yinit) + "," + str(zinit) + " vshift=" + str(vxinit) + "," + str(vyinit) + "," + str(vzinit))
os.system("gyrfalcON in=" + str(plumname) + ".shift out=" + str(plumname) + "." + "nbody tstop=" + str(tstop) + " step=" + str(step) + " eps=" + str(eps) + " kmax=" + str(kmax) + " startout=" + str(startout) + " lastout=" + str(lastout) + " accname=" + str(accname) + " accpars=" + str(omega) + "," + str(a) + "," + str(b) + "," + str(miya_mass) + "," + str(plummer_rc) + "," + str(plummer_mass) + "," + str(vhalo) + "," + str(q) + "," + str(d))
os.system("snapprint in=" + str(plumname) + "." + "nbody tab=" + str(plumname) + ".nbody.csv csv=t")
os.system("rm " + str(plumname))
os.system("rm " + str(plumname) + "." + "shift")
