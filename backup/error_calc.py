import math as ma
import numpy as np
l = float(raw_input("Enter l value: "))
b = float(raw_input("Enter b value: "))
d = float(raw_input("Enter d value: "))
sig_l = float(raw_input("Enter l error: "))
sig_b = float(raw_input("Enter b error: "))
sig_d = float(raw_input("Enter d error: "))

deg2rad = 3.1415926535897932385/180

l_rad = l*deg2rad
b_rad = b*deg2rad

dx_dd = ma.cos(b_rad)*ma.cos(l_rad)
dx_db = -d*ma.sin(b_rad)*ma.cos(l_rad)
dx_dl = -d*ma.cos(b_rad)*ma.sin(l_rad)

dy_dd = ma.cos(b_rad)*ma.sin(l_rad)
dy_db = -d*ma.sin(b_rad)*ma.sin(l_rad)
dy_dl = d*ma.cos(b_rad)*ma.cos(l_rad)

dz_dd = ma.sin(b_rad)
dz_db = d*ma.cos(b_rad)
dz_dl = 0

sig_x_d = dx_dd*sig_d
sig_x_b = dx_db*sig_b
sig_x_l = dx_dl*sig_l

sig_y_d = dy_dd*sig_d
sig_y_b = dy_db*sig_b
sig_y_l = dy_dl*sig_l

sig_z_d = dz_dd*sig_d
sig_z_b = dz_db*sig_b
sig_z_l = dz_dl*sig_l

sig_x_d_sq = np.power(sig_x_d,2)
sig_x_b_sq = np.power(sig_x_b,2)
sig_x_l_sq = np.power(sig_x_l,2)

sig_y_d_sq = np.power(sig_y_d,2)
sig_y_b_sq = np.power(sig_y_b,2)
sig_y_l_sq = np.power(sig_y_l,2)

sig_z_d_sq = np.power(sig_z_d,2)
sig_z_b_sq = np.power(sig_z_b,2)
sig_z_l_sq = np.power(sig_z_l,2)

sig_x_sq = sig_x_d_sq + sig_x_b_sq + sig_x_l_sq
sig_x = np.sqrt(sig_x_sq)
print("X error = " + str(sig_x))

sig_y_sq = sig_y_d_sq + sig_y_b_sq + sig_y_l_sq
sig_y = np.sqrt(sig_y_sq)
print("Y error = " + str(sig_y))

sig_z_sq = sig_z_d_sq + sig_z_b_sq + sig_z_l_sq
sig_z = np.sqrt(sig_z_sq)
print("Z error = " + str(sig_z))