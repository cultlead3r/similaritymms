import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

import networkx as nx
import measures
import RDD
import visualize

g1 = nx.Graph()


g1.add_edges_from([
    (1, 2),
    (2, 3),
    (2, 4),
    (3, 4),
    (3, 6),
    (4, 5),
])

app = dash.Dash(__name__)

app.layout = html.Div([
       
    html.H3("What measure do you want to use?"),

    dcc.Dropdown(id='measure_choice', placeholder="Choose measure", options=[
        {'label': 'triangles node is part of', 'value': 'triangles'},
        {'label': 'global degree', 'value': 'global_graph_degree'},
        {'label': 'local degree', 'value': 'local_graph_degree'},
        {'label': 'global clique', 'value': 'global_graph_clique'},
        {'label': 'local clique', 'value': 'local_graph_clique'},
        
    ]),

    dcc.Dropdown(id='network_choice', placeholder="Choose network", options=[
    {'label': 'the sample graph', 'value': 'the_g1'}
    ]),

    dcc.Graph(id='network'),

])


@app.callback(
    Output('network', 'figure'),
    [
     Input('network_choice', 'value'),
     Input('measure_choice', 'value'),
    ])
def update_network(network_choice, measure_choice):
    network = None
    measure = None
    choice = None
    if measure_choice == 'triangles':
        measure=measures.triangles
    elif measure_choice == 'global_graph_degree':
        measure=measures.global_graph_degree
    elif measure_choice == 'local_graph_degree':
        measure=measures.local_graph_degree
    elif measure_choice == 'global_graph_clique':
        measure=measures.global_graph_clique
    elif measure_choice == 'local_graph_clique':
        measure=measures.local_graph_clique

    if network_choice == 'the_g1':
        choice = g1
    if choice and measure:
        fig = visualize.visualize_rdd(choice, measure)
        return fig
    else:
        fig = go.Figure()
        fig.update_layout(template='plotly_dark')
        return fig


if __name__ == '__main__':
    app.run_server(debug=True)