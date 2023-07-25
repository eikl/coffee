import super_secret
from sqlalchemy import text, create_engine
import pandas as pd


DATABASE_URL = super_secret.DATABASE_URL
engine = create_engine(DATABASE_URL)

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
