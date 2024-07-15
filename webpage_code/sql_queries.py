import super_secret
from sqlalchemy import text, create_engine
import pandas as pd
import datetime as dt
from flask_sqlalchemy import SQLAlchemy

DATABASE_URL = super_secret.DATABASE_URL

engine = create_engine(DATABASE_URL)

def get_level_data():
    with engine.connect() as connection:
        query = text("SELECT * FROM level_data ORDER BY date DESC LIMIT 350")
        data = connection.execute(query)
        dates = []
        temp1 = []
        temp2 = []
        for date,temp_1,temp_2 in data:
            dates.append(date)
            temp1.append(temp_1)
            temp2.append(temp_2)
        df = pd.DataFrame()
        df.insert(loc=0,column="date",value=dates)
        df.insert(loc=1,column="temp1",value=temp1)
        df.insert(loc=2,column='temp2',value = temp2)
        df["date"] = pd.to_datetime(df["date"])
    return df

def get_latest_level():
    with engine.connect() as connection:
        query = text('SELECT * FROM level_data ORDER BY date DESC LIMIT 1')
        data = connection.execute(query)
        latest_date = dt.datetime.now()
        latest_temp1 = 0
        return (latest_date.strftime('%m/%d/%Y %H:%M:%S'),str(latest_temp1))

def get_atm_data():
    with engine.connect() as connection:
        query = text('SELECT * FROM atm_data ORDER BY date DESC LIMIT 100')
        data = connection.execute(query)
        dates = []
        vocs = []
        pms = []
        rhs = []
        for date, voc, pm25, rh in data:
            dates.append(date)
            vocs.append(voc)
            pms.append(pm25)
            rhs.append(rh)
        df = pd.DataFrame()
        df.insert(loc=0,column="date",value=dates)
        df.insert(loc=1,column="voc",value=vocs)
        df.insert(loc=2,column="pm",value=pms)
        df.insert(loc=3,column="rh",value=rhs)
        df["date"] = pd.to_datetime(df["date"])
    return df

def get_all_data():
    with engine.connect() as connection:
        query = text("SELECT * FROM level_data ORDER BY date")
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

def nuke():
    with engine.connect() as connection:
        query = text("DELETE FROM level_data")
        data = connection.execute(query)
    return 0