import super_secret
from sqlalchemy import text, create_engine
import pandas as pd
from flask_sqlalchemy import SQLAlchemy

DATABASE_URL = super_secret.DATABASE_URL

engine = create_engine(DATABASE_URL)

def get_level_data():
    with engine.connect() as connection:
        query = text("SELECT * FROM level_data ORDER BY date DESC LIMIT 100")
        data = connection.execute(query)
        dates = []
        levels = []
        for date,level in data:
            dates.append(date)
            levels.append(level)
        df = pd.DataFrame()
        df.insert(loc=0,column="date",value=dates)
        df.insert(loc=1,column="level",value=levels)
        df["date"] = pd.to_datetime(df["date"])
    return df

def get_latest_level():
    with engine.connect() as connection:
        query = text('SELECT * FROM level_data ORDER BY date DESC LIMIT 1')
        data = connection.execute(query)
        for date,level in data:
            latest_date = date
            latest_level = round(level,1)
        return (latest_date.strftime('%m/%d/%Y %H:%M:%S'),str(latest_level))

def get_atm_data():
    with engine.connect() as connection:
        query = text('SELECT * FROM atm_data ORDER BY date DESC LIMIT 100')
        data = connection.execute(query)
        dates = []
        temps = []
        hums = []
        pres = []
        for date, temperature, humidity, pressure in data:
            dates.append(date)
            temps.append(temperature)
            hums.append(humidity)
            pres.append(pressure)
        df = pd.DataFrame()
        df.insert(loc=0,column="date",value=dates)
        df.insert(loc=1,column="temp",value=temps)
        df.insert(loc=2,column="hum",value=hums)
        df.insert(loc=3,column="pres",value=pres)
        df["date"] = pd.to_datetime(df["date"])
        print(df)
    return df
