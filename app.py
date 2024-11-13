# Import the dependencies.
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import os

def check_file_permissions(file_path):
    """Check if the file exists and is readable."""
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return False
    
    if not os.access(file_path, os.R_OK):
        print(f"Error: You do not have read permissions for '{file_path}'.")
        return False
    
    print(f"The file '{file_path}' exists and is readable.")
    return True

#################################################
# Database Setup
#################################################
# Construct the database file path
database_path = os.path.join("Resources", "hawaii.sqlite")

# Check file permissions
if not check_file_permissions(database_path):
    raise PermissionError(f"Unable to access the database file '{database_path}'.")

# Create the engine
engine = create_engine(f"sqlite:///{database_path}")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Use inspector to get table information
inspector = inspect(engine)

# Get table names
table_names = inspector.get_table_names()
print("Tables in the database:", table_names)

# Print the column names for each table
for table_name in table_names:
    columns = inspector.get_columns(table_name)
    print(f"\nColumns in {table_name}:")
    for column in columns:
        print(column['name'])

# Print the classes that automap found
print("\nClasses found by automap:")
for class_name in Base.classes.keys():
    print(class_name)

# Save references to each table
try:
    Measurement = Base.classes.measurement
    Station = Base.classes.station
except AttributeError as e:
    print(f"Error: {e}")
    print("Make sure your database tables are named 'measurement' and 'station' (case-sensitive)")
    raise

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
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

# Add your other route definitions here...

if __name__ == '__main__':
    app.run(debug=True)