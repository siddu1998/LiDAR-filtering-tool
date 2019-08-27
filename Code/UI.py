import os
from mpl_toolkits.mplot3d import axes3d
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import style
import pandas as pd 
import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib
from matplotlib.figure import Figure
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
import tkinter as tk
from tkinter import ttk 
from tkinter import *
from PIL import ImageTk, Image,ImageDraw
import statistics
#from constants import *
import time
#from mathematics import *
from scipy.spatial import distance
from pyproj import Proj, transform, Geod
from math import atan2, cos, sin
from tkinter import filedialog as fd


from scipy.spatial.ckdtree import cKDTree
import pandas as pd 
import navpy
import math
import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, DBSCAN
import hdbscan


#font size
LARGE_FONT=("Verdana",9)
MIN_ELEVATION =2
MAX_ELEVATION =10

LAT_REF = 33.79588248
LON_REF = -84.24924553
ALT_REF = 200



#Creating the Tkinter APP
class SignAnalyzer(tk.Tk):
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        container=tk.Frame(self)

        container.pack(side="top",fill="both",expand=True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)

        self.frames={}
        for F in (StartPage,second_page):
            frame = F(container,self)
            self.frames[F]=frame
            frame.grid(row=0,column=0,sticky="nsew")
        
        self.show_frame(StartPage)

    def show_frame(self,cont):
        frame=self.frames[cont]
        frame.tkraise()


class second_page(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)


#Front page
class StartPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)

        print("[USER] Please select the LiDAR file")   
        self.lidar_file = fd.askopenfilename()
        print(self.lidar_file)

        print("[USER] Please select the coords file") 
        self.coords_file  = fd.askopenfilename()
        print(self.coords_file)

        print("[USER] Please select the sign inventory file file") 
        self.sign_inventory_file = fd.askopenfilename()
        print(self.sign_inventory_file)

        self.master_list=[]


        retro_treshold=tk.Entry(self)
        retro_treshold.pack(side='left',padx='5',pady='10')
        button=ttk.Button(self,text="Get point clouds of signs",command=lambda:self.make_buckets(retro_treshold.get()))
        button.pack(side='left',padx='5',pady='10')


        sign_id_entry=tk.Entry(self)
        sign_id_entry.pack(side='left',padx='5',pady='10')
        button_get_sign_lidar=ttk.Button(self,text='Get Sign id point cloud',command=lambda:self.get_details(sign_id_entry.get()))
        button_get_sign_lidar.pack(side='left',padx='5',pady='10')

    def DataFrameLLA2Cartesian(self,df):
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

    def make_buckets(self,retro_treshold):
        self.master_list=[]
        df_retro=pd.DataFrame()
        print("[INFO] Reading LiDAR data")
        chunksize=10**6
        for chunk in pd.read_csv(self.lidar_file,chunksize=chunksize):
            print("[INFO] Reading Chunks")
            df_retro = df_retro.append(chunk,ignore_index=True)

        print("[INFO] Getting points with retro greater then 0.45")
        df_retro = df_retro.loc[(df_retro['Retro']>=float(retro_treshold))]

        print("[INFO] Converting filtered points coordinates' from lla to NED..")
        df_retro = self.DataFrameLLA2Cartesian(df_retro)
        
        print("[INFO] Adding extra coloumn in the starting for sign ids")
        df_retro['sign_id'] = [-1 for i in range(len(df_retro))]
        
        print("[INFO] Building a tree of all lidar point coordinates")
        X = df_retro[["x_cart", "y_cart", "z_cart"]].values
        kdtree = cKDTree(X)
        print("[INFO] Finished buidling the kdtree")

        print("[INFO] Reading the sign Inventory")
        df_inventory = pd.read_csv(self.sign_inventory_file)

        print("[INFO] Creating new dataframe for buckets")
        df_sign = pd.DataFrame(columns = df_retro.columns)



        df_camera_coords = pd.read_csv(self.coords_file)

        for row in df_inventory.iterrows():
            index=row[0]
            value=row[1]
            if value['frame_id_2018']=='None':
                print('[INFO] {} no gps location located by URA for this sign id'.format(value['sign_id']))            
            else:
                print('[INFO] {} has gps, convertring them to kdtree cordinates'.format(value['sign_id']))
                frame=int(value['frame_id_2018'])
                frame=frame+1
                temp_df=df_camera_coords.loc[df_camera_coords['image_name'] == frame]
                x_sign, y_sign, z_sign = navpy.lla2ned(temp_df['lat'],temp_df['long'],temp_df['alt'],
                                        LAT_REF, LON_REF, ALT_REF,
                                        latlon_unit='deg', alt_unit='m', model='wgs84')
                query_point = np.array([x_sign,y_sign,z_sign]).reshape(1,-1)
                query_return = kdtree.query_ball_point(query_point,r=20)
                if len(query_return[0])>0:
                    for i in query_return[0]:
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
                        temp_list[15]=int(temp_df['alt'])-int(temp_list[7])
                        temp_list[16]=df_retro.iloc[i]['x_cart']
                        temp_list[17]=df_retro.iloc[i]['y_cart']
                        temp_list[18]=df_retro.iloc[i]['z_cart']
                        temp_list[19]=value['frame_id_2018']
                        temp_list[20]=value['physical_condition']
                        self.master_list.append(temp_list)

        print("[INFO] Saving to file")
        df_lidar = pd.DataFrame(self.master_list,columns=['sign_id','lat_sign','long_sign','alt_sign','index','lidar_lat','lidar_long','lidar_alt','retro','mutcd_code','count','car_lat','car_long','car_alt','overhead','alt_diff','x_cart','y_cart','z_cart','frame','physical_condition'])
        # output_file=self.lidar_file+'signs.csv'
        df_lidar.to_csv('output_file.csv',index=False,header=True)
        print("[INFO] Finished extracting points and saved to output csv file")

    def get_details(self,sign_id):

        print('[INFO] Extracting and analysing sign id {}'.format(sign_id))
        print('[INFO] Reading the lidar-sign relation file')
        df_sign_info = pd.read_csv('output_file.csv')
        print('[INFO] Grouping by your selected Sign is')
        df_sign_info = df_sign_info.groupby('sign_id')
        print('[INFO] Getting your group')
        df_sign_info = df_sign_info.get_group(int(sign_id))
        print('[INFO] Extracting Lidar lat and Lidar Long')
        points = df_sign_info[["lidar_lat", "lidar_long"]].values
        print('[INFO] Converting to radians')
        rads = np.radians(points)
        print('[INFO] Clustering the points using HDBSCAN')
        clusterer = hdbscan.HDBSCAN(min_cluster_size=20,metric='haversine').fit(points)
        print('[INFO] Creating new coloumn for cluster label')
        df_sign_info["cluster_group"] = clusterer.labels_
        print('[INFO] creating output for sign {}'.format(sign_id))
        ouput_path='../Data/output_{}.csv'.format(sign_id)
        df_sign_info.to_csv(ouput_path)
        print('[INFO] Analysis results finished!')





        

                
app=SignAnalyzer()
app.mainloop()
