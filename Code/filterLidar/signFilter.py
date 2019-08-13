"""
#####################################################################
Author		: Esther Ling (lingesther@gatech.edu)
Date        : June 2019
Summary     : Filters traffic signs from LIDAR point cloud data
Version 1.0 

Author         : Sai Siddartha Maram (msaisiddartha1@gmail.com)
Date 	       : June 2019
Change log     : New function to take in coords.csv instead of frames.csv
#####################################################################

Description
---------------------------
Filters points belonging to traffic signs on the right-hand side of the road (ignores sign-bridges and left-hand side). The following rules are used:

1. Retro-Intensity (use ../../c++/filterCloud/filteronly code)
2. Elevation
3. Lateral offset from vehicle trajectory (not yet implemented)

After running this code, run refineSign.py on the output, which refines the sign:

4. Estimates a centroid of the points representing the sign, and removes spurious points
5. Hit count

Inputs
---------------------------
: path to point cloud csv (4GB)
: path to annotated sign inventory (must contain associated frame path)
: path to vehicle coordinates csv

Outputs
---------------------------
: csv file containing the points surrounding each sign (intermediate output)
--> Apply the sign topology to filter the point cloud of the sign from the previous output 
csv file containing the lidar points associated with a sign_id that corresponds to the sign inventory

Example
---------------------------

Normalized
run signFilter.py \
	--lidar "../../Data/i75_2018/normalizedData/nb_run1/csv/output_csv.csv" \
	--sign_inventory "../../Data/i75_2018_output/SignInventory_i75_FRNB2015_completed.csv" \
	--frames "../../Data/i75_2018/FR_20180804_I75_nb_run1/frames.csv" \
	--outfolder "../../Data/i75_2018_output/signFilter_nb/"

Raw
run signFilter.py \
	--lidar "../../Data/i75_2018/FILTER_ONLY/RETRO_040/signFilter_nb_raw.csv" \
	--sign_inventory "../../Data/i75_2018_output/SignInventory_i75_FRNB2015_completed.csv" \
	--frames "../../Data/i75_2018/FR_20180804_I75_nb_run1/frames.csv" \
	--outfolder "../../Data/i75_2018_output/Exp2/signFilter_raw_nb/" \

run signFilter.py \
	--lidar "../../Data/i75_2018/FILTER_ONLY/RETRO_040/signFilter_sb_raw.csv" \
	--sign_inventory "../../Data/i75_2018_output/SignInventory_i75_FRSB2015_completed.csv" \
	--frames "../../Data/i75_2018/FR_20180804_I75_sb_run1/frames.csv" \
	--outfolder "../../Data/i75_2018_output/Exp2/signFilter_raw_sb/"

References
---------------------------
1. "Critical Assessment of an Enhanced Traffic Sign Detection Method Using Mobile LIDAR and INS Technologies", C. Ai, Y.C Tsai, Journal of Transportation Engineering 2015, 141(5)

DEBUGGING CODES
---------------------------
df_lidar_chunk.plot("Y","Z", kind="scatter")
df_lidar_chunk.plot("X","Y", kind="scatter"); plt.show()
df_lidar_chunk

"""
import cv2
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import pandas as pd
import numpy as np
import argparse
import os, sys
import navpy
# from sklearn.neighbors import KDTree
from scipy.spatial.ckdtree import cKDTree
import math

"""
FILTER THRESHOLDS. ADJUSTABLE
"""
MIN_ELEVATION = 2
MAX_ELEVATION = 10
# RIGHTLATERAL = 2 ## Not yet implemented

## REFERENCE FOR LLA-local cartesian PROJECTION ##
## Use a position that is to the south-east of the vehicle to put the vehicle in the first quadrant ##
## Coordinates in Montgomery, AL ##
LAT_REF = 32.378584
LON_REF = -86.311959
ALT_REF = 200

# def MapFrameToPos(df_frames):
# 	"""
# 	Maps frame_id to gps coordinate of camera when the frame was captured.

# 	Params:
# 	--------------
# 		df_frames: pandas dataframe containing frame information

# 	Returns:
# 	--------------
# 		map_frame2pos: dict containing mapping from frame number -> position (x,y,z) in NED system
# 	"""
# 	lon = df_frames["X"].values
# 	lat = df_frames["Y"].values
# 	alt = df_frames["Z"].values
# 	cartesian = navpy.lla2ned(lat, lon, alt,
# 							LAT_REF, LON_REF, ALT_REF,
# 							latlon_unit='deg', alt_unit='m', model='wgs84')
# 	map_frame2pos = {}
# 	for (frame_no, row) in enumerate(cartesian):
# 		map_frame2pos[frame_no] = row
# 	return map_frame2pos

def MapFrameToPos(df_frames):
	"""
	Maps frame_id to gps coordinate of camera when the frame was captured.

	Params:
	--------------
		df_frames: pandas dataframe containing frame information

	Returns:
	--------------
		map_frame2pos: dict containing mapping from frame number -> position (x,y,z) in NED system
	"""
	lon = df_frames["long"].values
	lat = df_frames["lat"].values
	alt = df_frames["alt"].values
	cartesian = navpy.lla2ned(lat, lon, alt,
							LAT_REF, LON_REF, ALT_REF,
							latlon_unit='deg', alt_unit='m', model='wgs84')
	map_frame2pos = {}
	for (frame_no, row) in enumerate(cartesian):
		map_frame2pos[frame_no] = row
	return map_frame2pos


# def FilterByIntensity(lidar_path, out_path, verbose=False):
# 	"""
# 	Filter the point cloud by retro-intensity
#	- use ../../c++/filterCloud/filteronly as it is faster in c++
#	- takes about 5 min in c++ for a 4-5 GB file, whereas in Python the time was > 40 min
# 	"""
# 	if not os.path.exists(out_path):
# 		print("[WARNING] Save time by using filteronly in the c++ folder for this particular function...")
# 		chunksize = 5000
# 		data_lidar = pd.read_csv(lidar_path, chunksize=chunksize, usecols=range(1,9))
# 		df_retro = pd.DataFrame()
# 		r = 1
# 		for df_lidar_chunk in data_lidar:
# 			df_retro = df_retro.append(df_lidar_chunk[df_lidar_chunk["Normalized Retro"] > RETROINTENSITY])
# 			if verbose:
# 				print("[INFO] Read rows: %f \n" % (r*chunksize))
# 				r = r+1
# 		print("Writing to file..")
# 		df_retro.to_csv(out_path)
# 	else:
# 		if verbose:
# 			print("[INFO] Reading filtered point cloud csv..")
# 		df_retro = pd.read_csv(out_path)
# 	return df_retro

def DataFrameLLA2Cartesian(df):
	"""
	Convert point cloud to local cartesian X-Y-Z. North-East-Down (NED) system is used

	Params:
	--------------
	df: Dataframe with X,Y,Z columns representing longitude, latitude and altitude respectively

	Returns:
	--------------
	df: with appended columns x_ned, y_ned, z_ned
	"""
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

def main(opt):
	lidar_path = opt.lidar
	inventory_path = opt.sign_inventory
	frame_path = opt.frames
	out_folder = opt.outfolder

	## Read vehicle frames
	print("[INFO] Getting frame to timestamp and position information..")
	df_frames = pd.read_csv(frame_path)
	map_frame2pos = MapFrameToPos(df_frames)

	## Filter point cloud by intensity
	# print("[INFO] Filtering point cloud..")
	#if not os.path.exists(out_folder):
	#	os.mkdir(out_folder)
	#temp_outfile = os.path.join(out_folder, "signFilter.csv")
	#df_retro = FilterByIntensity(lidar_path, temp_outfile, verbose=True)
	df_retro = pd.read_csv(lidar_path)

	## Convert point cloud to NED X-Y-Z
	print("[INFO] Converting filtered points coordinates' from lla to NED..")
	df_retro = DataFrameLLA2Cartesian(df_retro)

	## Add a sign_id placeholder column to df_retro (to contain mapping from lidar point to sign inventory)
	df_retro['sign_id'] = [-1 for i in range(len(df_retro))]

	print("[INFO] Building a tree of filtered lidar point coordinates..")
	X = df_retro[["x_cart", "y_cart", "z_cart"]].values
	# kdtree = KDTree(X, metric = 'euclidean')
	kdtree = cKDTree(X)

	"""
	Associate sign inventory with filtered point cloud
	1. Project lat-lon-alt to NED (x,y,z)
	2. Query point: x,y,z of sign
	3. Find lidar-points that fall within a SEARCHRADIUS
	4. Filter by elevation, lateral offset
	"""
	print("[INFO] Reading sign inventory..")
	df_inventory = pd.read_csv(inventory_path)
	df_sign = pd.DataFrame(columns = df_retro.columns)
	for row in df_inventory.iterrows():
		idx = row[0]
		val = row[1]

		if val['frame_id_2018'] == 'None':
			print("[INFO] No frame associated with this sign")
			continue

		else:
			## Project sign's position to local cartesian
			x_sign, y_sign, z_sign = navpy.lla2ned(val['lat'], val['long'], val['alt'],
									LAT_REF, LON_REF, ALT_REF,
									latlon_unit='deg', alt_unit='m', model='wgs84')

			## Compute 3D distance between frame and sign
			frame_pos = map_frame2pos.get(int(val['frame_id_2018']))
			dist_frame2sign = math.sqrt( (frame_pos[0]-x_sign)**2 + (frame_pos[1]-y_sign)**2 + (frame_pos[2]-z_sign)**2 )
			print("[INFO] distance between frame and sign: %f" % dist_frame2sign)

			## Filter lidar points based on distance to the position of the vehicle
			sign_query = np.array([x_sign, y_sign, z_sign]).reshape(1, -1)
			## points_idx = kdtree.query_radius(sign_query, r = SEARCHRADIUS) # look around a pre-defined SEARCHRADIUS
			# points_idx = kdtree.query_radius(sign_query, r = dist_frame2sign) # look around a SEARCHRADIUS of dist_frame2sign
			points_idx = kdtree.query_ball_point(sign_query, r = dist_frame2sign) # look around a SEARCHRADIUS of dist_frame2sign

			points_idx = points_idx[0]
			if len(points_idx) > 0:
				df_dist = df_retro.iloc[points_idx]

				elevation = z_sign - df_dist['z_cart']
				keep_indices = (elevation >= MIN_ELEVATION) & (elevation <= MAX_ELEVATION) ## Filter based on elevation
				keep_rows = df_dist[keep_indices]
				keep_rows['sign_id'] = [val['sign_id'] for i in range(len(keep_rows))]
				df_sign = df_sign.append(keep_rows)

				"""
				OPTIONAL TODO: integrate colorizer into this pipeline
				- load image, project lidar points onto sign and grab rgb values
				"""
				# img = cv2.imread(val['frame_path_2018'])
				## Uncomment to visualize bounding box annotations
				# bbox_x1 = int(float(val["bbox_x1"]))
				# bbox_y1 = int(float(val["bbox_y1"]))
				# bbox_x2 = int(float(val["bbox_x2"]))
				# bbox_y2 = int(float(val["bbox_y2"]))
				# img = cv2.rectangle(img, (bbox_x1, bbox_y1), (bbox_x2, bbox_y2), [0,0,255], 1)
				# cv2.namedWindow('img', cv2.WINDOW_NORMAL)
				# cv2.imshow('img', img)
				# cv2.waitKey(0)
				# cv2.destroyAllWindows()

			else:
				nearest_dist, nearest_idx = kdtree.query(sign_query, k=1)
				print("[INFO] No lidar points found around the radius for this sign. Nearest distance: %f" % nearest_dist)

	## Save results
	if not os.path.exists(out_folder):
		os.mkdir(out_folder)
	outpath = os.path.join(out_folder, "associatedSigns.csv")
	df_sign.to_csv(outpath, index=False)
	print("[INFO] Wrote results to %s!" % outpath)

	## Detection rate analysis
	num_rhs_signs = len(df_inventory[df_inventory.bbox_x1 != 'None'])
	detection_rate = float(len(df_sign)) / num_rhs_signs
	print("[INFO] Approximate detection rate: %f" % detection_rate)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	#parser.add_argument("--lidar", type=str, help="path to normalized lidar points csv file", default="../../Data/i75_2018/normalizedData/nb_run1/csv/output_csv.csv")
	parser.add_argument("--lidar", type=str, help="path to normalized lidar points csv file", default="../../Data/i75_2018/FILTER_ONLY/RETRO_055/signFilter_nb_raw.csv")
	parser.add_argument("--sign_inventory", type=str, help="path to sign inventory file", default="../../Data/i75_2018_output/SignInventory_i75_FRNB2015_completed.csv")
	parser.add_argument("--frames", type=str, help="path to frame coordinates", default="../../Data/i75_2018/FR_20180804_I75_nb_run1/frames.csv")
	parser.add_argument("--outfolder", type=str, help="folder path to save output", default="../../Data/i75_2018_output/signFilter_raw_nb/")

	opt = parser.parse_args()
	main(opt)
