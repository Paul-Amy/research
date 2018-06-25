import scipy as sp
import numpy as np
import files as fi
import os
from decimal import *
#Startup stuff

star_file = "hyllus_pm2_041218_high_feh.csv" #raw_input("Enter star file: ")
g0_col = 9 #int(raw_input("Column of g0 magnitude: "))
r0_col = 12 #int(raw_input("Column of r0 magnitude: "))
#i0_col = int(raw_input("Column of i0 magnitude: "))
isochrone = "z00039545_single_isochrone_hb_removed.csv" #raw_input("Isochrone file: ")
gmag_col = 24 #int(raw_input("Column of g magnitude: "))
rmag_col = 25 #int(raw_input("Column of r magnitude: "))
rgb_cutoff = 4 #int(raw_input("RGB gmag cutoff: "))
hb_cutoff = -1 #int(raw_input("HB gmag cutoff: "))
#imag_col = int(raw_input("Column of i magnitude: "))

#Open files and get appropriate columns:
#os.system("touch dist_output_low")
output = open("dist_output_high","r+")
star_data = fi.read_file(str(star_file), ",")
g0 = star_data[:,g0_col]
r0 = star_data[:,r0_col]
n_stars = len(g0)
#i0 = star_data[:,i0_col]
iso_data = fi.read_file(str(isochrone), ",")
gmag_base = iso_data[:,gmag_col]
N = len(gmag_base)
k = 0
l = 0
#Need to focus on just the red giant branch, so we cut off any isochrone points on the main sequence or horizontal branch:
rgb_cutoff_list = []
hb_cutoff_list = []
while k < N:
    if iso_data[k,gmag_col] < rgb_cutoff:
        rgb_cutoff_list.append(iso_data[k,:])
        k = k + 1
    else:
        k = k + 1
rgb_cutoff_arr = np.array(rgb_cutoff_list)
gmag_rgb = rgb_cutoff_arr[:,0]
N_RGB = len(gmag_rgb)
while l < N_RGB:
    if rgb_cutoff_arr[l,gmag_col] > hb_cutoff:
        hb_cutoff_list.append(rgb_cutoff_arr[l,:])
        l = l + 1
    else:
        l = l + 1
hb_cutoff_arr = np.array(hb_cutoff_list)
#Now we make the magnitude and color arrays:
gmag = hb_cutoff_arr[:,gmag_col]
rmag = hb_cutoff_arr[:,rmag_col]
gmr_star = np.subtract(g0,r0)
gmr_iso = np.subtract(gmag,rmag)
star_mags = zip(g0,gmr_star)
iso_mags = zip(gmag,gmr_iso)
iso_mags_arr = np.array(iso_mags)
star_mags_arr = np.array(star_mags)

#Iterate through star file, checking each star's g-r color against all isochrone g-r colors:
i = 0
dist_list = []
while i < n_stars:
    j = 0
    color_sub_list = []
    temp_mag_list = []
    while j < len(gmag):
        color_sub = np.subtract(gmr_star[i],gmr_iso[j])
        color_sub_list.append(color_sub)
        j = j + 1
    color_sub_arr = np.array(color_sub_list)
    color_sub_abs = np.absolute(color_sub_arr)
    color_sub_min = np.amin(color_sub_abs)
    min_row_tup = np.where(color_sub_abs == color_sub_min)
    min_row = int(min_row_tup[0][0])
    iso_row = iso_mags_arr[min_row,:]
    dist_mod = np.subtract(star_mags_arr[i,0],iso_row[0])
    dist_exp = dist_mod / 5 + 1
    dist_pc = np.power(10,dist_exp)
    dist_kpc = dist_pc / 1000
    dist_list.append(dist_kpc)
    i = i + 1

dist_arr = np.array(dist_list)
m = 0
for m in range(len(dist_arr)):
    output.write(str(dist_arr[m]) + "\n")
output.close()
        

