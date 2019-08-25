from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

import pandas as pd 




df_visual_data = pd.read_csv('visualize_I258_2015_inaccuracy.csv')
df_visual_data_2018 = pd.read_csv('visualize_radius_group_indices_frame_2018.csv')



sign_to_plot   = int(input("Please enter the sign you want to plot"))


df_visual_data = df_visual_data.groupby('sign_id')
df_visual_data_2018 = df_visual_data_2018.groupby('sign_id')

print(len(df_visual_data),'2015')
print(len(df_visual_data_2018),'2018')

df_visual_data = df_visual_data.get_group(sign_to_plot)
df_visual_data_2018 = df_visual_data_2018.get_group(sign_to_plot)




print(len(df_visual_data),'2015')
print(len(df_visual_data_2018),'2018')





fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

fig_1 = plt.figure()
ax_1 = fig_1.add_subplot(111, projection='3d')


x_1=[]
y_1=[]
z_1=[]
for row in df_visual_data_2018.iterrows():
	index=row[0]
	value=row[1]

	x_1.append(value['lidar_lat'])
	y_1.append(value['lidar_long'])
	z_1.append(value['lidar_alt'])

#print(len(x))




x=[]
y=[]
z=[]
for row in df_visual_data.iterrows():
	index=row[0]
	value=row[1]

	x.append(value['lidar_lat'])
	y.append(value['lidar_long'])
	z.append(value['lidar_alt'])



# x_sign=df_visual_data['lat_sign']
# y_sign=df_visual_data['long_sign']
# z_sign=df_visual_data['alt_sign']


# x_car=df_visual_data['car_lat']
# y_car=df_visual_data['car_long']
# z_car=df_visual_data['car_alt']



ax.scatter(x, y, z,s=3, c='r', marker='o')
# ax.scatter(x_sign, y_sign, z_sign, c='g', marker='^')
# ax.scatter(x_car,y_car,z_car,c='y',marker='*')
ax_1.scatter(x_1, y_1, z_1,s=3, c='g', marker='o')




ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
ax.set_title('2015')

ax_1.set_xlabel('X Label')
ax_1.set_ylabel('Y Label')
ax_1.set_zlabel('Z Label')
ax_1.set_title('2018')

plt.show()
