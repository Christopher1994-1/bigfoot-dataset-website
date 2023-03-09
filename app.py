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


# West Virginia State Page
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



# Florida State Page
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



# Illnois State Page 
@app.route('/illnois.html')
def illnois():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("illnois")
    passing_variables = ["IL", "Illnois", "illnois.png"]
    images_host.append('illnois.png')
    
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
    return render_template('/states/illnois.html',
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




# Minnesota State Page 
@app.route('/minnesota.html')
def minnesota():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("minnesota")
    passing_variables = ["MN", "Minnesota", "minnesota.png"]
    images_host.append('minnesota.png')
    
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
    return render_template('/states/minnesota.html',
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




# Maryland State Page 
@app.route('/maryland.html')
def maryland():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("maryland")
    passing_variables = ["MD", "Maryland", "maryland.png"]
    images_host.append('maryland.png')
    
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
    return render_template('/states/maryland.html',
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



# Rhode Island State Page 
@app.route('/rhode_island.html')
def rhode_island():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("rhode island")
    passing_variables = ["RI", "Rhode Island", "rhode-island.png"]
    images_host.append('rhode-island.png')
    
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
    return render_template('/states/rhode_island.html',
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




# Idaho State Page 
@app.route('/idaho.html')
def idaho():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("idaho")
    passing_variables = ["ID", "Idaho", "idaho.png"]
    images_host.append('idaho.png')
    
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
    return render_template('/states/idaho.html',
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




# New Hampshire State Page 
@app.route('/new_hampshire.html')
def new_hampshire():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("new hampshire") # lower case
    passing_variables = ["NH", "New Hampshire", "new-hampshire.png"]
    images_host.append('new-hampshire.png')
    
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
    return render_template('/states/new_hampshire.html',
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




# North Carolina State Page 
@app.route('/north_carolina.html')
def north_carolina():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("north carolina") # lower case
    passing_variables = ["NC", "North Carolina", "north-carolina.png"]
    images_host.append('north-carolina.png')
    
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
    return render_template('/states/north_carolina.html',
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




# Vermont State Page 
@app.route('/vermont.html')
def vermont():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("vermont") # lower case
    passing_variables = ["VT", "Vermont", "vermont.png"]
    images_host.append('vermont.png')
    
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
    return render_template('/states/vermont.html',
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




# Connecticut State Page 
@app.route('/connecticut.html')
def connecticut():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("connecticut") # lower case
    passing_variables = ["CT", "Connecticut", "connecticut.png"]
    images_host.append('connecticut.png')
    
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
    return render_template('/states/connecticut.html',
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



# Delaware State Page 
@app.route('/delaware.html')
def delaware():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("delaware") # lower case
    passing_variables = ["DE", "Delaware", "delaware.png"]
    images_host.append('delaware.png')
    
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
    return render_template('/states/delaware.html',
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




# New Mexico State Page 
@app.route('/new_mexico.html')
def new_mexico():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("new mexico") # lower case
    passing_variables = ["NM", "New Mexico", "new-mexico.png"]
    images_host.append('new-mexico.png')
    
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
    return render_template('/states/new_mexico.html',
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



# California State Page 
@app.route('/california.html')
def california():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("california") # lower case
    passing_variables = ["CA", "California", "california.png"]
    images_host.append('california.png')
    
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
    return render_template('/states/california.html',
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




# New Jersey State Page 
@app.route('/new_jersey.html')
def new_jersey():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("new jersey") # lower case
    passing_variables = ["NJ", "New Jersey", "new-jersey.png"]
    images_host.append('new-jersey.png')
    
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
    return render_template('/states/new_jersey.html',
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




# Wisconsin State Page 
@app.route('/wisconsin.html')
def wisconsin():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("wisconsin") # lower case
    passing_variables = ["WI", "Wisconsin", "wisconsin.png"]
    images_host.append('wisconsin.png')
    
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
    return render_template('/states/wisconsin.html',
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



# Oregon State Page 
@app.route('/oregon.html')
def oregon():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("oregon") # lower case
    passing_variables = ["OR", "Oregon", "oregon.png"]
    images_host.append('oregon.png')
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
    return render_template('/states/oregon.html',
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




# Nebraska State Page 
@app.route('/nebraska.html')
def nebraska():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("nebraska") # lower case
    passing_variables = ["NE", "Nebraska", "nebraska.png"]
    images_host.append('nebraska.png')
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
    return render_template('/states/nebraska.html',
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




# Pennsylvania State Page 
@app.route('/pennsylvania.html')
def pennsylvania():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("pennsylvania") # lower case
    passing_variables = ["PA", "Pennsylvania", "pennsylvania.png"]
    images_host.append('pennsylvania.png')
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
    return render_template('/states/pennsylvania.html',
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



# Washington State Page 
@app.route('/washington.html')
def washington():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("washington") # lower case
    passing_variables = ["WA", "Washington", "washington.png"]
    images_host.append('washington.png')
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
    return render_template('/states/washington.html',
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




# Louisiana State Page 
@app.route('/louisiana.html')
def louisiana():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("louisiana") # lower case
    passing_variables = ["LA", "Louisiana", "louisiana.png"]
    images_host.append('louisiana.png')
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
    return render_template('/states/louisiana.html',
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




# Georgia State Page 
@app.route('/georgia.html')
def georgia():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("georgia") # lower case
    passing_variables = ["GA", "Georgia", "georgia.png"]
    images_host.append('georgia.png')
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
    return render_template('/states/georgia.html',
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




# Alabama State Page 
@app.route('/alabama.html')
def alabama():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("alabama") # lower case
    passing_variables = ["AL", "Alabama", "alabama.png"]
    images_host.append('alabama.png')
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
    return render_template('/states/alabama.html',
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




# Utah State Page 
@app.route('/utah.html')
def utah():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("utah") # lower case
    passing_variables = ["UT", "Utah", "utah.png"]
    images_host.append('utah.png')
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
    return render_template('/states/utah.html',
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



# Ohio State Page 
@app.route('/ohio.html')
def ohio():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("ohio") # lower case
    passing_variables = ["OH", "Ohio", "ohio.png"]
    images_host.append('ohio.png')
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
    return render_template('/states/ohio.html',
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




# Colorado State Page 
@app.route('/colorado.html')
def colorado():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("colorado") # lower case
    passing_variables = ["CO", "Colorado", "colorado.png"]
    images_host.append('colorado.png')
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
    return render_template('/states/colorado.html',
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




# South Carolina State Page 
@app.route('/south_carolina.html')
def south_carolina():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("south carolina") # lower case
    passing_variables = ["SC", "South Carolina", "south-carolina.png"]
    images_host.append('south-carolina.png')
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
    return render_template('/states/south_carolina.html',
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




# Oklahoma State Page 
@app.route('/oklahoma.html')
def oklahoma():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("oklahoma") # lower case
    passing_variables = ["OK", "Oklahoma", "oklahoma.png"]
    images_host.append('oklahoma.png')
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
    return render_template('/states/oklahoma.html',
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



# Tennessee State Page 
@app.route('/tennessee.html')
def tennessee():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("tennessee") # lower case
    passing_variables = ["TN", "Tennessee", "tennessee.png"]
    images_host.append('tennessee.png')
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
    return render_template('/states/tennessee.html',
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




# Wyoming State Page 
@app.route('/wyoming.html')
def wyoming():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("wyoming") # lower case
    passing_variables = ["WY", "Wyoming", "wyoming.png"]
    images_host.append('wyoming.png')
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
    return render_template('/states/wyoming.html',
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





# North Dakota State Page 
@app.route('/north_dakota.html')
def north_dakota():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("north dakota") # lower case
    passing_variables = ["ND", "North Dakota", "north-dakota.png"]
    images_host.append('north-dakota.png')
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
    return render_template('/states/north_dakota.html',
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





# Kentucky State Page 
@app.route('/kentucky.html')
def kentucky():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("kentucky") # lower case
    passing_variables = ["KY", "Kentucky", "kentucky.png"]
    images_host.append('kentucky.png')
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
    return render_template('/states/kentucky.html',
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



# Maine State Page 
@app.route('/maine.html')
def maine():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("maine") # lower case
    passing_variables = ["ME", "Maine", "maine.png"]
    images_host.append('maine.png')
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
    return render_template('/states/maine.html',
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




# New York State Page 
@app.route('/new_york.html')
def new_york():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("new york") # lower case
    passing_variables = ["NY", "New York", "new-york.png"]
    images_host.append('new-york.png')
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
    return render_template('/states/new_york.html',
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



# Michigan State Page 
@app.route('/michigan.html')
def michigan():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("michigan") # lower case
    passing_variables = ["MI", "Michigan", "michigan.png"]
    images_host.append('michigan.png')
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
    return render_template('/states/michigan.html',
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





# Arkansas State Page 
@app.route('/arkansas.html')
def arkansas():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("arkansas") # lower case
    passing_variables = ["AR", "Arkansas", "arkansas.png"]
    images_host.append('arkansas.png')
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
    return render_template('/states/arkansas.html',
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




# Mississippi State Page 
@app.route('/mississippi.html')
def mississippi():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("mississippi") # lower case
    passing_variables = ["MS", "Mississippi", "mississippi.png"]
    images_host.append('mississippi.png')
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
    return render_template('/states/mississippi.html',
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





# Missouri State Page 
@app.route('/missouri.html')
def missouri():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("missouri") # lower case
    passing_variables = ["MO", "Missouri", "missouri.png"]
    images_host.append('missouri.png')
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
    return render_template('/states/missouri.html',
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





# Montana State Page 
@app.route('/montana.html')
def montana():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("montana") # lower case
    passing_variables = ["MT", "Montana", "montana.png"]
    images_host.append('montana.png')
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
    return render_template('/states/montana.html',
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




# Kansas State Page 
@app.route('/kansas.html')
def kansas():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("kansas") # lower case
    passing_variables = ["KS", "Kansas", "kansas.png"]
    images_host.append('kansas.png')
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
    return render_template('/states/kansas.html',
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




# Indiana State Page 
@app.route('/indiana.html')
def indiana():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("indiana") # lower case
    passing_variables = ["IN", "Indiana", "indiana.png"]
    images_host.append('indiana.png')
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
    return render_template('/states/indiana.html',
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





# South Dakota State Page 
@app.route('/south_dakota.html')
def south_dakota():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("south dakota") # lower case
    passing_variables = ["SD", "South Dakota", "south-dakota.png"]
    images_host.append('south-dakota.png')
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
    return render_template('/states/south_dakota.html',
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




# Massachusetts State Page 
@app.route('/massachusetts.html')
def massachusetts():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("massachusetts") # lower case
    passing_variables = ["MA", "Massachusetts", "massachusetts.png"]
    images_host.append('massachusetts.png')
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
    return render_template('/states/massachusetts.html',
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





# Virginia State Page 
@app.route('/virginia.html')
def virginia():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("virginia") # lower case
    passing_variables = ["VA", "Virginia", "virginia.png"]
    images_host.append('virginia.png')
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
    return render_template('/states/virginia.html',
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



# Iowa State Page 
@app.route('/iowa.html')
def iowa():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("iowa") # lower case
    passing_variables = ["IA", "Iowa", "iowa.png"]
    images_host.append('iowa.png')
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
    return render_template('/states/iowa.html',
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



# Arizona State Page 
@app.route('/arizona.html')
def arizona():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("arizona") # lower case
    passing_variables = ["AZ", "Arizona", "arizona.png"]
    images_host.append('arizona.png')
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
    return render_template('/states/arizona.html',
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



# Alaska State Page 
@app.route('/alaska.html')
def alaska():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("alaska") # lower case
    passing_variables = ["AK", "Alaska", "alaska.png"]
    images_host.append('alaska.png')
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
    return render_template('/states/alaska.html',
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




# Hawaii State Page 
@app.route('/hawaii.html')
def hawaii():
    value_get.clear()
    state_selected.clear()
    images_host.clear()
    state_selected.append("hawaii") # lower case
    passing_variables = ["HI", "Hawaii", "hawaii.png"]
    images_host.append('hawaii.png')
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
    return render_template('/states/hawaii.html',
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