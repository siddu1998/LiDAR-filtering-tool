from scipy.spatial.ckdtree import cKDTree
import pandas as pd 
import navpy
import math
import numpy as np
import os
import matplotlib.pyplot as plt

MIN_ELEVATION =2
MAX_ELEVATION =10

LAT_REF = 33.79588248
LON_REF = -84.24924553
ALT_REF = 200
def DataFrameLLA2Cartesian(df):
	lon = df["X"].values
	lat = df["Y"].values
	alt = df["Z"].values
	cartesian = navpy.lla2ned(lat, lon, alt,
						LAT_REF, LON_REF, ALT_REF,
						latlon_unit='deg', alt_unit='m', model='wgs84')
	df['x_cart'] = cartesian[:, 0]
	df['y_cart'] = cartesian[:, 1]
	df['z_cart'] = cartesian[:, 2]
	return df


df_coords = pd.read_csv('coords_i24_eb.csv')


print("[INFO] Loading LiDAR data to memory")
df_retro = pd.read_csv('/home/pramodith/Desktop/lidar_sign_extractor_v1/Data/V_20181217_I24_EB(0).csv')

print("[INFO] getting points with retro greater then 0.61")
df_retro = df_retro.loc[(df_retro['Retro']>=0.7)]
print("[INFO] Points below retro treshold are removed")



print("[INFO] Converting GPS of LiDAR data to cartesian points")
df_retro = DataFrameLLA2Cartesian(df_retro)


print("[INFO] Building a tree of all lidar point coordinates")
X = df_retro[["x_cart", "y_cart", "z_cart"]].values
kdtree = cKDTree(X)
print("[INFO] Finished buidling the kdtree")

check_list=[]
for row in df_coords.iterrows():
	index=row[0]
	value=row[1]

	print("[INFO] query point {}".format(value['image_name']))

	
	x_sign, y_sign, z_sign = navpy.lla2ned(value['lat'],value['long'],value['alt'],
									LAT_REF, LON_REF, ALT_REF,
									latlon_unit='deg', alt_unit='m', model='wgs84')
	

	print("[INFO] Starting Spherical Search of 20meters")
	query_point = np.array([x_sign,y_sign,z_sign]).reshape(1,-1)
	query_return = kdtree.query_ball_point(query_point,r=20)

	if len(query_return[0])>70:
		for i in query_return[0]:

			print(len(query_return[0]))
			temp_list=[None,None,None,None,None,None,None,None,None,None,None,None,None,None]


			#COORDINATE ID
			temp_list[0]=value['image_name']
			#COORDINATE LOCATION
			temp_list[1]=value['lat']
			temp_list[2]=value['long']
			temp_list[3]=value['alt']

			#INDEX in LIDAR SHEET
			temp_list[4]=i

			#LIDAR LOCATIONS
			temp_list[5]=df_retro.iloc[i]['Y']
			temp_list[6]=df_retro.iloc[i]['X']
			temp_list[7]=df_retro.iloc[i]['Z']

			#LIDAR RETRO
			temp_list[8]=df_retro.iloc[i]['Retro']
			
			#HITCOUNT
			temp_list[9]=len(query_return[0])


			#CARTESIAN OF LIDAR COORDINATES
			temp_list[10]=df_retro.iloc[i]['x_cart']
			temp_list[11]=df_retro.iloc[i]['y_cart']
			temp_list[12]=df_retro.iloc[i]['z_cart']

			#car-lidar_point
			temp_list[13]=value['alt']-temp_list[7]
			print(temp_list)
			check_list.append(temp_list)





print("[INFO] Saving to file")
df_lidar = pd.DataFrame(check_list,columns=['coordinate_id','coordinate_lat','coordinate_long','coordinate_alt','index','lidar_lat','lidar_long','lidar_alt','retro','count','x_cart','y_cart','z_cart','alt_diff'])
df_lidar.to_csv('boom.csv',index=False,header=True)
print("[INFO] Finished extracting points")

