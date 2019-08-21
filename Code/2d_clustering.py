import numpy as np
import matplotlib.pyplot as plt

# Fixing random state for reproducibility
#p.random.seed(19680801)
import pandas as pd 


df = pd.read_csv('visualize_radius_group_indices_frame.csv')

df = df.groupby('sign_id')

sign_to_plot   = int(input("Please enter the sign you want to plot"))

df = df.get_group(sign_to_plot)





#N = 50
x =df['lidar_lat']
y =df['lidar_alt']


x_sign=df['lat_sign']
y_sign=df['alt_sign']

x_car=df['car_lat']
y_car=df['car_alt']




from sklearn.preprocessing import StandardScaler  # For scaling dataset
from sklearn.cluster import KMeans, AgglomerativeClustering, AffinityPropagation #For clustering
from sklearn.mixture import GaussianMixture

pts = df[["lidar_lat", "lidar_alt"]].values

number_of_clusters=1
model=KMeans(1)
model.fit(pts)
#clust_labels = model.predict()
centroid = model.cluster_centers_
#kmeans = pd.DataFrame(clust_labels)
print(centroid)
print(len(centroid))
plt.scatter(x, y, s=20, c='r', alpha=0.5)
plt.scatter(x_sign,y_sign,s=20,c='g',marker='*')
plt.scatter(x_car,y_car,s=20,c='b',marker='^')

# plt.scatter(centroid[0][0],centroid[0][1],s=20,c='b',marker='^')
# plt.scatter(centroid[1][0],centroid[1][1],s=20,c='b',marker='^')
# plt.scatter(centroid[2][0],centroid[2][1],s=20,c='b',marker='^')

list_of_heights=[]
x=325

for i in range(325,337):
  plt.scatter(0,i,s=20,c='b')


 




plt.show()
