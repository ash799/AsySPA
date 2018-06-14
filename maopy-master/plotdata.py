# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 15:49:47 2018

@author: zhangjiaqi
"""

import numpy as np
import scipy.io as sio 
from logistic_regression import LogisticRegression
import matplotlib.pyplot as plt

filepath = './dataset_covtype/data_partition_5/'
samples = []
labels = []
for i in range(5):
    data = sio.loadmat(filepath+str(i)+'.mat')
    samples = np.append(samples, data['samples'].ravel(order = 'F'))
    labels = np.append(labels, data['labels'].ravel(order = 'F'))


samples = samples.reshape((data['samples'].shape[0],-1), order = 'F')
labels = labels.reshape((data['labels'].shape[0],-1), order = 'F')
lr = LogisticRegression(samples = samples, labels = labels)

centralized_data = sio.loadmat('./data./centralized_result_1.mat')
f_best = lr.obj_func(centralized_data['estimate'][-1]) / lr.n_s + 0.01
colormap = plt.rcParams['axes.prop_cycle'].by_key()['color']

def plot1():

    # exact convergence
    plotdata = sio.loadmat('./data/dis_result_exact_conv_8/plotdata.mat')
    for i in range(len(plotdata.keys()) - 3):       # 3 irrevalent terms
        t = plotdata['Agent '+ str(i)][0]['time'][0].T
        name = 'Agent '+ str(i)
        f_value = plotdata[name][0]['f_value'][0][0] / lr.n_s
        label = 'Algorithm 2 (baseline)' if i == 0 else '_nolegend_'
        plt.semilogy(t, f_value - f_best, label = label,
                     color = colormap[i])    
    # non-exact convergence
    plotdata = sio.loadmat('./data/dis_result_nonexact_conv_8/plotdata.mat')
    ax = plt.gca()
    #ax.set_xlim([1,3000])
    #ax.set_ylim([5e-2,1e1])
    for i in range(len(plotdata.keys()) - 3):       # 3 irrevalent terms
        t = plotdata['Agent '+ str(i)][0]['time'][0].T
        name = 'Agent '+ str(i)
        f_value = plotdata[name][0]['f_value'][0][0] / lr.n_s
        label = 'Algorithm in [3]' if i == 0 else '_nolegend_'
        plt.semilogy(t, f_value - f_best, label = label,
                     color = colormap[i], linestyle = '--')    
    plt.xlabel('Time (s)')
    plt.ylabel('$f(X)-\hat{f}^\star$')
    plt.title('Training error decay with time')
    plt.legend()
    leg = ax.get_legend()
    for leghandle in leg.legendHandles:
        leghandle.set_color('black')
    plt.savefig("./figs/fig6.pdf", bbox_inches='tight')
    plt.close()


def plot6():

    # exact convergence
    plotdata = sio.loadmat('./data/dis_result_exact_conv_8_same_freq/plotdata.mat')
    for i in range(len(plotdata.keys()) - 3):       # 3 irrevalent terms
        t = plotdata['Agent '+ str(i)][0]['time'][0].T
        name = 'Agent '+ str(i)
        f_value = plotdata[name][0]['f_value'][0][0] / lr.n_s
        label = 'Algorithm 2 (baseline)' if i == 0 else '_nolegend_'
        plt.semilogy(t, f_value - f_best, label = label,
                     color = colormap[0], marker = '^', markevery = 15, ms = 3)    
    # non-exact convergence
    plotdata = sio.loadmat('./data/dis_result_nonexact_conv_8_same_freq/plotdata.mat')
    ax = plt.gca()
    for i in range(len(plotdata.keys()) - 3):       # 3 irrevalent terms
        t = plotdata['Agent '+ str(i)][0]['time'][0].T
        name = 'Agent '+ str(i)
        f_value = plotdata[name][0]['f_value'][0][0] / lr.n_s
        label = 'Algorithm in [3]' if i == 0 else '_nolegend_'
        plt.semilogy(t, f_value - f_best, label = label, color = colormap[1],
                     linestyle=':', marker = 'o', markevery = 20, ms = 3)    
    plt.xlabel('Time (s)')
    plt.ylabel('$f(X)-\hat{f}^\star$')
    plt.title('Training error decay with time (same frequency)')
    plt.legend()
#    leg = ax.get_legend()
#    for leghandle in leg.legendHandles:
#        leghandle.set_color('black')
    plt.savefig("./figs/fig11.pdf", bbox_inches='tight')
    plt.close()

def plot2():

    # error of consensus term, stepsize = 8
    plotdata = sio.loadmat('./data/dis_result_exact_conv_8/plotdata.mat')
    
    est_value = [plotdata['Agent '+ str(i)][0]['est'][0] \
                          for i in range(len(plotdata.keys()) - 3)]
    est_value_mean = np.mean(est_value, axis = 0)
    for i in range(len(plotdata.keys()) - 3):       # 3 irrevalent terms
        name = 'Agent '+ str(i)
        t = plotdata[name][0]['time'][0].T
        est_value = plotdata[name][0]['est'][0]
        est_error = [np.linalg.norm(i) / 5 for i in est_value - est_value_mean]
#        plt.semilogy(t, est_error, label = name, color = colormap[i])    
    # error of consensus term, stepsize = 1
    plotdata = sio.loadmat('./data/dis_result_exact_conv_1/plotdata.mat')
    
    est_value = [plotdata['Agent '+ str(i)][0]['est'][0] \
                          for i in range(len(plotdata.keys()) - 3)]
    est_value_mean = np.mean(est_value, axis = 0)
    ax = plt.gca()
    for i in range(len(plotdata.keys()) - 3):       # 3 irrevalent terms
        name = 'Agent '+ str(i)
        t = plotdata[name][0]['time'][0].T
        est_value = plotdata[name][0]['est'][0]
        est_error = [np.linalg.norm(i) / 5 for i in est_value - est_value_mean]
        label = 'Agent '+ str(i+1)
        plt.semilogy(t, est_error, label = label,
                     color = colormap[i])    
    plt.xlabel('Time (s)')
    plt.ylabel(r'$||X(t)-\bar X(t)||_F$')
    plt.title('Error of consensus term')
    plt.legend()
    leg = ax.get_legend()
    plt.savefig("./figs/fig10.pdf", bbox_inches='tight')
    plt.close()

def plot3():
    # asynchronous
    plotdata = sio.loadmat('./data/dis_result_exact_conv_8/plotdata.mat')
    for i in range(len(plotdata.keys()) - 3):       # 3 irrevalent terms
        t = plotdata['Agent '+ str(i)][0]['time'][0].T
        name = 'Agent '+ str(i)
        f_value = plotdata[name][0]['f_value'][0][0] / lr.n_s
        label = 'Algorithm 2 (baseline)' if i == 0 else '_nolegend_'
        plt.semilogy(t, f_value - f_best, label = label,
                     color = colormap[i])    
    # synchronous with the same delays
#    plotdata = sio.loadmat('./data./syn_dis_delay_same/plotdata.mat')
#    for i in range(len(plotdata.keys()) - 3):       # 3 irrevalent terms
#        t = plotdata['Agent '+ str(i)][0]['time'][0].T
#        name = 'Agent '+ str(i)
#        f_value = plotdata[name][0]['f_value'][0][0] / lr.n_s
#        label = 'Syn-SPA (same delays)' if i == 0 else '_nolegend_'
#        plt.semilogy(t, f_value - f_best, label = label,
#                     color = colormap[i], linestyle = '--')    
    # synchronous with different delays
    plotdata = sio.loadmat('./data./syn_dis_delay_different/plotdata.mat')
    for i in range(len(plotdata.keys()) - 3):       # 3 irrevalent terms
        t = plotdata['Agent '+ str(i)][0]['time'][0].T
        name = 'Agent '+ str(i)
        f_value = plotdata[name][0]['f_value'][0][0] / lr.n_s
        label = 'Syn-SPA' if i == 0 else '_nolegend_'
        plt.semilogy(t, f_value - f_best, label = label,
                     color = colormap[i], linestyle = ':')    
    ax = plt.gca()
    plt.xlabel('Time (s)')
    plt.ylabel('$f(X)-f^\star$')
#    plt.title('Synchronous and asynchronous SPA')
    plt.legend()
    leg = ax.get_legend()
    for leghandle in leg.legendHandles:
        leghandle.set_color('black')
    plt.savefig("./figs/fig7.pdf", bbox_inches='tight')
    plt.close()
    
def plot4():
    
    # stepsize = 10/n_s
    plotdata = sio.loadmat('./data/dis_result_exact_conv_8/plotdata.mat')
    for i in range(len(plotdata.keys()) - 3):       # 3 irrevalent terms
        t = plotdata['Agent '+ str(i)][0]['time'][0].T
        name = 'Agent '+ str(i)
        f_value = plotdata[name][0]['f_value'][0][0] / lr.n_s
        label = r'$\rho(k)={8}n_s^{-1}/\sqrt{k}}$ (baseline)' if i == 0 else '_nolegend_'
        plt.semilogy(t, f_value - f_best, label = label,
                     color = colormap[i])    
    # stepsize = 1/n_s
    plotdata = sio.loadmat('./data./dis_result_exact_conv_1/plotdata.mat')
    for i in range(len(plotdata.keys()) - 3):       # 3 irrevalent terms
        t = plotdata['Agent '+ str(i)][0]['time'][0].T
        name = 'Agent '+ str(i)
        f_value = plotdata[name][0]['f_value'][0][0] / lr.n_s
        label = r'$\rho(k)=n_s^{-1}/\sqrt{k}}$' if i == 0 else '_nolegend_'
        plt.semilogy(t, f_value - f_best, label = label,
                     color = colormap[i], linestyle = '--')    
    # constant stepsize 0.1
    plotdata = sio.loadmat('./data./dis_result_exact_conv_constant_step_0.1/plotdata.mat')
    for i in range(len(plotdata.keys()) - 3):       # 3 irrevalent terms
        t = plotdata['Agent '+ str(i)][0]['time'][0].T
        name = 'Agent '+ str(i)
        f_value = plotdata[name][0]['f_value'][0][0] / lr.n_s
        label = r'$\rho(k)={0.1}{n_s^{-1}}$' if i == 0 else '_nolegend_'
        plt.semilogy(t, f_value - f_best, label = label,
                     color = colormap[i], linestyle = '-.')   
    # constant stepsize 0.3
    plotdata = sio.loadmat('./data./dis_result_exact_conv_constant_step_0.3/plotdata.mat')
    for i in range(len(plotdata.keys()) - 3):       # 3 irrevalent terms
        t = plotdata['Agent '+ str(i)][0]['time'][0].T
        name = 'Agent '+ str(i)
        f_value = plotdata[name][0]['f_value'][0][0] / lr.n_s + 0.01
        label = r'$\rho(k)={0.3}{n_s^{-1}}$' if i == 0 else '_nolegend_'
        plt.semilogy(t, f_value - f_best, label = label,
                     color = 'silver', linestyle = ':', zorder = 0)          
    ax = plt.gca()
    plt.xlabel('Time (s)')
    plt.ylabel('$f(X)-f^\star$')
#    plt.title('Synchronous and asynchronous SPA')
    plt.legend()
    leg = ax.get_legend()
    for leghandle in leg.legendHandles[:-1]:
        leghandle.set_color('black')
    plt.savefig("./figs/fig8.pdf", bbox_inches='tight')   
    plt.close()

def plot5():
    
    # 7 agents
    plotdata = sio.loadmat('./data./7agents/plotdata.mat')
    for i in range(7):       # 3 irrevalent terms
        try:
            t = plotdata['Agent '+ str(i)][0]['time'][0].T
        except KeyError:
            print('Agent '+ str(i),'does not exist.')
            continue
        name = 'Agent '+ str(i)
        f_value = plotdata[name][0]['f_value'][0][0] / lr.n_s
        label = r'7 agents' if i == 1 else '_nolegend_'
        plt.semilogy(t, f_value - f_best, label = label,
                     color = colormap[2], linestyle = ':')       
    # 5 agents
    plotdata = sio.loadmat('./data/dis_result_exact_conv_8/plotdata.mat')
    for i in range(len(plotdata.keys()) - 3):       # 3 irrevalent terms
        t = plotdata['Agent '+ str(i)][0]['time'][0].T
        name = 'Agent '+ str(i)
        f_value = plotdata[name][0]['f_value'][0][0] / lr.n_s
        label = r'5 agents (baseline)' if i == 0 else '_nolegend_'
        plt.semilogy(t, f_value - f_best, label = label,
                     color = colormap[1], linestyle = '--')        
    # 3 agents
    plotdata = sio.loadmat('./data./3agents/plotdata.mat')
    for i in range(len(plotdata.keys()) - 3):       # 3 irrevalent terms
        t = plotdata['Agent '+ str(i)][0]['time'][0].T
        name = 'Agent '+ str(i)
        f_value = plotdata[name][0]['f_value'][0][0] / lr.n_s
        label = r'3 agents' if i == 0 else '_nolegend_'
        plt.semilogy(t, f_value - f_best, label = label,
                     color = colormap[0], linestyle = '-') 
    ax = plt.gca()
    plt.xlabel('Time (s)')
    plt.ylabel('$f(X)-f^\star$')
#    plt.title('Synchronous and asynchronous SPA')
    plt.legend()
    plt.savefig("./figs/fig9.pdf", bbox_inches='tight')  
    plt.close()

def plot7():

    # baseline
    plotdata = sio.loadmat('./data/dis_result_exact_conv_8/plotdata.mat')
    for i in range(len(plotdata.keys()) - 3):       # 3 irrevalent terms
        t = plotdata['Agent '+ str(i)][0]['time'][0].T
        name = 'Agent '+ str(i)
        f_value = plotdata[name][0]['f_value'][0][0] / lr.n_s
        label = 'Ring graph (baseline)' if i == 0 else '_nolegend_'
        plt.semilogy(t, f_value - f_best, label = label,
                     color = colormap[0])    
    # higer connectivity
    plotdata = sio.loadmat('./data/higher_connectivity_exact_8/plotdata.mat')
    ax = plt.gca()
    #ax.set_xlim([1,3000])
    #ax.set_ylim([5e-2,1e1])
    for i in range(len(plotdata.keys()) - 3):       # 3 irrevalent terms
        t = plotdata['Agent '+ str(i)][0]['time'][0].T
        name = 'Agent '+ str(i)
        f_value = plotdata[name][0]['f_value'][0][0] / lr.n_s
        label = 'Higher connectivity' if i == 0 else '_nolegend_'
        plt.semilogy(t, f_value - f_best, label = label,
                     color = colormap[1], linestyle = '--')    
    # undirected graphs
    plotdata = sio.loadmat('./data/higher_connectivity_exact_8_undirected/plotdata.mat')
    for i in range(len(plotdata.keys()) - 3):       # 3 irrevalent terms
        t = plotdata['Agent '+ str(i)][0]['time'][0].T
        name = 'Agent '+ str(i)
        f_value = plotdata[name][0]['f_value'][0][0] / lr.n_s
        label = 'Undirected graph' if i == 0 else '_nolegend_'
        plt.semilogy(t, f_value - f_best, label = label,
                     color = colormap[2], linestyle = ':', zorder = 0)    
    plt.xlabel('Time (s)')
    plt.ylabel('$f(X)-\hat{f}^\star$')
    plt.title('Training error decay with time')
    plt.legend()
#    leg = ax.get_legend()
#    for leghandle in leg.legendHandles:
#        leghandle.set_color('black')
    plt.savefig("./figs/fig12.pdf", bbox_inches='tight')
    plt.close()
    
for i in range(6):
    eval('plot'+str(i+1)+'()')
