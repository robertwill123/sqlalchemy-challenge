# Import the dependencies.
import datetime as dt

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text, func

from flask import Flask, jsonify
import pandas as pd
import numpy as np


#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine= create_engine("sqlite:///Resources/hawaii.sqlite")
# Declare a Base using `automap_base()`
Base= automap_base()

# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return(
        f"All Routes<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/<start><br/>"
        f"/api/v1.0/temp/<start>/<end><br/>"
    )

@app.route("/api/v1/precipitation")
def precipitation():
    prev_year = dt.date(2016,8,23)

    precipitation = session.query(Measurement.date,Measurement.prcp).\
        filter(Measurement.date>=prev_year).all()
    
    session.close()
    precipitation = {date: prcp for date, prcp in precipitation}
    return jsonify(precipitation)

@app.route("/api/v1/stations")
def stations(self):
    query = """
            SELECT station 
            FROM measurement
            GROUP BY station
        """
    df = pd.read_sql(text(query), con = self.engine)
    data = df.to_dict(orient="records")
    return data
    
@app.route("/api/v1/tobs")
def tobs(self, start, end):
    query = """
            SELECT min(tobs) as min_temp, avg(tobs) as avg_temp, max(tobs) as max_temp 
            FROM measurement
            WHERE date >= "{start}" and date < "{end}"
        """

    df = pd.read_sql(text(query), con = self.engine)
    data = df.to_dict(orient="records")
    return data
