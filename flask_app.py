from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, create_engine
import pandas as pd
import datetime
import sys
import super_secret
DATABASE_URL = super_secret.DATABASE_URL
engine = create_engine(DATABASE_URL)
app = Flask(__name__)


def get_level_data():
    with engine.connect() as connection:
        query = text("SELECT * FROM level_data")
        data = connection.execute(query)
        dates = []
        levels = []
        for date,level in data:
            dates.append(date)
            levels.append(level)
        df = pd.DataFrame()
        df.insert(loc=0,column="date",value=dates)
        df.insert(loc=1,column="level",value=levels)
    return df

def get_latest_level():
    with engine.connect() as connection:
        query = text('SELECT * FROM level_data ORDER BY date DESC LIMIT 1')
        data = connection.execute(query)
        for date,level in data:
            latest_date = date
            latest_level = level
        return (latest_date.strftime('%m/%d/%Y %H:%M:%S'),str(latest_level))
    
def calculate_consumption():
    with engine.connect() as connection:
        query = text('SELECT SUM(volume) FROM consumption_data')
        data = connection.execute(query)
        return data.first()




#
# This gives the latest coffee level
#
@app.route('/')
def show_latest_data():
    date,level = get_latest_level()
    consumption = calculate_consumption()
    consumption = str(consumption).strip('(),')
    return [date,level,consumption]