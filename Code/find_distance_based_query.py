"""
Input:
1. The LiDAR CSV containing all the points
2. sign_inventory with the bounding boxes
3. output path

Output:
1. A new csv with the lidar points corresponding to the sign 


Process: 
1. Get all the Lidar Points (option: remove all the lidar points which have retro value below 0.35(variable))
2. Pick the sign GPS coordinate, from the inventory
3. Generate kd-tree of the Lidar points
4. query the sign gps in the kd-tree 
5. get the radius points
6. pass all these points to the other Insight tool



Sign Topology:

*For sure these are good metrics 
1. The retro of the sign is greater then 0.45 
2. The elevation of the sign is greater then a fixed standard 

*Extra cases can be delt with latter
3. The distance between all the points should be simillar to the distance between the GPS location of the sign and camera
4. The UTM time stamp of the points will all fall within a specific range.



"""

from scipy.spatial.ckdtree import cKDTree
import pandas as pd 
import navpy
import math
import numpy as np

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



def apply_topology(self,bucket_of_points):    
    #we want to apply topology on it 
    # Sign topology 1 : get all those points whose retro is greater then 0.45 a.k.a get all those rows whose retro value is greater then 0.45
    # Sign topology 2 : get all those points whose elevation is greater then a fixed metric 
    return bucket_of_points.loc[(bucket_of_points['Retro'] >= 0.45) & (bucket_of_points['z_cart'] <= MAX_HEIGHT) & (bucket_of_points['z_cart'] <= MIN_HEIGHT)]




def make_buckets(lidar_path,inventory_path):

    print("[INFO] Reading LiDAR data")
    df_retro = pd.read_csv(lidar_path)
    print("[INFO] getting points with retro greater then 0.45")
    df_retro = df_retro.loc[(df_retro['Retro']>=0.3)]

    print("[INFO] Converting filtered points coordinates' from lla to NED..")
    df_retro = DataFrameLLA2Cartesian(df_retro)
    
    print("[INFO] Adding extra coloumn in the starting for sign ids")
    df_retro['sign_id'] = [-1 for i in range(len(df_retro))]
    
    print("[INFO] Building a tree of all lidar point coordinates")
    X = df_retro[["x_cart", "y_cart", "z_cart"]].values
    kdtree = cKDTree(X)
    print("[INFO] Finished buidling the kdtree")

    print("[INFO] Reading the sign Inventory")
    df_inventory = pd.read_csv(inventory_path)

    print("[INFO] Creating new dataframe for buckets")
    df_sign = pd.DataFrame(columns = df_retro.columns)

    check_list=[]
    for row in df_inventory.iterrows():
        #sign_id, 
        #gps_of_sign_lat
        #gps_of_sign_long
        #nearest_point_deteced index
        #distance between the point detected and the sign gps
        #gps coordinates_lat
        #gps_coordinates_lon

        #temp_list=[None,None,None,None,None,None,None,None,None]
        index=row[0]
        value=row[1]
        if value['frame_id_2018']=='None':
            print('[INFO] {} no gps location located by URA for this sign id'.format(value['sign_id']))
        
        else:
            print('[INFO] {} has gps, convertring them to kdtree cordinates'.format(value['sign_id']))
            x_sign, y_sign, z_sign = navpy.lla2ned(value['lat'], value['long'], value['alt'],
									LAT_REF, LON_REF, ALT_REF,
									latlon_unit='deg', alt_unit='m', model='wgs84')
            #print('[INFO] reshaping the converted cordinates for the query')

            query_point = np.array([x_sign,y_sign,z_sign]).reshape(1,-1)
            query_return = kdtree.query_ball_point(query_point,r=2)
            # temp_list[0]=value['sign_id']
            # temp_list[1]=value['lat']
            # temp_list[2]=value['long']
            # temp_list[3]=int(query_return[1])
            # temp_list[4]=float(query_return[0])
            # temp_list[5]=df_retro.iloc[int(query_return[1])]['Id'] 
            # temp_list[6]=df_retro.iloc[int(query_return[1])]['X']
            # temp_list[7]=df_retro.iloc[int(query_return[1])]['Y']
            # temp_list[8]=df_retro.iloc[int(query_return[1])]['Retro']
            

            check_list.append([value['sign_id'],query_return])
    print(check_list)



[[1953, array([list([1667211, 1667237, 1667271, 1667291, 1667615, 1667635, 1667636, 1667650, 1667651, 1667652, 1667668, 1667669, 1667690, 1667691, 1667736, 1667760, 1667761, 1667984, 1668005, 1668028, 1668055, 1668078, 1668102, 1668168, 1668185, 1668205, 1668231, 1668249, 1668262])],
      dtype=object)]
            

    print("[INFO] Saving to file")
    df_lidar = pd.DataFrame(check_list)
    df_lidar.to_csv('visualize_radius.csv',index=False,header=False)



            
make_buckets('/home/pramodith/Desktop/lidar_sign_extractor_v1/Data/V_20180816_I285_EB_run1(0).csv','/home/pramodith/Desktop/lidar_sign_extractor_v1/Data/SignInventory_i285_CW_output_V1.csv') 
