import astropy as ap
from astropy.io import ascii
from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.table import QTable
import files as fi
import os

filename = raw_input("Enter input filename: ")
#output = raw_input("Enter output file: ")
ra_col = int(raw_input("RA column: "))
dec_col = int(raw_input("Dec column: "))

ra_dec = fi.read_file(str(filename), ",")
ra_arr = ra_dec[:,ra_col]
dec_arr = ra_dec[:,dec_col]

sc = SkyCoord(ra = ra_arr*u.degree, dec = dec_arr*u.degree, frame = "fk5")
sco = sc.galactic
t = QTable([sco])

ascii.write(t, 'output_1.csv', format="ecsv", delimiter=",")

#out_arr = np.array(d)
#print out_arr
#out = open(str(output), "r+")
#out.write("#l,b\n")
#j = 0
#while j < len(ra_arr):
    #out.write(str(d[j,0]) + "," + str(d[j,1]) + "\n")
    #j = j + 1
