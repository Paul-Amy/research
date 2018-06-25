import numpy as np
import scipy as sp
import files as fi
import scipy.stats as stats
import os
import random

if __name__ == "__main__": 
    data = fi.read_file("hyllus_on_12to18kpc.csv", ",")
    l = data[:,2]
    j = 0
    n_iter = 1000000
    result_list = []
    while j < n_iter:
        test = random.sample(xrange(0,36), 9)
        i = 0
        k = 0
        counter = 0
        test_list = []
        while i < len(test):
            test_list.append(l[test[i]])
            i = i + 1
        test_arr = np.array(test_list)
        while k < len(test_arr):
            if test_arr[k] < 37:
                counter = counter + 1
                k = k + 1
            else:
                k = k + 1
        result_list.append(counter)
        j = j + 1
    result = np.array(result_list)
    a = 0
    master_counter = 0
    while a < len(result):
        if result[a] >= 7:
            master_counter = master_counter + 1
            a = a + 1
        else:
            a = a + 1
    print master_counter
        
    