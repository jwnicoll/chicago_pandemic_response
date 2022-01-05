#The City of Chicago database a csv of hospitals and their locations within 
#the city, but no information on capacity (number of beds). The UIC School of
#Public Health has a web table with hospital names and bed capacities, but no
#locations. This file seeks to match these two datasets to obtain one table
#of with hospital names, locations, and capacity. Then, we group by zip code
#to find the number of hospital beds per zip code.
#
#Used to make hospital_beds_by_zip.csv
#
#Sources used: 
#    --forgot how strip worked for strings, so I'm citing that here
#        https://www.w3schools.com/python/ref_string_strip.asp
#    --see README in csv_files section for data sources used

import pandas as pd
import jellyfish
import bs4
import requests
import util


def get_hospital_capacities(url):
    '''
    Function that takes in the url containing a table of hospitals in Chicago
    and their bed capacities, and returns a dataframe

    Inputs:
        url (string): the url of the website containing the hospital bed info
            (https://publichealth.uic.edu/uic-covid-19-public-health-response/
             covid-19-maps-chicago-illinois/number-of-hospital-beds-in-chicago/)
    
    Outputs:
        capacity_df (Pandas DataFrame) dataframe containing hospitals,
            number of ICU beds in the hospitals, and number of medical
            or surgical beds in the hospital
    '''

    request = util.get_request(url)
    if request == None:
        return 'Request Failed'

    soup = bs4.BeautifulSoup(request.text, 'html5lib')

    #Extract information from the table on the site
    col_list = soup.find_all('th', scope = 'col')
    hosp_list = soup.find_all('th', scope = 'row')
    numbers_list = soup.find_all('td')

    hosp_to_medbed = {}
    hosp_to_icubed = {}

    for i, hosp in enumerate(hosp_list):
        
        #Skip the last two rows of the site table, contains totals
        #for city and state, which are not used in our analysis
        if i == len(hosp_list) - 2:
            break

        hosp_to_medbed[hosp.text.strip()] = int(numbers_list[2*i].text.strip())
        hosp_to_icubed[hosp.text.strip()] = int(numbers_list[1 + 2*i].text.strip())

    capacity_df = pd.DataFrame([hosp_to_medbed, hosp_to_icubed]).T.reset_index()

    capacity_df.rename(columns = {'index':col_list[0].text.strip(),
        0:col_list[1].text.strip(),
        1:col_list[2].text.strip()}, inplace = True)

    return capacity_df


def get_city_df(filepath):
    '''
    Function that takes in a filepath and returns the dataframe of hospitals from
    the City of Chicago Data Portal. This data does not include hospital capacities
    so we must link with the data scraped in the previous functions to match
    hospital capacities and their locations.

    Inputs:
        filepath (string): the filepath where csv from city database is

    Outputs:
        city_df (pandas DataFrame): DataFrame containing hospital names and location
            information
    '''

    city_df = pd.read_csv(filepath)
    city_df = city_df[['COMMONNAME,C,254', 'CITY,C,254', 'ADDRESS,C,254', 'ZIP,C,5']]
    col_rename = {'COMMONNAME,C,254':'Hospital', 'CITY,C,254':'City', \
            'ADDRESS,C,254':'Address', 'ZIP,C,5':'Zip_Code'}

    city_df.rename(columns = col_rename, inplace = True)

    return city_df


def match_with_city_csv(capacity_df, city_df):
    '''
    Function that does sort of a pseudo-record linkage to match the hospitals 
    from UIC data (hospital bed data) with the hospitals in the city csv. Uses
    Jaro-Winkler scores to determine similarity between the hospital names
    in both sets, and if they are very high, we classify them as a match
    and match them in a resulting dataset. If they are so-so, we bin into
    a possible dataset and examine by eye/google search.

    Inputs:
        capacity_df (Pandas DataFrame): Pandas DataFrame of UIC web data
        city_df (Pandas DataFrame): Pandas DataFrame of City Data Portal data
    
    Outputs:
        matches, maybe, nope (Pandas DataFrames): DataFrames with columns
            in capacity_df and city_df, where each row is a pairing between
            rows of city_df and capacity_df. matches have high J-W scores
            between names, maybe have sort of high vales, nope have low 
            values and are not worth sifting through
    '''

    #ci stands for 'city', ca stands for 'capacity'
    match_inds_ci = []
    match_inds_ca = []
    maybe_inds_ci = []
    maybe_inds_ca = []
    nope_inds_ci = []
    nope_inds_ca = []

    for i, hosp1 in city_df.iterrows():
        for j, hosp2 in capacity_df.iterrows():
            #Wanted to take out the word Hospital from the names, might give
            #more true matches
            score = jellyfish.jaro_winkler(hosp1['Hospital'].replace('Hospital', ''), \
                    hosp2['Hospital'].replace('Hospital', ''))

            if score >= 0.90:
                match_inds_ci.append(i)
                match_inds_ca.append(j)

            elif score >= 0.65 and score < 0.90:
                #dont include pairings in the maybe file where one hospital in 
                #the pair has already been matched
                if i not in match_inds_ci and j not in match_inds_ca:
                    maybe_inds_ci.append(i)
                    maybe_inds_ca.append(j)

            else:
                if i not in match_inds_ci and j not in match_inds_ca:

                    nope_inds_ci.append(i)
                    nope_inds_ca.append(j)

    matches = pd.concat([city_df.iloc[match_inds_ci].reset_index(drop = True), \
            capacity_df.iloc[match_inds_ca].reset_index(drop = True)], axis = 1)
    maybe = pd.concat([city_df.iloc[maybe_inds_ci].reset_index(drop = True), \
            capacity_df.iloc[maybe_inds_ca].reset_index(drop = True)], axis = 1)
    nope = pd.concat([city_df.iloc[nope_inds_ci].reset_index(drop = True), \
            capacity_df.iloc[nope_inds_ca].reset_index(drop = True)], axis = 1)

    return matches, maybe, nope

#After eyeballing the matches and maybe matches data, it seemed like
#all the matches were correct, and the following indices of the maybe
#matches were also correct. It seems like there is a significant disconnect
#between our Chicago hospital data and the bed info we found (significant
#lack of overlap with hospitals included), some hospitals no longer exist,
#and some names can be different to the point where it is impossible to tell
#if they are the same without physically googling and matching addresses.

#combinations of hospitals in the maybe dataframe that I googled and for sure
#can say are actually matches
MATCHES_MAYBE = [4, 6, 7, 8, 9, 10, 12, 16, 21, 23, 38, 35]


def add_matches_maybe(url, citydf_filepath):
    '''
    Function to take the matches dataframe from the previous function and
    tack on the rows from maybe where I physically looked at it and could
    tell that these rows were actually matches.

    Inputs:

        url (string): the UIC url (above)
        citydf_filepath (string): the filepath to find the Hospitals.csv
            file from the city database

    Outputs:

        city_df (Pandas DataFrame): Hospitals.csv data in DataFrame format
        capacity_df (Pandas DataFrame): UIC web table data in DataFrame format
        combined_df (Pandas DataFrame): DataFrame whose rows are known matches
            between the two datasets
    '''

    capacity_df = get_hospital_capacities(url)
    city_df = get_city_df(citydf_filepath)
    matches, maybe, nope = match_with_city_csv(capacity_df, city_df)
    matches_from_maybe = maybe.iloc[MATCHES_MAYBE]
    combined_df = pd.concat([matches, matches_from_maybe]).reset_index(drop = True)
    
    return city_df, capacity_df, combined_df

#Now, after looking at the combined_df, I tried to match the rest of the 
#hospitals from the city_df and capacity_df not included in combined_df
#by googling the names of the hospitals and in each frame and physically
#matching them in this way so as to achieve the most complete data.
#It should be noted that some hospitals in the city database were
#addiction centers/mental health clinics, so it makes sense that these
#would not be included in the UIC hospital bed data.

#indices from city and capacity dataframes that match
HANDPICKED_INDS_CI = [14, 24, 25, 29, 30, 34]
HANDPICKED_INDS_CA = [24, 10, 18, 15, 14, 1]


def make_final_matches(url, citydf_filepath):
    '''
    Function that takes the output of the last function (an incomplete set of matches)
    and returns a dataframe with rows added from the known matches I picked out
    by googling (given by HANDPICKED_INDS_CI and HANDPICKED_INDS_CA)

    Inputs:

        url (string): UIC url
        citydf_filepath(string): the filepath to find the Hospitals.csv
            file from the city database

    Outputs: 

        final_df (Pandas DataFrame): DataFrame with number of ICU beds and 
            surgical/medical beds per zip code
    '''

    city_df, capacity_df, record_linkage_df = add_matches_maybe(url, citydf_filepath)

    handpicked_rows_ci = city_df.iloc[HANDPICKED_INDS_CI].reset_index(drop = True)
    handpicked_rows_ca = capacity_df.iloc[HANDPICKED_INDS_CA].reset_index(drop = True)

    handpicked_rows = pd.concat([handpicked_rows_ci, handpicked_rows_ca], axis = 1)
    final_df = pd.concat([record_linkage_df, handpicked_rows]).reset_index(drop = True)

    return final_df


def get_beds_by_zip(url, citydf_filepath):
    '''
    The grandest function of them all: computes the output from the last function,
    and takes this most complete data table of hospitals with locations and 
    capacities and returns a DataFrame with number of beds for each zip code.

    '''

    hosp_bed_df = make_final_matches(url, citydf_filepath)
    
    beds_to_zip_df = hosp_bed_df.groupby('Zip_Code').agg({'ICU Beds' : sum, 'Medical and Surgical Beds' : sum}).reset_index()

    return beds_to_zip_df


bed_info_url = 'https://publichealth.uic.edu/uic-covid-19-public-health-response/covid-19-maps-chicago-illinois/number-of-hospital-beds-in-chicago/'
city_df_filepath = '../csv_files/source_csv_files/Hospitals.csv'


get_beds_by_zip(bed_info_url, city_df_filepath).to_csv('../csv_files/hospital_beds_by_zip.csv', index = False)
