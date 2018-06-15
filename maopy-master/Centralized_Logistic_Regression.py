# -*- coding: utf-8 -*-
"""
Created on Fri Jun  1 10:38:01 2018

@author: zhangjiaqi
"""
import numpy as np
import scipy.io as sio 
from logistic_regression import LogisticRegression
from gossip_comm import GossipComm


# Message passing and network variables
COMM = GossipComm.comm
SIZE = GossipComm.size
UID = GossipComm.uid
NAME = GossipComm.name

filepath = './dataset_covtype/'

data = sio.loadmat(filepath+'covtype.mat')
samples = data['samples']
labels = data['labels']


lr = LogisticRegression(samples = samples, labels = labels)
est, est_history, t = lr.minimizer(x_start = None,
                                step_size = 0.1,
                                terminate_by_time=True,
                                termination_condition=1500,
                                log = True,
                                constant_stepsize = True)
#print(str(est), flush=True)

# save the result
if UID == 0:
    filepath = 'data/centralized_5agents_8/centralized_0.5_result_constant_step_0.1.mat'
    sio.savemat(filepath, mdict={'estimate': est_history,
                                 'time': t})

# load the result obtained from asynchronous algorithms
#est_asy = data['estimate'][-1,:,:]
#grad_asy = lr.gradient(est_asy)
#grad_asy_norm = np.linalg.norm(grad_asy)
