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






if __name__ == "__main__":
    app.run(debug=True)