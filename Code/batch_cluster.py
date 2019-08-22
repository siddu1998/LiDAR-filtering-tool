import pandas as pd
import numpy as np
import os, sys
import argparse
import math
from sklearn.cluster import KMeans, DBSCAN
import hdbscan

import matplotlib.pyplot as plt
import seaborn as sns






df_visual_data = pd.read_csv('boom.csv')
df_visual_data['cluster']=67


sign_id_list=df_visual_data['coordinate_id'].tolist()


sign_id_list=set(sign_id_list)
df_visual_data = df_visual_data.groupby('coordinate_id')


for i in sign_id_list:

	df_visual_data=df_visual_data.get_group(i)
	points = df_visual_data[["lidar_lat", "lidar_long"]].values
	rads = np.radians(points)

	clusterer = hdbscan.HDBSCAN(min_cluster_size=70,metric='haversine').fit(points)
	df_visual_data['cluster']=clusterer.labels_


df_visual_data.to_csv('clustered_i24eb.csv')



