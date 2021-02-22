import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import numpy as np
import pandas as pd


##Build out app from plotly below
external_stylesheets = ['https://codepen.io/chriddyp/pen/dZVMbK.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = get_all()

np.random.seed(42) 
   
random_x= np.random.randint(1, 101, 100) 
random_y= np.random.randint(1, 101, 100)
 
fig = px.bar(random_x, y = random_y)

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
    app.run_server
