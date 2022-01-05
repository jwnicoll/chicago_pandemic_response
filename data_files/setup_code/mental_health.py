#Code to extract the mental health-related data from pandemic impacts. Takes
#in the raw csv from the Cook County Medical Examiner and returns number of
#suicides and opioid-related deaths pre and post-pandemic (10 month periods,
#one before and one after the pandemic)

import pandas as pd

death_data = pd.read_csv('../csv_files/source_csv_files/Medical_Examiner_Case_Archive.csv', index_col = 'OBJECTID')

def find_zipcode_deaths(date1, date2, death_type, death_data):
    '''
    Function that takes in two dates (start and end date) and finds the number
    of deaths of either suicide or opioid overdose per zip code over this period
    of time.

    Inputs:
        date1, date2 (string): start and ending dates
        death_type(string): either opioid or suicide
        death_data (Pandas DataFrame): the Medical Examiner csv
    '''

    year1 = date1[-4:]
    year2 = date2[-4:]

    if death_type == 'opioid':
        is_death_type = death_data['Opioid Related'] == True

    elif death_type == 'suicide':
        is_death_type = death_data['Manner of Death'] == 'SUICIDE'

    is_chicago = death_data['Residence City'] == 'Chicago'

    chicago_death = death_data[is_chicago & is_death_type]
    death_dates = chicago_death['Date of Death']

    deaths_in_range = chicago_death[((death_dates.str.contains(year1)) & \
        (death_dates > date1)) | ((death_dates.str.contains(year2)) & \
            (death_dates < date2))]

    zipcode_deaths = deaths_in_range.groupby(['Residence_Zip']).size(). \
            to_frame("Count").reset_index()

    return zipcode_deaths

#get appropriate numbers of deaths for either opioid overdose or suicide
#and then join them

pre_suicide_df = find_zipcode_deaths('02/1/2020', '04/1/2019', \
        'suicide', death_data)
post_suicide_df = find_zipcode_deaths('04/1/2020', '02/1/2021', \
        'suicide', death_data)
pre_suicide_df.rename(columns={'Count' : 'pre_suicide_count', \
    'Residence_Zip' : 'Zip_Code'}, inplace = True)
post_suicide_df.rename(columns={'Count' : 'post_suicide_count', \
    'Residence_Zip' : 'Zip_Code'}, inplace = True)
suicides = pd.merge(pre_suicide_df, post_suicide_df, on = 'Zip_Code', \
        how = 'outer').fillna(0)
pre_opioid_df = find_zipcode_deaths('02/1/2020', '04/1/2019', 'opioid', \
        death_data)
post_opioid_df = find_zipcode_deaths('04/1/2020', '02/1/2021', 'opioid', \
        death_data)
pre_opioid_df.rename(columns={'Count' : 'pre_opioid_count', \
        'Residence_Zip' : 'Zip_Code'}, inplace = True)
post_opioid_df.rename(columns={'Count' : 'post_opioid_count', \
        'Residence_Zip' : 'Zip_Code'}, inplace = True)
opioids = pd.merge(pre_opioid_df, post_opioid_df, on = 'Zip_Code',\
        how = 'outer').fillna(0)

#zip code is 99999, probably a bad zip, so we drop it
opioids.drop(index = 60, inplace = True)
opioids.to_csv('../csv_files/opioids_deaths.csv')
suicides.to_csv('../csv_files/suicide_deaths.csv')
