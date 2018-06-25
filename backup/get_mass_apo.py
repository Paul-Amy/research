import math as ma
import scipy as sp
import numpy as np
import files as fi
import os
import csv
import fileinput

base_name = raw_input("Enter base filename: ")
iterations = float(raw_input("Enter number of files: "))
np.set_printoptions(threshold=np.nan)
n_iter = 0
apo_list = []
peri_list = []

while n_iter < iterations:
  data = fi.read_file(str(base_name) + "." + str(n_iter) + ".params", ",")
  rgal = data[:,6]
  apo = 