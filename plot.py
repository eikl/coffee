import matplotlib.pyplot as plt
import pandas as pd

file = '/home/eino/oh_setit/data/180723_data.csv'

df = pd.read_csv(file)
date = pd.to_datetime(df["date"])
level = df["level"]

plt.plot(date,level)
plt.show()