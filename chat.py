import pandas as pd
import json
import math


# Function that gets the four states with the most sightings for index
def the_four_states():
    
    bigfoot_geo_reports = pd.read_csv('bfro_reports_geocoded.csv')
    df = bigfoot_geo_reports

    rates = df['state'].value_counts().to_dict()    
    
    return rates



a = the_four_states()


print(a)