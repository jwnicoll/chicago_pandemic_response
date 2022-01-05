'''
This file produces a heatmap based on data which is indexed by zipcode.
'''

#Source used to fix bug with matplotlib:
#https://stackoverflow.com/questions/27147300/matplotlib-tcl-asyncdelete-async-handler-deleted-by-the-wrong-thread

import pandas as pd
import geopandas as gpd
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt


def plot_heatmap(data, one):
    '''
    Creates heatmap for the data requested by the user

    Inputs:
        data (pandas Series): Contains data for the quantifier requested
            by the user, indexed by zip code
        one (bool): Saves as the heatmap for the first variable when
            one is True, and for the second variable when one is False
    
    Saves the heatmap as a .png
    '''
    shapefile = './res/Neighborhoods/geo_export_a131bb4a-42f9-4af9-bd33-aedec365203f.shp'
    chicago = gpd.read_file(shapefile)
    new_chicago = chicago.set_index('zip', drop=False)
    
    merged = pd.merge(left = new_chicago, right = data, on = new_chicago.index, how = 'inner')
    
    data_name = data.name
    fig, ax = plt.subplots(1, 1)
    merged.plot(column=data_name, ax=ax, legend=True, cmap='OrRd')
    # Control which heatmap is made
    if one:
        plt.savefig('static/var1.png')
    else:
        plt.savefig('static/var2.png')
    plt.close(fig)
