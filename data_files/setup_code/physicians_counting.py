#Obtain counts of physicians by zip code from Physicians.csv

import pandas as pd

FILENAME = 'Physicians.csv'
OUTPUT_FILENAME = 'Physicians_Counts.csv'

def write_counts():
    '''
    Function which will write the desired CSV.
    '''
    phys_df = pd.read_csv(FILENAME)
    counts = phys_df.groupby('Zip_Code')['Address'].count()
    counts.rename('Counts', inplace = True)
    counts.to_csv(path_or_buf = OUTPUT_FILENAME, sep = ',')
