import numpy as np
import scipy as sp
import files as fi
import scipy.stats as stats
import os
import csv
from numpy import loadtxt

def calc_p_all_range(v_test):
    r_min = 10
    r_max = 25
    init_range = 2
    range_lim = 15
    r_range = r_max - r_min
    a = r_min
    sig_counter = 0
    test_counter = 0
    while a < r_range:
        l = a + init_range
        while l < a + range_lim + 1:
            k = 0
            range_vgsr_list = []
            while k < n_v:
                if v_test[k,0] > a and v_test[k,0] < a + l:
                    range_vgsr_list.append(v_test[k,1])
                    k = k + 1
                else:
                    k = k + 1
            range_vgsr_arr = np.array(range_vgsr_list)
            if len(range_vgsr_arr) < 2:
                l = l + 1
            else:
                test_counter = test_counter + 1
                D,p = sp.stats.kstest(range_vgsr_arr, 'norm', args = (0,120))
                if p < significance:
                    sig_counter = sig_counter + 1
                    l = l + 1
                else:
                    l = l + 1
        a = a + 1
    #while a < r_max - init_range:
        #range_list = []
        #k = 0
        #l = init_range
        #while k < n_v:
            #while a + l < a + range_lim:
                #if v_test[k,0] > a and v_test[k,0] < a + l:
                    #range_list.append(v_test[k,1])
                    #k = k + 1
                    #l = l + 1
                #else:
                    #k = k + 1
        #range_arr = np.array(range_list)
        #if len(range_arr) < 2:
            #a = a + 1
        #else:
            #D,p = sp.stats.kstest(range_arr, 'norm', args=(0,120))
            #if p < significance:
                #sig_counter = sig_counter + 1
                #a = a + 1
            #else:
                #a = a + 1
    sig_counter_list.append(sig_counter)
    test_counter_list.append(test_counter)

if __name__ == "__main__": 
    filename = "hyllus_on_combined_new_dist.csv" #raw_input("Enter data filename: ")
    data = fi.read_file(str(filename), ",")
    r = data[:,4]
    n_v = len(r)
    significance = 0.00261
    i = 0
    N_iter = 10000
    p_list = []
    sig_counter_list = []
    test_counter_list = []
    while i < N_iter:
        rand_vgsr = np.random.normal(0,120,size=(n_v,))
        r_vgsr = zip(r,rand_vgsr)
        v_test = np.array(r_vgsr)
        calc_p_all_range(v_test)
        i = i + 1
        if i % 100 == 0:
            frac_done = float(i)/float(N_iter)
            pct_done = frac_done*100
            print(str(pct_done) + " percent finished")
    sig_counter_arr = np.array(sig_counter_list)
    test_counter_arr = np.array(test_counter_list)
    N = np.sum(sig_counter_arr)
    tests = np.sum(test_counter_arr)
    print(str(N) + " tests less than " + str(significance) + " out of " + str(tests) + ".")
    #p_array = np.array(p_list)
    #sig_iter = 0
    #sig_count = 0
    #while sig_iter < len(p_array):
        #if p_array[sig_iter] < significance:
            #sig_count = sig_count + 1
            #sig_iter = sig_iter + 1
        #else:
            #sig_iter = sig_iter + 1
    #sig_float = float(sig_count)
    #N_float = float(N_iter)
    #frac = np.divide(sig_float,N_iter)
    #pct = np.multiply(frac,100)
    #print("Results: " + str(sig_count) + " out of " + str(N_iter) + " (" + str(pct) + " percent) iterations yielded a p < " + str(significance))
    