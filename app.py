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

# nw = visualize.visualize_rdd(want_network)

tips=px.data.tips()

px.defaults.template = "plotly_dark"


app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='graph', config={
        'scrollZoom': True
    }),

    html.H3("What should determine graph color?"),
    dcc.Dropdown(id='plot_against',
        options=[{'label': x, 'value': x} for x in tips.columns]),

    html.H3("Choose a marginal graph"),
    dcc.Dropdown(id='dropdown', options=[
        {'label': 'boxplot', 'value': 'box'},
        {'label': 'violin chart', 'value' : 'violin'}]),

    html.H3("Do you want a violin plot on the right?"),  
    dcc.Checklist(id='want_violin', options=[
        {'label': 'violin', 'value': 'box'}]),
    
    html.H3("Do you want to plot a network?"),  
    dcc.Checklist(id='want_network', options=[
        {'label': 'network', 'value': 'want_network'}]),

    dcc.Dropdown(id='network_choice', options=[
        {'label': 'the sample graph', 'value': 'the_g1'}
    ]),

    dcc.Graph(id='network'),

])



@app.callback(
    Output('graph', 'figure'),
    [Input('dropdown', 'value'),
    Input('want_violin', 'value'),
    Input('plot_against', 'value')])
def update_figure(dropdown_selection, the_violin, plot_against):
    the_violin = 'violin' if the_violin else None
    fig = px.scatter(tips, x='total_bill', y='tip',
                 marginal_x=dropdown_selection,
                 marginal_y=the_violin,
                 color=plot_against,
                 size='tip',
                 trendline='ols')
    fig.update_layout(dragmode='pan')
    return fig


@app.callback(
    Output('network', 'figure'),
    [Input('want_network', 'value'),
     Input('network_choice', 'value')])
def update_network(want_network, network_choice):
    choice = None
    print(network_choice)
    if network_choice == 'the_g1':
        choice = g1
    if want_network and choice:
        fig = visualize.visualize_rdd(choice)
        return fig
    else:
        fig = go.Figure()
        fig.update_layout(template='plotly_dark')
        return fig


if __name__ == '__main__':
    app.run_server(debug=True)