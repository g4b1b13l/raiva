import dash

external_stylesheets = ['https://codepen.io/g4b1b13l/pen/VwwrYdL.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(children=[
    html.H1(children='AMO TU MO'),



])



if __name__ == '__main__':
    app.run_server(debug=True)
