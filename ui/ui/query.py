#File that compiles SQL queries together based on user input from web interface,
#similar to the methods used in PA3. The database we query is project.db

import sqlite3
from math import radians, cos, sin, asin, sqrt

#Dictionary mapping possible selections of dropdown menus to the SELECT chunk
#of the query
COL_DICT = {'percent_cases': ['tdvz.Cases_Percent'],
        'percent_deaths': ['tdvz.Deaths_Percent'],
        'percent_tests': ['tdvz.Tests_Percent'],
        'icu_beds': ['hosp.[ICU Beds]'],
        'medical_and_surgical_beds': ['hosp.[Medical and Surgical Beds]'],
        'percent_senior': ['ages.[percent_65+]'],
        'percent_poverty': ['income.Percent_less_10000'],
        'percent_change_opioid': ['find_percent_change(od.pre_opioid_count, od.post_opioid_count) AS change'],
        'percent_change_suicide': ['find_percent_change(sd.pre_suicide_count, sd.post_suicide_count) AS change'],
        'percent_uninsured': ['uninsured.percent_uninsured'],
        'test_sites': ['site.site_count'],
        'therapists': ['therapists.number'],
        'physicians': ['physicians.number'],
        'vaccinations': ['tdvz.Percent_Vacc_Series_Completed'],
        'icu_accessibility': ['SUM(score_between_zips(l1.longitude, l1.latitude, l2.longitude, l2.latitude, hosp.[ICU Beds]))'],
        'physician_accessibility': ['SUM(score_between_zips(l1.longitude, l1.latitude, l2.longitude, l2.latitude, physicians.number))'],
        'therapist_accessibility': ['SUM(score_between_zips(l1.longitude, l1.latitude, l2.longitude, l2.latitude, therapists.number))'],
        'test_site_access': ['SUM(score_between_zips(l1.longitude, l1.latitude, l2.longitude, l2.latitude, site.site_count))'],
        'deaths_adjusted': ['adjust_by_factor(tdvz.Deaths_Percent, ages.[percent_65+])'],
        'vaccinations_adjusted': ['adjust_by_factor(tdvz.Percent_Vacc_Series_Completed, health.percent_healthworkers)']}

#Dictionary mapping the possible selections of dropdown menus to the tables that will be needed
TABLE_DICT = {'percent_cases': ['tests_deaths_vacs_zip AS tdvz'],
        'percent_deaths': ['tests_deaths_vacs_zip AS tdvz'],
        'percent_tests': ['tests_deaths_vacs_zip AS tdvz'],
        'icu_beds': ['hospital_beds AS hosp'],
        'medical_and_surgical_beds': ['hospital_beds AS hosp'],
        'percent_senior': ['ages'],
        'percent_poverty': ['income'],
        'percent_change_opioid': ['opioid_deaths AS od'],
        'percent_change_suicide': ['suicide_deaths AS sd'],
        'percent_uninsured': ['uninsured'],
        'test_sites': ['test_sites AS site'],
        'therapists': ['therapists'],
        'physicians': ['physicians'],
        'vaccinations': ['tests_deaths_vacs_zip AS tdvz'],
        'icu_accessibility': ['location AS l2', 'location AS l1', 'hospital_beds as hosp'],
        'physician_accessibility': ['location AS l2', 'location AS l1', 'physicians'],
        'therapist_accessibility': ['location AS l2', 'location AS l1', 'therapists'],
        'vaccinations_adjusted': ['tests_deaths_vacs_zip AS tdvz', 'healthworkers AS health'],
        'test_site_access': ['location AS l2', 'location AS l1', 'test_sites AS site'],
        'deaths_adjusted': ['tests_deaths_vacs_zip AS tdvz', 'ages']}

#Dictionary mapping the table names to their abbreviations
TABLE_ABBR_KEY = {'tests_deaths_vacs_zip AS tdvz' : 'tdvz',
        'hospital_beds AS hosp' : 'hosp',
        'ages' : 'ages',
        'income' : 'income',
        'uninsured': 'uninsured',
        'opioid_deaths AS od' : 'od',
        'suicide_deaths AS sd' : 'sd',
        'test_sites AS site' : 'site',
        'therapists' : 'therapists',
        'physicians' : 'physicians',
        'healthworkers AS health' : 'health',
        'location AS l2' : 'l2'}

#For certain inputs, we need join conditions. This maps the columns
#to the join condition clause, if it needs one
JOIN_CONDS = {'icu_accessibility': ['hosp.Zip_Code == l1.Zip_Code'],
        'physician_accessibility': ['physicians.Zip_Code == l1.Zip_Code'],
        'therapist_accessibility': ['therapists.Zip_Code == l1.Zip_Code'],
        'vaccinations_adjusted': ['tdvz.Zip_Code == health.Zip_Code'],
        'test_site_access': ['site.Zip_Code == l1.Zip_Code'],
        'deaths_adjusted': ['tdvz.Zip_Code == ages.Zip_Code']}


def find_columns(args):
    '''
    Takes in a list with two items, one corresponding to the first
    piece of information we want to see by zip code, and the second for
    the other piece of information. Makes two separate SQL queries to get this
    info and returns a list of tuples where each tuple is a combination of Zip_Code and
    the value of interest to be plotted on the heatmaps

    Inputs:
        args (dictionary): dictionary whose values are the dropdown menu
            selections given by the user

    Outputs:
        output1, output2 (strings) the SQL queries for the database
    '''

    arg1 = args[0]
    arg2 = args[1]

    output1 = find_column(arg1)
    output2 = find_column(arg2)
    
    return output1, output2

def find_column(arg):
    '''
    The main function: takes in an argument from the user drop down menus,
    makes a query string for the database, and gives the output in the form
    of a list of tuples where each tuple is a combination of Zip_Code and
    the value of interest to be plotted on the heatmaps

    Inputs:
        arg (string): the string from the dropdown menu

    Outputs:
        output (list of tuples): described above 
    '''

    q_string = make_query_string(arg)
    connection = sqlite3.connect('project.db')
    connection.create_function('adjust_by_factor', 2, adjust_by_factor)
    connection.create_function('score_between_zips', 5, score_between_zips)
    connection.create_function('find_percent_change', 2, find_percent_change)
    connection.create_function('haversine', 4, haversine)

    curs = connection.cursor()
    curs.execute(q_string, ())
    output = curs.fetchall()

    connection.close()

    return output


def make_query_string(arg):
    '''
    Takes in a string argument corresponding to what you might want to see
    on a heatmap and returns a sql query string to get te necessary columns/
    calculations. Arg must be a string that corresponds to a pre-created
    drop-down menu choice.

    Inputs:
        arg (string): dropdown menu option, what the user wants to see

    Outputs:
        query_string (string): string to query the database with
    '''

    selects = COL_DICT[arg].copy()
    joins = TABLE_DICT[arg]
    selects.insert(0, TABLE_ABBR_KEY[joins[0]] + '.Zip_Code')

    select_string = ', '.join(selects)
    join_string = ' JOIN '.join(joins)

    if len(joins) > 1:
        join_conds = JOIN_CONDS[arg]
        join_conds_string = ' AND '.join(join_conds)
        query_string = 'SELECT ' + select_string + ' FROM ' + join_string + ' ON ' + join_conds_string

    else:
        query_string = 'SELECT ' + select_string + ' FROM ' + join_string

    #special case: if we are doing a distance calculation across zip codes
    #do a group by on each zip code
    if 'l2.Zip_Code' in select_string:
        query_string = query_string + ' GROUP BY l2.Zip_Code'

    return query_string


def find_percent_change(pre, post):
    '''
    Function to find the percent change in opioid/suicide deaths from sometime
    before the pandemic compared to sometime after. 

    Inputs:
        pre (integer): the cumulative number of events in a period before pandemic
        post (integer): the cumulative number of events during pandemic

    Outputs:
        The percent change. Note, we take the liberty of calculating this as
        (post - pre)*100 if there are no events in the period before the pandemic
    '''

    if pre == 0:
        return (post - pre)*100

    return ((post - pre)/pre)*100


def haversine(lon1, lat1, lon2, lat2):
    '''
    Calculate the circle distance between two points
    on the earth (specified in decimal degrees).
    Taken from PA3, but this time returning km instead of m.

    Inputs:
        lon1, lat1, lon2, lat2: the coordinates of the two zip codes

    Outputs:
        km (float): the distance between the zips
    '''
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))

    # 6367 km is the radius of the Earth
    km = 6367 * c
    return km


def score_between_zips(lon1, lat1, lon2, lat2, quantity):
    '''
    Function that takes in two locations and the quantity associated with
    one of the locations and spits out the quantity scaled by 1/distance,
    to be summed up to create physician accessibility, therapist accessibility,
    and test site access metrics.

    Inputs:
        lon1, lat1, lon2, lat2: the coordinates of the zip codes

    Outputs:
        The value of the quantity, scaled by 1/distance
    '''

    dist = haversine(lon1, lat1, lon2, lat2)
    if dist == 0:
        return quantity*10

    return quantity/dist


def adjust_by_factor(orig, factor):
    '''
    Function that takes in an original rate/proportion for a zip code
    and scales by some fractional quantity to adjust for some factor. In this
    case, we are mainly focused on vaccination percentages and death percentages
    per zip and using a scaling factor to adjust for percent population healthcare
    worker and percent population 65+.

    Inputs:
        orig (float): the original number
        factor (float): the quantity with which we will adjust the number

    Outputs:
        The adjusted quantity
    '''

    return orig*(1 - factor/100)
