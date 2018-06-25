import scipy as sp
import numpy as np
import files as fi

filename = raw_input("Input orbit file to be fit: ")
x_col = int(raw_input("Column number of x coordinates: " ))
y_col = int(raw_input("Column number of y coordinates: " ))
order = int(raw_input("Order of fit: "))

orbit = fi.read_file(str(filename), ",")
x_index = x_col - 1
y_index = y_col - 1
x = orbit[:,x_index]
y = orbit[:,y_index]

fit = np.polyfit(x,y,order)

print fit