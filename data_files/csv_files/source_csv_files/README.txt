Welcome to the source_csv_files directory!

These are all of the raw csv files we took from our various sources, which were then
processed in setup_codes to make the clean and processed, ready-to-be-loaded-into
-the-SQLite3-database files in csv_files directory. Note if a file is not in here,
it was either in good enough shape just to need a lil iPython work to clean it up,
or was taken from web crawling and scraping.

Contents:

COVID-19_Cases__Tests__and_Deaths_by_ZIP_Code.csv
COVID-19_CasesTestsDeaths_Date.csv

--source: City of Chicago Data Portal
--used to make csv_file: Cumulative_Cases_Tests_Deaths_Vacs_Zip_percapita.csv

COVID-19_Testing_Sites.csv

--source: City of Chicago Data Portal
--used to make csv_file: test_sites_by_zip.csv

COVID-19_Vaccinations_by_ZIP_Code.csv

--source: City of Chicago Data Portal
--used to make csv_file: vaccinations_and_healthcare_workers.csv

Hospitals.csv

--source: City of Chicago Data Portal
--used to make csv_file: hospital_beds_by_zip.csv

Medical_Examiner_Case_Archive.csv

--source: Cook County Medical Examiner Case Archive (Cook County Data Portal)
--used to make csv_files: suicide_deaths.csv, opioids_deaths.csv

occupations_2019.csv

--source: US Census Bureau 2019 5-Year Estimates
--used to make csv_files: vaccinations_and_healthcare_workers.csv

Public_Health_Services-_Chicago_Primary_Care_Community_Health_Centers.csv
Physicians.csv

--source: City of Chicago Data Portal
--used to make csv_files: Physicians_Counts.csv
