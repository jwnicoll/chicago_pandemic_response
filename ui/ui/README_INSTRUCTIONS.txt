Welcome! This readme contains instructions on how to run our database
and what you might see and how you might use it to answer questions about
Chicago's response and preparedness for the pandemic, as well as 
the impact on the city on the level of zip codes.

Instructions:

The following command needs to be run one time:
    python3 manage.py migrate
After that, the website can be run with the following command:
    python3 manage.py go
Paste the link and you're good to go!
NOTE: you might have to refresh the page in order for the plots to update.
NOTE ALSO: This is tested to work in vdesk. I'm not sure if that changes
anything, but just in case, everything works fine over there.

User Options/Guidance:

Users have the option of selecting from many different variables relevant
to the city's response and preparedness to respond to the pandemic, as well
as it's impact, on a Zip Code level. The following groups the potential options
according to choose from in drop down menus according to these categories.

Impact:

--percent_cases: number of cases as a percentage of ZIP population
--percent_deaths: number of deaths as a percentage of ZIP population
--percent_poverty: percent of individuals in ZIP code making less than
    $10000 per year
--percent_change_opioid: percent change in opioid deaths comparing number of deaths
    over a 10 month period before the pandemic to a 10 month period post-beginning
    of the pandemic (specifically: 2/1/2019 - 4/1/2020, 4/1/2020 - 2/1/2021). Given
    by ((post-pre)/pre)*100. If there were no deaths in the period before the pandemic,
    we calculate this score as (post - pre)*100.
--percent_change_suicide: similar to opioid, but for suicides instead
--deaths_adjusted: percent_deaths, but adjusted by the percentage of the ZIP
    population above age 65, the idea being that older individuals are more susceptible
    to severe COVID illness and death. We use the following formula for this metric:
    adjusted = unadjusted_percent*(1-percent_65/100)
--percent_uninsured: percentage of the Zip Code that has no health insurance
--percent_senior: percentage of the Zip Code that is over the age of 65

Response:

--percent_tests: number of tests, normalized (divided by) population, and
    multplied by 100 (so tests per capita times 100)
--test_sites: number of test sites in each Zip Code
--test_site_access: just because you don't have many test_sites in your zip code
    doesn't mean they aren't accessible (can drive, walk, etc. and leave your ZIP).
    So, for each ZIP, test_site_access calculates a weighted sum over all ZIPS, where 
    each term is the number of test sites in a zip code weighted by 1/distance between
    this zip code in the sum and the zip code at hand (the zip code for which the statistic
    is being calculated).
--vaccinations: percent of individuals in the zip code that have completed a full
    vaccination series
--vaccinations_adjusted: at this point, mostly healthcare workers have been vaccinated,
    so this might prove a confounder for any analyses about the distribution of 
    vaccinations across the city. So, we adjust the vaccination percentages by 
    penalizing zip codes with greater proportions of healthcare workers. We
    use the formula adjusted = unadjusted_percent*(1-percent_health/100), where
    percent_health is the percentage of the population that is healthcare workers.

Preparedness:

--icu_beds: number of ICU beds in hospitals per ZIP code
--medical_and_surgical_beds: number of medical and surgical beds per ZIP code
--therapists: number of licensed therapists with practices in a zip code
--physicians: number of community physicians with practices in a zip code
--icu_accessibility: just because a ZIP code doesn't have ICU beds doesn't
    mean ICU beds aren't accessible. So, for each ZIP, icu_accessibility calculates
    a weighted sum over all ZIPS, where each term is the number of ICU beds in a 
    zip code weighted by 1/distance between this zip code in the sum and the zip
    code at hand (the zip code for which icu_accessibility is being calculated).
--physician_accessibility: similar to icu_accessibility, but instead of summing
    over the number of ICU beds in a ZIP, it's the number of physicians per zip
--therapist_accessibility: similar to icu_accessibility, but instead of summing
    over ICU beds, we sum over number of therapists

Choose any two variables to plot side-by-side heatmaps to analyze any trends
that might elucidate trends in the city's response, preparedness, or impact.
For instance, to assess the city's preparedness for the mental health crisis
of COVID, we might plot therapist_accessibility alongside percent_change_suicide
to see if neighborhoods with greater suicide rates have less accessibility to
therapists. Or perhaps, you would like to see if the city's response to the 
pandemic has been disproportionately weighted against the poor, so you might
plot vaccinations_adjusted alongside percent_poverty. 

Furthermore, after selecting variables you find interesting, you may also
select a fit to perform on a scatter plot, and you may visually determine 
goodness of fit to see if the relationships between variables can be modeled
according to common fit functions.

The format of this directory is similar to the ui directory used in pa3,
and much of the code in the search and ui subdirectories are the same.
The main.css function in the static directory is also the same as that which
was used in pa3.

Links to the pa3 website and course home page are given below:
https://www.classes.cs.uchicago.edu/archive/2021/winter/12200-1/pa/pa3/index.html
https://www.classes.cs.uchicago.edu/archive/2021/winter/12200-1/
