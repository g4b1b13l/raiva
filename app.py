import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/g4b1b13l/pen/VwwrYdL.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = 

        html.H1(children= '''Parabéns Leidson!

                             Para: Leidson
                             De: Estagiária de mixagem''')
       



if __name__ == '__main__':
    app.run_server(debug=True)
