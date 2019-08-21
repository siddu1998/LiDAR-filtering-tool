from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

import pandas as pd 




df_visual_data = pd.read_csv('visualize_radius_group_indices_frame.csv')





df_visual_data = df_visual_data.groupby('sign_id')
print(len(df_visual_data))
sign_to_plot   = int(input("Please enter the sign you want to plot"))

df_visual_data = df_visual_data.get_group(sign_to_plot)



fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x=[]
y=[]
z=[]
for row in df_visual_data.iterrows():
	index=row[0]
	value=row[1]
	if int(value['alt_diff'])>-5:
		print(value)

		x.append(value['lidar_lat'])
		y.append(value['lidar_long'])
		z.append(value['lidar_alt'])

print(len(x))


x_sign=df_visual_data['lat_sign']
y_sign=df_visual_data['long_sign']
z_sign=df_visual_data['alt_sign']


x_car=df_visual_data['car_lat']
y_car=df_visual_data['car_long']
z_car=df_visual_data['car_alt']



ax.scatter(x, y, z, c='r', marker='o')
ax.scatter(x_sign, y_sign, z_sign, c='g', marker='^')
ax.scatter(x_car,y_car,z_car,c='y',marker='*')




ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()