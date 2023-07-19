import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
import glob
def linear(x,k,b):
    return k*x+b

files = glob.glob('D:\coffee_level\calibration')
print(files)