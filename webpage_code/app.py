from flask import Flask, render_template
import pandas as pd
import datetime as dt
import sql_queries
import bokeh_figure as bokeh
application = Flask(__name__)
#
# This gives the latest coffee level
#
@application.route('/')
def home():
    script,div = bokeh.plot()
    date,level = sql_queries.get_latest_level()
    atm_df = sql_queries.get_atm_data()
    temperature = round(float(atm_df["temp"].iloc[-1]),1)
    level = round(level,1)
    print(atm_df)
    return render_template('index.html', date=date, level=level,
                           script=script,div=div,temperature=temperature)

if __name__ == "__main__":
    application.run(host='0.0.0.0',port=8080)