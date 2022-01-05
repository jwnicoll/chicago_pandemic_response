import pandas as pd

'''
Data was already in pretty good shape from US Census Bureau, so some processing
was done in iPython, but this file mainly served to reformat the zip codes
into a form conducive to our queries.
'''

#code to process the ages info/standardize into database, not to be run again
ages_zip_df = pd.read_csv('../csv_files/ages_by_zip.csv')
ages_zip_df['Zip_Code'] = ages_zip_df['Zip code'].str.extract(' (\d{5})')
ages_zip_df.drop(columns = ['Zip code', 'Unnamed: 0'], inplace = True)
ages_zip_df.to_csv('../csv_files/ages_by_zip.csv', index = False)

#code to process the income info/standardize for the database, not to be run again
income_zip_df = pd.read_csv('../csv_files/income_by_zip.csv')
income_zip_df['Zip_Code']= income_zip_df['Zip code'].str.extract(' (\d{5})')
income_zip_df.drop(columns = ['Zip code', 'Unnamed: 0', 'Unnamed: 0.1'], inplace = True)
income_zip_df.to_csv('../csv_files/income_by_zip.csv', index = False)
