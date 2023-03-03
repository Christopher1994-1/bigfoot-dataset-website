import pandas as pd




bigfoot_locations = pd.read_csv('bfro_locations.csv')
# number
# title
# classification
# timestamp
# latitude
# longitude

bigfoot_geo_reports = pd.read_csv('bfro_reports_geocoded.csv')
# observed
# location_details
# county
# state
# season
# title
# latitude
# longitude
# date
# number
# classification
# geohash
# temperature_high
# temperature_mid
# temperature_low
# dew_point
# humidity
# cloud_cover
# moon_phase
# precip_intensity
# precip_probability
# precip_type
# pressure
# summary
# uv_index
# visibility
# wind_bearing
# wind_speed
# location



bigfoot_reports = pd.read_csv('bfro_reports.csv')
# year
# season
# state
# county
# nearest_town
# nearest_road
# observed
# also_noticed
# other_witnesses
# other_stories
# time_and_conditions
# environment
# report_number
# report_class
# location_details
# month
# date




df_loc = bigfoot_geo_reports[(bigfoot_geo_reports['number'] == 1261.0)] 
# head = bigfoot_reports.head(1)
json_rows = []
for a, row in df_loc.iterrows():
    json_row = row.to_dict()
    json_rows.append(json_row)
ref_number = int(str(json_rows[0]['number']).split('.')[0])
float_ref_number = json_rows[0]['number']

print(json_rows)
print()
print("=" * 25)
print()







df_reports = bigfoot_reports[(bigfoot_reports['report_number'] == ref_number)]

json_rows2 = []
for b, row2 in df_reports.iterrows():
    json_row2 = row2.to_dict()
    json_rows2.append(json_row2)

print(json_rows2)
print()
print("=" * 25)
print()









df_time = bigfoot_locations[(bigfoot_locations['number'] == float_ref_number)]


json_rows3 = []
for c, row3 in df_time.iterrows():
    json_row3 = row3.to_dict()
    json_rows3.append(json_row3)

print(json_rows3)