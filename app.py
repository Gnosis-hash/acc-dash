import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from query import get_all

external_stylesheets = ['https://codepen.io/chriddyp/pen/dZVMbK.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = get_all()

fig = px.bar(df, x="year", y="loan", color="degree_type", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='A Continuous Charity'),

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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
