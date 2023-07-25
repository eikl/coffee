from flask import Flask, render_template
import pandas as pd
import datetime as dt
import sql_queries
import bokeh_figure as bokeh
app = Flask(__name__)
#
# This gives the latest coffee level
#
@app.route('/')
def home():
    script,div = bokeh.plot()
    date,level = sql_queries.get_latest_level()
    consumption = sql_queries.calculate_consumption()
    consumption = str(consumption).strip('(),')
    return render_template('index.html', date=date, level=level, consumption=consumption,
                           script=script,div=div)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080)