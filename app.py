import dash
import dash_core_components as dcc
import dash_html_components as html
import math
from dash.dependencies import Input, Output
import csv
import json
import pandas as pd
import plotly.express as px
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

d = pd.read_csv('co2_data.csv')
def output_(input_value):
    try:
        pi=math.pi
        na=6.022e23
        d=1.5
        h=15
        rho=500
        V=pi*h*(d/2)**2
        mt=rho*V
        fcarbon=0.5
        mcarbon=fcarbon*mt
        mucarbon=0.012
        ncarbon=mcarbon*na/mucarbon
        Ntree=7.5e9*int(input_value)
        NCO2=Ntree*ncarbon
        muair=28.97e-3
        mair=5e18
        Nair=mair*na/muair
        fractionCO2=NCO2/Nair
        ppmCO2=fractionCO2*1e6
        newppm=400-ppmCO2
        ss="CO2 with "+input_value+" Tree per Person  = "+str(newppm)+" ppm"
        return ss
    except:
        return 'enter a valid number'

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


actions_page = html.Div([
    dcc.Link('Plant-a-tree', href='/Plant-a-tree'),
    html.Br(),
    dcc.Link('Health', href='/Health'),
])

Plant_a_tree_layout = html.Div([
    html.H1('Plant-a-tree'),
    dcc.Input(id='input-box', value='0',type='text',required='required'),
    html.Div(id='my-div'),
    html.Button('Submit', id='button'),
    html.Div(id='container-button-basic',children='Enter a value and press submit'),
    dcc.Graph(
        id='example-graph',
        figure = px.bar(d, x='year', y='ppm', color='ppm')
    ),
    html.Div(id='Plant-a-tree-content'),
    html.Br(),
    dcc.Link('Go back to actions_page', href='/'),
])

@app.callback(
    dash.dependencies.Output('container-button-basic', 'children'),
     [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-box', 'value')])
def update_output_div(clicks,value):
    s=output_(value)
    return s


Health_layout = html.Div([
    html.H1('Health'),
    dcc.RadioItems(
        id='Health-radios',
        options=[{'label': i, 'value': i} for i in ['Environment', 'Lifestyle', 'Vector-borne-diseases']],
        value='Lifestyle'
    ),
    html.Div(id='Health-content'),
    html.Br(),
    dcc.Link('Go back to actions_page', href='/')
])

@app.callback(dash.dependencies.Output('Health-content', 'children'),
              [dash.dependencies.Input('Health-radios', 'value')])
def page_2_radios(value):
    return 'You have selected "{}"'.format(value)


# Update the actions_page
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/Plant-a-tree':
        return Plant_a_tree_layout
    elif pathname == '/Health':
        return Health_layout
    else:
        return actions_page



if __name__ == '__main__':
    app.run_server(debug=True)
