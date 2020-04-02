#Importing
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


### Engine Creation/Connection
engine = create_engine("sqlite:///resource/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine,reflect = True)

Measurement = Base.classes.measurement


# App Creations

app = Flask(__name__)

# User Index Routes
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"Welcome to the Climate Analysis Home Page!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"  
    )

# Precipttion Route
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    last_date = '2017-08-23'
    one_year_before = '2016-08-23'

    # Perform a query to retrieve the data and precipitation scores
    last_12months_ps = session.query(Measurement.prcp, Measurement.date).\
        filter(Measurement.date >= one_year_before).filter(Measurement.date <= last_date).all()
    session.close()

    precipitation_dict = dict(last_12months_ps)
    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations = session.query(Measurement.station).group_by(Measurement.station).all()
    session.close()
    station_list = list(np.ravel(stations))
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    last_date = '2017-08-23'
    one_year_before_date = '2016-08-23'
    most_active_station = 'USC00519281'
    temperature = session.query(Measurement.tobs).filter_by(station = recent_stations).\
    filter(Measurement.date >= one_year_before).filter(Measurement.date <= last_date).all()
    session.close()
    temperature_list = list(np.ravel(temperature))
  
    return jsonify(temperature_list)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def cal_temp(start=None,end=None):
    session = Session(engine)
    if not end:
        result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).all()
    else:
        result= session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)