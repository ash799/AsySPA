# -*- coding: utf-8 -*-
"""
Demo to apply the AsyGradientPush algorithm to a multiclass logistic regression problem 
on covtype dataset

To run the demo, run the following:
    mpiexec -n $(num_nodes) python distributed_asy_logistic_regression.py

Created on Sun Jun  3 17:00:07 2018

@author: zhangjiaqi
"""

import numpy as np
import scipy.io as sio 
from logistic_regression import LogisticRegression
from asy_gradient_push import AsyGradientPush
import asy_gradient_push

UID = asy_gradient_push.UID
SIZE = asy_gradient_push.SIZE
#delay = 0.1*((5-UID)**1.5)
delay = 0

def demo_lr_covtype(filepath = 'dataset_covtype/data_partition_3/'):
    """
    Demo to apply the AsyGradientPush algorithm to a multiclass logistic regression problem 
    on covtype dataset

    To run the demo, run the following:
        mpiexec -n $(num_nodes) python distributed_asy_logistic_regression.py
    """
    from logistic_regression import LogisticRegression
    
    # Load the dataset   
    filename = filepath + str(UID) + '.mat'
    data = sio.loadmat(filename)
    samples = data['samples']
    labels = data['labels']
    
    # initialize the problem
    lr = LogisticRegression(samples = samples, labels = labels)
    objective = lr.obj_func
    gradient = lr.gradient
    
    x_start = np.random.randn(lr.n_f, lr.n_c)
    
    pd = AsyGradientPush(objective=objective,
                    sub_gradient=gradient,
                    arg_start= x_start,
                    synch=False,
#                    peers=[(UID + 1) % SIZE, (UID - 1) % SIZE],
                    peers=[(UID + 1) % SIZE],
                    step_size= 0.1 / (lr.n_s * 5),
                    constant_step_size = True,
                    terminate_by_time=True,
                    termination_condition=1500,
                    log=True,
                    in_degree=2,
                    num_averaging_itr=1,
                    delay = delay,
                    exact_convergence=True)
    
    # start the optimization
    loggers = pd.minimize(print_info = True)
#    l_argmin_est = loggers['argmin_est']
#    l_argmin_est.print_gossip_value(UID, label='argmin_est', l2=False)
    
    # Save the data into a mat file
    data_save(samples, labels, loggers, 
              filepath = 'data/3_dis_result_exact_conv_constant_step_0.1_same_freq_nodelay/')
            
def data_save(samples, labels, loggers, filepath = 'data/'):
    """ Save the data into a .mat file. """
    try:
        l_argmin_est = loggers['argmin_est']
        itr = np.fromiter(l_argmin_est.history.keys(), dtype=float)
        t = np.array([i[0] for i in l_argmin_est.history.values()])
        est = np.array([i[1] for i in l_argmin_est.history.values()])
        l_ps_w = loggers['ps_w']
        l_ps_n = loggers['ps_n']
        l_ps_l = loggers['ps_l']
        ps_w = np.array([i[1] for i in l_ps_w.history.values()])
        ps_n = np.array([i[1] for i in l_ps_n.history.values()])
        ps_l = np.array([i[1] for i in l_ps_l.history.values()])
        filename = filepath + str(UID) + '.mat'
        sio.savemat(filename, mdict={'samples': samples, 'labels': labels, 'itr': itr,
                                     'time': t, 'ps_w': ps_w, 'ps_n': ps_n,
                                     'ps_l': ps_l, 'estimate': est})
    except Exception as e:
        print(e)

# Solve the logistic regression problem on covtype dataset
demo_lr_covtype()