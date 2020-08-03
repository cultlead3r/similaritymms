import pandas as pd
import plotly.graph_objects as go
from networkx import spring_layout
from rdd.Node import Node
from rdd import measures


def visualize_rdd(g1, u, m=measures.global_graph_degree):
    """takes a graph and plots it, coloring vertices by RDD

    Args:
    -----
        g1: a networkx graph
        u: source node
        m: a measure function from measures

    Returns:
    --------
        fig: a figure object of a scatter plot"""

    df = measures.get_rdds_for_visuals(g1, u, m, 4)
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
        x0,y0 = pos[e[0]]
        x1,y1 = pos[e[1]]
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
    fig.update_traces(marker={'size': 10, 'color': df['rdd'], 'colorscale' : 'Jet'})
    fig.write_html("graph.html", config={'scrollZoom':True})

    return fig.show(config={'scrollZoom':True})