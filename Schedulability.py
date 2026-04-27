# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 08:45:38 2026

@author: alyss
"""
# Pour run : python3 schedulability.py

#%% importation of the modules
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from functools import reduce # for the hyperperiod
import WCET

#%% tree
C1 = WCET.WCET_values("Task_1.c", nb_iter = 10000) 
# return in order : min_time, max_time, Q1, Q2, Q3, avg_time

print("Min : ", C1[0]," s")
print("Max : ", C1[1]," s")
print("Q1 : ", C1[2]," s")
print("Q2 : ", C1[3]," s")
print("Q3 : ", C1[4]," s")
print("Mean : ", C1[5]," s") 

#C1 is the Worst Case Execution time
C1 = math.floor(C1[1]*1000) # max_time
print ("WCET is", C1, " ms")
#%% 
tasks = np.array([["t1", C1, 10],
                  ["t2", 3, 10],
                  ["t3", 2, 20],
                  ["t4", 2, 20],
                  ["t5", 2, 40],
                  ["t6", 2, 40],
                  ["t7", 3, 80]])



#%% Scheduling Algorithms

def lcm(a, b): # for the hyperperiod
    return a * b // math.gcd(a, b)

def EDF(tasks):
    ''' 
    Input : array with the tasks [name, execution_time, period/deadline]
    Output : waiting_time, schedule
    '''
    nb_task = tasks.shape[0]
    
    names = tasks[:, 0]
    C = tasks[:, 1].astype(int) # execution time (astype because they are read as strings)
    T = tasks[:, 2].astype(int) # period/deadline

    hyperperiod = reduce(lcm, T)

    remaining     = np.zeros(nb_task,)  # the time necessary to complete the task
    next_release  = np.zeros(nb_task)  # the next time the task is available
    deadline      = np.zeros(nb_task) # the next deadline of each task
    waiting_time  = np.zeros(nb_task,) # the waiting time for each task
    
    schedule      = []                             

    t = 0
    while t < hyperperiod: # We run the simulation for one hyperperiod
        min_deadline = float("inf")
        for i in range(nb_task):
            if t == next_release[i]: #if the task is released
                remaining[i] = C[i]
                deadline[i] = t + T[i] #it need to be executed before the next period
                next_release[i] += T[i]

        chosen = -1
        min_deadline = float("inf")
        for i in range(nb_task):
            if remaining[i] > 0 and deadline[i] < min_deadline: #if there is a task non completed and with deadline earlier than the current minimum : 
                min_deadline = deadline[i]
                chosen = i

        # Add the waiting time for the tasks that are not chosen
        for i in range(nb_task):
            if remaining[i] > 0 and i != chosen:
                waiting_time[i] += 1

        # Execute the chosen task
        if chosen != -1:
            remaining[chosen] -= 1
            schedule.append(chosen)
            # Verification deadline miss
            if remaining[chosen] > 0 and t + 1 > deadline[chosen]:
                print(f"Deadline miss for task {names[chosen]} at t={t+1}")
                return None, schedule
        else: #if there is no task to execute
            schedule.append(-1)

        t += 1

    print(f"Total waiting time for EDF : {sum(waiting_time)}")

    return waiting_time, schedule

def RMS(tasks):
    ''' 
    Input : array with the tasks [name, execution_time, period/deadline]
    Output : waiting_time, schedule
    '''
    nb_task = tasks.shape[0]
    
    names = tasks[:, 0]
    C = tasks[:, 1].astype(int) # execution time
    T = tasks[:, 2].astype(int) # period/deadline
    hyperperiod = reduce(lcm, T)

    remaining = np.zeros(nb_task,)  # the time necessary to complete the task
    next_release = np.zeros(nb_task)  # the next time the task is available

    waiting_time = np.zeros(nb_task,) # the waiting time for each task
    schedule = []  

    t = 0
    while t < hyperperiod: # We run the simulation for one hyperperiod  
        chosen = -1
        min_period = float("inf")
        for i in range(nb_task): # State of each task at time t
             if t == next_release[i]:
                remaining[i] = C[i]
                next_release[i] += T[i]

        for i in range(nb_task): # Choice of the task to execute : the one with the shortest period
            if remaining[i] > 0:  # task ready to execute
                if T[i] < min_period:
                    min_period = T[i]
                    chosen = i

        for i in range(nb_task): # Add the waiting time for the tasks that are not chosen
            if remaining[i] > 0 and i != chosen:
                waiting_time[i] += 1

        if chosen != -1: # Execute the chosen task
            remaining[chosen] -= 1
            schedule.append(chosen)

        else: #if there is no task to execute
            schedule.append(-1)

        t += 1

    print(f"Total waiting time for RMS : {sum(waiting_time)}")  

    return waiting_time, schedule

#Plot of the scheduling

def plot_schedule(schedule, tasks, hyperperiod): #made with IA for the visualization of the schedule
    names = tasks[:, 0]
    C = tasks[:, 1].astype(int)
    T = tasks[:, 2].astype(int)
    nb_task = tasks.shape[0]

    colors = plt.cm.tab10.colors

    fig, ax = plt.subplots(figsize=(14, nb_task * 1.5))

    for i in range(nb_task):
        # Périodes en arrière plan (couleur claire)
        t_period = 0
        while t_period < hyperperiod:
            ax.barh(i, T[i], left=t_period, height=0.6,
                    color=colors[i % 10], alpha=0.15, edgecolor="grey", linewidth=0.5)
            t_period += T[i]

        for t, task_idx in enumerate(schedule):
            if task_idx == i:
                ax.barh(i, 1, left=t, height=0.6,
                        color=colors[i % 10], alpha=0.9, edgecolor="white", linewidth=0.5)

    ax.set_xlim(0, hyperperiod)
    ax.set_xlabel("Time")
    ax.set_yticks(range(nb_task))
    ax.set_yticklabels(names)
    ax.set_title("Scheduling EDF")
    ax.xaxis.set_major_locator(plt.MultipleLocator(1))
    ax.grid(axis="x", linestyle="--", alpha=0.4)

    legend = [mpatches.Patch(color=colors[i % 10], label=f"{names[i]} (C={C[i]}, T={T[i]})")
              for i in range(nb_task)]
    ax.legend(handles=legend, loc="upper right")

    plt.tight_layout()
    plt.show()

    return

# Comparision of the two algorithms
waiting_time_RMS, schedule_RMS = RMS(tasks)
waiting_time_EDF, schedule_EDF = EDF(tasks)
hyperperiod = reduce(lcm, tasks[:,2].astype(int))
#plot_schedule(schedule_EDF, tasks, hyperperiod)
