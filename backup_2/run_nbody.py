import scipy as sp
import numpy as np
import os

pi = float(np.pi)
struct = 222288.47
#mkplum parameters
plumname = raw_input("Name for Plummer sphere: ")
nbody = 20000 #float(raw_input("Number of bodies: "))
plumr = float(raw_input("Scale radius in kpc: "))
plummasssol = float(raw_input("Mass in solar masses: "))
plummass = np.divide(plummasssol,struct)
#snapshift parameters
xinit = float(raw_input("Initial x in kpc: "))
yinit = float(raw_input("Initial y in kpc: "))
zinit = float(raw_input("Initial z in kpc: "))
vxinit = float(raw_input("Initial vx in km/s: "))
vyinit = float(raw_input("Initial vy in km/s: "))
vzinit = float(raw_input("Initial vz in km/s: "))
#potential parameters
accname = raw_input("Potential to use: ")
potquery = str(raw_input("Type 1 for Dumas 2015 parameters, 2 for Law et al 2005 parameters, 3 for custom: "))
if potquery == '1':
  omega = 0.0
  a = 5.0
  b = 0.26
  miya_mass = 329751.696
  plummer_rc = 0.33
  plummer_mass = 85024.6529
  vhalo = 114.0
  q = 1.0
  d = 12.0
if potquery == '2':
    omega = 0.0
    a = 6.5
    b = 0.26
    miya_mass = 445865.888
    plummer_rc = 0.7
    plummer_mass = 152954.402
    vhalo = 73.0 
    q = 1.0 
    d = 12.0
if potquery == '3':
  omega = raw_input("Enter omega value: ")
  a = raw_input("Enter Miyamoto a value: ")
  b = raw_input("Enter Miyamoto b value: ")
  miya_mass = raw_input("Enter Miyamoto mass: ")
  plummer_rc = raw_input("Enter Plummer scale radius: ")
  plummer_mass = raw_input("Enter Plummer mass: ")
  vhalo = raw_input("Enter halo velocity: ")
  q = raw_input("Enter flattening parameter: ")
  d = raw_input("Enter halo scale: ")
#gyrfalcON parameters:    
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
step = tstop #raw_input("Interval for output: ")

os.system("mkplum out=" + str(plumname) + " nbody=" + str(nbody) + " r_s=" + str(plumr) + " mass=" + str(plummass))
os.system("snapshift in=" + str(plumname) +  " out=" + str(plumname) + ".shift rshift=" + str(xinit) + "," + str(yinit) + "," + str(zinit) + " vshift=" + str(vxinit) + "," + str(vyinit) + "," + str(vzinit))
os.system("gyrfalcON in=" + str(plumname) +  ".shift out=" + str(plumname) + ".nbody tstop=" + str(tstop) + " step=" + str(step) + " eps=" + str(eps) + " kmax=" + str(kmax) + " startout=" + str(startout) + " lastout=" + str(lastout) + " accname=" + str(accname) + " accpars=" + str(omega) + "," + str(a) + "," + str(b) + "," + str(miya_mass) + "," + str(plummer_rc) + "," + str(plummer_mass) + "," + str(vhalo) + "," + str(q) + "," + str(d))
os.system("snapprint in=" + str(plumname) + ".nbody tab=" + str(plumname) + ".nbody.csv csv=t")
os.system("rm " + str(plumname))
os.system("rm " + str(plumname) + ".shift")
  
