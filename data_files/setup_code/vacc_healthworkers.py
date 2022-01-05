#Puts cumulative vaccination rates by zip code and the percent healthcare
#workers all in one place. Allows us to adjust vaccination rates by zip code
#when comparing across zips for a more valid comparison.

import pandas as pd

occupations = pd.read_csv('../csv_files/source_csv_files/occupations_2019.csv')
vaccinations = pd.read_csv('../csv_files/source_csv_files/COVID-19_Vaccinations_by_ZIP_Code.csv')

def create_vaccocc_csv(date):
    '''
    Function that takes in a date, and finds the cumulative vaccinations by
    zip up to that date, and joins it with the percent healthcare workers
    in that zip.

    Inputs:
        date (string): the date

    Outputs:
        vacc_date (pandas DataFrame): 
    '''

    health_care_zips = occupations['NAME'].str.extract('(\d{5}$)')[1:]
    health_occs = occupations['S2402_C01_015E'][1:].astype('int') + \
        occupations['S2402_C01_019E'][1:].astype('int')
    health_care_zips['Total Workers'] = health_occs
    health_care_zips = health_care_zips.rename(columns = {0 : 'Zip Code'})

    total = vaccinations.merge(health_care_zips)

    vacc_date = total[total['Date'] == date][['Zip Code', 'Total Doses - Cumulative',\
            'Vaccine Series Completed - Cumulative', 'Total Workers', 'Population']]

    vacc_date['percent_healthworkers'] = (vacc_date['Total Workers']/vacc_date['Population'])*100
    vacc_date.rename(columns = {'Zip Code' : 'Zip_Code'}, inplace = True)

    return vacc_date

vacc_date = create_vaccocc_csv('02/19/2021')

vacc_date.to_csv('../csv_files/vaccinations_and_healthcare_workers.csv', index = False)
