#Make a DataFrames for testing site centers (both locations and counts per zip)

import pandas as pd

def get_site_info(city_csv):
    '''
    Function to grab the site locations from the City Database.

    Inputs: 
        city_csv (string): filepath for the test sites from the City Database

    Outputs:
        zips_n_locs (DataFrame): DataFrame with Zip Codes and the locations
            of testing centers
        zips_cts (DataFrame): DataFrame with counts of test sites per zip
    '''

    test_sites = pd.read_csv(city_csv)
    zips = test_sites['Address'].str.extract('(\d+$)')
    zips.rename(columns = {'0','ZIP'}, inplace= True)
    zips_cts = zips.groupby([0]).size().to_frame('Count').reset_index()
    zips_n_locs = pd.concat([zips, test_sites['Location']], axis = 1)

    return zips_n_locs, zips_cts

city_csv = '../csv_files/COVID-19_Testing_Sites.csv'

site_zips, zips_cts = get_site_info(city_csv)

site_zips.to_csv('../csv_files/test_sites.csv')
zips_cts.to_csv('../csv_files/test_site_ZIP_counts.csv')
