from pyntcloud import PyntCloud

import pandas as pd


df= pd.read_csv("../Data/V_20180816_I285_EB_run1(0).csv")
df.rename(columns={'X':'x',
                          'Y':'y',
                          'Z':'z'}, 
                 inplace=True)



anky_cloud = PyntCloud(df)

anky_cloud.plot()