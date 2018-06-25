import scipy as sp
import numpy as np
import files as fi
import os

#Open files
isochrones = fi.read_file("combined_isochrones.csv",",")
star_data_name = "hyllus_new_off_rgbs.csv" #raw_input("Enter data file: ")
star_data = fi.read_file(str(star_data_name),",")
#Create output file
os.system("touch new_dist_output.csv")
output = open("new_dist_output.csv","r+")
#Get data
iso_feh_col = 22#int(raw_input("Isochrone metallicity column: "))
iso_grav_col = 6#int(raw_input("Isochrone surface gravity column: "))
iso_g_col = 25#int(raw_input("Isochrone g magnitude column: "))
iso_r_col = 26#int(raw_input("Isochrone r magnitude column: "))
star_feh_col = 11#int(raw_input("Stellar metallicity column: "))
star_grav_col = 10#int(raw_input("Stellar surface gravity column: "))
star_g_col = 14#int(raw_input("Stellar g0 magnitude column: "))
star_r_col = 15#int(raw_input("Stellar r0 magnitude column: "))

iso_feh = isochrones[:,iso_feh_col]
iso_grav = isochrones[:,iso_grav_col]
iso_g = isochrones[:,iso_g_col]
iso_r = isochrones[:,iso_r_col]
star_feh = star_data[:,star_feh_col]
star_grav = star_data[:,star_grav_col]
star_g = star_data[:,star_g_col]
star_r = star_data[:,star_r_col]
#Make composite columns and create reduced arrays
iso_gmr = np.subtract(iso_g,iso_r)
star_gmr = np.subtract(star_g,star_r)
iso_zip = zip(iso_gmr,iso_feh,iso_grav)
star_zip = zip(star_gmr,star_feh,star_grav)
iso_data_array = np.array(iso_zip)
star_data_array = np.array(star_zip)
#Now we begin iteration through the dataset to find closest isochrone point to each star
i = 0
dist_list = []
while i < len(star_g):
    j = 0
    temp_dist_list = []
    while j < len(iso_g):
        gmr_sub = np.subtract(star_data_array[i,0],iso_data_array[j,0])
        gmr_sq = np.power(gmr_sub,2)
        feh_sub = np.subtract(star_data_array[i,1],iso_data_array[j,1])
        feh_sq = np.power(feh_sub,2)
        logg_sub = np.subtract(star_data_array[i,2],iso_data_array[j,2])
        logg_sq = np.power(logg_sub,2)
        comb1 = np.add(gmr_sq,feh_sq)
        comb2 = np.add(comb1,logg_sq)
        dist = np.sqrt(comb2)
        temp_dist_list.append(dist)
        j = j + 1
    temp_dist = np.array(temp_dist_list)
    match = np.amin(temp_dist)
    row = temp_dist_list.index(match)
    abs_mag = iso_g[row]
    dist_mod = np.subtract(star_g[i],abs_mag)
    dist_mod_add = np.add(dist_mod,5)
    dist_mod_quot = np.divide(dist_mod_add,5)
    star_dist_pc = np.power(10,dist_mod_quot)
    star_dist_kpc = np.divide(star_dist_pc,1000)
    dist_list.append(star_dist_kpc)
    i = i + 1

new_dist = np.array(dist_list)
k = 0
for k in range(len(star_g)):
    output.write(str(new_dist[k]) + "\n")
output.close()
        
        
    



