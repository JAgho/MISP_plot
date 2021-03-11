# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 14:24:32 2021

@author: James
"""


from cbor2 import dumps, loads, load
from pathlib import Path
import numpy as np
from matplotlib import pyplot as plt

data_folder = Path(r"./")

spiral = np.loadtxt(data_folder / "spiral_ms5_short.txt", skiprows=1)

plt.plot(spiral)

binobj = {"xgrad":list(spiral[:,0]), "ygrad":list(spiral[:,1]), "zgrad":[]}

binary = dumps(binobj)
with open(data_folder / 'spiralbin.cbor', 'wb') as fp:
    fp.write(binary)
    fp.close()