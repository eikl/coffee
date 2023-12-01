from flask import Flask, render_template, Response
import pandas as pd
import datetime as dt
import sql_queries
import bokeh_figure as bokeh
application = Flask(__name__)

broken = False

def korsi_check():
    now = dt.datetime.now()
    if now.weekday() == 4:  # Monday is 0 and Sunday is 6
        if now.hour >= 16:
            return True
        else:
            return False
    else:
        return False
#
# This gives the latest coffee level
#
@application.route('/')
def home():
    current_day = dt.datetime.now().weekday()

    viikonloppu = current_day >= 5
    
    if not broken:
        try:
            script,div = bokeh.plot()
            date,level = sql_queries.get_latest_level()
            #atm_df = sql_queries.get_atm_data()
            #temperature = round(float(atm_df["temp"].iloc[-1]),1)
            return render_template('index.html', date=date, level=level, script=script, div=div)
        except:
            return render_template('no_internet.html')
    else:
        return render_template('broken.html')
    
@application.route('/lataa')
def lataus():
    #
    # TODO: hae kaikki data ladattavaksi
    #
    df = sql_queries.get_all_data()
    # d = {'col1': [1, 2], 'col2': [3, 4]}
    # df = pd.DataFrame(data=d)
    return Response(
        df.to_csv(),
        mimetype="text/csv",
        headers={"Content-disposition":
        "attachment; filename=filename.csv"})


@application.route('/nuke')
def nuke():
    sql_queries.nuke()
    return render_template('broken.html')


if __name__ == "__main__":
    application.run(host='0.0.0.0',port=8080)
