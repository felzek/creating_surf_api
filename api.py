import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
app = Flask(__name__)

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

@app.route("/api/precipitation")
def precipitation():
    today = dt.date.today()
    prev_year = today - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)
        dict[row.date] = row.prcp
   

@app.route("/api/stations")
def stations():
    stations_list = []
    stations = session.query(Stations.station, Stations.name, Stations.latitude, Stations.longitude, Stations.elevation).all()
    for station in stations:
        station_dict = {"station_id": station[0], "name": station[1], "latitude": station[2], "longitude": station[3], "elevation": station[4]}
        stations_list.append(station_dict)
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def temps_json():
    results = prcp_or_temps(Measurements.tobs)
    return jsonify(results)

@app.route("/api/<start>")
def temp_summary_start(start):
    temps = session.query(func.min(Measurements.tobs), func.max(Measurements.tobs), func.avg(Measurements.tobs)).filter(Measurements.date >= start_date).first()
    temps_dictionary1 = {"minimum temperuture": temps[0], "maximum temperature": temps[1], "average temperature": temps[2]}
    return jsonify(temps_dictionary1)

@app.route("/api/<start>/<end>")
def temp_summary_range(start, end):
     temps = session.query(func.min(Measurements.tobs), func.max(Measurements.tobs), func.avg(Measurements.tobs)).filter(Measurements.date >= start_date, Measurements.date <= end_date).first()
    temps_dictionary2 = {"TMIN": temps[0], "TMAX": temps[1], "TAVG": temps[2]}
    return jsonify(temps_dictionary2)

if __name__ == '__main__':
	app.run(debug=False)
