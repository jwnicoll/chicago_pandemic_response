'''
This file handles the output from the query.py file, produces pandas objects,
and performs statistical analyses corresponding to user selections.
'''

#Source consulted to fix bug with matplotlib/Django interaction:
#https://stackoverflow.com/questions/27147300/matplotlib-tcl-asyncdelete-async-handler-deleted-by-the-wrong-thread

import pandas as pd
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import geopandas as gpd


def make_df(data, name):
    '''
    Given list of tuples with zip codes and quantifiers,
    convert to a series object

    Inputs:
        data: list of tuples with zip codes and quantifiers
        name: variable name

    Returns:
        Pandas series object with indexes for all zip codes for which
            perform statistical analyses
    '''
    dic = {}
    for datum in data:
        dic[datum[0]] = datum[1]
    series = pd.Series(dic, name = name)
    # Here we ensure the desired number of zip codes have values,
    # which may be missing
    all_zips = pd.read_csv('./res/AllZips.csv', index_col = 0)
    merged = pd.DataFrame(index = all_zips.index)
    merged[name] = series
    series = merged[name]
    # For th purposes of statistical analyses, we fill missing values with
    # the mean values across all other zip codes
    series.fillna(series.mean(skipna=True), inplace = True)
    return series


def df_for_heatmap(data, name):
    '''
    A function similar to make_df, but we produce series of length 61
    to account for the duplicate zip code in the heatmap shapefile

    Inputs:
        data (list of tuples): A list of tuples whose entries correspond
            to zip codes and a quantifier
        name (str): The name of the variable selected by the user, and which
            corresponds to data
    
    Returns:
        Pandas series object with indexes for all zip codes in the shapefile
    '''
    dic = {}
    for datum in data:
        dic[datum[0]] = datum[1]
    series = pd.Series(dic, name = name)
    # Here we ensure the desired number of zip codes have values,
    # which may be missing
    shapefile = './res/Neighborhoods/geo_export_a131bb4a-42f9-4af9-bd33-aedec365203f.shp'
    chicago = gpd.read_file(shapefile)
    zips = chicago['zip'].apply(pd.to_numeric)
    merged = pd.DataFrame(index = zips)
    merged[name] = series
    series = merged[name]
    # For the purposes of making heatmaps, we fill missing values with -1
    series.fillna(-1, inplace = True)
    return series


def combine_series(data1, data2):
    '''
    Extract merged dataframe and variable names from series that have entries
    for all zip codes, which is guaranteed by df_for_heatmap and make_df

    Inputs:
        data1, data2 (Pandas Series): The series containing information
            corresponding to the user's selection

    Returns:
        var1, var2 (str): The names of the variables corresponding to
            data1 and data2
        merged (pandas DataFrame): A dataframe with the data for both
            variables, with all entries filled
    '''
    var1 = data1.name
    var2 = data2.name
    merged = pd.merge(left=data1, right = data2, on = data1.index,
                      how = 'inner')
    # Account for the case that the user inputs the same variable
    if var1 == var2:
        merged.rename(columns = {var1 + '_x' :var1, var2+'_y': var2},
                      inplace = True)
    return (var1, var2, merged)


def make_scatter(data1, data2):
    '''
    Make a scatter plot from two pandas series corresponding to the user's 
    selections

    Inputs:
        data1, data2 (Pandas Series): The series containing information
            corresponding to the user's selection
    
    Saves the scatter plot as a .png
    '''
    var1, var2, merged = combine_series(data1, data2)
    fig = plt.figure()
    # Index this way in case var1 == var2
    plt.scatter(merged.iloc[:, 1], merged.iloc[:,2])
    plt.xlabel(var1)
    plt.ylabel(var2)
    plt.title(var2+' vs. ' +var1 + ' Scatter Plot')
    fig.savefig('static/scatter.png')
    plt.close(fig)


def linear(x, m, b):
    '''
    Functional form for a linear fit
    '''
    return ((m * x) + b)


def power_law(x, a, b):
    '''
    Functional form for a power law fit
    '''
    return (a * (x**b))


def exp_fit(x, a, b):
    '''
    Functional form for an exponential fit
    '''
    return (a * (np.exp(b * x)))


def make_fit(data1, data2, fit_type):
    '''
    Plot regression according to the chosen fit type

    Inputs:
        data1, data2 (Pandas Series): The series containing information
            corresponding to the user's selection
        data2 will be plotted as a function of data1
            fit_type (str): The type of fit requested by the user
    
    Saves the plot as a .png
    '''
    var1, var2, merged = combine_series(data1, data2)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    X = np.linspace(merged[var1].min(), merged[var1].max(), 500)
    # We again use iloc to index to account for the case where var1 == var2
    ax.scatter(merged.iloc[:, 1], merged.iloc[:,2])
    ax.set_xlabel(var1)
    ax.set_ylabel(var2)
    ax.set_title(var2+' vs. ' +var1 + ' '+ fit_type + ' Fit')
    if fit_type == 'Linear':
        # p0 chosen to initially suggest no dependence of data2 on data1
        pars, cov = curve_fit(f=linear, xdata=merged.iloc[:, 1],
                              ydata=merged.iloc[:,2],
                              p0=[0,merged.iloc[:,2].mean()])
        ax.plot(X, linear(X, pars[0], pars[1]), 'r-', label = 'Linear Fit')
        textfit = '$f(x) = mx + b$ \n' \
                  '$m = %.3f$ \n' \
                  '$b = %.3f$ \n' \
                  % (pars[0], pars[1])
    if fit_type == 'Power Law':
        pars, cov = curve_fit(f=power_law, xdata=merged.iloc[:, 1],
                              ydata=merged.iloc[:,2],
                              p0=[merged.iloc[:,2].mean(),0])
        ax.plot(X, power_law(X, pars[0], pars[1]), 'r-',
                label = 'Power Law Fit')
        textfit = '$f(x) = ax^b$ \n' \
                  '$a = %.3f$ \n' \
                  '$b = %.3f$ \n' \
                  % (pars[0], pars[1])
    if fit_type == 'Exponential':
        pars, cov = curve_fit(f=exp_fit, xdata=merged.iloc[:, 1],
                              ydata=merged.iloc[:,2],
                              p0=[merged.iloc[:,2].mean(),0])
        ax.plot(X, exp_fit(X, pars[0], pars[1]), 'r-',
                label = 'Exponential Fit')
        textfit = '$f(x) = Ae^{\lambda x}$ \n' \
                  '$A = %.3f$ \n' \
                  '$\lambda = %.3f$ \n' \
                  % (pars[0], pars[1])
    ax.text(0.8, 0.95, textfit, transform=ax.transAxes, fontsize=8,
        verticalalignment='top')
    fig.savefig('static/fit.png')
    plt.close(fig)
