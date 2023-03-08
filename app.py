from flask import Flask, render_template, request, redirect, jsonify
import pandas as pd
import math
import json


app = Flask(__name__)

bigfoot_locations = pd.read_csv('bfro_locations.csv')
bigfoot_geo_reports = pd.read_csv('bfro_reports_geocoded.csv')
bigfoot_reports = pd.read_csv('bfro_reports.csv')



###########################################################################
# functions

# function that gets the 3 most recent sightings from whatever state that is selected
def getting_recent_reports(state):
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
    
    # try:
    specific_date = pd.to_datetime('2022-01-01')

    df = bigfoot_geo_reports
    df_state = df.loc[(bigfoot_geo_reports['state'] == state)]

    json_rows = []
    for a, row in df_state.iterrows():
        json_row = row.to_dict()
        json_rows.append(json_row['date'])
    number_of_sightings = len(json_rows) # return this
    
    dates = pd.to_datetime(json_rows)
        
    # find the nearest date before and after the specific date
    nearest_before = dates[dates <= specific_date].to_list()
    times = sorted(nearest_before)
    times2 = times[::-1][:3]
        
    date1 = str(times2[0]).split(' ')[0]
    
    
    # first recent sighting
    where_date1 = df.loc[(bigfoot_geo_reports['date'] == date1)]
    
    date_info = []
    for a, row in where_date1.iterrows():
        json_row = row.to_dict()
        date_info.append(json_row)
    
    first_report_title = str(date_info[0]['title']).split(':')[1].strip() # return this
    first_report_YEAR = date1.split('-')[0]
    first_report_MONTH = months[date1.split('-')[1]]
    first_report_county = date_info[0]['county']
    
    first_report_return_a_tag = f"{first_report_MONTH} {first_report_YEAR}, {first_report_county}" # return this
    first_report_class = date_info[0]['classification'] # return this
    first_number = date_info[0]['number'] # return this


    
    # # second recent sighting
    date2 = str(times2[1]).split(' ')[0]
    
    where_date2 = df.loc[(bigfoot_geo_reports['date'] == date2)]
    
    date_info2 = []
    for a, row in where_date2.iterrows():
        json_row = row.to_dict()
        date_info2.append(json_row)
    
    second_report_title = str(date_info2[0]['title']).split(':')[1].strip() # return this
    second_report_YEAR = date2.split('-')[0]
    second_report_MONTH = months[date2.split('-')[1]]
    county = date_info2[0]['county']
    
    second_report_return_a_tag = f"{second_report_MONTH} {second_report_YEAR}, {county}" # return this
    second_report_class = date_info2[0]['classification'] # return this
    second_number = date_info2[0]['number'] # return this
    
    
    # # second recent sighting
    date3 = str(times2[2]).split(' ')[0]
    
    where_date3 = df.loc[(bigfoot_geo_reports['date'] == date3)]
    
    date_info3 = []
    for a, row in where_date3.iterrows():
        json_row = row.to_dict()
        date_info3.append(json_row)
    
    third_report_title = str(date_info3[0]['title']).split(':')[1].strip() # return this
    third_report_YEAR = date3.split('-')[0]
    third_report_MONTH = months[date3.split('-')[1]]
    county = date_info3[0]['county']
    
    third_report_return_a_tag = f"{third_report_MONTH} {third_report_YEAR}, {county}" # return this
    third_report_class = date_info3[0]['classification'] # return this
    third_number = date_info3[0]['number'] # return this


    return {
    "report_one": {"title1": first_report_title, "first_atag": first_report_return_a_tag, "first_class": first_report_class, "number": first_number},
    "report_two": {"title2": second_report_title, "second_atag": second_report_return_a_tag, "second_class": second_report_class, "number": second_number},
    "report_three": {"title3": third_report_title, "third_atag": third_report_return_a_tag, "third_class": third_report_class, "number": third_number},
    "total_sightings": number_of_sightings,
    }


# function to get all of the counties
def getting_counties(state):

    bigfoot_geo_reports = pd.read_csv('bfro_reports_geocoded.csv')
    
    state = str(state).title()

    df = bigfoot_geo_reports
    df_state = df.loc[(bigfoot_geo_reports['state'] == state) & (bigfoot_geo_reports['date'].isna() == False)]

    json_rows = []
    for a, row in df_state.iterrows():
        json_row = row.to_dict()
        json_rows.append(json_row)

    county_values = df_state['county'].value_counts()
    counties = county_values.to_dict()

    return counties
    


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
        for key in ('date', 'title', 'classification', 'number'):
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
        for key in ('date', 'title', 'classification', 'number'):
            title = str(dic[key])
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
        for key in ('date', 'title', 'classification', 'number'):
            date = str(tim[key])
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
    
    
    
# function that gets the data for one case
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



# Function that gets the four states with the most sightings for index
def the_four_states():
    
    bigfoot_geo_reports = pd.read_csv('bfro_reports_geocoded.csv')
    df = bigfoot_geo_reports

    rates = df['state'].value_counts().to_dict()    
    
    return rates



# Function that is only used for when user clicks on most recent reports links
def recent_reports(state, number):
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
    number = float(number)
    
    # try:
    specific_date = pd.to_datetime('2022-01-01')

    df = bigfoot_geo_reports
    df_state = df.loc[(bigfoot_geo_reports['state'] == state) & (bigfoot_geo_reports['number'] == number)]

    json_rows = []
    for a, row in df_state.iterrows():
        json_row = row.to_dict()
        json_rows.append(json_row)
    number_of_sightings = len(json_rows) # return this
    
    

        
    return json_rows[0]['county']



###################################################################




# Empty lists for appending current state, county, image and id_number
state_selected = []
value_get = []
county_selected = []
images_host = []



#########################################################################################################
######################################################################################################

# Home Page
@app.route('/', methods=["GET", "POST"])
def index():
    state_selected.clear()
    county_selected.clear()
    value_get.clear()
    images_host.clear()
    
    index_states = the_four_states()
    
    return render_template('index.html', index_states=index_states)



# State Selection Page
@app.route('/state_selection', methods=["GET", "POST"])
def state_selection():
    
    return render_template('/routes/state_selection.html')



# County Selection Page
@app.route('/county_selection', methods=["POST", "GET"])
def county_selection():
    value_get.clear()
    selected_county = request.args.get('county')
    county_selected.append(selected_county)
    state = state_selected[0]
    image = images_host[0]

            
    # do something with the selected county
    rows = showing_reports(state, selected_county)
    length_of_rows = len(rows)
    return render_template('county_selection.html',
                           selected_county=selected_county,
                           state=state,
                           rows=rows,
                           image=image,
                           length_of_rows=length_of_rows,
        )





# Individual Case Page
@app.route('/individual_case')
def individual_case():
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
    value = str(value_get[0]).split('.')[0]
    
    original_value = value_get[0]
    state = state_selected[0]
    county = county_selected[0]
    image = images_host[0]
    
    rows = one_case(state, county, original_value)
    class1 = rows[0]['classification'] # pass this

    date = str(rows[0]['date']).split('-')

    YEAR = date[0] # pass this
    MONTH = months[date[1]] # pass this
    DAY = date[2] # pass this


    observed = rows[0]['observed'] # pass this


    season = rows[0]['season'] # pass this

    lat = rows[0]['latitude'] # pass this
    lon = rows[0]['longitude'] # pass this
    summary = rows[0]['summary'] # pass this
    location_details = rows[0]['location_details'] # pass this
    witness_date = f"{MONTH} {DAY} {YEAR}" # pass this
    
    
    
    
    return render_template('individual_case.html',
                           value=value,
                           original_value=original_value,
                           state=state,
                           county=county,
                           image=image,
                           class1=class1,
                           year=YEAR,
                           month=MONTH,
                           day=DAY,
                           observed=observed,
                           season=season,
                           lat=lat,
                           lon=lon,
                           summary=summary,
                           location_details=location_details,
                           witness_date=witness_date,
                )





# =========================================================================================================== #
# ============= JavaScript Backend Functions ============= #



# backend function that gets the id_number from selecting county
@app.route('/my-endpoint', methods=['POST'])
def my_endpoint():
    value_get.clear()
    data = request.json['data']
    value_get.append(data)
        
    return jsonify({'success': True})




# Backend function that gets recent report one ID number
@app.route('/report_one_pass', methods=['POST'])
def report_one_pass():
    value_get.clear()
    county_selected.clear()
    
    data = request.json['id']
    county = request.json['county']
    
    value_get.append(data)
    county_selected.append(county)
    

        
    return jsonify({'success': True})


# Backend function that gets recent report two ID number
@app.route('/report_two_pass', methods=['POST'])
def report_two_pass():
    value_get.clear()
    county_selected.clear()
    
    data = request.json['id']
    county = request.json['county']
    
    value_get.append(data)
    county_selected.append(county)
    

        
    return jsonify({'success': True})



# Backend function that gets recent report three ID number
@app.route('/report_three_pass', methods=['POST'])
def report_three_pass():
    value_get.clear()
    county_selected.clear()
    
    data = request.json['id']
    county = request.json['county']
    
    value_get.append(data)
    county_selected.append(county)
    

        
    return jsonify({'success': True})











# =========================================================================================================== #
# ============= State Routes ============= #


# Texas Page Route
@app.route('/texas.html')
def texas():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("texas")
    passing_variables = ["TX", "Texas", "texas.png"]
    images_host.append('texas.png')
    
    return_recent_reports_dict = getting_recent_reports(passing_variables[1])
    counties = getting_counties(passing_variables[1])

    report_one = return_recent_reports_dict['report_one']
    report_one_title = report_one['title1']
    report_one_atag = report_one['first_atag']
    report_one_class = report_one['first_class']
    report_one_number = report_one['number']

    report_two = return_recent_reports_dict['report_two']
    report_two_title = report_two['title2']
    report_two_atag = report_two['second_atag']
    report_two_class = report_two['second_class']
    report_two_number = report_two['number']

    report_three = return_recent_reports_dict['report_three']
    report_three_title = report_three['title3']
    report_three_atag = report_three['third_atag']
    report_three_class = report_three['third_class']
    report_three_number = report_three['number']

    total_sightings = return_recent_reports_dict['total_sightings']
    return render_template('/states/texas.html',
                           state_code=passing_variables[0],
                           state=passing_variables[1],
                           image=passing_variables[2],
                           total_sightings=total_sightings,
                           
                           
                           # First recent report varibales
                           report_one_title=report_one_title,
                           report_one_atag=report_one_atag,
                           report_one_class=report_one_class,
                           report_one_number=report_one_number,
                           
                           # Second recent report varibales
                           report_two_title=report_two_title,
                           report_two_atag=report_two_atag,
                           report_two_class=report_two_class,
                           report_two_number=report_two_number,
                           
                           
                           # Third recent report varibales
                           report_three_title=report_three_title,
                           report_three_atag=report_three_atag,
                           report_three_class=report_three_class,
                           report_three_number=report_three_number,
                           
                           
                           # County Dict
                           counties=counties,
)



# Texas Page Route
@app.route('/nevada.html')
def nevada():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("nevada")
    passing_variables = ["NV", "Nevada", "nevada.png"]
    images_host.append('nevada.png')
    
    return_recent_reports_dict = getting_recent_reports(passing_variables[1])
    counties = getting_counties(passing_variables[1])

    report_one = return_recent_reports_dict['report_one']
    report_one_title = report_one['title1']
    report_one_atag = report_one['first_atag']
    report_one_class = report_one['first_class']
    report_one_number = report_one['number']

    report_two = return_recent_reports_dict['report_two']
    report_two_title = report_two['title2']
    report_two_atag = report_two['second_atag']
    report_two_class = report_two['second_class']
    report_two_number = report_two['number']

    report_three = return_recent_reports_dict['report_three']
    report_three_title = report_three['title3']
    report_three_atag = report_three['third_atag']
    report_three_class = report_three['third_class']
    report_three_number = report_three['number']

    total_sightings = return_recent_reports_dict['total_sightings']
    return render_template('/states/nevada.html',
                           state_code=passing_variables[0],
                           state=passing_variables[1],
                           image=passing_variables[2],
                           total_sightings=total_sightings,
                           
                           
                           # First recent report varibales
                           report_one_title=report_one_title,
                           report_one_atag=report_one_atag,
                           report_one_class=report_one_class,
                           report_one_number=report_one_number,
                           
                           # Second recent report varibales
                           report_two_title=report_two_title,
                           report_two_atag=report_two_atag,
                           report_two_class=report_two_class,
                           report_two_number=report_two_number,
                           
                           
                           # Third recent report varibales
                           report_three_title=report_three_title,
                           report_three_atag=report_three_atag,
                           report_three_class=report_three_class,
                           report_three_number=report_three_number,
                           
                           
                           # County Dict
                           counties=counties,
)




@app.route('/west_virginia.html')
def west_virginia():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("west virginia")
    passing_variables = ["WV", "West Virginia", "west-virginia.png"]
    images_host.append('west-virginia.png')
    
    return_recent_reports_dict = getting_recent_reports(passing_variables[1])
    counties = getting_counties(passing_variables[1])

    report_one = return_recent_reports_dict['report_one']
    report_one_title = report_one['title1']
    report_one_atag = report_one['first_atag']
    report_one_class = report_one['first_class']
    report_one_number = report_one['number']

    report_two = return_recent_reports_dict['report_two']
    report_two_title = report_two['title2']
    report_two_atag = report_two['second_atag']
    report_two_class = report_two['second_class']
    report_two_number = report_two['number']

    report_three = return_recent_reports_dict['report_three']
    report_three_title = report_three['title3']
    report_three_atag = report_three['third_atag']
    report_three_class = report_three['third_class']
    report_three_number = report_three['number']

    total_sightings = return_recent_reports_dict['total_sightings']
    return render_template('/states/west_virginia.html',
                           state_code=passing_variables[0],
                           state=passing_variables[1],
                           image=passing_variables[2],
                           total_sightings=total_sightings,
                           
                           
                           # First recent report varibales
                           report_one_title=report_one_title,
                           report_one_atag=report_one_atag,
                           report_one_class=report_one_class,
                           report_one_number=report_one_number,
                           
                           # Second recent report varibales
                           report_two_title=report_two_title,
                           report_two_atag=report_two_atag,
                           report_two_class=report_two_class,
                           report_two_number=report_two_number,
                           
                           
                           # Third recent report varibales
                           report_three_title=report_three_title,
                           report_three_atag=report_three_atag,
                           report_three_class=report_three_class,
                           report_three_number=report_three_number,
                           
                           
                           # County Dict
                           counties=counties,
)




@app.route('/florida.html')
def florida():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("florida")
    passing_variables = ["FL", "Florida", "florida.png"]
    images_host.append('florida.png')
    
    return_recent_reports_dict = getting_recent_reports(passing_variables[1])
    counties = getting_counties(passing_variables[1])

    report_one = return_recent_reports_dict['report_one']
    report_one_title = report_one['title1']
    report_one_atag = report_one['first_atag']
    report_one_class = report_one['first_class']
    report_one_number = report_one['number']

    report_two = return_recent_reports_dict['report_two']
    report_two_title = report_two['title2']
    report_two_atag = report_two['second_atag']
    report_two_class = report_two['second_class']
    report_two_number = report_two['number']

    report_three = return_recent_reports_dict['report_three']
    report_three_title = report_three['title3']
    report_three_atag = report_three['third_atag']
    report_three_class = report_three['third_class']
    report_three_number = report_three['number']

    total_sightings = return_recent_reports_dict['total_sightings']
    return render_template('/states/florida.html',
                           state_code=passing_variables[0],
                           state=passing_variables[1],
                           image=passing_variables[2],
                           total_sightings=total_sightings,
                           
                           
                           # First recent report varibales
                           report_one_title=report_one_title,
                           report_one_atag=report_one_atag,
                           report_one_class=report_one_class,
                           report_one_number=report_one_number,
                           
                           # Second recent report varibales
                           report_two_title=report_two_title,
                           report_two_atag=report_two_atag,
                           report_two_class=report_two_class,
                           report_two_number=report_two_number,
                           
                           
                           # Third recent report varibales
                           report_three_title=report_three_title,
                           report_three_atag=report_three_atag,
                           report_three_class=report_three_class,
                           report_three_number=report_three_number,
                           
                           
                           # County Dict
                           counties=counties,
)



if __name__ == "__main__":
    app.run(debug=True)