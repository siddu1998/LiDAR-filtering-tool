from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

import pandas as pd 




df_visual_data = pd.read_csv('boom.csv')





df_visual_data = df_visual_data.groupby('coordinate_id')
print(len(df_visual_data))
sign_to_plot   = int(input("Please enter the coordinate_id you want to plot"))

df_visual_data = df_visual_data.get_group(sign_to_plot)



fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x=[]
y=[]
z=[]
for row in df_visual_data.iterrows():
	index=row[0]
	value=row[1]


	x.append(value['lidar_lat'])
	y.append(value['lidar_long'])
	z.append(value['lidar_alt'])

print(len(x))


ax.scatter(x, y, z,s=3, c='r', marker='o')




ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()