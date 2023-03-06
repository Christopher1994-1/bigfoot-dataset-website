import pandas as pd
import json
import math

def one_case(state, county, id_number):

    bigfoot_geo_reports = pd.read_csv('bfro_reports_geocoded.csv')
    
    state = str(state).title()
    id_number = float(id_number)

    df = bigfoot_geo_reports
    df_state = df.loc[(bigfoot_geo_reports['state'] == state) & (bigfoot_geo_reports['county'] == county) & (bigfoot_geo_reports['number'] == id_number)]

    json_rows = []
    for a, row in df_state.iterrows():
        json_row = row.to_dict()
        json_rows.append(json_row)
        

        
    return json_rows



months = {
    "01":"January",
    "02":"February",
    "03":"March",
    "04":"April",
    "05":"May",
    "06":"June",
    "07":"July",
    "08":"August",
    "09":"September",
    "10":"October",
    "11":"November",
    "12":"December",
}

# value = str(value_get[0]).split('.')[0]

# original_value = value_get[0]
original_value = 10438.0
state = 'texas'
county = 'Liberty County'
# state = state_selected[0]
# county = county_selected[0]
# image = images[state]

rows = one_case(state, county, original_value)
class_ = rows[0]['classification'] # pass this

date = str(rows[0]['date']).split('-')

YEAR = date[0] # pass this
MONTH = months[date[1]] # pass this
DAY = date[2] # pass this
witness_date = f"{MONTH} {DAY} {YEAR}"






print(rows)