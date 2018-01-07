from flask import Flask, jsonify
import datetime as dt

app = Flask(__name__)

@app.route("/api/precipitation")
def precipitation():
    today = dt.date.today()
    prev_year = today - dt.timedelta(days=365)
    dict = {}
    data = df[(df.date >= str(prev_year)) & (df.date <= str(today))].groupby(['date']).sum()
    for index, row in df.iterrows():
        dict[row.date] = row.prcp
    return jsonify(dict)

@app.route("/api/stations")
def stations():
    stations = list(df.station.unique())
    return jsonify(stations)

@app.route("/api/tobs")
def tobs():
    today = dt.date.today()
    prev_year = today - dt.timedelta(days=365)
    return jsonify(list( int(x) for x in df[(df.date >= str(prev_year)) & (df.date <= str(today))]['tobs']))

@app.route("/api/<start>")
def temp_summary_start(start):
    temps = df[(df.date >= start)]
    min_temp = temps.tobs.min()
    max_temp = temps.tobs.max()
    mean_temp = temps.tobs.mean()
    return jsonify({"min_temp": int(min_temp), "max_temp": int(max_temp), "mean_temp": int(mean_temp)})

@app.route("/api/<start>/<end>")
def temp_summary_range(start, end):
    temps = df[(df.date >= start) & (df.date <= end)]
    min_temp = temps.tobs.min()
    max_temp = temps.tobs.max()
    mean_temp = temps.tobs.mean()
    return jsonify({"min_temp": int(min_temp), "max_temp": int(max_temp), "mean_temp": int(mean_temp)})

if __name__ == '__main__':
	app.run(debug=False)
