import numpy as np
import scipy as sp
import files as fi
import scipy.stats as stats
import os
from decimal import Decimal
from pprint import pprint

def calc_p_all_rng(vgsr,r):
    os.system("touch ks_output_5.csv")
    results = open("ks_output_5.csv",'r+')
    results.write("#p,r_i,r_f,N\n")
    init_dist = 0
    final_dist = 70
    rng = np.subtract(final_dist,init_dist)
    j = 0
    list_iter = 0
    temp_v_list = []
    vgsr_r = zip(vgsr,r)
    while j < rng:
        k = j + 1
        temp_v_list = []
        list_iter = 0
        while k < rng + 1:
            while list_iter < len(r):
                if r[list_iter] > init_dist + j:
                    if r[list_iter] < init_dist + k:
                        temp_v_list.append(vgsr[list_iter])
                        list_iter = list_iter + 1
                    else:
                        list_iter = list_iter + 1
                else: 
                    list_iter = list_iter + 1
            v_test = np.array(temp_v_list)
            N = len(v_test)
            if N == 0:
                temp_v_list = []
                list_iter = 0
                k = k + 1
            else:
                D,p = sp.stats.kstest(v_test, 'norm', args=(0, 120))
                results.write(str(p) + "," + str(init_dist + j) + "," + str(init_dist + k) + "," + str(N) + "\n")
                temp_v_list = []
                list_iter = 0
                k = k + 1
        j = j + 1

def get_least_p():
    p_data = fi.read_file("ks_output_5.csv", ",")
    p_val = p_data[:,0]
    r_i = p_data[:,1]
    r_f = p_data[:,2]
    N = p_data[:,3]
    m = 0
    least_p_list = []
    while m < len(p_val):
        if p_data[m,0] < 0.05:
            if N[m] >=6:
                if r_f[m] - r_i[m] <= 8:
                    if r_f[m] - r_i[m] >= 3:
                        least_p_list.append(p_data[m,:])
                        m = m + 1
                    else:
                        m = m + 1
                else:
                    m = m + 1
            else:
                m = m + 1
        else:
            m = m + 1
    least_p_array = np.array(least_p_list)
    print least_p_array
    
if __name__ == "__main__": 
    os.system("rm ks_output_5.csv")
    np.set_printoptions(suppress=True, formatter={'float_kind':'{:0.8f}'.format})
    filename = raw_input("Enter data filename: ")
    data = fi.read_file(str(filename), ",")
    vgsr = data[:,20]
    r = data[:,18]
    calc_p_all_rng(vgsr,r)
    get_least_p()