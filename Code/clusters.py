import pandas as pd
import numpy as np
import os, sys
import argparse
import math
from sklearn.cluster import KMeans, DBSCAN

"""
FILTER THRESHOLDS. ADJUSTABLE
"""
RADIUS = 3.5 # largest sign dimension is 108 inches (https://mutcd.fhwa.dot.gov/htm/2009/part2/part2b.htm), which is 2.74m
DBSCAN_EPS = 2.75 # the maximum distance between two samples for one to be considered in the neighbourhood of the other
HITCOUNT = 10
UPPER_BOUND_REMOVAL = 500

def KMeansMethod(rows):
	"""
	Estimates a centroid of the points representing the sign using the KMeans algorithm.
	After estimating the centroid, remove points that fall beyond a certain radius.
	Params:
	--------------
		rows: pandas dataframe containing the rows that belong to a particular sign
	Returns:
	--------------
		keep_rows: a subset of rows to keep
	"""
	pts = rows[["x_cart", "y_cart", "z_cart"]].values

	## Kmeans to get centroid
	kmeans = KMeans(n_clusters = 1)
	kmeans.fit(pts)
	centroid = kmeans.cluster_centers_

	## Compute distance from all the points to the centroid
	dists = np.linalg.norm(pts - centroid, axis = 1)

	## Remove spurious points
	keep_indices = (dists < RADIUS)
	num_spurious_points = len(keep_indices) - sum(keep_indices)
	if num_spurious_points <= UPPER_BOUND_REMOVAL:
		keep_rows = rows[keep_indices]
		keep_rows['flag'] = [0 for i in range(len(keep_rows))]
		if num_spurious_points > 0:
			print("[INFO] Removed spurious %d points!" % num_spurious_points)
	else:
		## If there are many signs that are being removed; keep all the points and flag for manual inspection; perhaps the clustering has issues
		keep_rows = rows
		keep_rows['flag'] = [1 for i in range(len(keep_rows))]
	return keep_rows

def DBSCANMethod(rows):
	"""
	Uses the DBSCAN algorithm to cluster the points and remove outliers.
	Params:
	--------------
		rows: pandas dataframe containing the rows that belong to a particular sign
	Returns:
	--------------
		keep_rows: a subset of rows to keep
	"""
	pts = rows[["x_cart", "y_cart", "z_cart"]].values

	dbscan = DBSCAN(eps = DBSCAN_EPS, min_samples = HITCOUNT, metric = 'l1')
	dbscan.fit(pts)

	keep_indices = (dbscan.labels_ != -1) # noisy samples are labelled -1
	keep_rows = rows[keep_indices]

	return keep_rows

def main(opt, method='DBSCAN', verbose=True):
	sign_path = opt.signs
	out_folder = opt.outfolder

	## Read file
	df_sign = pd.read_csv(sign_path)
	sign_groups = df_sign.groupby('sign_id')
	df_save = pd.DataFrame(columns = df_sign.columns)
	if method == 'KMeans':
		df_save['flag'] = [0 for i in range(len(df_save))]

	
	for (i,grp) in enumerate(sign_groups):
		sign_id = grp[0]
		rows = grp[1]

		if method == 'KMeans':
			keep_rows = KMeansMethod(rows)
		else:
			keep_rows = DBSCANMethod(rows)

		## Filter by hitcount
		if len(keep_rows) >= HITCOUNT:
			if verbose:
				print("[INFO] Appended good sign")
			df_save = df_save.append(keep_rows)
		else:
			if verbose:
				print("[INFO] Removed bad 'sign' below HITCOUNT")

	## Save output
	#outpath = os.path.join(out_folder, "refinedSigns.csv")
	df_save.to_csv('output.csv', index=False)
	#print("[INFO] Saved to %s" % outpath)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("--signs", type=str, help="path to sign-associated lidar points",
								default="2025.csv")
	parser.add_argument("--outfolder", type=str, help="folder path to save output",
								default="../../Data/i75_2018_output/Exp1/signFilter_raw_nb/")
	opt = parser.parse_args()
	main(opt)
