from flask import Flask, render_template, request, redirect, jsonify
import pandas as pd


app = Flask(__name__)

bigfoot_locations = pd.read_csv('bfro_locations.csv')
bigfoot_geo_reports = pd.read_csv('bfro_reports_geocoded.csv')
bigfoot_reports = pd.read_csv('bfro_reports.csv')


# functions

def state_counts():
    pass


# Home Page
@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html')



# State Selection Page
@app.route('/state_selection', methods=["GET", "POST"])
def state_selection():
    
    return render_template('/routes/state_selection.html')





# =========================================================================================================== #
# ============= State Routes ============= #


# Texas Page Route
@app.route('/texas.html')
def texas():
    passing_variables = ["TX", "Texas", "texas.png"]
    total_sightings = 25
    return render_template('/states/texas.html',
                           state_code=passing_variables[0],
                           state=passing_variables[1],
                           image=passing_variables[2],
                           total_sightings=total_sightings,
)





if __name__ == "__main__":
    app.run(debug=True)