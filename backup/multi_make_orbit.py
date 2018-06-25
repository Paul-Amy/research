import scipy as sp
import numpy as np
import files as fi
import os

pot = "mpn"
potpars = "0,5.0,0.26,329751.696,0.33,85024.6529,114.0,1.0,12.0"
orbsteps = 5000
orbtimestep = 0.00003

file_base = raw_input("Enter base name for orbit files: ")
input_file = raw_input("Enter name of orbit parameter file: ")

params = fi.read_file(input_file, ",")
l_in = params[:,1]
b_in = params[:,2]
r_in = params[:,11]
vx_in = params[:,14]
vy_in = params[:,15]
vz_in = params[:,16]

n_orbits = len(b_in)

deg2rad = np.pi/180.0
rad2deg = 180.0/np.pi
sin_l = np.sin(l*deg2rad)
cos_l = np.cos(l*deg2rad)
sin_b = np.sin(b_in*deg2rad)
cos_b = np.cos(b_in*deg2rad)
x_arr1 = np.multiply(r_in,cos_b)
x_arr2 = np.multiply(x_arr1,cos_l)
x = np.subtract(x_arr2,8.0)
y_arr1 = np.multiply(r_in,cos_b)
y = np.multiply(y_arr1,sin_l)
z = np.multiply(r_in,sin_b)

orbit_iter = 1

while orbit_iter - 1 < n_orbits:
  os.system("mkorbit out=" + str(file_base) + "." + str(orbit_iter) + ".temp x=" + str(x[orbit_iter]) + " y=" + str(y[orbit_iter]) + " z=" + str(z[orbit_iter]) + " vx=" + str(vx_in[orbit_iter]) + " vy=" + str(vy_in[orbit_iter]) + " vz=" + str(vz_in[orbit_iter]) + " potname=" + str(pot) + " potpars=" + str(potpars))
  os.system("orbint in=" + str(file_base) + "." + str(orbit_iter) + ".temp out=" + str(file_base) + "." + str(orbit_iter) + ".forward.temp nsteps=" + str(orbsteps) + " dt=" + str(orbtimestep) + " potname=" + str(pot) + " potpars=" + str(potpars))
  os.system("orbint in=" + str(file_base) + "." + str(orbit_iter) + ".temp out=" + str(file_base) + "." + str(orbit_iter) + ".back.temp nsteps=" + str(orbsteps) + " dt=-" + str(orbtimestep) + " potname=" + str(pot) + " potpars=" + str(potpars))
  os.system("otos in=" + str(file_base) + "." + str(orbit_iter) + ".forward.temp out=" + str(file_base) + "." + str(orbit_iter) + ".forward.snap.temp")
  os.system("otos in=" + str(file_base) + "." + str(orbit_iter) + ".back.temp out=" + str(file_base) + "." + str(orbit_iter) + ".back.snap.temp")
  os.system("snapstack in1=" + str(file_base) + "." + str(orbit_iter) + ".forward.snap.temp in2=" + str(file_base) + "." + str(orbit_iter) + ".back.snap.temp out=" + str(file_base) + "." + str(orbit_iter) + ".total.snap.temp")
  os.system("snapprint in=" + str(file_base) + "." + str(orbit_iter) + ".total.snap.temp tab=" + str(file_base) + "." + str(orbit_iter) + ".orbit csv=t")
  os.system("rm *temp*")
  orbit_iter = orbit_iter + 1

