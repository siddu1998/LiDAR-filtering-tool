from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

import pandas as pd 




df_visual_data = pd.read_csv('visualize_radius_group_indices_visble_test.csv')
df_visual_data = df_visual_data.groupby('sign_id')

sign_to_plot   = int(input("Please enter the sign you want to plot"))

df_visual_data = df_visual_data.get_group(sign_to_plot)



fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x =df_visual_data['lidar_lat']
y =df_visual_data['lidar_long']
z =df_visual_data['lidar_alt']

x_sign=df_visual_data['lat']
y_sign=df_visual_data['long']
z_sign=df_visual_data['alt']

ax.scatter(x, y, z, c='r', marker='o')
ax.scatter(x_sign, y_sign, z_sign, c='g', marker='^')


ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()