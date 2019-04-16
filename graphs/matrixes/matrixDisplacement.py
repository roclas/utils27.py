#!/usr/bin/env python

import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np

#data = np.random.rand(10, 10) * 20
data = [
[0,0,0,0,11,0,11,0,0,0],
[0,0,0,0,11,0,11,0,0,0],
[0,0,0,0,11,0,11,0,0,0],
[0,0,0,0,11,0,11,0,0,0],
[0,0,0,0,11,0,11,0,0,0],
[0,0,0,0,11,0,11,0,0,0],
[0,0,0,0,11,0,11,0,0,0],
[0,0,0,0,11,0,11,0,0,0],
[0,0,0,0,11,0,11,0,0,0],
[0,0,0,0,11,0,11,0,0,0]]
angle= [
[0,1,0,0,0,0,0,0,0,0],
[0,0,1,0,0,0,0,0,0,0],
[0,0,0,1,0,0,0,0,0,0],
[0,0,0,0,1,0,0,0,0,0],
[0,0,0,0,0,1,0,0,0,0],
[0,0,0,0,0,0,1,0,0,0],
[0,0,0,0,0,0,0,1,0,0],
[0,0,0,0,0,0,0,0,1,0],
[0,0,0,0,0,0,0,0,0,1],
[0,0,0,0,0,0,0,0,0,0]]



def paintMatrix(m):
    # create discrete colormap
    cmap = colors.ListedColormap(['red', 'blue'])
    bounds = [0,10,20]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    fig, ax = plt.subplots()
    ax.imshow(m, cmap=cmap, norm=norm)
    
    # draw gridlines
    ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
    ax.set_xticks(np.arange(-.5, 10, 1));
    ax.set_yticks(np.arange(-.5, 10, 1));
    
    plt.show()

newdata=np.matrix(data)

for i in range(7):
    paintMatrix(newdata)
    newdata*=np.matrix(angle)
