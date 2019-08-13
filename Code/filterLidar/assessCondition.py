"""
#####################################################################
Author		: Esther Ling (lingesther@gatech.edu)
Date        : June 2019
Summary		: Generate histograms for the signs to assess condition
#####################################################################

Inputs:
: filtered signs

Outputs:
: saves the histograms to a folder

"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os, sys

sign_file = "../../Data/i75_2018_output/Exp1/signFilter_raw_nb/refinedSigns.csv"
base_folder = os.path.split(sign_file)[0]
save_folder = os.path.join(base_folder, "retro_hist")

if not os.path.exists(save_folder):
	os.mkdir(save_folder)

df_sign = pd.read_csv(sign_file)
df_sign.drop('SignId', axis=1, inplace=True)

sign_groups = df_sign.groupby('sign_id')
for sign in sign_groups:
	rows = sign[1]
	retro = rows['Retro']
	retro.hist()
	plt.ylabel('Freq')
	plt.xlabel('Retrointensity')
	file_name = str(int(rows.iloc[0].sign_id))
	save_name = os.path.join(save_folder, file_name + '.jpg')
	plt.title(file_name)
	plt.savefig(save_name)
	plt.close()
