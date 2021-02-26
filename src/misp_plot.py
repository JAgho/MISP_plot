# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 16:18:04 2021

@author: JG
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

def plot_nulls():
    fig, (ax0, ax1) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]})
    ax0.plot(0,0, label=r"$x$", color=(0.2,0.4,1,1))
    ax0.plot(0,0, label=r"$y$", color='r')
    ax0.plot(0,0, label=r"$z$", color='g')
    return fig, (ax0, ax1)

def plot_sequence(json, fname):
    offset = 0 
    fig, (ax0, ax1) = plot_nulls()
    fig.set_size_inches(4, 3)
    plt.rcParams.update({'font.size': 8})
    #centre_axis(ax0)
    mint, maxt = get_sequence_minmax(json)
    lims = find_max_grad(json)
    ax0.set_ylim(ymin= lims[0]*1.3, ymax= lims[1]*1.3)
    ax0.set_xlim(left=mint, right=maxt)
    ax1.set_xlim(left=mint, right=maxt)
    arrow = {'arrowstyle':'<->', 'relpos':(0,0)}
    line = {'arrowstyle':'-', 'relpos':(0,0)}
    for ev in json:
        keylist = ev.keys()
        
        for key in keylist:
            if key=="meta":
                continue
            elif key=="gr_pair":
                plot_trap(ev[key], ax0, offset)
            elif key=="rf_ex" or key=="rf_ref":
                plot_RF(ev[key], 1, ax1, offset)
            
        offset += ev["meta"]["t_ev"]
    map(format_axes, [ax0, ax1])

    ax1.set_xlabel("Time (ms)")
    ax0.set_ylabel("Gradient Field (" + r"$m T / m$)")
    ax1.set_ylabel("RF")
    for tick in ax0.xaxis.get_major_ticks():
        tick.label1.set_visible(False)
    #for tick in ax1.xaxis.get_major_ticks():
        #tick.label1.set_visible(False)
    #ax1.xaxis.set_ticklabels([])
    #ax1.get_xaxis().set_ticks([])
    ax0.legend(loc='best')
    fig.subplots_adjust(hspace=0)
    fig.savefig(fname)

def plot_trap(grad, axis, offset):

    points = trap_points(grad)
    print("points are")
    print(points[0]+ offset, points[0]+ grad.get('t_bdel')+ offset, points[1])
    #addoff = lambda x: x + grad.get('b_del')
    #offt = map(addoff, points[0])
    
    #print(points)
    try:
        axis.plot(points[0] + offset, points[1]*grad["ampl"][0],  color=(0.2,0.4,1,1))
        axis.plot(points[0]+ grad.get('t_bdel') + offset, points[1]*grad["ampl"][0], color=(0.2,0.4,1,1))
        
        axis.plot(points[0] + offset, points[1]*grad["ampl"][1],  color='r')
        axis.plot(points[0]+ grad.get('t_bdel') + offset, points[1]*grad["ampl"][1], color='r')
        
        axis.plot(points[0] + offset, points[1]*grad["ampl"][2],  color='g')
        axis.plot(points[0]+ grad.get('t_bdel') + offset, points[1]*grad["ampl"][2], color='g')
        

        print("Succesfully plotted Trap")
    except:
        print("Failed to plot Trap")
    return axis

def trap_points(grad):
    rise = grad.get('t_r')[0]
    plat = grad.get('t_p')[0]
    fall = grad.get('t_f')[0]
    ampl = grad.get('ampl')[0]
    xpts = np.array([0, rise, rise+plat, rise+plat+fall])
    ypts = np.array([0,1, 1, 0])
    return xpts, ypts


def fixed_width_sinc(l, r, height):
    x = np.linspace(l,r,200)
    y = height*np.sinc(np.linspace(2*np.pi, -2*np.pi, 200))
    return x, y

def plot_RF(rfevent, height, axis, offset):
    rf_tup = true_times_RF(rfevent, height, offset)
    
    print(rf_tup)
    x, y = fixed_width_sinc(rf_tup[0][1],rf_tup[0][2],1)
    axis.plot(x, y, color="black", linewidth=0.5)
    axis.annotate(str(rfevent['FA']) + r"$^{\circ}$" , xy=(rf_tup[0][1], rf_tup[1][1]), xytext=(rf_tup[0][1], rf_tup[1][1]+ (0.05*rf_tup[1][1])))
    axis.set_ylim(0, height*1.3)
    axis.yaxis.set_ticklabels([])
    axis.get_yaxis().set_ticks([])
    tims = str(rf_tup[0])
    amps = str(rf_tup[1])
    print("Plotting a %s degree RF pulse" % rfevent['FA'])
    return

def true_times_RF(rfevent, height, offset):
    t1 = rfevent['t_o'] + offset
    #print("RF t1 is %s" % t1)
    t2 = t1
    t3 = t1 + rfevent['t_dur']
    t4 = t3
    tlist = np.asarray([t1,t2,t3,t4])
    a1 = 0
    a2 = height
    a3 = a2
    a4 = 0
    alist = np.asarray([a1,a2,a3,a4])
    return (tlist, alist)       
    
def find_max_grad(json):
    mini = 0
    maxi = 0
    for ev in json:
        keylist = ev.keys()
        for key in keylist:
            if key=="meta":
                continue
            minmax = get_min_max_grad_in_subevent(key, ev[key])
            if minmax[0] >= maxi:
                maxi = minmax[0]
            if minmax[1] >= mini:
                mini = minmax[1]
            
    return (mini,maxi)

def get_min_max_grad_in_subevent(key, event):
    typ = key
    if typ=="gr_pair":
        return (max(event["ampl"]), min(event["ampl"]))
    elif typ=="rf_ex":
        return (0,0)
    elif typ=="rf_ref":
        return (0,0)
    elif typ=="readout":
        return (0,0)
    elif typ=="fwf_pair":
        return (max(event["ampl"]), min(event["ampl"]))
    else:
        return (0,0)
    
def format_axes(axis):
    axis.set_xlim(left=0)
    axis.spines['right'].set_visible(False)
    axis.spines['top'].set_visible(False)

def get_sequence_minmax(json):
    maxi, mini = 0, 0
    offset = 0
    for ev in json:
        maxi += ev["meta"]["t_ev"]
    for ev in json:
        for key, value in ev.items():
            mini = min([value.get("t_o", 0) + offset, mini])   
    return (mini, maxi)

def plot_mde(grad_desc):
    offset = 0 
    fig, (ax0, ax1) = plot_nulls()
    fig.set_size_inches(4, 3)
    plt.rcParams.update({'font.size': 8})
    #centre_axis(ax0)
    lims = find_max_grad(grad_desc, 1.3)
    ax0.set_ylim(ymin= 0, ymax= lims[1])
    arrow = {'arrowstyle':'<->', 'relpos':(0,0)}
    line = {'arrowstyle':'-', 'relpos':(0,0)}
    
    j = 1
    offset = 0
    for i in range(len(grad_desc)):
        grad = grad_desc.get('grad'+str(i+1))
        if grad:
            flag = True
            while flag:
                RF = grad.get('RF'+str(j))
                print('RF'+str(j))
                if not RF:
                    flag = False
                    j=1
                    break
                else:
                    plot_RF(RF, 1, offset, ax1)
                    j += 1
            
            plot_trap(grad, ax0, offset)
            
            if i == 0:
                mint, maxt = get_minmax_time(grad, offset)
                print("first loop")
            else:
                a, maxt = get_minmax_time(grad, offset)
            offset = offset + grad['b_del'] + grad['t_m']
    #print(mint, "\n", maxt)
    map(format_axes, [ax0, ax1])
    ax0.set_xlim(left=mint, right=maxt)
    ax1.set_xlim(left=mint, right=maxt)
    ax1.set_xlabel("Time (ms)")
    ax0.set_ylabel("Gradient Field (" + r"$m T / m$)")
    ax1.set_ylabel("RF")
    for tick in ax0.xaxis.get_major_ticks():
        tick.label1.set_visible(False)
    #for tick in ax1.xaxis.get_major_ticks():
        #tick.label1.set_visible(False)
    #ax1.xaxis.set_ticklabels([])
    #ax1.get_xaxis().set_ticks([])
    fig.subplots_adjust(hspace=0)
    
    return fig