# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 19:03:19 2021

@author: JG
"""
import misp_plot as misp
from pathlib import Path
from cbor2 import dumps, loads
import time
import matplotlib.pyplot as plt



spgse = [
  { # we must uniquely name each subevent in a list to schematically seperate their roles in defining sequence behaviour
   
    "gr_pair":{ # paired gradient object (permits shifting big delta)
        "pol": 1,
        "t_bdel": 30,
        "t_r": [2,0,0],
        "t_f": [2,0,0],
        "t_p": [20,0,0],
        "ampl": [50,0,0]},
    
    "rf_ex":{ # RF excitation pulse (stable in time)
             "t_o": -8,
             "FA": 90,
             "t_dur": 3 },
    
    "rf_ref":{ # Refocusing pulse (likely to move with big delta)
              "t_o": 25,
              "FA": 180,
              "t_dur": 3 },
    
    "readout":{"t_o":70,
               "t_dur":20},
    
    "meta":{
        "tr":{}, # object to specify multiparametric transforms which modify multiple data
                 # for example we could specify big delta as a transform here to move both
                 # the gradient pulse and the RF pulse by a programmaticaly determined amount
                 # alternatively we can change just spgse[1][1]["t_bdel"] = ...
        
        "ev_type":"sPGSE", # type of event - helps to label grouped subevents under a single
                           # label, permitting us to know we may call a particular function on
                           # this grouped event
        
        "t_ev":90}} # duration of the event
    ]


#print(misp.find_max_grad(spgse))
#print(misp.get_sequence_minmax(spgse))



dde = [
  {   
    "gr_pair":{  
        "pol": 1,
        "t_bdel": 30,
        "t_r": [2,0,0],
        "t_f": [2,0,0],
        "t_p": [20,0,0],
        "ampl": [50,0,0]},
    
    "rf_ex":{
             "t_o": -8,
             "FA": 90,
             "t_dur": 3 },
    
    "rf_ref":{
              "t_o": 25,
              "FA": 180,
              "t_dur": 3 },
    "meta":{
        "trf":{"t_m":60}, 
        "ev_type":"sPGSE",
        "t_ev":80}}, # duration of the event
  
  { # Second pulse pair 
   
    "gr_pair":{ 
        "pol": 1,
        "t_bdel": 30,
        "t_r": [2,0,0],
        "t_f": [2,0,0],
        "t_p": [20,0,0],
        "ampl": [0,20,0]},
    
    
    "rf_ref":{ 
              "t_o": 25,
              "FA": 180,
              "t_dur": 3 },
    "meta":{
        "trf":{}, 
        "ev_type":"diff_pair", # identified as a diffusion pulse pair
        "t_ev":70}
    },

  {
   "readout":{"t_o":0, "t_dur":20},
   "meta":{
       "trf":{},
       "ev_type":"readout",
       "t_ev": 20 }
  }  
    ]


fwf = [
  {    
    "fwf_pair":{ # paired free gradient object 
        "pol": 1,
        "t_bdel": 30,
        "t_sdel1": 27.87,
        "t_sdel2": 22.6,
        "xgrad1": {"indr":"xgrad1"},
        "ygrad1": {"indr":"ygrad1"},
        "zgrad1": {"indr":"zgrad1"},
        "xgrad2": {"indr":"xgrad2"},
        "ygrad2": {"indr":"ygrad2"},
        "zgrad2": {"indr":"zgrad2"},
        "ampl": [50,40,30]},
    
    "rf_ex":{ # RF excitation pulse 
             "t_o": -8,
             "FA": 90,
             "t_dur": 3 },
    
    "rf_ref":{ # Refocusing pulse 
              "t_o": 27.87,
              "FA": 180,
              "t_dur": 3 },
    
    "meta":{
    "trf":{},
    "ev_type":"fwf_pair",
    "indr":"../output/fwfbin.cbor",
    "t_ev":65}}, 

  {
   "readout":{"t_o":0, "t_dur":20}, 
   "meta":{
       "trf":{},
       "ev_type":"readout",
       "t_ev": 20 }
   
   }  
    ]

fwfbin = {
    "xgrad1": [0, 0.46127, 0.45644, 0.44544, 0.42466, 0.38548, 0.30815, 0.23679, 0.19735, 0.15406, 0.10712, 0.05675, 0.00325, -0.05302, -0.11163, -0.17204, -0.23363, -0.29566, -0.35389, -0.40361, -0.45494, -0.51112, -0.57867, -0.62482, -0.66228, -0.6916, -0.71165, -0.72139, -0.71987, -0.70631, -0.68009, -0.5978, -0.46921, -0.36978, -0.293, -0.23009, -0.17507, 0], 
    "ygrad1": [0, 0.72056, 0.72054, 0.72056, 0.72076, 0.72098, 0.71842, 0.62712, 0.46465, 0.28768, 0.10205, -0.08611, -0.27059, -0.44527, -0.60437, -0.7426, -0.85534, -0.93882, -0.97661, -0.96377, -0.94253, -0.91106, -0.86409, -0.75679, -0.62064, -0.46211, -0.28634, -0.09908, 0.09352, 0.28509, 0.46925, 0.60402, 0.66208, 0.70044, 0.72909, 0.75194, 0.77045, 0], 
    "zgrad1": [0, 0.6028, 0.60649, 0.61459, 0.6289, 0.6534, 0.69589, 0.7031, 0.66889, 0.62962, 0.58575, 0.53775, 0.48615, 0.43148, 0.37427, 0.31505, 0.25433, 0.19259, 0.12783, 0.05991, -0.004, -0.06386, -0.11764, -0.17679, -0.23537, -0.29256, -0.34822, -0.40224, -0.45451, -0.50492, -0.55337, -0.61085, -0.66093, -0.6841, -0.69132, -0.69064, -0.68637, 0], 
    "xgrad2": [0, 0.13595, 0.0977, 0.05475, 0.00506, -0.05502, -0.13325, -0.2516, -0.47483, -0.63685, -0.7071, -0.7468, -0.77092, -0.78454, -0.78958, -0.78657, -0.77515, -0.75423, -0.72171, -0.67383, -0.60282, 0.06818, 0.15535, 0.18555, 0.20569, 0.21994, 0.23008, 0.23708, 0.24148, 0.24361, 0], 
    "ygrad2": [0, -0.61042, -0.64525, -0.68069, -0.71759, -0.75737, -0.80255, -0.85785, -0.90114, -0.82708, -0.72882, -0.6292, -0.52822, -0.42451, -0.31663, -0.20321, -0.08279, 0.04628, 0.18613, 0.33999, 0.51395, 1, 0.96569, 0.96151, 0.95943, 0.95808, 0.95712, 0.95644, 0.956, 0.95579, 0], 
    "zgrad2": [0, 0.83919, 0.8182, 0.79311, 0.76183, 0.72021, 0.65841, 0.54419, 0.24048, -0.07555, -0.25331, -0.3765, -0.47118, -0.54739, -0.60963, -0.65982, -0.6983, -0.72412, -0.73473, -0.72505, -0.68396, 0.30116, 0.37236, 0.36936, 0.36404, 0.35925, 0.35544, 0.35265, 0.35084, 0.34995, 0],
    }



fexi = [
  { # we must uniquely name each subevent in a list to schematically seperate their roles in defining sequence behaviour
   
    "gr_pair":{ # paired gradient object (permits shifting big delta)
        "pol": 1,
        "t_bdel": 35,
        "t_r": [2,0,0],
        "t_f": [2,0,0],
        "t_p": [20,0,0],
        "ampl": [40,0,0]},
    
    "rf_ex":{ # RF excitation pulse (stable in time)
             "t_o": -8,
             "FA": 90,
             "t_dur": 3 },
    
    "rf_ref":{ # Refocusing pulse (likely to move with big delta)
              "t_o": 25,
              "FA": 180,
              "t_dur": 3 },
    
    
    "meta":{
        "trf":{}, # object to specify multiparametric transforms which modify multiple data
                 # for example we could specify big delta as a transform here to move both
                 # the gradient pulse and the RF pulse by a programmaticaly determined amount
                 # alternatively we can change just spgse[1][1]["t_bdel"] = ...
        
        "ev_type":"sPGSE", # type of event - helps to label grouped subevents under a single
                           # label, permitting us to know we may call a particular function on
                           # this grouped event
        
        "t_ev":70}}, # duration of the event
  
  {"gr_pair":{ # paired gradient object (permits shifting big delta)
        "pol": 1,
        "t_bdel": 120,
        "t_r": [1,0,0],
        "t_f": [1,0,0],
        "t_p": [8,0,0],
        "ampl": [10,3,6]},
    
    "rf_ex":{ # RF excitation pulse (stable in time)
             "t_o": 15,
             "FA": 90,
             "t_dur": 3 },
    "rf_reex":{ # RF excitation pulse (stable in time)
             "t_o": 110,
             "FA": 90,
             "t_dur": 3 },
    
    
    "spoiler1":{ # paired gradient object (permits shifting big delta)
        "t_o": 40,
        "t_r": [1,0,0],
        "t_f": [1,0,0],
        "t_p": [16,0,0],
        "ampl": [7,3,5]},
    
    
    "meta":{
        "trf":{}, # object to specify multiparametric transforms which modify multiple data
                 # for example we could specify big delta as a transform here to move both
                 # the gradient pulse and the RF pulse by a programmaticaly determined amount
                 # alternatively we can change just spgse[1][1]["t_bdel"] = ...
        
        "ev_type":"fexi_spoil", # type of event - helps to label grouped subevents under a single
                           # label, permitting us to know we may call a particular function on
                           # this grouped event
        
        "t_ev":140}},
  
  { # we must uniquely name each subevent in a list to schematically seperate their roles in defining sequence behaviour
   
    "gr_pair":{ # paired gradient object (permits shifting big delta)
        "pol": 1,
        "t_bdel": 35,
        "t_r": [2,0,0],
        "t_f": [2,0,0],
        "t_p": [20,0,0],
        "ampl": [40,0,0]},
    
    
    "rf_ref":{ # Refocusing pulse (likely to move with big delta)
              "t_o": 25,
              "FA": 180,
              "t_dur": 3 },
    
    
    "readout":{"t_o":70,
               "t_dur":20},
    
    "meta":{
        "trf":{}, # object to specify multiparametric transforms which modify multiple data
                 # for example we could specify big delta as a transform here to move both
                 # the gradient pulse and the RF pulse by a programmaticaly determined amount
                 # alternatively we can change just spgse[1][1]["t_bdel"] = ...
        
        "ev_type":"diff_pair", # type of event - helps to label grouped subevents under a single
                           # label, permitting us to know we may call a particular function on
                           # this grouped event
        
        "t_ev":120}}
  

    ]

spiral = [
    {
    "gr_pair":{ # paired gradient object (permits shifting big delta)
        "pol": 1,
        "t_bdel": 30,
        "t_r": [2,0,0],
        "t_f": [2,0,0],
        "t_p": [20,0,0],
        "ampl": [50,0,0]},
    
    "rf_ex":{ # RF excitation pulse (stable in time)
             "t_o": -8,
             "FA": 90,
             "t_dur": 3 },
    
    "rf_ref":{ # Refocusing pulse (likely to move with big delta)
              "t_o": 25,
              "FA": 180,
              "t_dur": 3 },
    
    
    "meta":{
        "tr":{}, # object to specify multiparametric transforms which modify multiple data
                 # for example we could specify big delta as a transform here to move both
                 # the gradient pulse and the RF pulse by a programmaticaly determined amount
                 # alternatively we can change just spgse[1][1]["t_bdel"] = ...
        
        "ev_type":"sPGSE", # type of event - helps to label grouped subevents under a single
                           # label, permitting us to know we may call a particular function on
                           # this grouped event
        
        "t_ev":70}}, # duration of the event

  {
   "gr_spiral":{
       "xgrad1": {"indr":"xgrad"},
       "ygrad1": {"indr":"ygrad"},
       "zgrad1": {"indr":"zgrad"},
       "ampl":[60, 59, 0],
       "raster":0.010, #dur 34.06ms
       "t_o":0, 
       "t_dur":20},
   "readout_spiral": {
       "FOV":[230,230,230],
       "res":[1.5, 1.5, 0]
       },
   "meta":{
       "trf":{},
       "indr":"../output/spiralbin.cbor",
       "ev_type":"readout",
       "t_ev": 40 }
   
   }  
    ]

spokes = [
  { # we must uniquely name each subevent in a list to schematically seperate their roles in defining sequence behaviour
   
    "gr_pair":{ # paired gradient object (permits shifting big delta)
        "pol": 1,
        "t_bdel": 30,
        "t_r": [2,0,0],
        "t_f": [2,0,0],
        "t_p": [20,0,0],
        "ampl": [50,0,0]},
    
    "rf_wav":{
        "t_o":-12.67,
        "channels":8,
        "samples":1268,
        "raster":0.010,
        "rf_amp":{"indr":"rf_amp"},
        "rf_phase":{"indr":"rf_phase"}, 
        "xgrad1": {"indr":"xgrad"},
        "ygrad1": {"indr":"ygrad"},
        "zgrad1": {"indr":"zgrad"},
        },
    
    "rf_ex":{ # RF excitation pulse (stable in time)
             "t_o": -8,
             "FA": 90,
             "t_dur": 3 },
    
    "rf_ref":{ # Refocusing pulse (likely to move with big delta)
              "t_o": 25,
              "FA": 180,
              "t_dur": 3 },
    
    "readout":{"t_o":70,
               "t_dur":20},
    
    "meta":{
        "tr":{}, # object to specify multiparametric transforms which modify multiple data
                 # for example we could specify big delta as a transform here to move both
                 # the gradient pulse and the RF pulse by a programmaticaly determined amount
                 # alternatively we can change just spgse[1][1]["t_bdel"] = ...
        "indr":"../output/spiralrf.cbor",
        "ev_type":"sPGSE", # type of event - helps to label grouped subevents under a single
                           # label, permitting us to know we may call a particular function on
                           # this grouped event
        
        "t_ev":90}} # duration of the event
    ]



#binary = dumps(fwfbin)
#with open(data_folder / 'fwfbin.cbor', 'wb') as fp:
#    fp.write(binary)
#    fp.close()
# for event in fwf:
#     print(misp.expand_indr(event))
def plot_8rf():
    fig, (axes) = plt.subplots(9, 1, gridspec_kw={'height_ratios': [4, 1,1,1,1,1,1,1,1]})
    axes[0].plot(0,0, label=r"$x$", color=(0.2,0.4,1,1))
    axes[0].plot(0,0, label=r"$y$", color='r')
    axes[0].plot(0,0, label=r"$z$", color='g')
    plt.rcParams.update({'font.size': 8})
    axes[8].set_xlabel("Time (ms)")
    axes[0].set_ylabel("Gradient " + r"($m T / m$)")
    for i in range(8):
        axes[i+1].set_ylabel("RF"+str(i+1))
    for tick in axes[0].xaxis.get_major_ticks():
        tick.label1.set_visible(False)
    fig.subplots_adjust(hspace=0)
    
    return fig, (axes)

fig, (axes) = plot_8rf()

data_folder = Path(r"../output")

for ev in spokes:
    misp.expand_indr(ev)

#for rf in spokes[0]["rf_wav"]["rfx"].values():
 #   print(rf)
t1, grads, rf = misp.RF_waveform_points(spokes[0]["rf_wav"])    
axes[0].plot(t1, grads[0],  color=(0.2,0.4,1,1)) 
axes[0].plot(t1, grads[1], color='r') 
axes[0].plot(t1, grads[2], color='g')
axes[0].yaxis.set_ticklabels([])
axes[0].get_yaxis().set_ticks([])
for i in range(8):
    axes[i+1].plot(t1, rf[i][0]*20, linewidth = 0.5, color='b'); axes[i+1].plot(t1, rf[i][1], linewidth = 0.5, color='g')
    axes[i+1].yaxis.set_ticklabels([])
    axes[i+1].get_yaxis().set_ticks([])
fig.savefig(data_folder / "rf_spiral.svg")
#misp.plot_sequence(dde, data_folder / "dde.svg")

#misp.plot_sequence(spgse, data_folder / "spgse.svg")
#misp.plot_sequence(fwf, data_folder / "fwf.svg")
#misp.plot_sequence(fexi, data_folder / "fexi.svg")

#misp.plot_sequence(spiral, data_folder / "spiral.svg")

#a = time.perf_counter()
#misp.expand_indr(fwf[0])
#b = time.perf_counter()

#print("elapsed time: ", (b-a)*10e6, "us")