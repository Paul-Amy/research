import files as fi
import numpy as np
import matplotlib.pyplot as py
from pylab import *
from scipy import stats
from scipy.stats import norm
import os

#define constants for coordinate transform
deg2rad = np.pi/180
rad2deg = 180/np.pi
epsilon =  23.43693
ra_ngp = 192.859508
dec_ngp = 27.128336
l_ngp = 32.932
ra_ngp_rad = np.radians(ra_ngp)
dec_ngp_rad = np.radians(dec_ngp)
l_ngp_rad = np.radians(l_ngp)

#read in orbit file
orb_in = "hyllustest_hv.combined.500M.csv.params" #raw_input("Enter orbit file: ")
l_col = 10 #int(raw_input("L column: "))
b_col = 11 #int(raw_input("B column: "))
orb_dat = fi.read_file(str(orb_in),",")
l_arr = orb_dat[:,l_col]
b_arr = orb_dat[:,b_col]

#trig values
l_rad = np.radians(l_arr)
b_rad = np.radians(b_arr)
sin_ra_ngp = np.sin(ra_ngp_rad)
cos_ra_ngp = np.cos(ra_ngp_rad)
sin_dec_ngp = np.sin(dec_ngp_rad)
cos_dec_ngp = np.cos(dec_ngp_rad)
sin_l_ngp = np.sin(l_ngp_rad)
cos_l_ngp = np.cos(l_ngp_rad)
l_ngp_term = np.subtract(l_rad,l_ngp_rad)
sin_l_ngp_term = np.sin(l_ngp_term)
cos_l_ngp_term = np.cos(l_ngp_term)
sin_l = np.sin(l_rad)
cos_l = np.cos(l_rad)
sin_b = np.sin(b_rad)
cos_b = np.cos(b_rad)

#get declination values
sin_dec_1 = np.multiply(sin_dec_ngp,sin_b)
sin_dec_2 = np.multiply(cos_dec_ngp,cos_b)
sin_dec_3 = np.multiply(sin_dec_2,sin_l_ngp_term)
sin_dec = np.add(sin_dec_1,sin_dec_3)
dec_rad = np.arcsin(sin_dec)
dec = np.degrees(dec_rad)

#get right ascension values
ra_num = np.multiply(cos_b,cos_l_ngp_term)
ra_denom_1 = np.multiply(cos_dec_ngp,sin_b)
ra_denom_2 = np.multiply(sin_dec_ngp,cos_b)
ra_denom_3 = np.multiply(ra_denom_2,sin_l_ngp_term)
ra_denom = np.subtract(ra_denom_1,ra_denom_3)
ra_rad_quot = np.divide(ra_num,ra_denom)
ra_rad_part = np.arctan(ra_rad_quot)
ra_rad = np.add(ra_rad_part,ra_ngp_rad)
ra = np.degrees(ra_rad)

add_list = zip(ra,dec)
add_arr = np.array(add_list)
orb_dat_ext = np.concatenate((orb_dat,add_arr), axis = 1)

print "Coordinate transform complete."

#read in data file
star_in = "ra_diff_on_velocity.csv"
star_dat = fi.read_file(str(star_in),",")
ra_col = star_dat[:,0]
dec_col = star_dat[:,1]
#create output file
os.system("touch " + str(star_in) + ".orbit.out")
os.system("touch " + str(star_in) + ".polyfit.out")
output_1 = open(str(star_in) + ".orbit.out","w")
output_2 = open(str(star_in) + ".polyfit.out","w")

#grillmair 2014 hyllus fit
dec_hyl = arange(10,50,0.1)
ra_hyl = 255.8150 - 0.78364*dec_hyl + 0.01532*dec_hyl**2

#the orbit search and interpolater are adapted from grad_desc.py
#first, check through orbit for closest orbit dec values on either side of each star.
j = 0
dec_search = []
while j < len(ra_col):
    dec_sub = np.subtract(dec[:],dec_col[j])
    dec_sub_plus = [m for m in dec_sub if m > 0]
    dec_sub_minus = [n for n in dec_sub if n < 0]
    dec_min_plus = np.amin(dec_sub_plus)
    dec_min_minus = np.amax(dec_sub_minus)
    dec_minus = np.add(dec_min_minus,dec_col[j])
    dec_plus = np.add(dec_min_plus,dec_col[j])
    dec_search.append(dec_minus)
    dec_search.append(dec_plus)
    j = j + 1
dec_array = np.array(dec_search)

print "Found closest declination values to data points."

#now find the corresponding right ascensions for those points.
k = 0
ra_search = []
while k < 2 * len(ra_col):
    ra_minus_tup = orb_dat_ext[np.where((orb_dat_ext[:, 13] - dec_array[k]) == 0)]
    ra_plus_tup = orb_dat_ext[np.where((orb_dat_ext[:, 13] - dec_array[k + 1]) == 0)]
    ra_plus = ra_plus_tup[0,12]
    ra_minus = ra_minus_tup[0,12]
    ra_search.append(ra_minus)
    ra_search.append(ra_plus)
    k = k + 2

ra_array = np.array(ra_search)

print "Found corresponding right ascensions."

ra_model_list = []
a = 0
b = 0
c = 0
#interpolate to find predicted right ascensions for stars:
while a < 2 * len(ra_col):
    ra_int_num = np.subtract(ra_array[a+1],ra_array[a])
    ra_int_denom = np.subtract(dec_array[a+1],dec_array[a])
    ra_int_sub = np.subtract(dec[c],dec_array[a])
    ra_int_quot = np.divide(ra_int_num,ra_int_denom)
    ra_int_prod = np.multiply(ra_int_quot,ra_int_sub)
    ra_model = np.add(ra_int_prod,ra_array[a])
    ra_model_list.append(ra_model)
    a = a + 2
    c = c + 1

ra_model_array = np.array(ra_model_list)

print "Interpolation finished."

print "Calculating RA difference from orbit."

#calculate difference of RA of point from RA of orbit fit
ra_diff_orb = np.subtract(ra_model_array,ra_col)

print "Calculating RA difference from polyfit."

#calculate difference of RA of point from RA of G14 polyfit
dec_sq = np.power(dec_col,2)
ra_polyfit_2nd_term = np.multiply(dec_sq,0.01532)
ra_polyfit_1st_term = np.multiply(dec_col,-0.78364)
ra_polyfit_comb = np.add(ra_polyfit_2nd_term,ra_polyfit_1st_term)
ra_polyfit = np.add(255.8150,ra_polyfit_comb)
ra_diff_polyfit = np.subtract(ra_polyfit,ra_col)

print "Writing to output files."

#write outputs to file
d = 0
e = 0
for d in range(len(ra_col)):
    output_1.write(str(ra_diff_orb[d]) + "\n")
output_1.close()
for e in range(len(ra_col)):
    output_2.write(str(ra_diff_polyfit[e]) + "\n")
output_2.close()

print "Done!"