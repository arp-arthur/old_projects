from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

df = pd.DataFrame({
    'Fruta': ['Maçãs', 'Laranjas', 'Bananas', 'Maçãs', 'Laranjas', 'Bananas'],
    'Quantidade': [4, 1, 2, 2, 4, 5],
    'Cidade': ['SP', 'RJ', 'Tere', 'CWB', 'CWB', 'CWB']
})

fig = px.bar(df, x='Fruta', y='Quantidade', color='Cidade', barmode='group')

app.layout = html.Div(children=[
    html.H1(children='Hello world'),
    html.Div(children='''
        Teste com o dash
        '''),
    dcc.Graph(
        id='exemplo-Grafo',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)