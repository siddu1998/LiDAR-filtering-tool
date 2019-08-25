"""
Author : Sai Siddartha Maram    (msaisiddartha1@gmail.com)
Data   : July 2019
Summary: 
An software pipeline to extract, the sign point cloud from the incoming GTSV vehicle, 
frame information from which the sign was captured
###############################################


Input:
1. The LiDAR CSV containing all the points
2. sign_inventory, with the signs and the frame in which they were found
3. coords.csv

Output:
1. An csv file with the sign_id and the corresponnding lidar points associated for that sign_id

Process: 
1. Get all the Lidar Points (option: remove all the lidar points which have retro value below 0.61(adjust for better results)
2. Pick the frame from the inventory
3. Generate kd-tree of the Lidar points
4. query the frame gps in the kd-tree 
5. get the points within an adjustable radius
6. pass all these points to the other Insight tool
"""

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

"""
Summary  : The function is used to convert gps system cordinates to cartesian system 
Input    : The function takes in a dataframe, which have gps cordinates in coloumns, X,Y,Z
Output   : It returns the dataframe appending the x_cartesian,y_cartesian and z_cartesian

"""


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



"""
Summary : Pull out the point cloud coresponding to the sign in a particular frame
Input   : Takes the inventory,coords.csv and the global lidar point cloud data
Output : returns output.csv associting the sign_id with its corresponding lidar points
"""
def make_buckets(lidar_path,inventory_path,coords_path):

    print("[INFO] Reading LiDAR data")
    df_retro = pd.read_csv(lidar_path)
    print("[INFO] getting points with retro greater then 0.61 (adjust to experiment)")
    df_retro = df_retro.loc[(df_retro['Retro']>=0.61)]

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


    print("[INFO] Loading the camera cordinates")
    df_camera_coords = pd.read_csv(coords_path)



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
            print('[INFO] {} has an image match, checking image gps and convertring them to kdtree cordinates'.format(value['sign_id']))


            frame=int(value['frame_id_2018'])
            frame=frame+1

            temp_df=df_camera_coords.loc[df_camera_coords['image_name'] == frame]



            print('[INFO] reshaping the converted cordinates of {} for the query'.format(value['sign_id']))
            x_sign, y_sign, z_sign = navpy.lla2ned(temp_df['lat'],temp_df['long'],temp_df['alt'],
									LAT_REF, LON_REF, ALT_REF,
									latlon_unit='deg', alt_unit='m', model='wgs84')
            

            
            print("[INFO] Converting cordinates suitable for KD-Tree Search")
            query_point = np.array([x_sign,y_sign,z_sign]).reshape(1,-1)
            query_return = kdtree.query_ball_point(query_point,r=20)
            
            """
            please adjust the length limit based on the retro, and after visualizing the point cloud for better result
            """
            if len(query_return[0])>0:
                for i in query_return[0]:
                    #print(len(query_return[0]))
                    temp_list=[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]
                    
                    temp_list[0]=value['sign_id']
                    temp_list[1]=value['lat']
                    temp_list[2]=value['long']
                    temp_list[3]=value['alt']
                
                    temp_list[4]=i
                    
                    temp_list[5]=df_retro.iloc[i]['Y']
                    temp_list[6]=df_retro.iloc[i]['X']
                    temp_list[7]=df_retro.iloc[i]['Z']

                    temp_list[8]=df_retro.iloc[i]['Retro']
                    temp_list[9]=value['mutcd_code']
                    temp_list[10]=len(query_return[0])

                    temp_list[11]=float(temp_df['lat'])
                    temp_list[12]=float(temp_df['long'])
                    temp_list[13]=float(temp_df['alt'])

                    temp_list[14]=value['overhead_type']
                    #car-sign if below car +ve if above car -ve
                    temp_list[15]=int(temp_df['alt'])-int(temp_list[7])

                    temp_list[16]=df_retro.iloc[i]['x_cart']
                    temp_list[17]=df_retro.iloc[i]['y_cart']
                    temp_list[18]=df_retro.iloc[i]['z_cart']

                    temp_list[19]=value['frame_id_2018']
                    temp_list[20]=value['physical_condition']


                    check_list.append(temp_list)


    print("[INFO] Saving to file")
    df_lidar = pd.DataFrame(check_list,columns=['sign_id','lat_sign','long_sign','alt_sign','index','lidar_lat','lidar_long','lidar_alt','retro','mutcd_code','count','car_lat','car_long','car_alt','overhead','alt_diff','x_cart','y_cart','z_cart','frame','physical_condition'])
    df_lidar.to_csv('output.csv',index=False,header=True)
    print("[INFO] Finished extracting points")


#insert             
make_buckets('/home/pramodith/Desktop/lidar_sign_extractor_v1/Data/V_20180816_I285_EB_run1(0).csv','/home/pramodith/Desktop/lidar_sign_extractor_v1/Data/SignInventory_i285_CW_output_V1.csv','../Data/coords.csv') 
