import psycopg2 as psy
import dash
import dash_core_components as dcc    
import dash_html_components as html
import os
import glob
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output, State                                                          
from faker import Factory
import plotly.offline as py
import plotly.graph_objs as go 
from IPython.display import Image
import sys
import logging
import dash_bootstrap_components as dbc
import base64
from datetime import datetime
now = datetime.now()


#Até aqui apenas declaramos as bibliotecas, pode ter algumas que foram importadas mas não esta sendo utilizada, pois foi sendo descartada
#com o tempo



# Agora iremos criar os dicionarios, que sera utilizado para codificar e descodificar as chaves utilizadas no banco de dados

dict_mudar = {
    'evd' : 'evadidos',
    'ing' : 'ingressantes'
}



dict_ano =               {
        0: 2013,
        1: 2014,
        2: 2015,
        3: 2016,
        4: 2017
        }

dict_raca= { 0:'Não quis declarar',
            1: 'Branca',
            2: 'Preta',
            3: 'Parda',
            4: 'Amarela',
            5: 'Indígena',
            6: 'Não dispõe',
            9: 'Não dispõe'
    
}

dict_ies= { 0:'nd',
            1: 'FPB',
            2: 'Nassau JP',
            3: 'Nassau CG',
            4: 'IFPB',
            5: 'UFCG',
            6: 'UFPB'
    
}

dict_order_axis_x= { 'Quantidade integralizada':['(0 - 500)','(500 - 1000)', '(1000 - 2500)', '(3000>)'],  #Coloca a ordem que ficara no eixo X BARRA
                    'Por idade': ['(15-21)', '(21-25)', '(25-35)', '(35>)'],
                    'Por raca' : [''],
                    'Por sexo': [''],
                    'Por deficiencia': [''],
                    'Por quantidade': [2013,2014,2015,2016,2017],
                    'Atividade Extracurricular': [''],
                    'Vagas Reservadas' : [''],
                    'Para outra Ies': ['']
    
}



dict_radio = { 'evd' : 'fato_evasao',
                'ing' : 'fato_ingresso'
    
}

dict_no = { 'FPB':1,
            'NASSAU JP':2,
            'NASSAU CG':3,
            'IFPB':4  ,
            'UFCG':5 ,
            'UFPB':6
}           


dict_sexo={0: 'Masculino',
            1: 'Feminino',
            2: 'Masculino'
}



dict_deficiencia= { 0:'Não',
            1: 'Sim',
            2: 'Não dispõe',
            9: 'Não dispõe'
    
}


dict_qt_integ= {None:None,
    'Não possui informação' : 'Não possui informação',
           '(0 - 500)' : '(0 - 500)',
           '(500 - 1000)' : '(500 - 1000)',
            '(1000 - 2500)' : '(1000 - 2500)',
            '(2500 - 3000)': '(2500 - 3000)',
            '(3000>)' : '(3000>)'
}


dict_gamb={a:a for a in range(0,4000)}

dict_idade= {       
            '(15-21)':'(15-21)',
            '(21-25)':'(21-25)',
            '(25-35)':'(25-35)',      
            '(35>)':'(35>)'
            
}
 
dict_atividade= { 0: 'Não Possui',
                    1: 'Possui'
    

}

dict_reserva = {0:'Não reversado',
                1: 'Reservado'
    

}


dict_dicionario={ 'Quantidade integralizada' : dict_qt_integ,  #Qual dicionario vai ser usado para decodificar os valores
                    'Por raca' : dict_raca,
                    'Por sexo': dict_sexo,
                    'Por deficiencia': dict_deficiencia,
                    'Por idade' : dict_idade,
                    'Por quantidade': dict_gamb,
                    'Atividade Extracurricular' : dict_atividade,
                    'Vagas Reservadas': dict_reserva,
                    'Para outra Ies': dict_ies
    
}

dict_coluna= {'Quantidade integralizada' : 'qt_carga_horaria_integ', # Diz qual eh a coluna no banco de dados que vai corresponder a pergunta
                  'Por raca' : 'tp_cor_raca',
                    'Por sexo': 'tp_sexo',
                    'Por deficiencia': 'tp_deficiencia',
                    'Por idade' : 'idade',
                    'Por quantidade': 'censo',
                    'Atividade Extracurricular': 'in_atividade_extracurricular',
                    'Vagas Reservadas': 'in_reserva_vagas',
                    'Para outra Ies': 'sk_ies'

    
}

dict_eixo_x= {'Quantidade integralizada' : 'Quantidade integralizada', # Diz o que vai aparecer no eixo X de barra
                  'Por raca' : 'Raça',
                    'Por sexo': 'Sexo',
                    'Por deficiencia': 'Deficiencia',
                    'Por idade' : 'Idade',
                    'Por quantidade': 'Anos',
                    'Atividade Extracurricular' : 'Atividade Extracurricular',
                    'Vagas Reservadas': 'Vagas Reservadas',
                    'Para outra Ies': 'IES - Elétrica'
    
}

dict_eixo_y= {'Quantidade integralizada' : 'Quantidade de alunos ', # Diz o que vai aparecer no eixo Y de barra
                  'Por raca' : 'Quantidade de alunos ',
                    'Por sexo': 'Quantidade de alunos ',
                    'Por deficiencia': 'Quantidade de alunos ',
                    'Por idade' : 'Quantidade de alunos ',
                    'Por quantidade': 'Quantidade de alunos ',
                    'Atividade Extracurricular' : 'Quantidade de alunos',
                    'Vagas Reservadas': 'Quantidade de alunos',
                    'Para outra Ies': 'Quantidade de alunos'
    
}



# Termina aqui os dicionarios

mydb=psy.connect (
host='ec2-54-235-100-99.compute-1.amazonaws.com',
user = 'mhxcrjdnckxtbr',
password='041d51b54231eb4e36b2a8d58f5ae16bc5cfaab2303d426676580f62e52ebcc1',
database='d9k1k422mp16r5')

#mydb=psy.connect (
#host='localhost',
#user = 'ODG_adapt',
#password='observatorio',
#database='ODG_adapt')

mycursor=mydb.cursor()

#Aqui decalaramos o que ficara dentros dos botoes

Ies=['FPB','NASSAU JP', 'NASSAU CG', 'IFPB', 'UFCG', 'UFPB']

alo=dbc.themes.BOOTSTRAP

anos = [2013,2014,2015,2016,2017]
external_stylesheets = ['https://codepen.io/g4b1b13l/pen/VwwrYdL.css']

evadidos=['Quantidade integralizada',
'Por raca',
'Por sexo',
'Por deficiencia',
'Por idade',
'Por quantidade',
'Atividade Extracurricular',
'Para outra Ies'
]

ingressante=[
'Por raca',
'Por sexo',
'Por deficiencia',
'Por idade',
'Por quantidade',
'Vagas Reservadas']

dict_mudar_list = {     #é para saber o que tem dentro de cada lista quando olhado as fatos.
    'evd' : evadidos,
    'ing' : ingressante
}

formato=['Pizza', 'Barra', 'Barra - Stacked']

#termina aqui os parametros dos botoes

#Comeca entao o codigo 

app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
        meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ])

server = app.server


app.title = 'Plataforma_ODG'


app.layout = html.Div([



    html.Div(

        [html.H1(children= 'ODG - Observatório de Dados da Graduação'),
       
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


    
    dbc.Button('Menu', outline=True, id='menu_lateral'),

    dcc.Checklist(
    id='check',
    options=[   
    {'label': '', 'value': 'ativado'},


    ],
    value=['d'],
    labelStyle={'display': 'none'}
    ),


    html.Div([

        html.Div([

            html.Div([
                html.Div([

        html.Div([
        html.Label('Comparar com dois graficos?',style={'padding-top': '30px'}),
        dcc.RadioItems(  
            options=[
                {'label': 'Sim', 'value': 'sim'},
                {'label': 'Não', 'value': 'nao'},
                
            ],
            id='dois_graphs',
            value='nao',
            
            ),
        ],),


        html.Div([

            html.Label('Qual grafico deseja configurar?'),
            dcc.Dropdown(
                options=[
                    {'label': 'Gráfico 1, da esquerda', 'value': 'g1'},
                    {'label': 'Gráfico 2, da direita', 'value': 'g2'}, 
                    
                ],
                id='config_graph',
                value='g1',
                multi=False,
                searchable=False,
                #className='two columns',
                #style={'display': 'block',
                #'z-index': '1',
                #}
                ),

            ],
            
            id='configa_graph'
            #className='two columns',
                
            ),

        ],
        #className='row',
        ),




                dcc.RadioItems(
                    options=[
                        #{'label': 'None', 'value': 'none'},
                        {'label': 'Evasão', 'value': 'evd'},
                        {'label': 'Ingresso', 'value': 'ing'}
                    ],
                    id='escolher',
                    value='evd',
                    labelStyle={'display': 'inline-block',
                    'margin-top':'30px'}
                ),

               

                html.Div([
                    html.Label('Censo'),
                    html.Div([

                    dcc.RangeSlider(
                        min=0,
                        max=4.2,
                        marks={
                            0: '2013',
                            1: '2014',
                            2: '2015', 
                            3: '2016',
                            4: '2017'
                        },
                        value=[0,4],
                        id='variavel',
                        step=1,
                        #count= 1,

                    ),

                    ],
                    #id='variavel',
                    style = {'margin-top': '5px',
                    'margin-bottom': '25px',
                    'margin-left':'10px'},),


                    #html.Label('Censo'),

                    #dcc.Dropdown(
                    #    id = 'variavel',
                    #    options=[
                    #        {'label': j, 'value': j} for j in anos 
                    #    ],
                    #    multi=True
                    #),

                    html.Div([
                        html.Label('Tipo do Grafico'),
                        dcc.Dropdown(
                            id = 'pi_ou_bar',

                            options=[
                                {'label': fo, 'value': fo} for fo in formato 
                            ],

                            value='',

                            multi=False,
                            searchable=False,
                        )],
                    ),

                    html.Div([
                        html.Label('Ies'),
                        dcc.Dropdown(
                            id = 'ies',

                            options=[
                                {'label': a, 'value': a} for a in Ies 
                            ],

                            multi=True,
                            searchable=False,
                            value= ''
                        )],
                        
                        id='tudo_ies'
                    ),

                    html.Div([
                        html.Label(children='Alunos evadidos por',
                        id='trocar_nome_da_pergunta'),
                        dcc.Dropdown(
                            id = 'tipo',
                            value='',
                            options=[
                                {'label': a, 'value': a} for a in evadidos 
                            ],

                            multi=False,
                            searchable=False,
                            )],
                            style = {'display': 'block'},
                            id='evasao'
                        ),


                    ],
                    id='dropdowns',
                    style = {'display': 'block'}

                    )


            ],
            style={
            #'margin-top': '60px',
            #'display': 'inline-block'
            #'background-color': '#add8e6',
            } ,
            id='tudin',
            #className='two columns',  


            ),
            ],
        id='testando',
        style={
        #'left': '-300px',
        'margin-left': '15px'}, 
        className='barra'
        ),



            html.Div(

                [dcc.Graph(id = 'feature-graphic'),
                ]
                , 

                id='class',
                style={'display': 'inline-block',
                    'position': 'absolute',
                    'z-index': '2'


                },
                className='twelve columns',
                 
            ),

                #dcc.Graph(id = 'feature-graphic'),
                
            html.Div(

                [dcc.Graph(id='grafico-dois',),
                ],
                style={'margin-left': '100px',
                 },
                className='five columns'
            ),

                
            html.Div(
                [dcc.Graph(id='grafico-tres',
                ),
                ],

                className='five columns'
            ),
                


    ],
    className='row'
    ),

    html.Div([

        html.Div([

            html.H5('Deixe sua sugestão de pergunta abaixo: '),

            dbc.Form(
            [

                dbc.FormGroup(
                    [
                        dbc.Label("Email  *", className="mr-2"),
                        dbc.Input(id='email',type="email", placeholder="Ex.: odg@gmail.com"),
                    ],
                    className="mr-3",
                ),

                dbc.FormGroup(
                    [
                        dbc.Label("Sugestão  *", className="mr-2"),
                        dbc.Input(id='sugestao',type="text", placeholder="Ex.: Quantos alunos..."),
                    ],
                    className="mr-3",
                ),

                dbc.FormGroup(
                    [
                        dbc.Label("Nome", className="mr-2"),
                        dbc.Input(id='nome',type="text", placeholder="Ex.: João da Silva"),
                    ],
                    className="mr-3",
                ),

                html.Div([
                dbc.Button("Enviar",id='submit-button', color="primary")],
                style = {
                        'margin-top': '5px',
                #'height' : '60%',
                
                #'margin-left': '150px',
                #'margin-bottom': '60px'}
                }),

            ],
            inline=False,
            ),

            ],
            className='two columns',

        ),
            
        html.Div([ 

            dbc.Alert(
                [
                #html.H2("Quadro de mensagens"
                #         ),
                dbc.Alert(
                    #html.H2(
                        children="Campo obrigatório não informado!",
                      #  style= {'color': '#ffffff'},
                     #   ),
                        id='alerta_vermelho',
                        is_open=False,
                        #duration=6000,
                        dismissable = True,
                        style = {
                        'background-color': '#ff0000',
                        'font-size': '18px',
                        'color': '#ffffff'
                #'height' : '60%',
                
                #'margin-left': '150px',
                #'margin-bottom': '60px'}
                }),

                dbc.Alert(

                    #html.H2(
                    children="Mensagem enviada com sucesso, tentaremos um retorno o mais breve possivel!",
                    #    style= {'color': '#ffffff'},
                    #    ),
                    #'Testando este espaço',
                    id='alerta_verde',
                    is_open=False,
                    #duration=6000,
                    dismissable = True,
                    style = {
                    'background-color': '#77DD77',
                    'font-size': '18px',
                    'color': '#ffffff'
                    #'height' : '60%',
                
                    #'margin-left': '150px',
                    #'margin-bottom': '60px'}
                }),

                dbc.Alert(

                    #html.H2("Dado indisponível para este censo!",
                    #    style= {'color': '#ffffff'},
                    #    ),
                    children="Dado indisponível para este censo, campo valido apenas para censo de 2017 ou superior!",

                    #'Testando este espaço',
                    id='alerta_censo',
                    is_open=False,
                    #duration=6000,
                    dismissable = True,
                    style = {
                'font-size': '18px',
                'background-color': '#ff0000',
                'color': '#ffffff'
                #'height' : '60%',
                
                #'margin-left': '150px',
                #'margin-bottom': '60px'}
                }),


                html.Hr(),



            ]
            )
        ,],
        className='eight columns',
        style = {
        #'background-color': '#ff0000',
        #'height' : '60%',        
        'margin-left': '150px',
        'margin-bottom': '60px'}
        )
        ],
        className='row'
        ),



    html.Div(id='output'),

    ],className='row',  
    style={'width': '100%',
    'background-color': '#ffffff',
    #'height' : '60%',
    'display': 'inline-block'}
    )

app.suppress_callback_exceptions=True     

#esta funcao abaixo esta incompleta e precisa ser melhor trabalhada

@app.callback(
    dash.dependencies.Output('alerta_censo', 'is_open'),
    [dash.dependencies.Input('ies', 'value'),
    dash.dependencies.Input('variavel', 'value')])             

def mostra_alerta_quando_dado_errado(ies,censo):
    #if radio=='evd':
    if ies=='FPB' and censo < 2017 :
        return True
    else:
        return False
###

@app.callback(
    dash.dependencies.Output('tipo', 'options'),
    [dash.dependencies.Input('escolher', 'value')])             

def Muda_os_parametros_da_caixinha_da_pergunta(radio):
    #if radio=='evd':
    if radio=='ing':
        return [{'label': i, 'value': i} for i in ingressante]
    else:
        return [{'label': i, 'value': i} for i in evadidos]

@app.callback(
    dash.dependencies.Output('trocar_nome_da_pergunta', 'children'), 
    [dash.dependencies.Input('escolher', 'value')])             

def muda_nome_da_pergunta_label(radio):
    if radio == 'ing':
        return 'Alunos ingressantes por'
    if radio == 'evd':
        return 'Alunos evadidos por'

@app.callback(
   dash.dependencies.Output('class', 'style'),
    [dash.dependencies.Input('dois_graphs', 'value')])             

def some_o_grafico_para_aparecer_os_outros(valor):
    if valor == 'sim':
        return {'display': 'none'}
    if valor == 'nao':
        return {'display': 'block'} 
    else:
        return {'display': 'none'}

@app.callback(
    dash.dependencies.Output('grafico-tres', 'style'),
    [dash.dependencies.Input('dois_graphs', 'value')])             

def aparece_o_grafico_da_direita(valor):
    if valor == 'sim':
        return {'display': 'block'}
    if valor == 'nao':
        return {'display': 'none'} 
    else:
        return {'display': 'none'}


@app.callback(
    dash.dependencies.Output('grafico-dois', 'style'),
    [dash.dependencies.Input('dois_graphs', 'value')])             

def aparece_o_grafico_da_esquerda(valor):
    if valor == 'sim':
        return {'display': 'block'}
    if valor == 'nao':
        return {'display': 'none'} 
    else:
        return {'display': 'none'}



@app.callback(
    dash.dependencies.Output('configa_graph', 'style'),
    [dash.dependencies.Input('dois_graphs', 'value')])             

def aparece_caixinha_do_grafico_que_deseja_configurar_quando_clica_em_sim(toggle_value):
    if toggle_value == 'sim':
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    dash.dependencies.Output('dropdowns', 'style'),
    [dash.dependencies.Input('escolher', 'value')])             

def aparece_ou_some_as_caixinhas(toggle_value):
    if toggle_value == 'none':
        return {'display': 'none'}
    else:
        return {'display': 'block'}



# comecando daqui eh apenas configurando as caixinhas de sugestao

@app.callback(
    Output(component_id='nome', component_property='value'),

    [Input('submit-button', 'n_clicks'),
            ],
    state=[State(component_id='sugestao', component_property='value'),
    State(component_id='email', component_property='value')])

def update(am, sugestao, email):
    if(am):
        if (sugestao and email):
            return ''
    return valor


@app.callback(
    Output(component_id='email', component_property='value'),

    [Input('submit-button', 'n_clicks'),
            ],
    state=[State(component_id='sugestao', component_property='value'),
    State(component_id='email', component_property='value')])

def update(am, sugestao, email):
    if(am):
        if (sugestao and email):
            return ''
    return valor



@app.callback(
    Output(component_id='sugestao', component_property='value'),
    [Input('submit-button', 'n_clicks')],
    state=[State(component_id='sugestao', component_property='value'),                       
    State(component_id='email', component_property='value')])

def update(ama,sugestao, email):
    if(ama):
        if (sugestao and email):
            return ''
    
    return valor

#termina aqui as sugestoes


#aqui eh a configuracao para mostrar os alertas, esta em adamento ainda

@app.callback(Output(component_id='alerta_vermelho', component_property='is_open'),
                    [Input('submit-button', 'n_clicks'),
                  

                    ],
                        state=[State(component_id='sugestao', component_property='value'),
                State(component_id='email', component_property='value')]
                    )


def retornando_falso(n_clicks,sugestao,email):
    if n_clicks:
        if (sugestao and email):

            return False

        if n_clicks: 

            return True

#termina aqui

#Aqui é o commit da sugestao no banco de dados

@app.callback(
    Output(component_id='alerta_verde', component_property='is_open'),    
    [Input('submit-button', 'n_clicks'),],
    state=[State(component_id='sugestao', component_property='value'),
    State(component_id='email', component_property='value'),
    State(component_id='nome', component_property='value')])


def update_output_div(n_clicks, input_value, emailzin,nome):

    if(input_value and emailzin):
        mycursor.execute('''
                INSERT INTO sugestoes (nome, email, sugestao,dia,mes,ano)
                VALUES
                (%s,%s,%s,%s,%s,%s)
                ''',(nome,emailzin, input_value,now.day,now.month,now.year))
        mydb.commit()
        return True



def forma_classes_qt_integ(x):
    if x==None:
        return None
    else: 
        if x>=0.0 and x <500.0:
            return '(0 - 500)'
        if x>=500.0 and x <1000.0:
            return '(500 - 1000)'
        if x>=1000.0 and x <2500.0:
            return '(1000 - 2500)' 
        if x>=2500.0 and x <3000.0:
            return '(2500 - 3000)'
        if x>=3000.0:
            return '(3000>)'

def forma_classes_idade(x):
    if x==None:
        return None
    else: 
        if x>=15 and x <21:
            return '(15-21)'
        if x>=21 and x <25:
            return '(21-25)'
        if x>=25 and x <35:
            return '(25-35)'
        if x>=35:
            return '(35>)'




def cria_sql(pergunta,variavel,mycursor,mudar):



    if pergunta == 'Por sexo':
        return  '''SELECT C.TP_SEXO, P.sk_ies
                        FROM dim_aluno AS C 
                        JOIN ''' + dict_radio[mudar] + ''' AS P ON C.sk_aluno = P.sk_aluno
                        WHERE P.CENSO in %s '''
                            
    if pergunta == 'Por raca':

        return  '''SELECT C.TP_COR_RACA, P.sk_ies
                                FROM dim_aluno AS C 
                                JOIN ''' + dict_radio[mudar] + ''' AS P ON C.sk_aluno = P.sk_aluno
                                WHERE P.CENSO in %s
                                    '''
    if pergunta == 'Quantidade integralizada':
        return '''SELECT P.qt_carga_horaria_integ, P.sk_ies
                                FROM ''' + dict_radio[mudar] + ''' as P
                                WHERE P.Censo in %s'''
                        
    if pergunta == 'Por deficiencia':
        return  '''SELECT C.TP_DEFICIENCIA, P.sk_ies
                                FROM dim_aluno AS C 
                                JOIN ''' +  dict_radio[mudar] + ''' AS P ON C.sk_aluno = P.sk_aluno   
                                WHERE P.CENSO in %s
                                    '''
    if pergunta == 'Por idade':  
        return  '''SELECT P.sk_ies, (2017 - C.nu_ano_nascimento) as idade 
            FROM  dim_aluno AS C 
            JOIN ''' + dict_radio[mudar] + ''' AS P ON C.sk_aluno = P.sk_aluno
             WHERE P.CENSO in %s''' 

    if pergunta == 'Por quantidade':  
        return  '''SELECT sk_ies,censo
            FROM  ''' + dict_radio[mudar] + '''
             WHERE CENSO in %s''' 

    if pergunta == 'Atividade Extracurricular':  
        return  '''SELECT sk_ies,in_atividade_extracurricular
            FROM  ''' + dict_radio[mudar] + '''
             WHERE CENSO in %s''' 
    if pergunta == 'Vagas Reservadas':  
        return  '''SELECT sk_ies,in_reserva_vagas
            FROM  ''' + dict_radio[mudar] + '''
             WHERE CENSO in %s'''          

    if pergunta == 'Para outra Ies':  
        return  '''SELECT sk_ies,censo,sk_aluno,dt_ingresso_curso
            FROM  ''' + dict_radio[mudar] + '''
             WHERE CENSO in %s''' 


def cria_sql_para_ingressantes(pergunta,variavel,mycursor,mudar):
    return  '''SELECT sk_ies,censo,sk_aluno,dt_ingresso_curso
             FROM  fato_ingresso
             WHERE sk_aluno in %s'''  

    

def tipo_graph(variavel,pergunta,no_ies,tipo,buttons,mudar):  


    #if variavel == 'Todos':
    #    variavel=(2013,2014,2015,2016,2017)    
    #else:
    #    variavel=(variavel,0)
    variavel=[dict_ano[x] for x in variavel] 
    


    variavel=tuple(variavel)


    variavel= [a+1 for a in range(variavel[0] - 1,variavel[1])]
    variavel=tuple(variavel)
    fig=go.Figure()

    if variavel == () or pergunta not in dict_mudar_list[mudar]:
        return fig

    mycursor=mydb.cursor()

    sql=cria_sql(pergunta, variavel,mycursor,mudar)


    mycursor.execute(sql,(variavel,))

    myresult= mycursor.fetchall()
    colnames = [desc[0] for desc in mycursor.description]
        
    df = pd.DataFrame(data=myresult, columns=colnames )






        

    #print(df["qt_carga_horaria_integ"],flush=True)
    if(pergunta=='Quantidade integralizada'):
       df['qt_carga_horaria_integ']=df["qt_carga_horaria_integ"].apply(lambda x: forma_classes_qt_integ(x))

    if(pergunta=='Por idade'):
       df['idade']=df["idade"].apply(lambda x: forma_classes_idade(x))    
        #print(df['qt_carga_horaria_integ'],flush=True)

    dicionario=dict_dicionario[pergunta]
    
   # print('oi',flush=True)


    if(tipo=='Pizza'):
        xa =[dict_no[ies] for ies in no_ies]
        #if(no_ies == 'Todos'):
        #    x=[dict_no[x] for x in ['FPB','NASSAU JP', 'NASSAU CG', 'IFPB', 'UFCG', 'UFPB']]
        #    flag=df.isin({'sk_ies' : x})
        #    b=df[(flag.sk_ies)]
        #else:    
            #x = dict_no[no_ies]
            #a=df['sk_ies']==x
            #b=df[a]
        flag=df.isin({'sk_ies' : xa})
        b=df[(flag.sk_ies)]
        if(pergunta == 'Para outra Ies'):
            dict_aluno = {sk_aluno:data_ingresso for sk_aluno, data_ingresso in zip(list(b['sk_aluno']),list(b['dt_ingresso_curso']))}  
            dict_ies_flag = {sk_aluno:no_ies for sk_aluno, no_ies in zip(list(b['sk_aluno']),list(b['sk_ies']))}
            alunos=tuple(b.sk_aluno)
            dt_ingresso=tuple(b.dt_ingresso_curso)
            sql=cria_sql_para_ingressantes(pergunta, variavel,mycursor,mudar) 
            mycursor.execute(sql,(alunos,))
            myresult= mycursor.fetchall()
            colnames = [desc[0] for desc in mycursor.description]
            df = pd.DataFrame(data=myresult, columns=colnames )



            for index, row in df.iterrows():
                flag=row['sk_aluno']
                data_aluno = row['dt_ingresso_curso']
                data_aluno_2 = dict_aluno[flag]
                if row['sk_ies'] == dict_ies_flag[flag]:
                    if data_aluno.year <= data_aluno_2.year:
                        df.drop(index,inplace=True)
                else:
                    if data_aluno <= data_aluno_2: 
                        df.drop(index,inplace=True)


            #for index, row in df.iterrows():
            #    a=row['sk_aluno']
            #    if row['dt_ingresso_curso'] <= dict_aluno[a] :
            #        df.drop(index,inplace=True)

            b=df           
        #xa =[dict_no[ies] for ies in no_ies] 
        #flag=temp.isin({'CO_UF_CURSO' : CO_UF, 'NO_CURSO' : NO_CURSO })
        #temp=temp[(flag.CO_UF_CURSO) & (flag.NO_CURSO)]

        #a=df['sk_ies']==x
        #b=df[a]



        classes_mais_votadas = b[dict_coluna[pergunta]].value_counts()
        fig.add_trace((go.Pie(labels = [dicionario[x] for x in classes_mais_votadas.index],  

        values = classes_mais_votadas.values,       
        marker = {

                'line' : {'color':'#000000','width':2}
                                 },

                hoverinfo='label+percent+value',
                direction='clockwise'
                )))

        fig.update_layout(title={'text': 'Gráfico de ' + '<b>' + dict_mudar[mudar] + '</b>' + ' para análise por ' + dict_eixo_x[pergunta].lower(),
                                'xanchor': 'center',
                                'x': 0.5}
                            )

        fig.layout.update(
        updatemenus=[
        go.layout.Updatemenu(
        active=1,
        buttons=list(buttons),)])

    if (tipo.count("Barra")):

        xa =[dict_no[ies] for ies in no_ies] 
        for x in xa:
            a=df['sk_ies']==x
            b=df[a]
            if(pergunta == 'Para outra Ies'):
                dict_aluno = {sk_aluno:data_ingresso for sk_aluno, data_ingresso in zip(list(b['sk_aluno']),list(b['dt_ingresso_curso']))}
                dict_ies_flag = {sk_aluno:no_ies for sk_aluno, no_ies in zip(list(b['sk_aluno']),list(b['sk_ies']))}
                alunos=tuple(b.sk_aluno)
                dt_ingresso=tuple(b.dt_ingresso_curso)  
                sql=cria_sql_para_ingressantes(pergunta, variavel,mycursor,mudar) 
                mycursor.execute(sql,(alunos,))
                myresult= mycursor.fetchall()
                colnames = [desc[0] for desc in mycursor.description]
                df = pd.DataFrame(data=myresult, columns=colnames )

                for index, row in df.iterrows():
                    flag=row['sk_aluno']
                    data_aluno = row['dt_ingresso_curso']
                    data_aluno_2 = dict_aluno[flag]
                    if row['sk_ies'] == dict_ies_flag[flag]:
                        if data_aluno.year <= data_aluno_2.year:
                            df.drop(index,inplace=True)  
                    else:   
                        if data_aluno <= data_aluno_2: 
                            df.drop(index,inplace=True)
                

                #for index, row in df.iterrows():
                #    a=row['sk_aluno']  
                #    if row['dt_ingresso_curso'] <= dict_aluno[a] :
                #        df.drop(index,inplace=True)
                b=df 
            #xa =[dict_no[ies] for ies in no_ies] 
            flagzao=b[dict_coluna[pergunta]]
            #print([dicionario[x] for x in flagzao],flush=True)
            fig.add_trace((go.Histogram(
            hoverinfo='y',
            x=[dicionario[x] for x in flagzao],
            name = dict_ies[x],
            visible=True,

            opacity = 0.8)))
        #fig.layout.update(
        #updatemenus=[
        #go.layout.Updatemenu(
        #active=1,
        #buttons=list(buttons),)])
        fig.update_layout(title={'text': 'Gráfico de ' + '<b>' + dict_mudar[mudar] + '</b>' + ' para análise por ' + dict_eixo_x[pergunta].lower(),
                                'xanchor': 'center',
                                'x': 0.5} ,
        xaxis={'title': dict_eixo_x[pergunta],
        'categoryarray':dict_order_axis_x[pergunta],
        'type' : "category"},
        yaxis={'title': dict_eixo_y[pergunta] + dict_mudar[mudar] },)

        if tipo == 'Barra - Stacked':
            fig.update_layout(barmode='stack')
        
        fig.update_layout(

        bargap=0.2, 
        bargroupgap=0.1 
        )


    return go.Figure(fig)
        




@app.callback(Output('feature-graphic', 'figure'),  
    [Input('variavel', 'value'),
     Input('tipo','value'),
     Input('ies', 'value'),
     Input('pi_ou_bar', 'value'),
     Input(component_id='escolher', component_property='value'),
    Input('dois_graphs', 'value')
     ],
    #state=[State(component_id='escolher', component_property='value'),  
     #],
     )



def update_graph(variavel,tipo,ies,forma, mudar,dois_graf):
    fake = Factory.create()
    fig=go.Figure()
    trace=[]                  
    buttons=[]
    if(dois_graf=='nao'):
        if(mudar):
            if(tipo):
                return tipo_graph(variavel,tipo,ies,forma,buttons,mudar)
            else:
                return fig
    else:
        return fig

    #return testando(variavel,tipo,ies,forma)



    #return go.Figure(fig)


@app.callback(Output('grafico-dois', 'figure'),  
    [Input('variavel', 'value'),
     Input('tipo','value'),
     Input('ies', 'value'),
     Input('pi_ou_bar', 'value'),
     Input(component_id='escolher', component_property='value'),
    Input('dois_graphs', 'value'),
    Input('config_graph', 'value')
     ],
    #state=[State(component_id='escolher', component_property='value'),  
     #],
     )



def grafico_um(variavel,tipo,ies,forma, mudar,dois_graf,config_graf):
    fake = Factory.create()
    fig=go.Figure()
    trace=[]                  
    buttons=[]
    if(dois_graf == 'sim'):
        if(config_graf=='g1'):
            if(mudar):
                if(tipo):
                    return tipo_graph(variavel,tipo,ies,forma,buttons,mudar)  

                else:
                    return  fig
            else:
                return fig
        else:
            return valor              
    else:
       return fig




@app.callback(Output('grafico-tres', 'figure'),  
    [Input('variavel', 'value'),
     Input('tipo','value'),
    Input('ies', 'value'),
     Input('pi_ou_bar', 'value'),
     Input(component_id='escolher', component_property='value'),
    Input('dois_graphs', 'value'),
    Input('config_graph', 'value')
     ],
    #state=[State(component_id='escolher', component_property='value'),  
     #],
     )



def grafico_dois(variavel,tipo,ies,forma, mudar,dois_graf,config_graf):
    fake = Factory.create()
    fig=go.Figure()
    trace=[]                  
    buttons=[]
    if(dois_graf == 'sim'):
        if(config_graf=='g2'):
            if(mudar):
                if(tipo):
                    return tipo_graph(variavel,tipo,ies,forma,buttons,mudar)

                else:
                    return  fig
            else:
                return fig
        else:
            return valor              
    else:
       return fig


@app.callback( 
    dash.dependencies.Output('testando', 'style'),
    [dash.dependencies.Input('check', 'value')])             

def Muda_os_parametros_da_caixinha_da_pergunta(check):
    #print(check,flush=True)
    #if radio=='evd':
    #if 'ativado' in check:
    if 'ativado' in check:
        return {'left':'0'}
    else:
        return {'left':'-350px'}


@app.callback( 
    dash.dependencies.Output('check', 'value'),
    [dash.dependencies.Input('menu_lateral', 'n_clicks')],
    [dash.dependencies.State('check', 'value')]  )             

def clica_ou_nao_check(click,a):
    #print(check,flush=True)
    #if radio=='evd':
    #if 'ativado' in check:
    if click:
        if 'ativado' in a:
            return ['']
        else:
            return ['ativado'] 

    return ['']  

if(__name__ == '__main__'):
    app.run_server(debug=True,port=8093) 


