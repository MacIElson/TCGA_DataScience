#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt

# example data
x = np.arange(0.1, 4, 0.5)
y = np.exp(-x)

# example variable error bar values
yerr = 0.1 + 0.2*np.sqrt(x)
xerr = 0.1 + yerr

# First illustrate basic pyplot interface, using defaults where possible.
plt.figure()

x2 = ["1s","2s","3s","4s"]
x = np.array([1,2,3,4])
y = np.array([1,2,3,4])  
ymin = np.array([0,1,2,3])
ymax = np.array([3,6,5,6])
ytop = ymax-y
ybot = y-ymin

# This works
plt.errorbar( x, y, yerr=(ybot, ytop) )
plt.xticks(range(len(x)), x2, size='small')

plt.title("Simplest errorbars, 0.2 in x, 0.4 in y")
plt.show()