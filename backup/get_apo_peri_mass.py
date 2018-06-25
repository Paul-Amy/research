import math as ma
import scipy as sp
import numpy as np
import files as fi
import os
import csv
import fileinput
from numpy import random

base_name = raw_input("Enter base filename: ")
iterations = float(raw_input("Enter number of files: "))
rad2deg = np.divide(180,np.pi)
np.set_printoptions(threshold=np.nan)
n_iter = 0
apo_list = []
peri_list = []
ecc_list = []
inc_list = []
x = 0
y = 0
while n_iter < iterations:
  data = fi.read_file(str(base_name) + "." + str(n_iter) + ".params", ",")
  data_arr = np.array(data)
  #print data_arr
  rgal = data[:,6]
  l = data[:,10]
  apo_val = np.amax(rgal)
  peri_val = np.amin(rgal)
  #need semi-major and semi-minor axes to find eccentricity:
  semi_major_num = np.add(apo_val,peri_val)
  semi_major = np.divide(semi_major_num,2)
  semi_minor_arg = np.multiply(apo_val,peri_val)
  semi_minor = np.sqrt(semi_minor_arg)
  semi_maj_sq = np.power(semi_major,2)
  semi_min_sq = np.power(semi_minor,2)
  ecc_frac = np.divide(semi_min_sq,semi_maj_sq)
  ecc_arg = np.subtract(1,ecc_frac)
  ecc = np.sqrt(ecc_arg)
  apo_list.append(apo_val)
  peri_list.append(peri_val)
  ecc_list.append(ecc)
  #use vector product of points at each end of fit range in l to get inclination:
  l_sub_1 = np.subtract(l,20)
  l_sub_1_pos = [m for m in l_sub_1 if m > 0]
  lmin = np.amin(l_sub_1_pos)
  lnear = np.add(lmin,20)
  l_sub_2 = np.subtract(l,80)
  l_sub_2_pos = [n for n in l_sub_2 if n < 0]
  lmax = np.amax(l_sub_2_pos)
  lnear2 = np.add(lmax,80)
  lmintup = data_arr[np.where((data_arr[:,10] - lnear) == 0)]
  lmaxtup = data_arr[np.where((data_arr[:,10] - lnear2) == 0)]
  cross_prod_i = lmintup[0,1]*lmaxtup[0,2] - lmaxtup[0,1]*lmintup[0,2]
  cross_prod_j = lmintup[0,2]*lmaxtup[0,0] - lmaxtup[0,2]*lmintup[0,0]
  cross_prod_k = lmintup[0,0]*lmaxtup[0,1] - lmaxtup[0,0]*lmintup[0,1]
  cross_prod_sq = cross_prod_i**2 + cross_prod_j**2 + cross_prod_k**2
  cross_prod_mag = np.sqrt(cross_prod_sq)
  acos_arg = np.divide(cross_prod_k,cross_prod_mag)
  inc_rad = np.arccos(acos_arg)
  inc = inc_rad * rad2deg
  inc_list.append(inc)
  pct_comp_frac = np.divide(n_iter,iterations)
  pct_comp = np.multiply(pct_comp_frac,100)
  print(str(pct_comp) + "%")
  n_iter = n_iter + 1

apo_arr = np.array(apo_list)
peri_arr = np.array(peri_list)
ecc_arr = np.array(ecc_list)
inc_arr = np.array(inc_list)

apo_avg = np.average(apo_arr)
peri_avg = np.average(peri_arr)
ecc_avg = np.average(ecc_arr)
inc_avg = np.average(inc_arr)

apo_dev = np.std(apo_arr)
peri_dev = np.std(peri_arr)
ecc_dev = np.std(ecc_arr)
inc_dev = np.std(inc_arr)

print("Mean apogalacticon = " + str(apo_avg) + " +/- " + str(apo_dev))
print("Mean perigalacticon = " + str(peri_avg) + " +/- " + str(peri_dev))
print("Mean eccentricity = " + str(ecc_avg) + " +/- " + str(ecc_dev))
print("Mean inclination = " + str(inc_avg) + " +/- " + str(inc_dev))