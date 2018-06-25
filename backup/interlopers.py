import math as ma
import matplotlib.pyplot as py
from pylab import *
import scipy as sp
import numpy as np
import files as fi
import os
import random
from datetime import datetime

startTime = datetime.now()
print("Run started at " + str(startTime))

if __name__ == "__main__":
  os.system("rm interloper.output")
  os.system("touch interloper.output")
  output = open("interloper.output", "a")
  runs = 0
  N_runs = 10000
  output.write("#var_star,N*var_star,var_rand,N*var_rand,var_prime \n")
  while runs < N_runs:
    #This first bit just reads in the relevant data file and orbit file. Probably don't need to select individual colums in the data file.
    rawdata = fi.read_file("ref_resp_stars_trunc.csv", ",")
    lraw = rawdata[:,0]
    braw = rawdata[:,1]
    rraw = rawdata[:,2]
    vgsrraw = rawdata[:,3]
    orbit = fi.read_file("hermustest76.rounded.combined.300M.17to72.csv", ",")
    orbit_l = orbit[:,10]
    orbit_vgsr = orbit[:,9]
    #Creates a list of eleven random integers from 0 to 18, gets the corresponding rows of the dataset, and then puts their Galactic longitude and vgsr in an array together.
    selection = random.sample(xrange(0,18,1),11)
    select_list = []
    hermus_vgsr_list = []
    vgsr_list = []
    i = 0
    j = 0
    k = 0
    while i < len(selection):
      select = rawdata[selection[i]]
      select_list.append(select)
      i = i + 1
    select_stars = np.array(select_list)
    stars_l = select_stars[:,0]
    stars_vgsr = select_stars[:,3]
    stars_array = zip(stars_l,stars_vgsr)
    v = 0
    remain_check = np.in1d(lraw,stars_l)
    not_select_list = []
    while v < len(lraw):
      if remain_check[v] == False:
	not_select_list.append(rawdata[v,:])
	v = v + 1
      else:
	v = v + 1
    not_select = np.array(not_select_list)
    not_select_l = not_select[:,0]
    #Here we generate a Gaussian distribution of numbers to represent halo vgsrs, eight random longitude values so we can interpolate properly, and then apply our Hermus vgsr selection criteria to the generated vgsrs. The vgsrs are combined with the random longitudes, and then combined with the actual data to create our nineteen longitude/vgsr pairs. 
    rand_vgsr = np.random.normal(0,120,size=(1000,))
    rand_l = np.random.uniform(17,72,size=(8,))
    while j < len(rand_vgsr):
      if rand_vgsr[j] < 115 and rand_vgsr[j] > 10:
	hermus_vgsr_list.append(rand_vgsr[j])
	j = j + 1
      else:
	j = j + 1
    hermus_vgsr = np.array(hermus_vgsr_list)
    rand_select = random.sample(xrange(0,len(hermus_vgsr),1),8)
    while k < len(rand_select):
      rand_vgsr = hermus_vgsr[rand_select[k]]
      vgsr_list.append(rand_vgsr)
      k = k + 1
    herm_vgsr_select = np.array(vgsr_list)
    rand_data = zip(not_select_l,herm_vgsr_select)
    dataset = np.vstack((stars_array,rand_data))
    #Here we do the same thing as in the gradient descent: pick nearest two points in orbit on opposite side of each data point.
    l_search = []
    n_points = len(lraw)
    m = 0
    while m < n_points:
      l_sub = np.subtract(orbit[:,10],dataset[m,0])
      l_sub_plus =  [n for n in l_sub if n > 0]
      l_sub_minus = [o for o in l_sub if o < 0]
      l_min_plus = np.amin(l_sub_plus)
      l_min_minus = np.amax(l_sub_minus)
      l_minus = np.add(l_min_minus,dataset[m,0])
      l_plus = np.add(l_min_plus,dataset[m,0])
      l_search.append(l_minus)
      l_search.append(l_plus)
      m = m + 1
    l_array = np.array(l_search)
    p = 0
    vgsr_search = []
    while p < 2 * n_points:
      vgsr_minus_tup = orbit[np.where((orbit[:,10] - l_array[p]) == 0)]
      vgsr_plus_tup = orbit[np.where((orbit[:,10] - l_array[p + 1]) == 0)]
      vgsr_plus = vgsr_plus_tup[0,9]
      vgsr_minus = vgsr_minus_tup[0,9]
      vgsr_search.append(vgsr_minus)
      vgsr_search.append(vgsr_plus)
      p = p + 2
    vgsr_array = np.array(vgsr_search)
    q = 0
    r = 0
    vgsr_model_list = []
    while q < 2 * n_points:
      vgsr_int_num = np.subtract(vgsr_array[q + 1],vgsr_array[q])
      vgsr_int_denom = np.subtract(l_array[q + 1],l_array[q])
      vgsr_int_sub = np.subtract(dataset[r,0],l_array[q])
      vgsr_int_quot = np.divide(vgsr_int_num,vgsr_int_denom)
      vgsr_int_prod = np.multiply(vgsr_int_quot,vgsr_int_sub)
      vgsr_model = np.add(vgsr_int_prod,vgsr_array[q])
      vgsr_model_list.append(vgsr_model)
      q = q + 2
      r = r + 1
    vgsr_model = np.array(vgsr_model_list)
    s = 0
    vgsr_dev_list = []
    while s < n_points:
      vgsr_dev = np.subtract(vgsr_model[s],dataset[s,1])
      vgsr_dev_list.append(vgsr_dev)
      s = s + 1
    full_dev = np.array(vgsr_dev_list)
    star_dev = full_dev[:len(stars_l)-1]
    rand_dev = full_dev[len(stars_l):]
    t = 0
    star_var_list = []
    star_dev_mean = np.mean(star_dev)
    while t < len(star_dev):
      star_dev_sub = np.subtract(star_dev[t],star_dev_mean)
      star_dev_sq = np.power(star_dev_sub,2)
      star_dev_quot = np.divide(star_dev_sq,len(star_dev))
      star_var_list.append(star_dev_quot)
      t = t + 1
    star_var_red = np.array(star_var_list)
    star_var = np.sum(star_var_red)
    star_stdev = np.sqrt(star_var)
    u = 0
    rand_var_list = []
    rand_dev_mean = np.mean(rand_dev)
    while u < len(rand_dev):
      rand_dev_sub = np.subtract(rand_dev[u],rand_dev_mean)
      rand_dev_sq = np.power(rand_dev_sub,2)
      rand_var_list.append(rand_dev_sq)
      u = u + 1
    rand_var_red = np.array(rand_var_list)
    rand_var = np.sum(rand_var_red)
    rand_quot = np.divide(rand_var,5)
    rand_stdev = np.sqrt(rand_quot)
    star_var_mult = len(star_dev)*star_var
    comb_var_arg = star_var_mult + rand_var
    comb_var = comb_var_arg/(len(star_dev) + len(rand_dev))
    comb_stdev = np.sqrt(comb_var)
    output.write(str(star_var) + "," + str(star_var_mult) + "," + str(rand_quot) + "," + str(rand_var) + "," + str(comb_var) + "\n")
    runs = runs + 1

print datetime.now() - startTime