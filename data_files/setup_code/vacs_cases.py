#We'll extract cumulative statistics by zip code for cases,
#tests, positive test percentage, deaths, and vaccinations
#These csvs list statistics by week, so we take the most up to date
#cumulative statistics
#We normalize by zip code population where per capita data is lacking
#We provide a function to write to a csv with the desired data.

import pandas as pd

def extract_stats(csv_cases, csv_vacs):
    '''
    Function to take the csv file with data on cases, tests, and deaths,
    as well as the csv file with data on vaccinations,
    and produce a data frame with the desired cumulative statistics
    by zip code, normalized by zip code population

    Inputs:
        csv_cases (string): filepath for csv file of cases
        csv_vacs (string): filepath for csv file of vaccinations

    Outputs:
        merged_df (Pandas DataFrame): the final DataFrame
    '''
    vacs = pd.read_csv(csv_vacs)
    vacs['Date'] = pd.to_datetime(vacs['Date'])

    # Latest updates on vaccination percentages from 2/19/21 for all zip codes
    latest_vacs = vacs.groupby('Zip Code')['Date'].max()

    cum_perc_vacs = vacs.loc[vacs['Date'] == latest_vacs[0], ['Zip Code', \
            'Date', 'Vaccine Series Completed  - Percent Population']]

    cases = pd.read_csv(csv_cases)
    cases['Week End'] = pd.to_datetime(cases['Week End'])
    # Latest updates From 02/13/21 for all zip codes
    latest_cases = cases.groupby('ZIP Code')['Week End'].max()
    cases_zips = cases.loc[cases['Week End'] == latest_cases[0], \
            ['ZIP Code', 'Cases - Cumulative', 'Tests - Cumulative', \
            'Percent Tested Positive - Cumulative', 'Deaths - Cumulative', 'Population']]

    # No info for 60666
    cases_zips.fillna(0, inplace = True)

    cases_zips['Cases_Percent'] = (cases_zips['Cases - Cumulative'] / cases_zips['Population']) * 100
    cases_zips['Tests_Percent'] = (cases_zips['Tests - Cumulative'] / cases_zips['Population']) * 100
    cases_zips['Deaths_Percent'] = (cases_zips['Deaths - Cumulative'] / cases_zips['Population']) * 100
    cases_zips.fillna(0, inplace = True)

    cases_zips.rename(columns= {'ZIP Code':'Zip Code'}, inplace = True)

    merged_df = pd.merge(left = cum_perc_vacs, right = cases_zips, on='Zip Code')
    # Drop row with Unknown zip code (We think O'Hare)
    # This zip code has zero population in the cases csv, and 0 percent
    # vaccinated in the vacs csv.
    # It is listed as Unknown at every update of the cases csv
    merged_df = merged_df[merged_df['Zip Code'] != 'Unknown']
    merged_df.reset_index(drop = True, inplace = True)

    return merged_df


def write_csv():
    '''
    Write the dataframe with the desired statistics to a csv
    '''

    merged_df = extract_stats('COVID-19_Cases__Tests__and_Deaths_by_ZIP_Code.csv', \
            'COVID-19_Vaccinations_by_ZIP_Code.csv')
    merged_df.to_csv(path_or_buf = 'Cumulative_Cases_Tests_Deaths_Vacs_Zip_percapita.csv', \
            sep = ',')

def add_dates_to_cases():
    '''
    Adds 'Date' column to the cases csv such that dates are consistent
    with those in the vaccination csv.
    We will subtract 1 day from the Week End dates, and associate the result
    with the whole week.

    We originally added dates because we wanted the user to be able to select
    dates and see the progression of cases in a time series, but was not able
    to complete this in time.
    '''

    cases_df = pd.read_csv('COVID-19_Cases__Tests__and_Deaths_by_ZIP_Code.csv')
    cases_dates = cases_df['Week End']
    cases_dates = pd.to_datetime(cases_dates)
    cases_dates = cases_dates - pd.DateOffset(1)
    cases_df['Date'] = cases_dates
    cases_df.to_csv(path_or_buf = 'COVID-19_CasesTestsDeaths_Date.csv', sep = ',')
