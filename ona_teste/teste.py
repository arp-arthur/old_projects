import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import dash
import dash_core_components as dcc
import dash_html_components as html
from textwrap import dedent as d
from plotly.tools import mpl_to_plotly

# caminho para o arquivo excel da pesquisa

CAMINHO = './files/Simple_ONA_Survey.xlsx'

## pegando os dataframes

# respostas
pesquisa = pd.read_excel(CAMINHO, sheet_name='Response_Data')

# questionario
questoes = pd.read_excel(CAMINHO, sheet_name='Questionnaire_Items')

# dados hris
hris = pd.read_excel(CAMINHO, sheet_name='HRIS_Data')


external_style_sheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_style_sheets)
app.title = 'Exemplo ONA - NeuroRedes'

def desenha_grafo():
    network_data=pd.wide_to_long(pesquisa, stubnames=['Q1_','Q2_'], #questions we will put into a single column
                                          i='participant_email', #column we pivot on
                                          j='alter_id') #creating a new variable

    # preencher espaços vazios com zero (a ser implementado)
    network_data = network_data.fillna(0)
    # network_data = network_data[~pd.isna(network_data['Q1_'])]
    network_data.reset_index(inplace=True)

    # renomear o participant_email e Q1 para tornar mais claro...
    # renomear o Q2 para refletir a questão associada

    network_data.rename(columns={'participant_email': 'ego',
                                 'Q1_': 'alter',
                                 'Q2_': 'Gostaria de mais acesso'},
                        inplace=True)


    # print(network_data['alter_id'])
    # não precisamos mais dessa coluna
    network_data.drop('alter_id', axis=1)
    # del network_data['alter_id']
    # ordenando participantes
    network_data.sort_values(by='ego', inplace=True)


    # unindo os dataframes

    # primeiro, precisamos copiar o hris data
    ego_hris = hris.copy()

    # agora, nós renomearemos as colunas para combinar com os dados do df network
    ego_hris.rename(columns={'email': 'ego',
                             'Title': 'Titulo Ego',
                             'Department': 'time_ego'},
                    inplace=True)

    # agora, iremos unir o dataframe ego hris e os dados da network df

    network_data = pd.merge(network_data,
                            ego_hris,
                            on='ego',
                            how='left')

    # faremos a mesma coisa para o alter

    alter_hris = hris.copy()
    alter_hris.rename(columns={'email': 'alter',
                               'Title': 'Titulo Alter',
                               'Department': 'time_alter'},
                      inplace=True)

    network_data = pd.merge(network_data,
                            alter_hris,
                            on='alter',
                            how='left')

    # a função crosstab nos permite analisar a relação entre múltiplas variáveis
    cross_team = pd.crosstab(index=network_data['time_ego'],
                             columns=network_data['time_alter'],
                             normalize='index')

    # multiplica por 100 para obter a porcentagem
    cross_team * 100

    # vamos usar o networkx para gerar nosso grafo... estou usando o tipo de grafo DiGraph

    network_graph = nx.from_pandas_edgelist(network_data,
                                            source='ego',
                                            target='alter',
                                            create_using=nx.DiGraph())

    # agora que definimos qual dado e tipo de grafo usaremos com o networkx, vamos usar
    # o matplotlib para fazer alguns ajustes, seguido por nx.draw_networkx() para desenhar o grafo

    plt.figure(figsize=(20,20))  # muda o tamanho padrão do plot
    limits = plt.axis('off')  # nos livramos do cartesiano

    nx.draw_networkx(network_graph,
                         arrows=True,
                         node_color='b')

    trace_recode = []

    


    return mpl_to_plotly(plt.show())

def desenha_grafo2():
    figure = plt.figure()
    ax = figure.add_subplot(111)
    ax.plot(range(10), [i**2 for i in range(10)])
    ax.grid(True)
    return mpl_to_plotly(figure)


app.layout = html.Div([
    html.Div([html.H1('Grafo experimental ONA - NeuroRedes')],
            className='titulo',
            style={'textAlign': 'center'}),
    html.Div(
        className='linha',
        children=[
            dcc.Markdown(d(
                """
                **Buscar grafo**
                """
            )),
            dcc.Input(id='pesquisa-input', placeholder='Grafo'),
            html.Div(id='output')
        ],
        style={'height': '300px', 'textAlign': 'center'}
    ),
    html.Div(
        className='grafo',
        children=[dcc.Graph(id='meu-grafo', figure=desenha_grafo2())],
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)