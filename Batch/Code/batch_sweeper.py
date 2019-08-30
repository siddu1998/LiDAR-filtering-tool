import os
from tkinter import filedialog as fd
import pandas as pd
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








#3DimSmart60

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



def extracting_all(lidar_file_directory,sign_inventory_file,coords_file):
    print(lidar_file_directory)
    print(sign_inventory_file)
    print(coords_file)
    query_list=[]
    list_of_lidar_files=os.listdir(directory_of_lidar_files)
    
   
    df_inventory=pd.read_csv(sign_inventory_file)
    df_camera_coords=pd.read_csv(coords_file)
    
    for row in df_inventory.iterrows():
        index=row[0]
        values=row[1]
        if values['frame_id_2018']=='None':
            print('[INFO] {} has not been found on the interstate'.format(values['sign_id']))
        else:
            temp_list=[]
            frame=int(values['frame_id_2018'])
            frame=frame+1
            temp_df=df_camera_coords.loc[df_camera_coords['image_name'] == frame]
            temp_list=[
                        values['sign_id'],
                        float(values['lat']),
                        float(values['long']),
                        float(values['alt']),
                        float(temp_df['lat']),
                        float(temp_df['long']),
                        float(temp_df['alt']),
                        values['physical_condition'],
                        values['mutcd_code'],
                        values['frame_id_2018'],
                        values['overhead_type']
                        ]

            query_list.append(temp_list)

    df_query_sheet = pd.DataFrame(query_list,columns=['sign_id','sign_lat','sign_long','sign_alt','frame_lat','frame_long','frame_alt','physical_condition','mutcd_code','frame_id_2018','overhead_type'])
    df_query_sheet.to_csv('../Data/query_points.csv',index=False,header=True)
    df_query_sheet=pd.read_csv('../Data/query_points.csv')
    print('[INFO] Query points extracted')

    print('[INFO] Starting to query each lidar sheet')
    
    check_list=[]
    for lidar_sheet in list_of_lidar_files:
        print('*********************************************************')
        print('[INFO] Exracting Signs from {}'.format(lidar_sheet))
        


        df_retro=pd.DataFrame()
        chunksize=10**6
        for chunk in pd.read_csv('{}/{}'.format(directory_of_lidar_files,lidar_sheet),chunksize=chunksize):
            #print('[INFO] Reading Chunks')
            df_retro=df_retro.append(chunk,ignore_index=True)
        
        #print('[INFO] {}',len(df_retro))
        #print('[INFO] Eliminating points below 0.61')
        df_retro = df_retro.loc[df_retro['Retro']>=0.61]
        #print('[INFO] {}',len(df_retro))
        
        df_retro = DataFrameLLA2Cartesian(df_retro)
        #print(df_retro.head)
        
        df_retro['sign_id'] = [-1 for i in range(len(df_retro))]
        
        X = df_retro[["x_cart", "y_cart", "z_cart"]].values
        #print(X.head)
        
        kd_tree=cKDTree(X)
        #print('[INFO] Finished forming kdtree')
        
        for row in df_query_sheet.iterrows():

            index=row[0]
            value=row[1]
            x_sign, y_sign, z_sign = navpy.lla2ned(value['frame_lat'],value['frame_long'],value['frame_alt'],
                        LAT_REF, LON_REF, ALT_REF,
                        latlon_unit='deg', alt_unit='m', model='wgs84')

            query_point = np.array([x_sign,y_sign,z_sign]).reshape(1,-1)
            #print(query_point)
            query_return = kd_tree.query_ball_point(query_point,r=20)
            #print(query_return[0])
            if len(query_return[0])>0:
                print(query_return[0])
                for i in query_return[0]:
                    temp_list=[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]                    
                    temp_list[0]=value['sign_id']
                    temp_list[1]=value['sign_lat']
                    temp_list[2]=value['sign_long']
                    temp_list[3]=value['sign_alt']
                    temp_list[4]=df_retro.iloc[i]['Retro']
                    temp_list[5]=df_retro.iloc[i]['Y']
                    temp_list[6]=df_retro.iloc[i]['X']
                    temp_list[7]=df_retro.iloc[i]['Z']
                    temp_list[8]=value['mutcd_code']
                    temp_list[9]=value['physical_condition']
                    temp_list[10]=value['frame_id_2018']
                    temp_list[11]=value['frame_lat']
                    temp_list[12]=value['frame_long']
                    temp_list[13]=value['frame_alt']
                    temp_list[14]=lidar_sheet
                    temp_list[15]=len(query_return[0])
                    temp_list[16]=i

                    #print(temp_list)
                    check_list.append(temp_list)

    print('[INFO] Finished one sheet')

    df_lidar = pd.DataFrame(check_list,columns=['sign_id','lat_sign','long_sign','alt_sign','retro','lidar_lat','lidar_long','lidar_alt','mutcd_code','physical_condition','frame_id_2018','frame_lat','frame_long','frame_alt','lidar_sheet_year','hitcount','lidar_index'])
    df_lidar.to_csv('historical.csv',index=False,header=True)
    print("[INFO] Finished extracting points")

    








print('[USER] Choose the directory with LiDAR files')
directory_of_lidar_files=fd.askdirectory()



print('[USER] Choose the coords file')
coords_file=fd.askopenfilename()


print('[USER] Choose the Sign Inventory file')
sign_inventory_file=fd.askopenfilename()

extracting_all(directory_of_lidar_files,sign_inventory_file,coords_file)

