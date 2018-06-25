import numpy as np
from numpy.linalg import inv

#This transforms a l,b position and UVW Galactocentric velocity to RA,Dec position and proper motion, as well as a radial velocity.

#Constants (NGP RA,dec are J2000.0)
deg2rad = np.pi/180.0
rad2deg = 180.0/np.pi
UVW_Sun = [10.1,224.0,6.7]
k = 4.74057
ra_NGP = 192.85*deg2rad
dec_NGP = 27.13*deg2rad
theta_0 = 123.0*deg2rad

#User input of l,b, and U,V,W
#l_deg = float(raw_input("Enter l coordinate: "))
#b_deg = float(raw_input("Enter b coordinate: "))
#dist_kpc = float(raw_input("Enter distance (kpc): "))
l_deg = 347.7916
b_deg = 3.3064
dist_kpc = 10.3
l = l_deg*deg2rad
b = b_deg*deg2rad
dist = dist_kpc*1000

#U = float(raw_input("Enter U velocity in km/s: "))
#V = float(raw_input("Enter V velocity in km/s: "))
#W = float(raw_input("Enter W velocity in km/s: "))
U = -125.670608456
V = 109.572960358
W = -130.085870369
V_GC = [U,V,W]

#This generates a rotation matrix T that transforms from RA,dec to l,b:
T_0 = [[np.cos(theta_0), np.sin(theta_0), 0],[np.sin(theta_0),-np.cos(theta_0),0],[0,0,1]]
T_1 = [[-np.sin(dec_NGP),0,np.cos(dec_NGP)],[0,-1,0],[np.cos(dec_NGP),0,np.sin(dec_NGP)]]
T_2 = [[np.cos(ra_NGP),np.sin(ra_NGP),0],[np.sin(ra_NGP),-np.cos(ra_NGP),0],[0,0,1]]
T_partial = np.dot(T_0,T_1)
T = np.dot(T_partial,T_2)

#Take the inverse to transform from l,b to RA,dec:
T_inv = np.linalg.inv(T)

#Transform l,b position to RA,dec position:
XYZ_nodist = [np.cos(l)*np.cos(b),np.sin(l)*np.cos(b),np.sin(b)]
ra_dec_vec = np.dot(T_inv,XYZ_nodist)
RA_rad = np.arctan2(ra_dec_vec[1],ra_dec_vec[0])
RA = RA_rad*rad2deg
comp1 = np.power(ra_dec_vec[0],2)
comp2 = np.power(ra_dec_vec[1],2)
Dec_denom_arg = np.add(comp1,comp2)
Dec_denom = np.sqrt(Dec_denom_arg)
Dec_rad = np.arctan2(ra_dec_vec[2],Dec_denom)
Dec = Dec_rad*rad2deg
if RA < 0:
  RA = RA + 360
print("RA position: " + str(RA) + " degrees")
print("Dec position: " + str(Dec) + " degrees")

#Transform U,V,W Galactocentric velocities to rho, ra, dec proper motion
#First, subtract out solar motion:
V_HC = np.subtract(V_GC,UVW_Sun)
#Create transformation matrices from derived RA and Dec coordinates. A is coordinate transform matrix, C is RA,Dec "velocity" matrix, B is velocity transform matrix from RA,Dec proper motion and radial motion
#to UVW, so we invert it to transform the reverse direction.
#C = [np.cos(Dec)*np.cos(RA),np.cos(Dec)*np.sin(RA),np.sin(Dec)]
A = [[np.cos(RA)*np.cos(Dec),-np.sin(RA),-np.cos(RA)*np.sin(Dec)],[np.sin(RA)*np.cos(Dec),np.cos(RA),-np.sin(RA)*np.sin(Dec)],[np.sin(Dec),0,np.cos(Dec)]]
B = np.dot(T,A)
B_inv = np.linalg.inv(B)

#Multiply heliocentric UVW by inverse transform matrix to get out radial velocity and reduced proper motions. 
parallax = 1/dist
V_prop = np.dot(B_inv,V_HC)
radial = V_prop[0]
vgsr = radial + 10.1*np.cos(b)*np.cos(l)+224.0*np.cos(b)*np.sin(l)+6.7*np.sin(b)
mu_alpha_0 = V_prop[1]*parallax
mu_alpha_as = mu_alpha_0/k
mu_delta_0 = V_prop[2]*parallax
mu_delta_as = mu_delta_0/k
mu_alpha = mu_alpha_as*1000
mu_delta = mu_delta_as*1000
print("Vgsr = " + str(vgsr) + " km/s")
print("RA proper motion = " + str(mu_alpha) + " mas/yr")
print("Dec proper motion = " + str(mu_delta) + " mas/yr")

#XYZ_nodist = np.dot(T,C)

#l_rad = np.arctan2(XYZ_nodist[1],XYZ_nodist[0])

#x_norm_sq = np.power(XYZ_nodist[0],2)
#y_norm_sq = np.power(XYZ_nodist[1],2)

#b_denom_arg = np.add(x_norm_sq,y_norm_sq)
#b_denom = np.sqrt(b_denom_arg)
#b_rad = np.arctan2(XYZ_nodist[2],b_denom)

#l = np.multiply(l_rad,rad2deg)
#b = np.multiply(b_rad,rad2deg)
#if l < 0:
  #l = l + 360
  
#print l
#print b
#XYZ = np.multiply(dist,XYZ_nodist)

#print XYZ

