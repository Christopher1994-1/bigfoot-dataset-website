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


df = bigfoot_geo_reports['county'].describe()

print(df)


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



