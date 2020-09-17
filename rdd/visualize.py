import plotly.graph_objects as go
import networkx as nx
from rdd import RDD
from rdd import measures
from rdd import other_sims
from rdd import ascos
from rdd import cos_sim


def visualize_rdd(g1, u, r, pos, m=measures.global_graph_degree):
    """takes a graph and plots it, coloring vertices by RDD

    Args:
    -----
        g1: a networkx graph
        u: source node
        m: a measure function from measures
        r: target radius


    Returns:
    --------
        fig: a figure object of a scatter plot

    """
    df = RDD.get_rdds_for_visuals(g1, u, m, r)
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
        edges_x.append(None)
        edges_y.append(y0)
        edges_y.append(y1)
        edges_y.append(None)

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
    df = RDD.get_rdds_for_visuals_vector(g1, u, measure_vector, r)
    # pos = nx.spring_layout(g1)
    nodes_x = []
    nodes_y = []

    for node_name in g1.nodes:
        x, y = pos[node_name][0], pos[node_name][1]
        nodes_x.append(x)
        nodes_y.append(y)

    # for p in pos.values():
    #     x, y = p[0], p[1]
    #     nodes_x.append(x)
    #     nodes_y.append(y)

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
                             text=list(g1.nodes),
                             # text=['node_name'],
                             name="Node",
                             mode='markers+text'))
    fig.update_layout(template="plotly_dark", dragmode='pan', )
    fig.update_traces(marker={'size': 15, 'color': df['normalized_rdd'], 'colorscale': 'Jet'})
    fig.write_html("graph.html", config={'scrollZoom': True})
    return fig


def draw(g1, pos):
    """Draws a NetworkX Graph with Plotly."""
    # pos = nx.spring_layout(g1)
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


def add_markers_test(figure, pos, nodes):
    annotations = [{'x': pos[n][0],
                    'y': pos[n][1],
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
        edges_x.append(None)
        edges_y.append(y0)
        edges_y.append(y1)
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
        edges_x.append(None)
        edges_y.append(y0)
        edges_y.append(y1)
        edges_y.append(None)

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


def visualize_cosine_similarity(g1, u, pos):
    """takes a graph and plots it, coloring vertices by RDD

    Args:
    -----
        g1 (graph): a networkx graph
        u (int): source node
        pos (dict): position

    Returns:
    --------
        fig: a figure object of a scatter plot"""

    df = cos_sim.get_cosine(g1, u)
    # pos = spring_layout(g1)
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
    fig.update_traces(marker={'size': 15, 'color': df['cos_sim'], 'colorscale': 'Jet'})
    fig.write_html("graph.html", config={'scrollZoom': True})
    # return fig.show(config={'scrollZoom':True})
    return fig


def visualize_rdd_vector_kmeans(g1, u, r, measure_vector, pos, k=3, vistype=1):
    df = RDD.get_rdds_for_visuals_vector(g1, u, measure_vector, r)
    df = other_sims.k_means(df, measure_vector, k)
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
    fig.update_layout(template="plotly_dark", dragmode='pan',
                      annotations=[{'x': df.iloc[0]['nodes_x'],
                                    'y': df.iloc[0]['nodes_y'],
                                    'axref': 'x',
                                    'ayref': 'y',
                                    'arrowsize': 4,
                                    'arrowcolor': 'red',
                                    'showarrow': True,
                                    'arrowhead': 3}])
    if vistype == 0:
        fig.update_traces(
            marker={'size': ((df['k_mean_cluster'] * 5) + 10), 'color': df['normalized_rdd'], 'colorscale': 'Jet'})
    elif vistype == 1:
        fig.update_traces(
            marker={'size': 15, 'color': df['k_mean_cluster'], 'colorscale': 'Jet'})
    else:
        print('enter proper vistype')

    fig.write_html("graph.html", config={'scrollZoom': True})

    return fig

def visualize_rdd_vector_kmeans_others(g1, u, target_column, target_function,pos, k=3,vistype=1):
    df = target_function(g1, u)
    df = other_sims.k_means_other(df, target_column, k)
    #pos = nx.spring_layout(g1)
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
    if vistype == 0:
        fig.update_traces(
            marker={'size': ((df['k_mean_cluster'] * 5) + 10), 'color': df[target_column[0]], 'colorscale': 'Jet'})
    elif vistype == 1:
        fig.update_traces(
            marker={'size': 15, 'color': df['k_mean_cluster'], 'colorscale': 'Jet'})
    else:
        print('that vistype does not exist')

    fig.write_html("graph.html", config={'scrollZoom': True})

    return fig

def visualize_rdd_vector_mean_shift(g1, u, r, measure_vector, pos, vistype=1):
    df = RDD.get_rdds_for_visuals_vector(g1, u, measure_vector, r)
    df = other_sims.mean_shift(df, measure_vector)
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
        edges_x.append(None)
        edges_y.append(y0)
        edges_y.append(y1)
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
    if vistype == 0:
        fig.update_traces(
            marker={'size': ((df['mean_shift_cluster'] * 5) + 10), 'color': df['normalized_rdd'], 'colorscale': 'Jet'})
    elif vistype == 1:
        fig.update_traces(
            marker={'size': 15, 'color': df['mean_shift_cluster'], 'colorscale': 'Jet'})
    else:
        print('enter proper vistype')

    fig.write_html("graph.html", config={'scrollZoom': True})

    return fig


def visualize_rdd_vector_mean_shift_other(g1, u, target_column, target_function, pos, vistype=1):
    df = target_function(g1, u)
    df = other_sims.mean_shift_other(df, target_column)
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
    fig.update_layout(template="plotly_dark", dragmode='pan',
                      annotations=[{'x': df.iloc[0]['nodes_x'],
                                    'y': df.iloc[0]['nodes_y'],
                                    'axref': 'x',
                                    'ayref': 'y',
                                    'arrowsize': 4,
                                    'arrowcolor': 'red',
                                    'showarrow': True,
                                    'arrowhead': 3}])

    if vistype == 0:
        fig.update_traces(
            marker={'size': ((df['mean_shift_cluster'] * 5) + 10), 'color': df[target_column[0]], 'colorscale': 'Jet'})
    elif vistype == 1:
        fig.update_traces(
            marker={'size': 15, 'color': df['mean_shift_cluster'], 'colorscale': 'Jet'})
    else:
        print('enter proper vistype')

    fig.write_html("graph.html", config={'scrollZoom': True})

    return fig


def visualize_rdd_vector_3D2(g1, u, r, pos, measure_vector, df_functions, df_search, z_offset=1):
    df_list = []
    color_vals = []
    graphs_z = [] #z for each graph (all nodes in a graph will have same z)
    z = 0
    for f in df_functions:
        if f.__name__ == 'get_rdds_for_visuals_vector':
            df_list.append(f(g1, u, measure_vector, r))
        else:
            df_list.append(f(g1, u))

        graphs_z.append(z)
        z += z_offset

    nodes_x = []
    nodes_y = []
    nodes_z = []

    edges_x = []
    edges_y = []
    edges_z = []

    nodes_index =[]
    for val in range(len(graphs_z)):
        df = df_list[val]
        ni = 0
        # pos = nx.spring_layout(g1)
        for p in pos.values():
            x, y = p[0], p[1]
            nodes_x.append(x)
            nodes_y.append(y)
            nodes_z.append(graphs_z[val])
            nodes_index.append(df['node_name'][ni])
            ni += 1

        # df_list[val]['nodes_x'] = nodes_x
        # df_list[val]['nodes_y'] = nodes_y
        # df_list[val]['nodes_x'] = nodes_x

        lis = list(df_list[val][df_search[val]])

        color_vals.extend(lis)

        for e in g1.edges():
            x0, y0 = pos[e[0]]
            x1, y1 = pos[e[1]]
            z0, z1 = graphs_z[val], graphs_z[val]
            edges_x.append(x0)
            edges_x.append(x1)
            edges_x.append(None)
            edges_y.append(y0)
            edges_y.append(y1)
            edges_y.append(None)
            edges_z.append(z0)
            edges_z.append(z1)
            edges_z.append(None)

    fig = go.FigureWidget()
    fig.add_trace(go.Scatter3d(x=edges_x, y=edges_y, z=edges_z, name='edges', mode='lines', line={'width': 1}))
    fig.add_trace(go.Scatter3d(x=nodes_x,
                             y=nodes_y,
                             z=nodes_z,
                             text=nodes_index,
                             name="Node",
                             mode='markers'
                             ))
    fig.update_layout(template="plotly_dark", dragmode='pan', )
    fig.update_traces(marker={'size': 10, 'color': color_vals, 'colorscale': 'Jet'})
    fig.write_html("graph.html", config={'scrollZoom': True})
    return fig


def visualize_rdd_vector_3D(g1, u, r, pos, measure_vectors, df_functions, df_search,z_offset=1):
    df_list = []
    graphs_z = [] #z for each graph (all nodes in a graph will have same z)
    z = 0
    for f in df_functions:
        if f.__name__ == 'get_rdds_for_visuals_vector':
            df_list.append(f(g1, u, measure_vectors, r))
        else:
            df_list.append(f(g1, u))

        graphs_z.append(z)
        z+=z_offset
        
    # pos = nx.spring_layout(g1)
    fig = go.FigureWidget()
    ni=0
    color_vals = []
    for val in range(len(graphs_z)):
        nodes_x = []
        nodes_y = []
        nodes_z = []
        node_index = []
        df = df_list[val]
        for p in pos.values():
            x, y = p[0], p[1]
            nodes_x.append(x)
            nodes_y.append(y)
            nodes_z.append(graphs_z[val])
            node_index.append(ni)
            print(ni)
            ni += 1

        df['nodes_x'] = nodes_x
        df['nodes_y'] = nodes_y
        df['nodes_z'] = nodes_z
        lis = list(df_list[val][df_search[val]])

        color_vals.extend(lis)

        edges_x = []
        edges_y = []
        edges_z = []
        for e in g1.edges():
            x0, y0 = pos[e[0]]
            x1, y1 = pos[e[1]]
            z0, z1 = graphs_z[val], graphs_z[val]

            edges_x.append(x0)
            edges_x.append(x1)
            edges_x.append(None)
            edges_y.append(y0)
            edges_y.append(y1)
            edges_y.append(None)
            edges_z.append(z0)
            edges_z.append(z1)
            edges_z.append(None)

        # get the custom_data and build the hover template from the DataFrame column names
        custom_data = df.columns
        hover_template = ""
        for i, m in enumerate(custom_data):
            hover_template += "".join(m + ":" + ' %{customdata[' + str(i) + ']} <br> ')

        fig.add_trace(go.Scatter3d(x=edges_x, y=edges_y, z=edges_z, name='edges', mode='lines', line={'width': 1}))
        fig.add_trace(go.Scatter3d(x=df['nodes_x'],
                                y=df['nodes_y'],
                                z=df['nodes_z'],
                                customdata=df[custom_data],
                                hovertemplate=hover_template,
                                text=df['node_name'],
                                name="Node",
                                mode='markers'))
        fig.update_layout(template = "plotly_dark", dragmode='pan', )
    fig.update_traces(marker={'size': 10, 'color': color_vals, 'colorscale': 'Jet'})
    fig.write_html("graph.html", config={'scrollZoom': True})
    return fig