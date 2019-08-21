import numpy as np
import matplotlib.pyplot as plt

# Fixing random state for reproducibility
#p.random.seed(19680801)
import pandas as pd 

df=pd.read_csv('2025.csv')




#N = 50
x =df['lidar_lat']
y =df['lidar_alt']


x_sign=df['lat_sign']
y_sign=df['alt_sign']

plt.scatter(x, y, s=20, c='r', alpha=0.5)
plt.scatter(x_sign,y_sign,s=20,c='g',marker='*')

plt.show()