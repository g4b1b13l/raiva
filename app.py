import dash
import dash_core_components as dcc
import dash_html_components as html
import psycopg2 as psy

mydb=psy.connect (
host='ec2-54-235-100-99.compute-1.amazonaws.com',
user = 'mhxcrjdnckxtbr',
password='041d51b54231eb4e36b2a8d58f5ae16bc5cfaab2303d426676580f62e52ebcc1',
database='d9k1k422mp16r5')

external_stylesheets = ['https://codepen.io/g4b1b13l/pen/VwwrYdL.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(children=[
    html.H1(children='Que horas hoje?')
	])



if __name__ == '__main__':
    app.run_server(debug=True)
