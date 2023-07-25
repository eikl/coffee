from bokeh.sampledata.glucose import data
from bokeh.themes import Theme
from bokeh.plotting import figure
import pandas as pd
from bokeh.sampledata import download
from bokeh.embed import components
from bokeh.io import curdoc
import datetime as dt
import sql_queries

def plot():
    # Prepare some data
    download()
    #df = sql_queries.get_level_data()
    #
    # Try to get the last hour, if there is no data, return an empty dataframe
    #
    #try:
    #    df = df[dt.datetime.now()-dt.timedelta(hours=1),dt.datetime.now()]
    #except KeyError:
    #    df = pd.DataFrame(columns=["date","level"])

    #sample data
    df = data

    x = data.loc['2010-10-06'].index.to_series()
    y= df.loc['2010-10-06']["glucose"]

    #x = df["date"]
    #y = df["level"]
    # Create a new plot with a dark background
    p = figure(x_axis_label='Aika', 
               y_axis_label='Tilavuus (ml)',
               x_axis_type="datetime",
               width=700,
               height=400,
               sizing_mode="stretch_width",
               background_fill_color = '#2f3640',
               border_fill_color = '#2f3640',
               outline_line_color = '#2f3640'
               )
    
 
    # Add a line renderer with legend and line thickness
    p.line(x, y, line_width=2, line_color="#f5f6fa")
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