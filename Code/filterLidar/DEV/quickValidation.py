import pandas as pd

dfinv = pd.read_csv("../../Data/i75_2018_output/SignInventory_i75_FRSB2015_completed.csv")
# dfsigns = pd.read_csv("../../Data/i75_2018_output/Exp2/signFilter_raw_sb/associatedSigns.csv")
dfsigns = pd.read_csv("../../Data/i75_2018_output/Exp1/signFilter_raw_sb/refinedSigns.csv")

num_rhs_signs = len(dfinv[dfinv.bbox_x1 != 'None']) # total number of signs we are trying to detect
num_detected_signs = len(dfsigns.sign_id.unique()) # total number of signs we actually detected

# quick detection rate to tune parameters 
# if detection rate is low, lower the retrointensity threshold
print("Detection rate: %f" % (float(num_detected_signs) / num_rhs_signs))

