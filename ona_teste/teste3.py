import plotly.graph_objects as go
import networkx as nx

G = nx.random_geometric_graph(200, .125)

# criar edges

edge_x = []
edge_y = []

for edge in G.edges():
    x0, y0 = G.nodes[edge[0]]['pos']
    x1, y1 = G.nodes[edge[1]]['pos']
    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)

edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=.5, color='#888'),
    hoverinfo='none',
    mode='lines'
)

node_x = []
node_y = []

for node in G.nodes():
    x, y = G.nodes[node]['pos']
    node_x.append(x)
    node_y.append(y)

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        colorscale='YlGnBu',
        reversescale=True,
        color=[],
        size=10,
        colorbar=dict(
            thickness=15,
            title='Conexões',
            xanchor='left',
            titleside='right'
        ),
        line_width=2
    )
)

node_adjacencias = []
node_text = []

for node, adjacencias in enumerate(G.adjacency()):
    node_adjacencias.append(len(adjacencias[1]))
    node_text.append('N. de conexões: ' + str(len(adjacencias[1])))

node_trace.marker.size = node_adjacencias
node_trace.text = node_text

# agora, vamos criar o grafo
figura = go.Figure(data=[edge_trace, node_trace],
                   layout=go.Layout(
                       title='<br>Teste de grafo feito com python',
                       showlegend=False,
                       hovermode='closest',
                       margin=dict(b=20, l=5, r=5, t=40),
                       annotations=[dict(
                           text="Python code: <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>",
                           showarrow=True,
                           xref='paper', yref='paper',
                           x=.005, y=-.002
                       )],
                       xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                       yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                   ))

figura.show()