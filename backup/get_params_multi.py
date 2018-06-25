import math as ma
import scipy as sp
import numpy as np
import files as fi
import os
import csv
import fileinput

np.set_printoptions(threshold=np.nan)
arr = sp.array([0.0])
deg = 180.0 / np.pi
i = 0
def get_params(x,y,z,vx,vy,vz):
	xsol=x+8
	rgal=np.sqrt(np.power(x,2)+np.power(y,2)+np.power(z,2))
	rsol=np.sqrt(np.power(xsol,2)+np.power(y,2)+np.power(z,2))
	vgal=np.sqrt(np.power(vx,2)+np.power(vy,2)+np.power(vz,2)) #incorrect (can't be negative); revisit
	vsol=(xsol*vx+y*vy+z*vz)/rsol
	l=(np.arctan2(y,xsol))*(180.0/np.pi)
	for i in range(len(x)):
	  if l[i] < 0:
	    l[i] = l[i] + 360.0
	b=(np.arctan2(z,np.sqrt(np.power(xsol,2)+np.power(y,2))))*(180.0/np.pi)
	os.system("touch " + str(filename) + "." + str(k) + ".params")
	#params = open(str(filename) + "." + str(k) + ".params",'r+')
	#params.write('\n')
	#params.write('#x,y,z,vx,vy,vz,rgal,vgal,r,vgsr,l,b\n')
	params_list = zip(x,y,z,vx,vy,vz,rgal,vgal,rsol,vsol,l,b)
	params_arr_1 = np.array(params_list)
	np.savetxt(str(filename) + "." + str(k) + ".params", params_arr_1, delimiter=",")
	#params = open(str(filename) + "." + str(k) + ".params",'r+')
	#params.write('\n#x,y,z,vx,vy,vz,rgal,vgal,r,vgsr,l,b\n')
	#params=open(str(filename) + "." + str(k) + ".params",'r+') #terminal command to create file:
	#with open(str(filename) + "." + str(k) + ".params", 'w') as csvfile:
	  #commas = csv.writer(csvfile, delimiter=',',quotechar=' ',quoting=csv.QUOTE_ALL)
	  #commas.writerow([x] + [y] + [z] + [vx] + [vy] + [vz] + [rgal] + [vgal] + [rsol] + [vsol] + [l] + [b])
	  
	#j=0
	#for j in range(len(x)):
		#print >>params, x[j], y[j], z[j], vx[j], vy[j], vz[j], rgal[j], vgal[j], rsol[j], vsol[j], l[j], b[j]

	#params.close()

def line_pre_adder():
  column_titles = str('#x,y,z,vx,vy,vz,rgal,vgal,r,vgsr,l,b\n')
  f = fileinput.input(str(filename) + "." + str(k) + ".params", inplace = 1)
  for xline in f:
    if f.isfirstline():
      print column_titles.rstrip() + '\n'
    else:
      print xline

filename = raw_input("Specify name of data file: ")
iterations = float(raw_input("How many files? "))
k = 0
index = 0
while k < iterations:
	if __name__ == "__main__": 	
		data1=fi.read_file(str(filename) + "." + str(k) + ".orbit", ",")
		x=data1[:,0] #pulls out a single column (note: i=0,1,2,3...)
		y=data1[:,1]
		z=data1[:,2]
		vx=data1[:,3]
		vy=data1[:,4]
		vz=data1[:,5]
		get_params(x,y,z,vx,vy,vz)
		line_pre_adder()
		#replace_commas()
		comp = np.divide(k,iterations)
		comppct = np.multiply(comp,100)
		print str(comppct) + "% complete"
		
	k = k + 1
