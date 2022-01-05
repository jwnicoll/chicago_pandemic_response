#Added a column for zipcodes to the Physicians csv file.

import pandas as pd
import re

df = pd.read_csv('Public_Health_Services-_Chicago_Primary_Care_Community_Health_Centers.csv')
lst = []
for i in range(120):
    lst +=[re.findall('(\d{5}\n)',df.Address[i])[0][:-1]]
df['zipcodes'] = lst
df.to_csv(path_or_buf='Physicians.csv', sep=',')

