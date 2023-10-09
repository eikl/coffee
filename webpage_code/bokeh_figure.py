
from bokeh.themes import Theme
from bokeh.plotting import figure, show
import pandas as pd
from bokeh.sampledata import download
from bokeh.embed import components
from bokeh.io import curdoc
from bokeh.models import Range1d, LinearAxis
from bokeh.models import DatetimeTickFormatter, NumeralTickFormatter
import datetime as dt
import sql_queries

def plot():
    # Prepare some data

    df = sql_queries.get_level_data()
    df2 = sql_queries.get_atm_data()

    x = pd.to_datetime(df["date"])
    y = df["level"]
    y = y.rolling(window=10).mean()
    #y2 = df2["temp"]
    #x2 = df2["date"]
    # Create a new plot with a dark background
    p = figure(x_axis_label='Aika', 
               y_axis_label='Etäisyys anturista',
               x_axis_type = 'datetime',
               width=700,
               height=400,
               background_fill_color = '#2f3640',
               border_fill_color = '#2f3640',
               outline_line_color = '#2f3640',
               #y_range = Range1d(0,10),
               active_drag = None,
               active_scroll = None,
               active_tap = None
               )
    
    print(p.xaxis[0].formatter)
    # Add a line renderer with legend and line thickness
    p.xaxis[0].formatter = DatetimeTickFormatter(minsec='%H:%M:%S',hourmin='%H:%M:%S',seconds='%H:%M:%S',
                                                 minutes = '%H:%M:%S')

    
    p.line(x, y, line_width=2, line_color="#f5f6fa")

    #p.extra_y_ranges['temp'] = Range1d(0,100)
    #p.line(x, y2, color="orange", y_range_name="temp")

    #ax2 = LinearAxis(y_range_name="temp", axis_label="Lämpötila (C)")
    #ax2.axis_label_text_color ="navy"
    #p.add_layout(ax2, 'right')


    #p.yaxis[0].formatter = NumeralTickFormatter(format='0.00')
    p.toolbar_location = None
    p.toolbar.logo = None
    p.xaxis.major_label_text_color='white'
    p.yaxis.major_label_text_color='white'
    p.xgrid.visible = False
    p.ygrid.visible = False
    p.axis.major_label_text_color= "white"
    p.xaxis.axis_label_text_color ="white"
    p.yaxis.axis_label_text_color="white"
    p.xaxis.axis_line_color = "white"
    p.yaxis.axis_line_color= "white"
    # Generate the components of the plot
    script, div = components(p)
    return script,div
