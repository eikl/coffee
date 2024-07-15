from flask import Flask, render_template, Response, request, redirect, url_for, abort
import pandas as pd
import datetime as dt
import sql_queries
import bokeh_figure as bokeh
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
import super_secret
application = Flask(__name__)
application.secret_key = super_secret.key

login_manager = LoginManager()
login_manager.init_app(application)


broken = False

class User(UserMixin):
    def __init__(self, id):
        self.id = id

def korsi_check():
    now = dt.datetime.now()
    if now.weekday() == 4:  # Monday is 0 and Sunday is 6
        if now.hour >= 16:
            return True
        else:
            return False
    else:
        return False

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


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
            date,temp1 = sql_queries.get_latest_level()
            return render_template('index.html', date=date, level=temp1, script=script, div=div)
        except Exception as e:
            print(e)
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
    filename = dt.datetime.now().strftime('%m/%d/%Y')
    return Response(
        df.to_csv(),
        mimetype="text/csv",
        headers={"Content-disposition":
        f"attachment; filename={filename}.csv"})

@application.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == super_secret.password:  # Replace with your desired credentials
            user = User(id=1)
            login_user(user)
            return redirect(url_for('admin_panel'))
            print('success')
            return 0
        else:
            return abort(401)  # Unauthorized access
    return render_template('admin_login.html')

@application.route('/admin_panel')
@login_required
def admin_panel():
    return render_template('admin_panel.html')

@application.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@application.route('/nuke', methods=['POST'])
@login_required
def nuke():
    sql_queries.nuke()
    return render_template('nuked.html')


if __name__ == "__main__":
    application.run(host='0.0.0.0',port=8080)
