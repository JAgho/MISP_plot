# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 19:03:19 2021

@author: JG
"""
import misp_plot as misp
from pathlib import Path



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


print(misp.find_max_grad(spgse))
print(misp.get_sequence_minmax(spgse))



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
        "tr":{}, 
        "ev_type":"sPGSE",
        "t_ev":80}}, # duration of the event
  
  { # Second pulse pair 
   
    "gr_pair":{ 
        "type": "gr_tr", 
        "pair": True,
        "pol": 1,
        "t_bdel": 30,
        "t_r": [2,0,0],
        "t_f": [2,0,0],
        "t_p": [20,0,0],
        "ampl": [0,20,0]},
    
    
    "rf_ref":{"type":"rf_sq", 
              "t_o": 25,
              "FA": 180,
              "t_dur": 3 },
    "meta":{
        "tr":{}, 
        "ev_type":"diff_pair", # identified as a diffusion pulse pair
        "t_ev":70}
    },

  {
   "readout":{"t_o":0, "t_dur":20},
   "meta":{
       "ev_type":"readout",
       "t_ev": 20 }
  }  
    ]

data_folder = Path(r"../output")  

misp.plot_sequence(dde, data_folder / "dde.svg")

misp.plot_sequence(spgse, data_folder / "spgse.svg")
fwf = [
  {    
    "gr_pair":{ # paired free gradient object 
        "pair": True,
        "pol": 1,
        "t_bdel": 30,
        "s_del1": 27.87,
        "s_del2": 22.6,
        "xgrad1": [...],
        "ygrad1": [...],
        "zgrad1": [...],
        "xgrad2": [...],
        "ygrad2": [...],
        "zgrad2": [...],
        "ampl": [50,40,30]},
    
    "rf_ex":{"type":"rf_sq", # RF excitation pulse 
             "t_o": -8,
             "FA": 90,
             "t_dur": 3 },
    
    "rf_ref":{"type":"rf_sq", # Refocusing pulse 
              "t_o": 25,
              "FA": 180,
              "t_dur": 3 },
    
    "tr":{},
    "ev_type":"fwf_pair",
    "t_ev":80}, 

  {
   "ro":{}, 
   "ev_type":"readout",
   "t_ev": 300 
   
   }  
    ]