from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, create_engine
import pandas as pd
import datetime
import sys
import super_secret
from bokeh.plotting import figure
from bokeh.models import DatetimeTickFormatter
from bokeh.embed import components
import datetime as dt
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

def plot():
    # Prepare some data
    df = get_level_data()
    try:
        df = df[dt.datetime.now()-dt.timedelta(hours=1),dt.datetime.now()]
    except KeyError:
        df = pd.DataFrame(columns=["date","level"])
    x = df["date"]
    y= df["level"]

    # Create a new plot with a dark background
    p = figure(x_axis_label='x', 
               y_axis_label='y',
               x_axis_type="datetime",
               width=700,
               height=400,
               background_fill_color='#2f3640')

    # Set other visual attributes 
    p.title.text_color = "White"
    p.xaxis.axis_label_text_color = "White"
    p.yaxis.axis_label_text_color = "White"
    p.grid.grid_line_color = "#464866"
    p.xgrid.grid_line_color = "#464866"
    p.ygrid.grid_line_color = "#464866"
    p.xaxis.major_label_text_color = "White"
    p.yaxis.major_label_text_color = "White"
    p.outline_line_color = "#464866"
    p.border_fill_color = "#2f3640"
    p.toolbar.logo = None
    p.toolbar_location = None
    # Add a line renderer with legend and line thickness
    p.line(x, y, line_width=2, line_color="#f5f6fa")
    p.xaxis.formatter=DatetimeTickFormatter(
        hours=["%d %B %Y"],
        days=["%d %B %Y"],
        months=["%d %B %Y"],
        years=["%d %B %Y"],
    )
    p.xaxis.major_label_orientation = 1.0


    # Generate the components of the plot
    script, div = components(p)

    return script,div


#
# This gives the latest coffee level
#
@app.route('/')
def show_latest_data():
    script,div = plot()
    date,level = get_latest_level()
    consumption = calculate_consumption()
    consumption = str(consumption).strip('(),')
    return render_template('index.html', date=date, level=level, consumption=consumption,
                           script=script,div=div)