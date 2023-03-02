import pandas as pd




bigfoot_locations = pd.read_csv('bfro_locations.csv')
bigfoot_geo_reports = pd.read_csv('bfro_reports_geocoded.csv')
bigfoot_reports = pd.read_csv('bfro_reports.csv')



num_rows = bigfoot_locations.shape[0]

print("Total number of rows:", num_rows)