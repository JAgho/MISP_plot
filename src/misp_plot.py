# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 16:18:04 2021

@author: JG
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from cbor2 import dumps, loads, load

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
    set_t_m(json)
    mint, maxt = get_sequence_minmax(json)
    lims = find_max_grad(json)
    print("lims are: ", lims)
    centre_axis(ax0, lims)
    ax0.set_ylim(ymin= lims[0]*1.3, ymax= lims[1]*1.3)
    ax0.set_xlim(left=mint, right=maxt+10)
    ax1.set_xlim(left=mint, right=maxt+10)
    
    #arrow = {'arrowstyle':'<->', 'relpos':(0,0)}
    #line = {'arrowstyle':'-', 'relpos':(0,0)}
    for ev in json:
        
        expand_indr(ev)
        print(ev)
        keylist = ev.keys()
        
        for key in keylist:
            if key=="meta":        
                continue
            elif key=="gr_pair":
                plot_trap(ev[key], ax0, offset)
            elif key in ["spoiler1", "spoiler2", "spoiler3"]:
                plot_spoiler(ev[key], ax0, offset)
            elif key=="rf_ex" or key=="rf_ref" or key=="rf_reex":
                plot_RF(ev[key], 1, ax1, offset)
            elif key=="readout":
                plot_ro(ev[key], lims[1]*0.25,  ax0, offset)
            elif key=="fwf_pair":
                plot_fwf(ev[key], ax0, offset)
            elif key=="gr_spiral":    
                plot_spiral(ev[key], ax0, offset)
            
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
    ax0.legend(loc='best', frameon=False, labelspacing=0.3)
    fig.subplots_adjust(hspace=0)
    fig.savefig(fname)
    
def plot_ro(readout, height, axis, offset):
    xpts = np.array([0, 0, readout["t_dur"], readout["t_dur"]])+offset+readout["t_o"]
    ypts = np.array([0,height, height, 0])
    midx = (xpts[1]+xpts[2])/2
    #midy = (ypts[0]+ypts[1])/2
    axis.plot(xpts, ypts, color='black')
    axis.annotate(str("Readout") , xy=(midx, ypts[1]), xytext=(midx-(readout["t_dur"]/2), ypts[1]*1.3))

    
def find_indrs(event):
    path = event.get("meta").get("indr")
    if path:
        with open(path, 'rb') as fp:
            obj = load(fp)
            fp.close()
        return obj
    else:
        return False

def expand_indr(event):
    obj = find_indrs(event)
    if obj:
        for subev in event:
            #print("event is: ", subev)
            for key, entry in event[subev].items():
                if isinstance(entry, dict):
                    name = entry.get("indr", False)
                    if name:
                        event[subev][key] = obj.get(name)
        return True
    else:
        return False
                    
def set_t_m(json):
    flag = len(json)==3 and json[0].get("meta").get("ev_type")=="sPGSE" and json[1].get("meta").get("ev_type")=="diff_pair"
    #print(flag)
    if flag:
        t_m = json[0].get("meta").get("trf").get("t_m", 0)
        if t_m:
            json[0]["meta"]["t_ev"] = json[0]["gr_pair"]["t_bdel"] + t_m
        
    #else:
        #print("DDE is composed of sPGSE and diff_pair objects.")
        
def plot_fwf(grad, axis, offset):
    #print(grad)

    points = fwf_points(grad)
    #print("points are")
    #print(points[0]+ offset, points[0]+ grad.get('b_del')+ offset, points[1])
    #addoff = lambda x: x + grad.get('b_del')
    #offt = map(addoff, points[0])
    
    #print(points)
    try:
        #axis.plot(points[0] + offset, points[1],  color=(0.2,0.4,1,1))
        axis.plot(points[0] + offset, points[1][0,:], color=(0.2,0.4,1,1))
        axis.plot(points[0] + offset, points[1][1,:], color='r')
        axis.plot(points[0] + offset, points[1][2,:], color='g')
    except:
        print("Failed to plot fwf")
    return axis

def fwf_points(grad):
    p1 = len(grad.get("xgrad1"))
    p2 = len(grad.get("xgrad2"))
    arr1 = np.zeros((3, p1), dtype=float)
    arr2 = np.zeros((3, p2), dtype=float)
    
    for i, r in enumerate(["xgrad1", "ygrad1", "zgrad1"]):
        #print(np.array(grad.get(r)).size)
        if np.array(grad.get(r)).size != 1:
            arr1[i,:] = np.array(grad.get(r))*grad.get("ampl")[i]
        
    for i, r in enumerate(["xgrad2", "ygrad2", "zgrad2"]):
        #print(np.array(grad.get(r)).size)
        if np.array(grad.get(r)).size != 1:    
            arr2[i,:] = np.array(grad.get(r))*grad.get("ampl")[i]
    t1 = np.linspace(0, grad.get("t_sdel1"), p1)
    off = grad.get("t_bdel")
    t2 = np.linspace(0, grad.get("t_sdel2"), p2) + off
    #print(arr1, arr2)
    points = (np.concatenate((t1, t2), axis=0), np.concatenate((arr1, arr2), axis=1))
    return points           
                    
def spiral_points(grad):
    p1 = len(grad.get("xgrad1"))
    arr1 = np.zeros((3, p1), dtype=float)
    
    for i, r in enumerate(["xgrad1", "ygrad1", "zgrad1"]):
        #print(np.array(grad.get(r)).size)
        if np.array(grad.get(r)).size != 1 and np.array(grad.get(r)).size != 0:
            arr1[i,:] = np.array(grad.get(r))*grad.get("ampl")[i]
    step = grad.get("raster")
    t1 = np.linspace(0, step*p1, p1)#np.linspace(0, grad.get("t_sdel1"), p1)
    points = (t1, arr1)
    return points

def plot_spiral(grad, axis, offset):
    points = spiral_points(grad)
    print(points)
    try:
        axis.plot(points[0] + offset, points[1][0,:], color=(0.2,0.4,1,1), linewidth=0.5)
        axis.plot(points[0] + offset, points[1][1,:], color='r', linewidth=0.3)
        axis.plot(points[0] + offset, points[1][2,:], color='g', linewidth=0.3)
    except:
        print("Failed to plot fwf")
            
def plot_spoiler(grad, axis, offset):
    points = trap_points(grad)
    try:
        axis.plot(points[0] + offset + grad["t_o"], points[1]*grad["ampl"][0],  color=(0.2,0.4,1,1), linewidth=2)   
        axis.plot(points[0] + offset + grad["t_o"], points[1]*grad["ampl"][1],  color='r', linewidth=2)      
        axis.plot(points[0] + offset + grad["t_o"], points[1]*grad["ampl"][2],  color='g')
        #print("Succesfully plotted Trap")
    except:
        print("Failed to plot Trap")
    return axis

def plot_trap(grad, axis, offset):

    points = trap_points(grad)
    #print("points are")
    #print(points[0]+ offset, points[0]+ grad.get('t_bdel')+ offset, points[1])
    #addoff = lambda x: x + grad.get('b_del')
    #offt = map(addoff, points[0])
    
    #print(points)
    try:
        axis.plot(points[0] + offset, points[1]*grad["ampl"][0],  color=(0.2,0.4,1,1), linewidth=2)
        axis.plot(points[0]+ grad.get('t_bdel') + offset, points[1]*grad["ampl"][0], color=(0.2,0.4,1,1), linewidth=2)
        
        axis.plot(points[0] + offset, points[1]*grad["ampl"][1],  color='r', linewidth=2)
        axis.plot(points[0]+ grad.get('t_bdel') + offset, points[1]*grad["ampl"][1], color='r', linewidth=2)
        
        axis.plot(points[0] + offset, points[1]*grad["ampl"][2],  color='g')
        axis.plot(points[0]+ grad.get('t_bdel') + offset, points[1]*grad["ampl"][2], color='g', linewidth=2)
        

        #print("Succesfully plotted Trap")
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
    
    #print(rf_tup)
    x, y = fixed_width_sinc(rf_tup[0][1],rf_tup[0][2],1)
    axis.plot(x, y, color="black", linewidth=0.5)
    axis.annotate(str(rfevent['FA']) + r"$^{\circ}$" , xy=(rf_tup[0][1], rf_tup[1][1]), xytext=(rf_tup[0][1], rf_tup[1][1]+ (0.05*rf_tup[1][1])))
    axis.set_ylim(0, height*1.3)
    axis.yaxis.set_ticklabels([])
    axis.get_yaxis().set_ticks([])
    tims = str(rf_tup[0])
    amps = str(rf_tup[1])
    #print("Plotting a %s degree RF pulse" % rfevent['FA'])
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
            if abs(minmax[0]) >= maxi:
                maxi = minmax[0]
            if abs(minmax[1]) >= abs(mini):
                mini = minmax[1]
            
    return (mini,maxi)

def get_min_max_grad_in_subevent(key, event):
    typ = key
    if typ=="gr_pair":
        return (max(event["ampl"]), min([min(event["ampl"]), 0]))
    elif typ=="rf_ex":
        return (0,0)
    elif typ=="rf_ref":
        return (0,0)
    elif typ=="readout":
        return (0,0)
    elif typ=="fwf_pair":
        return (max(event["ampl"]), -1*max(event["ampl"]))
    elif typ=="gr_spiral":
        return (max(event["ampl"]), -1*max(event["ampl"]))
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

def centre_axis(axis, lims):
    if lims[0] < 0:
        axis_mid = axis.twiny()
        axis_mid.spines["bottom"].set_position("center")
        make_patch_spines_invisible(axis_mid)
        axis_mid.spines["bottom"].set_visible(True)
        axis_mid.xaxis.set_ticks([])
        axis_mid.get_xaxis().set_ticks([])
    
def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)

# def plot_mde(grad_desc):
#     offset = 0 
#     fig, (ax0, ax1) = plot_nulls()
#     fig.set_size_inches(4, 3)
#     plt.rcParams.update({'font.size': 8})
#     #centre_axis(ax0)
#     lims = find_max_grad(grad_desc, 1.3)
#     ax0.set_ylim(ymin= 0, ymax= lims[1])
#     arrow = {'arrowstyle':'<->', 'relpos':(0,0)}
#     line = {'arrowstyle':'-', 'relpos':(0,0)}
    
#     j = 1
#     offset = 0
#     for i in range(len(grad_desc)):
#         grad = grad_desc.get('grad'+str(i+1))
#         if grad:
#             flag = True
#             while flag:
#                 RF = grad.get('RF'+str(j))
#                 print('RF'+str(j))
#                 if not RF:
#                     flag = False
#                     j=1
#                     break
#                 else:
#                     plot_RF(RF, 1, offset, ax1)
#                     j += 1
            
#             plot_trap(grad, ax0, offset)
            
#             if i == 0:
#                 mint, maxt = get_minmax_time(grad, offset)
#                 print("first loop")
#             else:
#                 a, maxt = get_minmax_time(grad, offset)
#             offset = offset + grad['b_del'] + grad['t_m']
#     #print(mint, "\n", maxt)
#     map(format_axes, [ax0, ax1])
#     ax0.set_xlim(left=mint, right=maxt)
#     ax1.set_xlim(left=mint, right=maxt)
#     ax1.set_xlabel("Time (ms)")
#     ax0.set_ylabel("Gradient Field (" + r"$m T / m$)")
#     ax1.set_ylabel("RF")
#     for tick in ax0.xaxis.get_major_ticks():
#         tick.label1.set_visible(False)
#     #for tick in ax1.xaxis.get_major_ticks():
#         #tick.label1.set_visible(False)
#     #ax1.xaxis.set_ticklabels([])
#     #ax1.get_xaxis().set_ticks([])
#     fig.subplots_adjust(hspace=0)
    
#     return fig