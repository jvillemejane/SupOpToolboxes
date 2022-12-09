# -*- coding: utf-8 -*-
"""
Pandas library first example
- Opening a data file
- Visualizing data (plotly / express)

Author : Julien VILLEMEJANE
Laboratoire d Enseignement Experimental - Institut d Optique Graduate School
Version : 1.0 - 2022-12-04
"""

'''
TEST with plotly
import plotly
import plotly.graph_objects as go       # to plot data
import plotly.io as pio
'''

import pandas as pd
import numpy as np

from matplotlib import pyplot as plt


## Open a CSV file and convert data into a dataframe
df_lang_indus_file = pd.read_csv('data_indus_langages.csv', index_col=0, 
                            encoding = "utf-8").T
    # Open *.csv file and make first column as index (here year) and transpose data
print(df_lang_indus_file)

print(df_lang_indus_file.index)

## Display Main Development Domain depending on Main Activity
df_lang_activity = df_lang_indus_file.loc[
                        ['main_activity','main_dev'], :].T
print(df_lang_activity)

# Collect all the main activity types, but only once for each type
unique_activity = np.sort(df_lang_activity['main_activity'].unique())
print(unique_activity)
# Collect all the main products types, but only once for each type
unique_products = np.sort(df_lang_activity['main_dev'].unique())
print(unique_products)
# For each type, count the number of each product

    
kk = df_lang_activity.groupby(['main_activity']).count().sort_values(                                      
                    ['main_dev'], ascending=False).rename(
                        columns={"Product" : "Number"}).reset_index()   
print(kk)

'''
NOT TERMINATED

plt.figure()
df_lang_activity.plot()
plt.show()
'''