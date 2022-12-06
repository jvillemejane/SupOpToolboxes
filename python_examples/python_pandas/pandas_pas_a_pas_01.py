# -*- coding: utf-8 -*-
"""
Pandas library first example
- Creating Series and DataFrames
- Opening a data file
- Sorting data
- Visualizing data (matplotlib)

Author : Julien VILLEMEJANE
Laboratoire d Enseignement Experimental - Institut d Optique Graduate School
Version : 1.0 - 2022-12-01
"""

'''
TEST steamlit for web interface from plotly
https://www.youtube.com/watch?v=Sb0A9i6d320

TEST with plotly
import plotly
import plotly.graph_objects as go       # to plot data
import plotly.io as pio
'''

import pandas as pd
import numpy as np

from matplotlib import pyplot as plt


## Create a series
data_series = pd.Series([5, 1, 2, 5, 7, np.nan, np.pi])
print(data_series)

data_series2 = data_series.copy() # independent copy of data_series

# Create an indexed series
data_series_index = pd.Series([5, 3, 1, 7], index = ['a', 'b', 'c', 'd'])
# Add an index to an existing series
data_series2.reindex(['a','b','c','d','e','f','g'])

## Histogram of a Series
s = pd.Series(np.random.randint(0, 5, size=10))
print('Random List')
print(s)
hist = s.value_counts()
hist.sort_index(ascending=True)
print('histogramme')
print(hist)
plt.figure()
s.hist(range = (0, 5), bins = 5,alpha=1)
plt.show()



# Create series
year = pd.Series(np.arange(2013, 2022+1, 1))
promo = pd.Series([99, 113, 115, 120, 136, 153, 157, 124, 147, 110], index=year)
promo_h = pd.Series([71, 85, 81, 88, 90, 111, 110, 69, 99, 82], index=year)
promo_f = promo - promo_h

## Create a dataframe from Series
df_promo = pd.DataFrame([promo, promo_h, promo_f], 
                        index = ['Promo', 'Homme','Femme'])
## Display datas in a dataframe
print(df_promo)
print(df_promo.head(1))   # display only the n first rows
print(df_promo.tail(2))   # display only the n last rows

## Manipulate dataframe
df_2 = df_promo[2015]  # select only columns with specific value
print(df_2)

# Manipulate by labels
df_3 = df_promo.loc['Promo']  # select only specific rows
print(df_3)
df_4 = df_promo.loc[['Homme','Femme'], 2016:2020] 
            # select only specific rows and columns
print(df_4)

# Select by values
df_promo_T = df_promo.T     # Transpose datas
df_5 = df_promo_T[df_promo_T['Promo'] > 120]    
    # Select only rows where Promo is higher than 120
print(df_5)

## Statistics
mean_promo = df_promo_T.mean()  # Calculate average 
print(mean_promo)

## Display data with Matplotlib.pyplot
plt.figure()
df_promo_T.plot.area(stacked=False)
plt.legend(loc='best')
plt.show()


## Open a CSV file and convert data into a dataframe
df_promo_file = pd.read_csv('iogs_promo_annee.csv', index_col=0, 
                            encoding = "utf-8").T
    # Open *.csv file and make first column as index (here year) and transpose data
print(df_promo_file)

df_3_file = df_promo_file.loc['promo']  # select only specific rows
print(df_3_file)

# Display only 4 columns from 2016 to 2022
df_4_file = df_promo_file.loc[['promo','bordeaux','saint_etienne','palaiseau'], 2016:].T
plt.figure()
df_4_file.plot.bar()
plt.legend(loc='best')
plt.show()
