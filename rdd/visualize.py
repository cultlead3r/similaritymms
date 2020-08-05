import pandas as pd
import plotly.graph_objects as go
import networkx as nx
from rdd.Node import Node
from rdd import measures
from rdd import other_sims
from rdd import ascos
from rdd import cos_sim


def visualize_rdd(g1, u, v, pos, m=measures.global_graph_degree):
    """takes a graph and plots it, coloring vertices by RDD

    Args:
    -----
        g1: a networkx graph
        u: source node
        v: target radius
        m: a measure function from measures

    Returns:
    --------
        fig: a figure object of a scatter plot"""
    # TODO: why is the argument for radius 'v'?
    df = measures.get_rdds_for_visuals(g1, u, m, v)
    # pos = spring_layout(g1)
    # pos = nx.spring_layout(g1, scale=5)
    nodes_x = []
    nodes_y = []

    for p in pos.values():
        x, y = p[0], p[1]
        nodes_x.append(x)
        nodes_y.append(y)

    df['nodes_x'] = nodes_x
    df['nodes_y'] = nodes_y

    edges_x = []
    edges_y = []
    for e in g1.edges():
        x0, y0 = pos[e[0]]
        x1, y1 = pos[e[1]]
        edges_x.append(x0)
        edges_x.append(x1)
        # why do these need to be here?
        edges_x.append(None)
        edges_y.append(y0)
        edges_y.append(y1)
        # why do these need to be here?
        edges_y.append(None)

        # fig = px.scatter(df, x='nodes_x', y='nodes_y', text='node_name', custom_data=['rdd'], color='rdd')
    # fig.update_traces(hovertemplate='Node: %{text}, RDD: %{customdata[0]}')
    # fig.update_layout(font_size=20)
    # fig.update_traces(marker={'size': 20})
    # fig.add_trace(go.Scatter(x=edges_x, y=edges_y, mode='lines', line={'width': 3}))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=edges_x, y=edges_y, name='edges', mode='lines', line={'width': 1}))
    fig.add_trace(go.Scatter(x=df['nodes_x'],
                             y=df['nodes_y'],
                             customdata=df[['rdd', 'degree']].values,
                             hovertemplate="Node: %{text} <br> RDD: %{customdata[0]} <br> Degree: %{customdata[1]} <extra></extra>",
                             text=df['node_name'],
                             name="nodes",
                             mode='markers+text'))
    fig.update_layout(template="plotly_dark", dragmode='pan')
    fig.update_traces(marker={'size': 10, 'color': df['rdd'], 'colorscale': 'Jet'})
    fig.write_html("graph.html", config={'scrollZoom': True})

    return fig.show(config={'scrollZoom': True})


def visualize_rdd_vector(g1, u, r, pos, measure_vector):
    df = measures.get_rdds_for_visuals_vector(g1, u, measure_vector, r)
    # pos = nx.spring_layout(g1)
    nodes_x = []
    nodes_y = []

    for p in pos.values():
        x, y = p[0], p[1]
        nodes_x.append(x)
        nodes_y.append(y)

    df['nodes_x'] = nodes_x
    df['nodes_y'] = nodes_y

    edges_x = []
    edges_y = []
    for e in g1.edges():
        x0, y0 = pos[e[0]]
        x1, y1 = pos[e[1]]
        edges_x.append(x0)
        edges_x.append(x1)
        # why do these need to be here?
        edges_x.append(None)
        edges_y.append(y0)
        edges_y.append(y1)
        # why do these need to be here?
        edges_y.append(None)

    # get the custom_data and build the hover template from the DataFrame column names
    custom_data = df.columns
    hover_template = ""
    for i, m in enumerate(custom_data):
        hover_template += "".join(m + ":" + ' %{customdata[' + str(i) + ']} <br> ')

    fig = go.FigureWidget()
    fig.add_trace(go.Scatter(x=edges_x, y=edges_y, name='edges', mode='lines', line={'width': 1}))
    fig.add_trace(go.Scatter(x=df['nodes_x'],
                             y=df['nodes_y'],
                             customdata=df[custom_data],
                             hovertemplate=hover_template,
                             text=df['node_name'],
                             name="Node",
                             mode='markers+text'))
    fig.update_layout(template="plotly_dark", dragmode='pan', )
    fig.update_traces(marker={'size': 15, 'color': df['normalized_rdd'], 'colorscale': 'Jet'})
    fig.write_html("graph.html", config={'scrollZoom': True})
    return fig


def draw(g1):
    """Draws a NetworkX Graph with Plotly."""
    pos = nx.spring_layout(g1)
    nodes_x = []
    nodes_y = []

    for p in pos.values():
        x, y = p[0], p[1]
        nodes_x.append(x)
        nodes_y.append(y)

    edges_x = []
    edges_y = []
    for e in g1.edges():
        x0, y0 = pos[e[0]]
        x1, y1 = pos[e[1]]
        edges_x.append(x0)
        edges_x.append(x1)
        # why do these need to be here?
        edges_x.append(None)
        edges_y.append(y0)
        edges_y.append(y1)
        # why do these need to be here?
        edges_y.append(None)

    fig = go.FigureWidget()
    fig.add_trace(go.Scatter(x=edges_x, y=edges_y, name='edges', mode='lines', line={'width': 1}))
    fig.add_trace(go.Scatter(x=nodes_x,
                             y=nodes_y,
                             text=list(g1.nodes),
                             name='Node',
                             mode='markers+text'))
    fig.update_layout(template="plotly_dark", dragmode='pan', )
    fig.update_traces(marker={'size': 15, 'colorscale': 'Jet'})
    fig.write_html("graph.html", config={'scrollZoom': True})
    return fig


def add_markers(figure, nodes):
    annotations = [{'x': figure.data[1]['x'][n - 1],
                    'y': figure.data[1]['y'][n - 1],
                    'axref': 'x',
                    'ayref': 'y',
                    'arrowsize': 2,
                    'arrowcolor': 'red',
                    'showarrow': True,
                    'arrowhead': 3} for n in nodes]
    figure.update_layout(annotations=annotations)
    return figure


def visualize_simrank(g1, u, pos):
    """takes a graph and plots it, coloring vertices by RDD

    Args:
    -----
        g1: a networkx graph
        u: source node
        v: target radius
        m: a measure function from measures

    Returns:
    --------
        fig: a figure object of a scatter plot"""

    df = other_sims.simrank(g1, u)
    # pos = nx.spring_layout(g1)
    nodes_x = []
    nodes_y = []

    for p in pos.values():
        x, y = p[0], p[1]
        nodes_x.append(x)
        nodes_y.append(y)

    df['nodes_x'] = nodes_x
    df['nodes_y'] = nodes_y

    edges_x = []
    edges_y = []
    for e in g1.edges():
        x0, y0 = pos[e[0]]
        x1, y1 = pos[e[1]]
        edges_x.append(x0)
        edges_x.append(x1)
        # why do these need to be here?
        edges_x.append(None)
        edges_y.append(y0)
        edges_y.append(y1)
        # why do these need to be here?
        edges_y.append(None)

    # fig = px.scatter(df, x='nodes_x', y='nodes_y', text='node_name', custom_data=['rdd'], color='rdd')
    # fig.update_traces(hovertemplate='Node: %{text}, RDD: %{customdata[0]}')
    # fig.update_layout(font_size=20)
    # fig.update_traces(marker={'size': 20})
    # fig.add_trace(go.Scatter(x=edges_x, y=edges_y, mode='lines', line={'width': 3}))

    fig = go.FigureWidget()
    fig.add_trace(go.Scatter(x=edges_x, y=edges_y, name='edges', mode='lines', line={'width': 1}))
    fig.add_trace(go.Scatter(x=df['nodes_x'],
                             y=df['nodes_y'],
                             customdata=df[['simrank', 'degree']].values,
                             hovertemplate="Node: %{text} <br> SimRank: %{customdata[0]} <br> Degree: %{customdata[1]} <extra></extra>",
                             text=df['node_name'],
                             name="nodes",
                             mode='markers+text'))
    fig.update_layout(template="plotly_dark", dragmode='pan')
    fig.update_traces(marker={'size': 15, 'color': df['simrank'], 'colorscale': 'Jet'})
    fig.write_html("graph.html", config={'scrollZoom': True})

    # return fig.show(config={'scrollZoom':True})
    return fig


def visualize_ascos(g1, u, pos):
    """takes a graph and plots it, coloring vertices by RDD

    Args:
    -----
        g1: a networkx graph
        u: source node
        v: target radius
        m: a measure function from measures

    Returns:
    --------
        fig: a figure object of a scatter plot"""

    df = ascos.get_ascos(g1, u)
    # pos = nx.spring_layout(g1)
    nodes_x = []
    nodes_y = []

    for p in pos.values():
        x, y = p[0], p[1]
        nodes_x.append(x)
        nodes_y.append(y)

    df['nodes_x'] = nodes_x
    df['nodes_y'] = nodes_y

    edges_x = []
    edges_y = []
    for e in g1.edges():
        x0, y0 = pos[e[0]]
        x1, y1 = pos[e[1]]
        edges_x.append(x0)
        edges_x.append(x1)
        # why do these need to be here?
        edges_x.append(None)
        edges_y.append(y0)
        edges_y.append(y1)
        # why do these need to be here?
        edges_y.append(None)

    # fig = px.scatter(df, x='nodes_x', y='nodes_y', text='node_name', custom_data=['rdd'], color='rdd')
    # fig.update_traces(hovertemplate='Node: %{text}, RDD: %{customdata[0]}')
    # fig.update_layout(font_size=20)
    # fig.update_traces(marker={'size': 20})
    # fig.add_trace(go.Scatter(x=edges_x, y=edges_y, mode='lines', line={'width': 3}))

    fig = go.FigureWidget()
    fig.add_trace(go.Scatter(x=edges_x, y=edges_y, name='edges', mode='lines', line={'width': 1}))
    fig.add_trace(go.Scatter(x=df['nodes_x'],
                             y=df['nodes_y'],
                             customdata=df[['ascos', 'degree']].values,
                             hovertemplate="Node: %{text} <br> Ascos: %{customdata[0]} <br> Degree: %{customdata[1]} <extra></extra>",
                             text=df['node_name'],
                             name="nodes",
                             mode='markers+text'))
    fig.update_layout(template="plotly_dark", dragmode='pan')
    fig.update_traces(marker={'size': 15, 'color': df['ascos'], 'colorscale': 'Jet'})
    fig.write_html("graph.html", config={'scrollZoom': True})

    # return fig.show(config={'scrollZoom':True})
    return fig


def visualize_cosine_similarity(g1, u):
    """takes a graph and plots it, coloring vertices by RDD

    Args:
    -----
        g1: a networkx graph
        u: source node
        v: target radius
        m: a measure function from measures

    Returns:
    --------
        fig: a figure object of a scatter plot"""

    df = cos_sim.get_cosine(g1, u)
    pos = spring_layout(g1)
    nodes_x = []
    nodes_y = []

    for p in pos.values():
        x, y = p[0], p[1]
        nodes_x.append(x)
        nodes_y.append(y)

    df['nodes_x'] = nodes_x
    df['nodes_y'] = nodes_y

    edges_x = []
    edges_y = []
    for e in g1.edges():
        x0, y0 = pos[e[0]]
        x1, y1 = pos[e[1]]
        edges_x.append(x0)
        edges_x.append(x1)
        # why do these need to be here?
        edges_x.append(None)
        edges_y.append(y0)
        edges_y.append(y1)
        # why do these need to be here?
        edges_y.append(None)

    # fig = px.scatter(df, x='nodes_x', y='nodes_y', text='node_name', custom_data=['rdd'], color='rdd')
    # fig.update_traces(hovertemplate='Node: %{text}, RDD: %{customdata[0]}')
    # fig.update_layout(font_size=20)
    # fig.update_traces(marker={'size': 20})
    # fig.add_trace(go.Scatter(x=edges_x, y=edges_y, mode='lines', line={'width': 3}))

    fig = go.FigureWidget()
    fig.add_trace(go.Scatter(x=edges_x, y=edges_y, name='edges', mode='lines', line={'width': 1}))
    fig.add_trace(go.Scatter(x=df['nodes_x'],
                             y=df['nodes_y'],
                             customdata=df[['cos_sim', 'degree']].values,
                             hovertemplate="Node: %{text} <br> CosSim: %{customdata[0]} <br> Degree: %{customdata[1]} <extra></extra>",
                             text=df['node_name'],
                             name="nodes",
                             mode='markers+text'))
    fig.update_layout(template="plotly_dark", dragmode='pan')
    fig.update_traces(marker={'size': 10, 'color': df['cos_sim'], 'colorscale': 'Jet'})
    fig.write_html("graph.html", config={'scrollZoom': True})

    # return fig.show(config={'scrollZoom':True})
    return fig


def visualize_rdd_vector_kmeans(g1, u, r, measure_vector, k=3):
    df = measures.get_rdds_for_visuals_vector(g1, u, measure_vector, r)
    df = other_sims.k_means(df, measure_vector, k)
    pos = nx.spring_layout(g1)
    nodes_x = []
    nodes_y = []

    for p in pos.values():
        x, y = p[0], p[1]
        nodes_x.append(x)
        nodes_y.append(y)

    df['nodes_x'] = nodes_x
    df['nodes_y'] = nodes_y

    edges_x = []
    edges_y = []
    for e in g1.edges():
        x0, y0 = pos[e[0]]
        x1, y1 = pos[e[1]]
        edges_x.append(x0)
        edges_x.append(x1)
        # why do these need to be here?
        edges_x.append(None)
        edges_y.append(y0)
        edges_y.append(y1)
        # why do these need to be here?
        edges_y.append(None)

    # get the custom_data and build the hover template from the DataFrame column names
    custom_data = df.columns
    hover_template = ""
    for i, m in enumerate(custom_data):
        hover_template += "".join(m + ":" + ' %{customdata[' + str(i) + ']} <br> ')

    fig = go.FigureWidget()
    fig.add_trace(go.Scatter(x=edges_x, y=edges_y, name='edges', mode='lines', line={'width': 1}))
    fig.add_trace(go.Scatter(x=df['nodes_x'],
                             y=df['nodes_y'],
                             customdata=df[custom_data],
                             hovertemplate=hover_template,
                             text=df['node_name'],
                             name="Node",
                             mode='markers+text'))
    fig.update_layout(template="plotly_dark", dragmode='pan',
                      annotations=[{'x': df.iloc[0]['nodes_x'],
                                    'y': df.iloc[0]['nodes_y'],
                                    'axref': 'x',
                                    'ayref': 'y',
                                    'arrowsize': 4,
                                    'arrowcolor': 'red',
                                    'showarrow': True,
                                    'arrowhead': 3}])
    fig.update_traces(
        marker={'size': ((df['k_mean_cluster'] * 5) + 10), 'color': df['normalized_rdd'], 'colorscale': 'Jet'})
    fig.write_html("graph.html", config={'scrollZoom': True})

    return fig
