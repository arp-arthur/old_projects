import dash
import dash_core_components as dcc
import dash_html_components as html
import networkx as nx
import plotly.graph_objs as go
import pandas as pd
from colour import Color
from datetime import datetime
from textwrap import dedent as d
import json

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'NeuroRedes - Grafo Experimental'

ANO = [2012, 2022]
CONTA = 'A0001'

def network_neuroredes(ano_range, conta):
    edge1 = pd.read_csv('edge1.csv')
    node1 = pd.read_csv('node1.csv')
    edge1['Datetime'] = ''
    conta_set = set()
    for index in range(0, len(edge1)):
        edge1['Datetime'][index] = datetime.strptime(edge1['Date'][index], '%d/%m/%Y')
        if edge1['Datetime'][index].year < ano_range[0] or edge1['Datetime'][index].year > ano_range[1]:
            edge1.drop(axis=0, index=index, inplace=True)
            continue

        conta_set.add(edge1['Source'][index])
        conta_set.add(edge1['Target'][index])


    shells = []
    shell1 = []
    shell1.append(conta)
    shells.append(shell1)
    shell2 = []

    for ele in conta_set:
        if ele != conta:
            shell2.append(ele)

    shells.append(shell2)

    # construindo a rede usando a biblioteca Networkx
    network = nx.fro.m_pandas_edgelist(edge1, 'Source', 'Target', ['Source', 'Target', 'TransactionAmt', 'Date'], create_using=nx.MultiDiGraph())
    nx.set_node_attributes(network, node1.set_index('Account')['CustomerName'].to_dict(), 'CustomerName')
    nx.set_node_attributes(network, node1.set_index('Account')['Type'].to_dict(), 'Type')

    if len(shell2) > 1:
        posicao = nx.drawing.layout.shell_layout(network, shells)
    else:
        posicao = nx.drawing.layout.spring_layout(network)

    for node in network.nodes:
        network.nodes[node]['posicao'] = list(posicao[node])

    if len(shell2) == 0:
        trace_route = []

        node_trace = go.Scatter(x=tuple([1]), y=tuple([1]),
                                mode='markers',
                                marker={'size': 50, 'color': 'LightSkyBlue'},
                                opacity=0)

        trace_route.append(node_trace)

        figure = {
            'data': trace_route,
            'layout': go.Layout(title='Interactive Transaction Visualization', showlegend=False,
                                margin={'b': 40, 'l': 40, 'r': 40, 't': 40},
                                xaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
                                height=600)
        }

        return figure

    trace_recode = []

    colors = list(Color('lightcoral').range_to(Color('darkred'), len(network.edges())))

    colors = ['rgb' + str(x.rgb) for x in colors]

    index = 0

    for edge in network.edges:
        x0, y0 = network.nodes[edge[0]]['posicao']
        x1, y1 = network.nodes[edge[1]]['posicao']

        peso = float(network.edges[edge]['TransactionAmt']) / max(edge1['TransactionAmt']) * 10
        trace = go.Scatter(x=tuple([x0, x1, None]), y=tuple([y0, y1, None]),
                           mode='lines',
                           line={'width': peso},
                           marker=dict(color=colors[index]),
                           opacity=1)
        trace_recode.append(trace)
        index = index + 1

    node_trace = go.Scatter(x=[],
                            y=[],
                            hovertext=[],
                            text=[],
                            mode='markers+text',
                            textposition='bottom center',
                            hoverinfo='text',
                            marker={'size': 50, 'color': 'LightSkyBlue'})

    index = 0

    for node in network.nodes():
        x, y = network.nodes[node]['posicao']
        hover_text = 'CustomerName: ' + str(network.nodes[node]['CustomerName']) + '<br>' + 'AccountType: ' + str(
            network.nodes[node]['Type']
        )
        text = node1['Account'][index]
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])
        node_trace['hovertext'] += tuple([hover_text])
        node_trace['text'] += tuple([text])

        index = index + 1

    trace_recode.append(node_trace)

    middle_hover_trace = go.Scatter(x=[],
                                    y=[],
                                    hovertext=[],
                                    mode='markers',
                                    hoverinfo='text',
                                    marker={'size': 20, 'color': 'LightSkyBlue'},
                                    opacity=0)

    index = 0

    for edge in network.edges:
        x0, y0 = network.nodes[edge[0]]['posicao']
        x1, y1 = network.nodes[edge[1]]['posicao']
        hover_text = 'From: ' + str(network.edges[edge]['Source']) + '<br>' + 'To: ' + str(
            network.edges[edge]['Target']) + '<br>' + 'TransactionDate: ' + str(network.edges[edge]['Date'])

        middle_hover_trace['x'] += tuple([(x0 + x1) / 2])
        middle_hover_trace['y'] += tuple([(y0 + y1) / 2])

        middle_hover_trace['hovertext'] += tuple([hover_text])

        index = index + 1

    trace_recode.append(middle_hover_trace)

    figure = {
        'data': trace_recode,
        'layout': go.Layout(title='Interactive Transaction Visualization', showlegend=False, hovermode='closest',
                            xaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
                            yaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
                            height=600,
                            clickmode='event+select',
                            annotations=[
                                dict(
                                    ax=(network.nodes[edge[0]]['posicao'][0] + network.nodes[edge[1]]['posicao'][0]) / 2,
                                    ay=(network.nodes[edge[0]]['posicao'][1] + network.nodes[edge[1]]['posicao'][1]) / 2, axref='x', ayref='y',
                                    x=(network.nodes[edge[1]]['posicao'][0] * 3 + network.nodes[edge[0]]['posicao'][0]) / 4,
                                    y=(network.nodes[edge[1]]['posicao'][1] * 3 + network.nodes[edge[0]]['posicao'][1]) / 4, xref='x', yref='y',
                                    showarrow=True,
                                    arrowhead=3,
                                    arrowsize=4,
                                    arrowwidth=1,
                                    opacity=1,
                                ) for edge in network.edges]
                            )}

    return figure

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}


@app.callback(
    dash.dependencies.Output('meu-grafo', 'figure'),
    [dash.dependencies.Input('range-slider', 'value'), dash.dependencies.Input('pesquisa-input', 'value')]
)
def update_output(value, pesquisa_input):
    ANO = value
    CONTA = pesquisa_input
    return network_neuroredes(value, pesquisa_input)

@app.callback(
    dash.dependencies.Output('hover-data', 'children'),
    [dash.dependencies.Input('meu-grafo', 'hoverData')]
)
def display_hover_data(hoverData):
    return json.dumps(hoverData, indent=2)

@app.callback(
    dash.dependencies.Output('click-data', 'children'),
    [dash.dependencies.Input('meu-grafo', 'clickData')]
)
def display_click_data(clickData):
    return json.dumps(clickData, indent=2)

app.layout = html.Div([
    html.Div([html.H1('Grafo experimental ONA - NeuroRedes')],
             className='titulo',
             style={'textAlign': 'center'}),

    html.Div(
        className='row',
        children=[
            html.Div(
                className='duas colunas',
                children=[
                    dcc.Markdown(d("""
                        ** Range de tempo para visualização **
                        Deslize a barra para definir o gap de ano
                        """)),
                    html.Div(
                        className='doze colunas',
                        children=[
                            dcc.RangeSlider(
                                id='range-slider',
                                min=2012,
                                max=2022,
                                step=1,
                                value=[2012, 2022],
                                marks={
                                    2012: {'label': '2012'},
                                    2013: {'label': '2013'},
                                    2014: {'label': '2014'},
                                    2015: {'label': '2015'},
                                    2016: {'label': '2016'},
                                    2017: {'label': '2017'},
                                    2018: {'label': '2018'},
                                    2019: {'label': '2019'},
                                    2020: {'label': '2020'},
                                    2021: {'label': '2021'},
                                    2022: {'label': '2022'},
                                }
                            ),
                            html.Br(),
                            html.Div(id='output-container-range-slider')
                        ],
                        style={'height': '300px'}
                    ),
                    html.Div(
                        className='doze colunas',
                        children=[
                            dcc.Markdown(d("""
                                ** Contas para pesquisar **
                                Entre com a conta para visualizar
                                """)),
                            dcc.Input(id='pesquisa-input', placeholder='Conta'),
                            html.Div(id='output')
                        ],
                        style={'height': '300px'}
                    )
                ]
            ),
            html.Div(
                className='oito colunas',
                children=[dcc.Graph(id='meu-grafo', figure=network_neuroredes(ANO, CONTA))],
            ),
            html.Div(
                className='duas colunas',
                children=[
                    html.Div(
                        className='doze colunas',
                        children=[
                            dcc.Markdown(d("""
                                ** Hover Data **
                                Passe o mouse sobre os valores no grafo
                                """)),
                            html.Pre(id='hover-data', style=styles['pre'])
                        ],
                        style={'height': '400px'}),
                    html.Div(
                        className='doze colunas',
                        children=[
                            dcc.Markdown(d("""
                                ** Clicar nos dados **
                                Clique nos pontos do grafo
                                """)),
                            html.Pre(id='click-data', style=styles['pre'])
                        ],
                        style={'height': '400px'}
                    )
                ]
            )
        ]
    )
])


if __name__ == '__main__':
    app.run_server(debug=True)