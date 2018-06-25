import numpy as np
import files as fi

def get_devs(b,v,r):
  N = len(b)
  b_mean = np.mean(b)
  v_mean = np.mean(v)
  r_mean = np.mean(r)
  bsub = np.subtract(b,b_mean)
  bsq = np.power(bsub,2)
  bquot = np.divide(bsq,N)
  bsum = np.sum(bquot)
  bd = np.sqrt(bsum)
  print str("b error = " + str(bd))
  vsub = np.subtract(v,v_mean)
  vsq = np.power(vsub,2)
  vquot = np.divide(vsq,N)
  vsum = np.sum(vquot)
  vd = np.sqrt(vsum)
  print str("v error = " + str(vd))
  rsub = np.subtract(r,r_mean)
  rsq = np.power(rsub,2)
  rquot = np.divide(rsq,N)
  rsum = np.sum(rquot)
  rd = np.sqrt(rsum)
  print str("r error = " + str(rd))
  print data1
  print data2
  print data3
  

if __name__ == "__main__": 	
	data1 = fi.read_file("bdev")
	data2 = fi.read_file("vdev")
	data3 = fi.read_file("rdev")
	b = data1[:]
	v = data2[:]
	r = data3[:]
	get_devs(b,v,r)