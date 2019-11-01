import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/g4b1b13l/pen/VwwrYdL.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout =     html.Div(

        [html.H1(children= 'VAI ROLAR HOJE?'),
       
        ]
              , 

         style={
        'font-size': '5pt',
        #'height': '75px',
        'margin': '-10px -10px -10px',
        'background-color': '#ADD8E6',
        'text-align': 'center',
        #'border-radius': '2px',
        #'display': 'flex',
        #'margin-left': '0',
        } 
        ),



if __name__ == '__main__':
    app.run_server(debug=True)
