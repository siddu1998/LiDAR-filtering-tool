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
        self.sign_id_present=[]
        self.colors_= ['r','y','g','b','yellow','gray','m','black','cyan','burlywood']
        self.markers_=['.','*','^','+']

        self.width_of_panel=600
        self.height_of_panel=600
        print('[USER] Please select the images for visualiazation purposes')
        self.img_path = self.get_directories()
        self.img_index=0
        self.image_name=None
        self.image_list=self.get_image_list(self.img_path)

        self.kd_tree=None
        self.df_retro=None

        self.farme_for_images=tk.Frame(self,relief='solid', bg='gray30')
        self.fig = Figure(figsize=(5,5), dpi=100)
        self.canvas=FigureCanvasTkAgg(self.fig,self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)

        self.img_label = tk.Label(self.farme_for_images)
        self.img_label.pack(side='right',padx='10')
        self.image=None


        self.ax1 = self.fig.add_subplot(111, projection='3d')
        self.farme_for_images.pack(side="top", padx="10", pady="10", fill='both', expand=0)

        retro_treshold=tk.Entry(self)
        retro_treshold.pack(side='left',padx='5',pady='10')
        button=ttk.Button(self,text="Filter Points!",command=lambda:self.create_kd_tree(retro_treshold.get()))
        button.pack(side='left',padx='5',pady='10')


        button_make_sign_inventory_buckets=ttk.Button(self,text='Make Sign Inventory Buckets',command=lambda:self.make_buckets())
        button_make_sign_inventory_buckets.pack(side='left',padx='5',pady='10')


        sign_id_entry=tk.Entry(self)
        sign_id_entry.pack(side='left',padx='5',pady='10')
        
        button_get_sign_lidar=ttk.Button(self,text='Get Sign id point cloud',command=lambda:self.get_details(sign_id_entry.get()))
        button_get_sign_lidar.pack(side='left',padx='5',pady='10')


        lat_entry=tk.Entry(self)
        lat_entry.pack(side='left',padx='5',pady='10')


        lon_entry=tk.Entry(self)
        lon_entry.pack(side='left',padx='5',pady='10')


        alt_entry=tk.Entry(self)
        alt_entry.pack(side='left',padx='5',pady='10')
        
        gps_button=ttk.Button(self,text="Get point clouds based on gps",command=lambda:self.make_bucket_based_on_gps(lat_entry.get(),lon_entry.get(),alt_entry.get()))
        gps_button.pack(side='left',padx='5',pady='10')



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

    def create_kd_tree(self,retro_treshold):
        self.df_retro=pd.DataFrame()
        print("[INFO] Reading LiDAR data")
        chunksize=10**6
        for chunk in pd.read_csv(self.lidar_file,chunksize=chunksize):
            print("[INFO] Reading Chunks")
            self.df_retro = self.df_retro.append(chunk,ignore_index=True)

        print("[INFO] Getting points with retro greater then mentioned treshold")
        self.df_retro = self.df_retro.loc[(self.df_retro['Retro']>=float(retro_treshold))]

        print("[INFO] Converting filtered points coordinates' from lla to NED..")
        self.df_retro = self.DataFrameLLA2Cartesian(self.df_retro)
        
        print("[INFO] Adding extra coloumn in the starting for sign ids")
        self.df_retro['sign_id'] = [-1 for i in range(len(self.df_retro))]
        
        print("[INFO] Building a tree of all lidar point coordinates")
        X = self.df_retro[["x_cart", "y_cart", "z_cart"]].values
        self.kd_tree=cKDTree(X)
        print("[INFO] Finished buidling the kdtree")
        


    def make_bucket_based_on_gps(self,lat,lon,alt):
        self.ax1.clear()
        check_list=[]
        x_sign, y_sign, z_sign = navpy.lla2ned(float(lat),float(lon),float(alt),
                        LAT_REF, LON_REF, ALT_REF,
                        latlon_unit='deg', alt_unit='m', model='wgs84')
        
        query_point = np.array([x_sign,y_sign,z_sign]).reshape(1,-1)
        query_return = self.kd_tree.query_ball_point(query_point,r=20)
        if len(query_return[0])>39:
            for i in query_return[0]:

                temp_list=[None,None,None,None,None,None,None,None,None,None,None,None]

                temp_list[0]=lat
                temp_list[1]=lon
                temp_list[2]=alt

                temp_list[3]=i

                temp_list[4]=self.df_retro.iloc[i]['Y']
                temp_list[5]=self.df_retro.iloc[i]['X']
                temp_list[6]=self.df_retro.iloc[i]['Z']
                temp_list[7]=self.df_retro.iloc[i]['Retro']
                
                temp_list[8]=len(query_return[0])
                

              
                temp_list[9]=self.df_retro.iloc[i]['x_cart']
                temp_list[10]=self.df_retro.iloc[i]['y_cart']
                temp_list[11]=self.df_retro.iloc[i]['z_cart']
                check_list.append(temp_list)
        else:
            print('[INFO] Not enough points')

        print("[INFO] Saving to file")
        df_lidar = pd.DataFrame(check_list,columns=['query_lat','query_lon','query_alt','index','lidar_lat','lidar_long','lidar_alt','retro','count','x_cart','y_cart','z_cart',])
        output_path='../Data/enter_gps/output_file_entered_gps_{}_{}_{}.csv'.format(lat,lon,alt)
        df_lidar.to_csv(output_path,index=False,header=True)
        print("[INFO] Finished extracting points and saved to output csv file")
        df_plot=pd.read_csv(output_path)

        self.ax1.scatter(df_plot['lidar_lat'], df_plot['lidar_long'],df_plot['lidar_alt'], s=30, c='b', marker='.')
        self.ax1.scatter(df_plot['query_lat'],df_plot['query_lon'],df_plot['query_alt'],s=20,marker='*')








    def make_buckets(self):
        self.master_list=[]

        print("[INFO] Reading the sign Inventory")
        df_inventory = pd.read_csv(self.sign_inventory_file)

        print("[INFO] Creating new dataframe for buckets")
        df_sign = pd.DataFrame(columns = self.df_retro.columns)



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
                query_return = self.kd_tree.query_ball_point(query_point,r=20)
                if len(query_return[0])>39:
                    self.sign_id_present.append(value['sign_id'])
                    for i in query_return[0]:
                        temp_list=[None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]
                        temp_list[0]=value['sign_id']
                        temp_list[1]=value['lat']
                        temp_list[2]=value['long']
                        temp_list[3]=value['alt']
                        temp_list[4]=i
                        temp_list[5]=self.df_retro.iloc[i]['Y']
                        temp_list[6]=self.df_retro.iloc[i]['X']
                        temp_list[7]=self.df_retro.iloc[i]['Z']
                        temp_list[8]=self.df_retro.iloc[i]['Retro']
                        temp_list[9]=value['mutcd_code']
                        temp_list[10]=len(query_return[0])
                        temp_list[11]=float(temp_df['lat'])
                        temp_list[12]=float(temp_df['long'])
                        temp_list[13]=float(temp_df['alt'])
                        temp_list[14]=value['overhead_type']
                        temp_list[15]=int(temp_df['alt'])-int(temp_list[7])
                        temp_list[16]=self.df_retro.iloc[i]['x_cart']
                        temp_list[17]=self.df_retro.iloc[i]['y_cart']
                        temp_list[18]=self.df_retro.iloc[i]['z_cart']
                        temp_list[19]=value['frame_id_2018']
                        temp_list[20]=value['physical_condition']
                        self.master_list.append(temp_list)

        print("[INFO] Saving to file")
        df_lidar = pd.DataFrame(self.master_list,columns=['sign_id','lat_sign','long_sign','alt_sign','index','lidar_lat','lidar_long','lidar_alt','retro','mutcd_code','count','car_lat','car_long','car_alt','overhead','alt_diff','x_cart','y_cart','z_cart','frame','physical_condition'])
        # output_file=self.lidar_file+'signs.csv'
        df_lidar.to_csv('../Data/lidar_sheets/output_file.csv',index=False,header=True)
        print("[INFO] Finished extracting points and saved to output csv file")

        print('[INFO] Reading the lidar-sign relation file')
        df_sign_info = pd.read_csv('../Data/lidar_sheets/output_file.csv')
        print('[INFO] Grouping by your selected Sign is')
        df_sign_info = df_sign_info.groupby('sign_id')
        self.sign_id_present=set(self.sign_id_present)
        print(len(self.sign_id_present))
        for sign_id in self.sign_id_present:
            df_sign = df_sign_info.get_group(int(sign_id))
            points = df_sign[["lidar_lat", "lidar_long"]].values
            rads = np.radians(points)
            clusterer = hdbscan.HDBSCAN(min_cluster_size=20,metric='haversine').fit(points)
            df_sign["cluster_group"] = clusterer.labels_
            output_path='../Data/sign_sheets/output_{}.csv'.format(sign_id)
            df_sign.to_csv(output_path,index=False)

        print('[INFO] Check Datasheets!')


    def get_details(self,sign_id):
        self.ax1.clear()



        sign_to_plot='../Data/sign_sheets/output_{}.csv'.format(sign_id)
        df_sign_info = pd.read_csv(sign_to_plot)
        print('[INFO] Plotting clusters for understanding')



        self.img_index=df_sign_info['frame'].iloc[2]
        self.image_name=self.image_list[int(self.img_index)]
        print(self.img_path+'/'+self.image_name)
        self.image=Image.open(self.img_path+'/'+self.image_name)
        self.image=self.image.resize((self.width_of_panel,self.height_of_panel),Image.ANTIALIAS)
        self.img_label.img = ImageTk.PhotoImage(self.image)
        self.img_label.config(image=self.img_label.img)

        x_sign=df_sign_info['lat_sign']
        y_sign=df_sign_info['long_sign']
        z_sign=df_sign_info['alt_sign']

        x_car=df_sign_info['car_lat']
        y_car=df_sign_info['car_long']
        z_car=df_sign_info['car_alt']


        clusters=set(df_sign_info['cluster_group'])

        for i in set(clusters):

            temp_df=df_sign_info.groupby('cluster_group')
            temp_df=temp_df.get_group(int(i))
            self.ax1.scatter(temp_df['lidar_lat'],temp_df['lidar_long'], temp_df['lidar_alt'],s=20, c=self.colors_[i],marker='*')



        self.ax1.scatter(x_sign, y_sign, z_sign, s=100, c='g', marker='^')
        self.ax1.scatter(x_car,y_car,z_car,s=100,c='y',marker='*')



    def get_image_list(self,img_path):
        image_list=[]
        sub_folders = sorted(os.listdir(img_path))
        jpg_cnt = sum(1 for f in sub_folders if f.endswith(".jpg"))
        if jpg_cnt == 0:
            # frames are in the sub-directories
            file_list = []
            for sub_folder in sub_folders:
                temp_list = (os.listdir(os.path.join(img_path, sub_folder)))
                temp_list = [os.path.join(sub_folder, f) for f in temp_list if f.endswith(".jpg")]
                file_list = file_list + temp_list
                
            file_list.sort()
            image_list = file_list
        else:
            # frames are in the folder
            image_list = sub_folders
        
        return image_list

    def get_directories(self):
        return filedialog.askdirectory()
        

                
app=SignAnalyzer()
app.mainloop()

