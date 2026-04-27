# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 08:44:48 2026

@author: alyss
"""

#%% moduls importation 
import os
import subprocess
import time

#%% Execution parameters
def execution_time(program):   
    start = time.perf_counter()
    subprocess.run(f"./{program}", capture_output=True)
    end = time.perf_counter()
    return (end - start)

def WCET_values(file, nb_iter) :
    "nb_iter (int) : nb of iteration of the program"
    
    # Compilation of the file
    program = file[:-2] # We don't keep the ".c"
    os.system(f"gcc {file} -o {program}")    
    
    execution_times = []
    
    for i in range (nb_iter) :
        execution_times.append(execution_time(program))
    
    execution_times.sort()
    min_time = execution_times[0]
    max_time = execution_times[-1]
    
    #numpy.percentile
    Q1 = execution_times[nb_iter//4] # 25%
    Q2 = execution_times[nb_iter//2] # 50% (median)
    Q3 = execution_times[3*nb_iter//4] #75%

    # On pourrait également faire :
    # Q1 = np.percentile(execution_times,25)
    # Q2 = np.percentile(execution_times,50)
    # Q3 = np.percentile(execution_times,75)
    
    avg_time = sum(execution_times)/len(execution_times) #mean
    
    return (min_time, max_time, Q1, Q2, Q3, avg_time)
    
    
    
