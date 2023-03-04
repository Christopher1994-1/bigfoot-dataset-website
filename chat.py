import pandas as pd
import json




def getting_counties(state):

    bigfoot_geo_reports = pd.read_csv('bfro_reports_geocoded.csv')
    
    state = str(state).title()

    df = bigfoot_geo_reports
    df_state = df.loc[(bigfoot_geo_reports['state'] == state)]

    json_rows = []
    for a, row in df_state.iterrows():
        json_row = row.to_dict()
        json_rows.append(json_row)

    county_values = df_state['county'].value_counts()
    counties = df_state['county']
    
    
    new = {'count'}

    
# TODO run this in git bash
   

    
    

passing = 'nevada'

getting_counties(passing)



