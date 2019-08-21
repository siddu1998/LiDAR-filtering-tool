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




from sklearn.preprocessing import StandardScaler  # For scaling dataset
from sklearn.cluster import KMeans, AgglomerativeClustering, AffinityPropagation #For clustering
from sklearn.mixture import GaussianMixture

pts = df[["lidar_lat", "lidar_alt"]].values

number_of_clusters=3
model=KMeans(3)
model.fit(pts)
#clust_labels = model.predict()
centroid = model.cluster_centers_
#kmeans = pd.DataFrame(clust_labels)
print(centroid)
plt.scatter(x, y, s=20, c='r', alpha=0.5)
plt.scatter(x_sign,y_sign,s=20,c='g',marker='*')
plt.scatter(centroid[0][0],centroid[0][1],s=20,c='b',marker='^')
plt.scatter(centroid[1][0],centroid[1][1],s=20,c='b',marker='^')
plt.scatter(centroid[2][0],centroid[2][1],s=20,c='b',marker='^')

plt.show()
