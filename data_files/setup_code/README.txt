Welcome to the setup_code directory!

These are all the codes we've constructed to put our data into nice formats,
either data taken from an online database or from scraping. This also where
we did any sort of record linkage, all to put the data in a nice form for
the SQLite3 database (project.db in the ui directory). If the program
processes something from an online database, the original csv it processed
is stored in source_csv_files within the csv_files directory. The resultant
csv files from these codes are stored in csv_files.

As before, note that some csv's have very short scripts, and that is because
those csv's already came in a suitable format and only needed some mild iPython/
some changes worth documenting in a .py file to get into good shape.

NOTE: These files are not meant to be run, we ran them once to obtain the data.

Contents: 

Provided are the csv_file the script created, and the source the file acts on.
If taken from an online database, the source_csv_file is provided. If scraped/
crawled, the web url is provided.

ages_by_income_by_zip.py

    --csv_files: ages_by_zip, income_by_zip
    --source: was modified in place after importing from source

hospitals.py

    --csv_files: hospital_beds_by_zip.csv
    --sources: Hospitals.csv, UIC School of Public Health (https://publichealth
        .uic.edu/uic-covid-19-public-health-response/covid-19-maps-chicago-
        illinois/number-of-hospital-beds-in-chicago/)

mental_health.py

    --csv_files: opioids_deaths.csv, suicides_deaths.csv
    --sources: Medical_Examiner_Case_Archive.csv


physicians_counting.py

    --csv_files: Physicians_Counts.csv 
    --sources: Physicians.csv

test_sites.py

    --csv_files: test_sites_by_zip.csv 
    --sources: COVID-19_Testing_Sites.csv

therapists_crawler.py

    --csv_files: therapists_by_zip.csv
    --sources: Psychology Today (https://www.psychologytoday.com/us/therapists/il/
        chicago?sid=602d7d88d7062&rec_next=1)

util.py

    File to facilitate web requests, crawling, and scraping from PA2

vacc_healthworkers.py

    --csv_files: vaccinations_and_healthcare_workers.csv
    --sources: COVID-19_Vaccinations_by_ZIP_Code.csv, occupations_2019.csv

vacs_cases.py

   --csv_files: Cumulative_Cases_Tests_Deaths_Vacs_Zip_percapita.csv
   --sources: COVID-19_Cases__Tests__and_Deaths_by_ZIP_Code.csv

zip_location_key.py

   --csv_files: zip_location_key.csv
   --sources: City of Chicago Data Portal (shapefile; url: https://data.
        cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-
        Neighborhoods/9wp7-iasj?fbclid=IwAR39gUjBfc6TksctQvMdQQtr96YEZ74
        JM4SkDymnBTLHzlE9xlhx6uZjbYc) and pgeocode package (url: https://pypi.org
        /project/pgeocode/)`
