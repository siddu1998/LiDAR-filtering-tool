import pandas as pd
import numpy as np
import os, sys
import argparse
import math
from sklearn.cluster import KMeans, DBSCAN
import hdbscan

import matplotlib.pyplot as plt
import seaborn as sns
df_visual_data = pd.read_csv('2025.csv')





df_visual_data = df_visual_data.groupby('sign_id')
print(len(df_visual_data))
sign_to_plot   = int(input("Please enter the sign you want to plot"))

df_visual_data = df_visual_data.get_group(sign_to_plot)

points = df_visual_data[["lidar_lat", "lidar_long"]].values

print(points.shape)
print(points)
plt.scatter(*points.T, s=30, linewidth=0, c='b', alpha=0.25)
#plt.scatter(df_visual_data['lidar_alt'],df_visual_data['lidar_long'], s=50, linewidth=0, c='r', alpha=0.25)



plt.show()

N=10

rads = np.radians(points)
clusterer = hdbscan.HDBSCAN(min_cluster_size=20,metric='haversine').fit(points)
color_palette = sns.color_palette('deep', 8)
cluster_colors = [color_palette[x] if x >= 0
                  else (0.5, 0.5, 0.5)
                  for x in clusterer.labels_]
cluster_member_colors = [sns.desaturate(x, p) for x, p in
                         zip(cluster_colors, clusterer.probabilities_)]

print(clusterer.labels_)
#for x in clusterer.labels_:
#	print(x)
plt.scatter(*points.T, s=30, linewidth=0, c=cluster_member_colors, alpha=0.25)
plt.show()

print(len(df_visual_data))
print(len(clusterer.labels_))

df_visual_data["cluster_group"] = clusterer.labels_

df_visual_data.to_csv('clustered_2025.csv')