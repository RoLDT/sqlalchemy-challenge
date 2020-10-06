import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measures = Base.classes.measurement
Station = Base.classes.station
#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return(
        f"Available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    results = session.query(Measures.date, Measures.prcp)\
        .order_by(Measures.date.desc()).all()
    
    session.close()

    data = list(np.ravel(results))

    return jsonify(data)

@app.route("/api/v1.0/stations")
def stations():
    
    session = Session(engine)

    results = session.query(Measures.station, func.count(Measures.station)).group_by(Measures.station)\
    .order_by(func.count(Measures.station).desc()).all()

    session.close()

    data = list(np.ravel(results))
    
    return jsonify(data)

@app.route("/api/v1.0/tobs")
def tobs():
    date_year_ago = "2016-08-23"

    session = Session(engine)

    results = session.query(Measures.date, Measures.tobs).filter(Measures.station == "USC00519281").\
    filter(Measures.date > date_year_ago).all()

    session.close()

    data = list(np.ravel(results))
    
    return jsonify(data)

@app.route("/api/v1.0/<start>")
def temp_start(start):
    start = dt.datetime.strptime(start,"%Y-%m-%d")
    
    session = Session(engine)


    results = session.query(func.max(Measures.tobs),func.min(Measures.tobs),func.avg(Measures.tobs)).filter(Measures.date >= start).all()

    session.close()

    data = list(np.ravel(results))
    
    return jsonify(data)

@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start,end):
    start = dt.datetime.strptime(start,"%Y-%m-%d")
    end = dt.datetime.strptime(end,"%Y-%m-%d")

    session = Session(engine)

    results = session.query(func.max(Measures.tobs),func.min(Measures.tobs),func.avg(Measures.tobs)).filter(Measures.date >= start).filter(Measures.date <= end).all()

    session.close()

    data = list(np.ravel(results))

    
    return jsonify(data)
    
if __name__ == '__main__':
    app.run(debug=True)