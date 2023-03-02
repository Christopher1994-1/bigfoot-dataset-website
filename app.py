from flask import Flask, render_template, request, redirect
import pandas as pd


app = Flask(__name__)





# Home Page
@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html')






if __name__ == "__main__":
    app.run(debug=True)