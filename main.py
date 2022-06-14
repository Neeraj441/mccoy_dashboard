import json
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
import sqlalchemy
from flask import Flask, render_template
from plotly.subplots import make_subplots

host = '/cloudsql/turnkey-crowbar-351921:us-central1:instance2'
db = 'mccoy_energy'
table = 'mccoytotalsandsmweather'
user = 'root'
pasw = 'instance2'
query_string = dict({'unix_socket': host})
engine = sqlalchemy.create_engine(
    sqlalchemy.engine.url.URL(
        drivername='mysql+pymysql',
        username=user,
        password=pasw,
        database=db,
        query=query_string,
    ),
    pool_size=5,
    max_overflow=2,
    pool_timeout=30,
    pool_recycle=1800
)
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
def tempchart():
    connection = engine.connect()
    results = connection.execute("SELECT * FROM " + table)
    df = pd.DataFrame(results.fetchall())

    df.index = df['rec_day']

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(go.Scatter(x=df.index, y=df["btus"], name="Electricity Consumption"), secondary_y=False,
                  )

    fig.add_trace(go.Scatter(x=df.index, y=df["Temp Max"], name="Temperature Details"), secondary_y=True)

    # Add figure title
    fig.update_layout(
        title_text="<b>Electricity and temperature charts for McCoy Buildings</b>"
    )

    # Set x-axis title
    fig.update_xaxes(title_text="Time Period")

    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Electricity Consumption (In MILLIONS)</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Temperature in Fahrenheit</b>", secondary_y=True)

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('dashboard.html', graphJSON=graphJSON)


@app.route('/admin_login')
def admin_login():
    return render_template('admin_login.html')


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python3_render_template]
# [END gae_python38_render_template]
