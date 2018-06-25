import numpy as np
from numpy.linalg import inv

#Constants (NGP RA,dec are J2000.0)
deg2rad = np.pi/180.0
rad2deg = 180.0/np.pi
UVW_Sun = [10.1,224.0,6.7]
k = 4.74057
ra_NGP = 192.85*deg2rad
dec_NGP = 27.13*deg2rad
theta_0 = 123.0*deg2rad

#ra_deg = float(raw_input("Enter right ascension in degrees: "))
#dec_deg = float(raw_input("Enter declination in degrees: "))
#dist_kpc = float(raw_input("Enter distance in kpc: "))
ra_deg = 254.886166667
dec_deg = -37.1214166667
dist_kpc = 10.3
ra = ra_deg*deg2rad
dec = dec_deg*deg2rad
dist = dist_kpc*1000.0
#mu_delta_mas = float(raw_input("Enter declination proper motion in mas/yr: "))
#mu_alpha_mas = float(raw_input("Enter right ascension declination-corrected proper motion in mas/yr: "))
#radial = float(raw_input("Enter radial velocity in km/s: "))
mu_delta_mas = -0.63
mu_alpha_mas = -3.85
radial = -101.40
#Here we convert to the quantities required by Johnson et al., 1987:
parallax = 1/dist
mu_alpha = mu_alpha_mas/1000.0
mu_delta = mu_delta_mas/1000.0
mu_alpha_num = np.multiply(mu_alpha,k)
mu_alpha_red = np.divide(mu_alpha_num,parallax)
mu_delta_num = np.multiply(mu_delta,k)
mu_delta_red = np.divide(mu_delta_num,parallax)

#Create transform matrix T:
T_0 = [[np.cos(theta_0), np.sin(theta_0), 0],[np.sin(theta_0),-np.cos(theta_0),0],[0,0,1]]
T_1 = [[-np.sin(dec_NGP),0,np.cos(dec_NGP)],[0,-1,0],[np.cos(dec_NGP),0,np.sin(dec_NGP)]]
T_2 = [[np.cos(ra_NGP),np.sin(ra_NGP),0],[np.sin(ra_NGP),-np.cos(ra_NGP),0],[0,0,1]]
T_partial = np.dot(T_0,T_1)
T = np.dot(T_partial,T_2)

#Create secondary transform matrices A and B as described in Johnson et al., 1987:
A = [[np.cos(ra)*np.cos(dec),-np.sin(ra),-np.cos(ra)*np.sin(dec)],[np.sin(ra)*np.cos(dec),np.cos(ra),-np.sin(ra)*np.sin(dec)],[np.sin(dec),0,np.cos(dec)]]
B = np.dot(T,A)

#Complete the transformation and output:
V_prop = [radial,mu_alpha_red,mu_delta_red]
UVW_HC = np.dot(B,V_prop)
UVW_GC = np.add(UVW_HC,UVW_Sun)
print("UVW Galactocentric velocity = [" + str(UVW_GC[0]) + "," + str(UVW_GC[1]) + "," + str(UVW_GC[2]) + "]")