import matplotlib.pyplot as plt
import matplotlib.markers
import numpy as np
import random
import csv
import files as fi

#with open('150_orbits.csv', 'r') as csvfile:
  #plots = csv.reader(csvfile, delimiter=',')
  #print csv.line_num
  #for row in plots:
    #l.append(row[10])
    #b.append(row[11])
if __name__ == "__main__": 
  data = fi.read_file("150_orbits.csv", ",")
  lraw = data[:,10]
  braw = data[:,11]
  l_iter = 0
  l_list = []
  b_list = []
  while l_iter < len(lraw):
    n = random.uniform(0,1)
    if n < 0.2:
      l_list.append(lraw[l_iter])
      b_list.append(braw[l_iter])
      l_iter = l_iter + 1
    else:
      l_iter = l_iter + 1
  l = np.array(l_list)
  b = np.array(b_list)

plt.scatter(l,b, c='r', marker='.',s=1)
plt.xlabel('l',fontsize=20)
plt.ylabel('b',fontsize=20)
plt.title('L vs B of 150 Orbits')
plt.show()