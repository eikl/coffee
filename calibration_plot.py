import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
import glob
import re
def linear(x,k,b):
    return k*x+b


# This pattern will match any number of digits followed by 'ml'
import re
import glob
import pandas as pd
# Define the pattern
pattern = re.compile('\d+ml')

# Get a list of all filenames in directory
filenames = glob.glob("/home/eino/oh_setit/calibration/*")
filenames.sort()

df_merged = pd.DataFrame()
names=[0,100,200,300,400,500,600,700]
avgs = [0,0,0,0,0,0,0,0]
for i in range(len(filenames)):
    df = pd.read_csv(filenames[i])
    print(names[i],filenames[i])
    avgs[i] = df["level"].mean()

popt,popcv = curve_fit(linear,avgs,names)
k,b = popt
x = np.linspace(min(avgs),max(avgs),50000)
plt.scatter(avgs,names)
plt.plot(x,linear(x,k,b))
print(f"volume={k}*distance+{b}")
plt.show()

files = glob.glob('D:\coffee_level\calibration')
print(files)