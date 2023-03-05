import pandas as pd
import json
import math




def showing_reports(state, county):
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

    bigfoot_geo_reports = pd.read_csv('bfro_reports_geocoded.csv')
    
    state = str(state).title()

    df = bigfoot_geo_reports
    df_state = df.loc[(bigfoot_geo_reports['state'] == state) & (bigfoot_geo_reports['county'] == county)]

    json_rows = []
    for a, row in df_state.iterrows():
        json_row = row.to_dict()
        json_rows.append(json_row)
        
    new_list = []
    value = ''
    for d1 in json_rows:
        new_dict = {}
        for key in ('date', 'title', 'classification'):
            value = d1[key]

            new_dict[key] = value
        new_list.append(new_dict)

    # Remove dictionaries with NaN values
    cleaned_list = [d for d in new_list if not any(isinstance(v, float) and math.isnan(v) for v in d.values())]

    # Sort by date
    sorted_cleaned_list = sorted(cleaned_list, key=lambda x: str(x['date']), reverse=True)
    
    
    
    title_list = []
    for dic in sorted_cleaned_list:
        title_dict = {}
        for key in ('date', 'title', 'classification'):
            title = dic[key]
            if ":" in title:
                new_title = str(title).split(":")
                main_title = new_title[1].strip()
                title_dict[key] = main_title
            else:
                title_dict[key] = title
        title_list.append(title_dict)
        
    
    date_list = []
    for tim in title_list:
        last_dict = {}
        for key in ('date', 'title', 'classification'):
            date = tim[key]
            if '-' in date and len(date) == 10:
                date_split = str(date).split('-')
                YEAR = date_split[0]
                MONTH = months[date_split[1]]
                new_date = f"{MONTH} {YEAR}"
                last_dict[key] = new_date
            else:
                last_dict[key] = date
        date_list.append(last_dict)
        
    return date_list
    
    
    

    
    
    

passing = 'texas'
co = "Montgomery County"

a = showing_reports(passing, co)




# TODO add a number to total sightings in county selection page
# TODO maybe add something like this "13 total sightings in {county}"
