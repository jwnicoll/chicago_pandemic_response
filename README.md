CS122 Chicagos Response to the Pandemic Group Project

ui                              -- THE PROGRAM IS RUN FROM THIS DIRECTORY. TO
                                   ACCESS THE WEBSITE, PLEASE GO HERE.
                                   Instructions are provided there in a README.
                                   Some guidance about how to use the interface
                                   to answer questions about Chicago's response to
                                   the pandemic, its preparedness, and its impact by
                                   zip code is also provided. We also provide 
                                   information relevant to the user experience here 
                                   (clarification on options/quantities, etc.)
                                   This directory contains files which contribute 
                                   to the website's display and functions. This
                                   directory is just a modifed version of the
                                   ui directory from pa3.
    project.db                      -- The database we used for this project,
                                       created from our .csv files
    SQLconstruction.txt             -- The SQL queries we used to make the database
    heatmap.py                      -- The program which creates heat maps
    query.py                        -- The problem which interprets user input
                                       and generates the corresponding data
                                       from the project database
    stats.py                        -- Program which converts the output from
                                       query.py into pandas objects to be used
                                       in heatmap.py, and in this file to
                                       perform statistical analyses
    res                             -- Resource directory containing csv files
                                       which are accessed by programs in the
                                       ui directory
    search                          -- Directory corresponding to the app we
                                       have built in Django. This is a modified
                                       version of the search directory from pa3
        views.py                    -- The file which creates the search form
                                       that the user interacts with, accesses
                                       user inputs, passes them between other
                                       programs in the ui directory, and makes
                                       the processed results which will be
                                       displayed on the webpage
        templates                   -- Directory with the html template
            newsite.html                -- The html template for the website we
                                           created.
    static                          -- Directory containing files used in
                                       the website formatting.
                                       main.css is taken directly from pa3,
                                       so our website is laid out
                                       very similarly.
    ui                              -- Directory containing settings.py among
                                       other files. We did not modify these
                                       files, and they are the same as in pa3

data_files                      -- Directory containing data collection
                                   documents
    csv_files                       -- The csv_files used to create the project
                                       SQLite3 database (project.db in ui dir).
                                       The list of files, as well as their 
                                       descriptions and sources, are documented
                                       in the README.txt in this directory
        source_csv_files                -- Original csv_files taken from online
                                           sources, in their original formats
                                           Later cleaned and processed by codes
                                           in setup_code, with the processed files
                                           being saved in the parent directory 
                                           (csv_files). For a list of csv files,
                                           please refer to the README.txt in
                                           this directory. 
                                           
    setup_code                      -- Programs used to collect and clean data
                                       We performed web crawling/scraping, pandas
                                       operations, and pseudo-record linkage
                                       (using Jaro-Winkler scores). Code is not
                                       meant to be run again, but is illustrative
                                       of how we obtained the csv's in csv_files.
                                       Please refer to the README.txt in this 
                                       directory for a list of scripts and 
                                       the specific processed csv_files they create,
                                       as well as the source_csv_files on which
                                       they operate.

trials                          -- Directory containing trials of the bokeh
                                   module. This had the advantage of producing
                                   interactive heatmaps, but we did not end up
                                   getting it to work

README.txt                      -- this file

All Resources Used:
NOTE: this list includes online sources consulted for programming issues,
as well as sources from which our data was drawn. A comprehensive list of
sources and which sources contributed to which csv's can be found in the README
in the csv_files directory.
# https://stackoverflow.com/questions/41982475/scraper-in-python-gives-access-denied
# https://www.psychologytoday.com/us/therapists/il/chicago?sid=602d7d88d7062&rec_next=1
# https://docs.djangoproject.com/en/3.1/intro/tutorial01/
# https://www.classes.cs.uchicago.edu/archive/2021/winter/12200-1/pa/pa3/index.html
# https://www.classes.cs.uchicago.edu/archive/2021/winter/12200-1/
# https://pandas.pydata.org/docs/ 
# City of Chicago Data Portal (https://data.cityofchicago.org/)
# American Community Survey 5-Year Estimates (https://data.census.gov/cedsci/)
# https://publichealth.uic.edu/uic-covid-19-public-health-response/covid-19-maps-chicago
    -illinois/number-of-hospital-beds-in-chicago/
# https://pypi.org/project/pgeocode/
# https://stackoverflow.com/questions/13587314/sqlite3-import-csv-exclude-skip-header
# Cook County Medical Examiner Case Archive, Cook County Data Portal
# (https://datacatalog.cookcountyil.gov/Public-Safety/Medical-Examiner-Case-Archive/cjeq-bs86)
#https://stackoverflow.com/questions/27147300/matplotlib-tcl-asyncdelete-async-handler-deleted-by-the-wrong-thread
