"""
Project the found lidar signs onto the frame - for validation
"""
import cv2
import pandas as pd
import numpy as np
import navpy
import matplotlib.pyplot as plt

def LoadCameraMatrix():
	"""
	Obtain camera matrix for GTSV vehicle

	Hard-code for now: since GTSV is used, camera matrix and image dimensions are fixed
	Assume principal point (cx, cy) as the image centre
	TODO: estimate distortion parameters of camera from images

	Returns:
	-------------
	camera_matrix: 3x3 camera matrix

	"""
	## Information from camera_intrinsics.csv
	image_height = 2448.0
	image_width = 2048.0
	F = 85 # mm
	cx = image_width / 2
	cy = image_height / 2
	# pixel_size = 0.00000345 # mm

	## Sensor film information from datasheet
	sensor_width = 7.18 # mm
	sensor_height = 5.32 # mm

	fx = F * (image_width/sensor_width)
	fy = F * (image_height/sensor_height)

	camera_matrix = np.zeros((3,3))
	camera_matrix[0,0] = fx
	camera_matrix[1,1] = fy
	camera_matrix[2,2] = 1.0
	camera_matrix[0,2] = cx
	camera_matrix[1,2] = cy

	return camera_matrix

LAT_REF = 32.378584
LON_REF = -86.311959
ALT_REF = 200

inventory_path = "../../Data/i75_2018_output/SignInventory_i75_FRNB2015_completed.csv"
sign_path = "../../Data/i75_2018_output/Exp1/signFilter_raw_nb/associatedSigns.csv"
frames_path = "../../Data/i75_2018/FR_20180804_I75_nb_run1/frames.csv"
df_inventory = pd.read_csv(inventory_path)
df_sign = pd.read_csv(sign_path)
df_frames = pd.read_csv(frames_path)
camera_matrix = LoadCameraMatrix()

for row in df_inventory.iterrows():
	idx = row[0]
	val = row[1]

	if val['frame_path_2018'] != 'None':

		# Read image
		img = cv2.imread(val['frame_path_2018'])

		# Draw bounding box
		bbox_x1 = int(float(val["bbox_x1"]))
		bbox_y1 = int(float(val["bbox_y1"]))
		bbox_x2 = int(float(val["bbox_x2"]))
		bbox_y2 = int(float(val["bbox_y2"]))
		img = cv2.rectangle(img, (bbox_x1, bbox_y1), (bbox_x2, bbox_y2), [0, 0, 255], 1)

		# Get cam position
		cam = df_frames[df_frames['Frame_No'] == int(val['frame_id_2018'])]
		cam_pt = navpy.lla2ned(cam['Y'], cam['X'], cam['Z'],
								LAT_REF, LON_REF, ALT_REF,
								latlon_unit='deg', alt_unit='m', model='wgs84')

		# Get sign points
		sign = df_sign[df_sign['sign_id'] == val['sign_id']]
		sign_pts = sign[['x_cart', 'y_cart', 'z_cart']].values
		sign_pts_local = sign_pts - cam_pt

		# Swap the columns of lidar_points_cam to match the image coordinate system
		# x_im = x (right)
		# y_im = -z (down)
		# z_im = y (forward)
		sign_pts_local_ = np.zeros(sign_pts_local.shape)
		for (i,pt) in enumerate(sign_pts_local):
			x = pt[0]
			y = pt[1]
			z = pt[2]
			sign_pts_local_[i,:] = np.array((x, -z, y))

		# Project lidar points
		tvec = np.array((0.0, 0.0, 0.0))
		rvec, _ = cv2.Rodrigues(np.array((0.0, 0.0, 0.0)))
		sign_proj, _ = cv2.projectPoints(sign_pts_local_, rvec, tvec, camera_matrix, 0)
		sign_proj = sign_proj.reshape(-1, 2)

		RADIUS = 1
		img_pts = img.copy()
		for (u1,v1) in sign_proj:
			img_pts = cv2.circle(img_pts, (int(u1),int(v1)), int(RADIUS), [0, 255, 0], 1, 8)

		# Visualize
		img_pts = cv2.resize(img_pts, (1200,1000))
		cv2.namedWindow('img', cv2.WINDOW_NORMAL)
		cv2.imshow('img', img_pts)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

		## DEBUG CODES ##
		user_input = raw_input("Continue to next sign or exit? (any key to continue / N): ")
		if user_input == 'N' or user_input == 'n':
			break
		## END DEBUG CODES ##






