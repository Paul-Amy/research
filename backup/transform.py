import numpy as np
from numpy.linalg import inv

deg2rad = np.pi/180

ra_NGP = 192.85*deg2rad
dec_NGP = 27.13*deg2rad
theta_0 = 123*deg2rad

A = [[np.cos(theta), np.sin(theta), 0],[np.sin(theta),-np.cos(theta),0],[0,0,1]]

B = [[-np.sin(dec),0,np.cos(dec)],[0,-1,0],[np.cos(dec),0,np.sin(dec)]]

C = [[np.cos(ra),np.sin(ra),0],[np.sin(ra),-np.cos(ra),0],[0,0,1]]

T_0 = np.dot(A,B)

T = np.dot(T_0,C)

print T