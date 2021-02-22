import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from configparser import ConfigParser
import psycopg2
import pandas as pd

# Define Function for configuring DB connection
def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

# Connect to Heroku DB
def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

##Query the table from Heroku DB
def get_all():
    """ query parts from the parts table """
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        sql = "SELECT year, degree_type, SUM(loan_amount) AS loan FROM public.main GROUP BY 1, 2;"
        df = pd.read_sql_query(sql, conn)
        ##cur.execute(sql)
        ##rows = cur.fetchall()
        ##print(df)
        return df
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

##Build out app from plotly below
external_stylesheets = ['https://codepen.io/chriddyp/pen/dZVMbK.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = 'test'

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = get_all()

fig = px.bar(df, x="year", y="loan", color="degree_type", barmode="group")


app.layout = html.Div(children=[
    html.H1(children='A Continuous Charity test'),

    html.Div(children='''
        Loan Discovery Dashboard
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig,
        config={'displayModeBar': False}
    )
])

if __name__ == '__main__':
    app.run_server()
