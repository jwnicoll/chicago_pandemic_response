Welcome to the csv_files directory!
The csv's saved here are cleaned and processed through code in the setup_code
directory. These csv's were eventually loaded into our project SQLite3 database,
(project.db), so they represent the cleanest form of data we've scraped, found,
linked, etc. We provide info on the sources, the description of what can be found
in the csv's, the corresponding scripts in setup_code used to make these csv's, and,
if the data was gathered from an online database, the csv in source_csv_files from
which this data originates.

Files stored here:

ages_by_zip.csv

    --original source: Census Bureau 2019 5 Year Estimates (https://data.census.gov/cedsci/)
    --description: file containing data on the median age, age dependency ratio,
        old age dependency ratio, and population proportion over 65 years of age,
        for different zip codes in Chicago
    --setup_code .py file: most processing was done using iPython,
        extra processing did occur in ages_income_by_zip.py
    --source_csv_file: was modified in place after importing from source

Cumulative_Cases_Tests_Deaths_Vacs_Zip_percapita.csv

    --original source: City of Chicago Data Portal (https://data.cityofchicago.org/)
    --description: file containing data on proportion of population that has 
        completed vaccination series, number of cumulative cases, tests, and deaths, 
        cumulative percent tested positive, and percent of population that was
        infected or died as well as number of tests normalized by population 
        for different zip codes in Chicago. Note that these numbers are cumulative up to 2/19/2021.
    --setup_code .py file: vacs_cases.py
    --source_csv_file: COVID-19_Cases__Tests__and_Deaths_by_ZIP_Code.csv

hospital_beds_by_zip.csv

    --original sources: City of Chicago Data Portal, UIC School of Public Health 
        (url: https://publichealth.uic.edu/uic-covid-19-public-health-response/
        covid-19-maps-chicago-illinois/number-of-hospital-beds-in-chicago/)
    --description: file containing hospital number of ICU beds and Medical and 
        Surgical Beds for different zip codes in Chicago.
    --setup_code .py file: hospitals.py
    --source_csv_file: Hospitals.csv 

income_by_zips.csv

    --original sources: Census Bureau 2019 5 Year Estimates (https://data.census.gov/cedsci/)
    --description: contains information about percent of population with incomes less than 
    10000, median income, and mean income for zip codes across the city
    --setup_code .py file: iPython, only needed column name changes to process,
        extra processing did occur in: ages_income_by_zip.py
    --source_csv_file: was modified in place after importing from source

opioids_deaths.csv

    --original sources: Cook County Medical Examiner Case Archive (https://datacatalog.cookcountyil
        .gov/Public-Safety/Medical-Examiner-Case-Archive/cjeq-bs86)
    --description: contains information about number of opioid deaths over a set period
        of time before and after the pandemic across zip codes (specifically, tabulating
        over a 10 month period from 4/1/2019 to 2/1/2020, taken as pre-pandemic, and
        a 10 month period from 4/1/2020 to 2/1/2021, taken as post-pandemic)
    --setup_code .py file: mental_health.py
    --source_csv_file: Medical_Examiner_Case_Archive.csv

suicide_deaths.csv

    --original sources: Cook County Medical Examiner Case Archive (https://datacatalog.cookcountyil
        .gov/Public-Safety/Medical-Examiner-Case-Archive/cjeq-bs86)
    --description: contains information about number of suicides over a set period
        of time before and after the pandemic across zip codes (specifically, tabulating
        over a 10 month period from 4/1/2019 to 2/1/2020, taken as pre-pandemic, and
        a 10 month period from 4/1/2020 to 2/1/2021, taken as post-pandemic) 
    --setup_code .py file: mental_health.py
    --source_csv_file: Medical_Examiner_Case_Archive.csv

Physicians_Counts.csv

    --original sources: City of Chicago Data Portal (https://data.cityofchicago.org/)
    --description: contains information about the number physicians located in 
        in different zip codes
    --setup_code .py file: physicians_counting.py and physicians_to_csv.py
    --source_csv_file: Physicians.csv

pop_and_uninsured_zips.csv

    --original sources: Census Bureau 2019 5 Year Estimates (https://data.census.gov/cedsci/)
    --description: contains information about percentage of population without health
        insurance for different zip codes
    --setup_code .py file: iPython, only needed column name changes to process
    --source_csv_file: was modified in place after importing from source

test_sites_by_zip.csv

    --original source: City of Chicago Data Portal (https://data.cityofchicago.org/)
    --description: contains information about the number of COVID testing sites
        per zip code
    --setup_code .py file: test_sites.py
    --source_csv_file: COVID-19_Testing_Sites.csv

therapists_by_zip.csv

    --original source: Psychology Today (https://www.psychologytoday.com/us/therapists/il/
        chicago?sid=602d7d88d7062&rec_next=1)
    --description: contains number of licensed therapists per zip code in the city
    --setup_code .py file: therapists_crawler.py
    --source_csv_file: obtained from web crawling, not from a database

vaccinations_and_healthcare_workers.csv

    --original sources: City of Chicago Data Portal, Census Bureau 2019 5 Year Estimates
    --description: contains information about cumulative vaccine doses administered
        per zip code and the number of healthcare workers living in each zip code.
        Used to adjust vaccination rates to account for these individuals who get
        vaccinated at a greater rate than the general population. Note, 
        vaccination rates in plots are from Cumulative_Cases_Tests_Deaths_Vacs_Zip_percapita.csv,
        but adjusting for number of healthcare workers comes from here
    --setup_code .py file: vacc_healthworkers.py
    --source_csv_files: COVID-19_Vaccinations_by_ZIP_Code.csv,
        occupations_2019.csv 

zip_location_key.csv

    --original sources: City of Chicago Data Portal (shapefile; url: https://data.cityofchicago.org
        /Facilities-Geographic-Boundaries/Boundaries-Neighborhoods/9wp7-iasj?fbclid=IwAR39gUjBfc6Tk
        sctQvMdQQtr96YEZ74JM4SkDymnBTLHzlE9xlhx6uZjbYc) and pgeocode package (url: https://pypi.org
        /project/pgeocode/)
    --description: contains zip codes from a Chicago zip code shapefile that was used in the heatmaps,
    this was taken as the canonical list of zips in the city. The pgeocode package was used to 
    convert these zips into latitude and longitude to facilitate distance calculations from zips
    So, this file maps these canonical zips to their coordinate location.
    --setup_code .py file: zip_location_key.py
