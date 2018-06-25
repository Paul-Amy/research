import numpy as np

l = float(raw_input("Enter l: "))
b = float(raw_input("Enter b: "))
d = float(raw_input("Enter d in kpc: "))

deg2rad = np.divide(3.141592653538979324,180)

lrad = l*deg2rad
brad = b*deg2rad

sinl = np.sin(lrad)
cosl = np.cos(lrad)
sinb = np.sin(brad)
cosb = np.cos(brad)

xang = cosl*cosb
xmult = xang*d
x = xmult - 8

yang = sinl*cosb
y = yang*d

z = sinb*d

print("GC X = " + str(x))
print("GC Y = " + str(y))
print("GC Z = " + str(z))



