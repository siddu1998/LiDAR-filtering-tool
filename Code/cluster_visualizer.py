from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

import pandas as pd 




df_visual_data = pd.read_csv('clustered_1977.csv')
df_visual_data = df_visual_data.groupby('sign_id')

sign_to_plot   = int(input("Please enter the sign you want to plot"))

df_visual_data = df_visual_data.get_group(sign_to_plot)


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')



colors = ['r','y','g','b','yellow','gray']
markers=['.','*','^','+']


clusters=set(df_visual_data['cluster_group'])




for i in set(clusters):

	temp_df=df_visual_data.groupby('cluster_group')
	temp_df=temp_df.get_group(int(i))
	ax.scatter(temp_df['lidar_lat'],temp_df['lidar_long'], temp_df['lidar_alt'],s=20, c='orange', marker='*')


# for i in set(clusters):
# 	df_visual_data=df_visual_data.groupby(df_visual_data['cluster_group'])
# 	df_visual_data=df_visual_data.get_group(int(i))

# 	ax.scatter(df_visual_data['lidar_lat'],df_visual_data['lidar_long'], df_visual_data['lidar_long'],s=3, c=colors[i], marker=markers[i])


x_sign=df_visual_data['lat_sign']
y_sign=df_visual_data['long_sign']
z_sign=df_visual_data['alt_sign']


x_car=df_visual_data['car_lat']
y_car=df_visual_data['car_long']
z_car=df_visual_data['car_alt']


ax.scatter(x_sign, y_sign, z_sign, s=100, c='g', marker='^')
ax.scatter(x_car,y_car,z_car,s=100,c='y',marker='*')



ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()