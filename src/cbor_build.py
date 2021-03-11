# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 14:24:32 2021

@author: James
"""


from cbor2 import dumps, loads, load
from pathlib import Path
import numpy as np
from parse import compile, parse
from itertools import islice




data_folder = Path(r"./")


def fetch_meta(fp):
    meta = []
    for i, line in enumerate(fp):
        if i == 11:
            break
        meta.append(line)
    pulses = int(parse("NUsedChannels = {}", meta[2]).fixed[0])
    samples = int(parse("Samples = {}", meta[4]).fixed[0])
    
    return pulses, samples

def build_cbor_from_ini(fname):
    g = compile("G[{}]=   {}   {}   {}\n")
    rf = compile("RF[{}]=   {}   {}\n")
    with open(fname, 'r') as fp:
        pulses, samples = fetch_meta(fp)
        it = iter(fp)
        grad = (g.parse(line).fixed[:] for line in it)
        b = np.array(list(islice(grad, samples-1)))
        rflist = []
        for w in range(pulses):
            print(w)
            next(it); next(it); next(it); next(it)
            grad = (rf.parse(line).fixed[:] for line in it)
            rflist.append(np.array(list(islice(grad, samples-1))))
        obj = {}
        obj["xgrad"] = b[:,1].tolist(); obj["ygrad"] = b[:,2].tolist(); obj["zgrad"] = b[:,3].tolist()
        rfx = [str(i) for i in range(len(rflist))]
        rfy = [str(i) for i in range(len(rflist))]
        obj["rf_amp"] = {}
        obj["rf_phase"] = {}
        for rf, x, y in zip(rflist, rfx, rfy):
            obj["rf_amp"][x] = rf[:,1].tolist()
            obj["rf_phase"][y] = rf[:,2].tolist()
    return obj
    

binobj = build_cbor_from_ini(data_folder / "example_spiral_ptx.ini")

#spiral = np.loadtxt(data_folder / "spiral_ms5_short.txt", skiprows=1)

#plt.plot(spiral)

#binobj = {"xgrad":list(spiral[:,0]), "ygrad":list(spiral[:,1]), "zgrad":[]}

binary = dumps(binobj)
with open(data_folder / 'spiralbin.cbor', 'wb') as fp:
    fp.write(binary)
    fp.close()