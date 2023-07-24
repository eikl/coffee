from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, create_engine
import pandas as pd
import datetime
import sys
import super_secret
from bokeh.plotting import figure
from bokeh.embed import components

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
    
@app.route('/plot')
def plot():
    # Prepare some data
    x = [1, 2, 3, 4, 5]
    y = [6, 7, 2, 4, 5]

    # Create a new plot with a dark background
    p = figure(title="simple line example", 
               x_axis_label='x', 
               y_axis_label='y',
               width=400,
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
    p.border_fill_color = "#464866"

    p.toolbar.logo = None
    p.toolbar_location = None
    # Add a line renderer with legend and line thickness
    p.line(x, y, legend_label="Temp.", line_width=2, line_color="#f5f6fa")

    # Generate the components of the plot
    script, div = components(p)

    # Return them to the template
    return render_template('plot.html', script=script, div=div)


#
# This gives the latest coffee level
#
@app.route('/')
def show_latest_data():
    date,level = get_latest_level()
    consumption = calculate_consumption()
    consumption = str(consumption).strip('(),')
    return render_template('index.html', date=date, level=level, consumption=consumption)