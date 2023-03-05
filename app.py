from flask import Flask, render_template, request, redirect, jsonify
import pandas as pd
import math
import json


app = Flask(__name__)

bigfoot_locations = pd.read_csv('bfro_locations.csv')
bigfoot_geo_reports = pd.read_csv('bfro_reports_geocoded.csv')
bigfoot_reports = pd.read_csv('bfro_reports.csv')


images = {
    "texas":"texas.png",
}


# functions


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


    return {
    "report_one": {"title1": first_report_title, "first_atag": first_report_return_a_tag, "first_class": first_report_class},
    "report_two": {"title2": second_report_title, "second_atag": second_report_return_a_tag, "second_class": second_report_class},
    "report_three": {"title3": third_report_title, "third_atag": third_report_return_a_tag, "third_class": third_report_class},
    "total_sightings": number_of_sightings,
    }



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
    
    
    


# Home Page
@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html')



# State Selection Page
@app.route('/state_selection', methods=["GET", "POST"])
def state_selection():
    
    return render_template('/routes/state_selection.html')


state_selected = []


@app.route('/county_selection')
def county_selection():
    selected_county = request.args.get('county')
    state = state_selected[0]
    image = images[state]
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


@app.route('/individual_case', methods=["POST", "GET"])
def individual_case():
    value = ''
    if request.method == "POST":
        if request.content_type == 'application/json':
            value = request.json.get('text')
            print(value)
        else:
            value = request.form.get('text')
            print(value)

    return render_template('individual_case.html', value=value)


# =========================================================================================================== #
# ============= State Routes ============= #


# Texas Page Route
@app.route('/texas.html')
def texas():
    state_selected.clear()
    state_selected.append("texas")
    passing_variables = ["TX", "Texas", "texas.png"]
    
    return_recent_reports_dict = getting_recent_reports(passing_variables[1])
    counties = getting_counties(passing_variables[1])

    report_one = return_recent_reports_dict['report_one']
    report_one_title = report_one['title1']
    report_one_atag = report_one['first_atag']
    report_one_class = report_one['first_class']

    report_two = return_recent_reports_dict['report_two']
    report_two_title = report_two['title2']
    report_two_atag = report_two['second_atag']
    report_two_class = report_two['second_class']

    report_three = return_recent_reports_dict['report_three']
    report_three_title = report_three['title3']
    report_three_atag = report_three['third_atag']
    report_three_class = report_three['third_class']

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
                           
                           # Second recent report varibales
                           report_two_title=report_two_title,
                           report_two_atag=report_two_atag,
                           report_two_class=report_two_class,
                           
                           
                           # Third recent report varibales
                           report_three_title=report_three_title,
                           report_three_atag=report_three_atag,
                           report_three_class=report_three_class,
                           
                           
                           # County Dict
                           counties=counties,
)





if __name__ == "__main__":
    app.run(debug=True)