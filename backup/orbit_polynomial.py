import os
import scipy as sp
import numpy as np
import math as ma
import matplotlib.pyplot as py
import files as fi

#filename = raw_input("Enter filename: ")
#lcol = int(raw_input("Enter l column: "))
#bcol = int(raw_input("Enter b column: "))

#lmin = float(raw_input("Min l value: "))
#lmax = float(raw_input("Max l value: "))
#bmin = float(raw_input("Min b value: "))
#bmax = float(raw_input("Max b value: "))

def orbit_polynomial(l,b):
  l1 = l[0,:]
  b1 = b[0,:]
  #print l
  #print b
  orbfit = np.polyfit(l1, b1, 3)

  print orbfit

if __name__ == "__main__": 	
	data1 = fi.read_file("hermus_ra_dec_l_b", ",")
	l = np.array([data1[:,2]])
	b = np.array([data1[:,3]])
	orbit_polynomial(l,b)