import plotly.graph_objects as go
import networkx as nx
from typing import Dict

def create_relationship_graph(relationships: Dict) -> go.Figure:
    """
    Create a plotly figure for relationship visualization
    """
    graph = relationships['graph']
    
    # Create layout
    pos = nx.spring_layout(graph)
    
    # Create edge traces
    edge_traces = []
    for edge in graph.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        
        edge_trace = go.Scatter(
            x=[x0, x1],
            y=[y0, y1],
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines'
        )
        edge_traces.append(edge_trace)
    
    # Create node trace
    node_trace = go.Scatter(
        x=[pos[node][0] for node in graph.nodes()],
        y=[pos[node][1] for node in graph.nodes()],
        mode='markers+text',
        hoverinfo='text',
        text=[node for node in graph.nodes()],
        textposition='bottom center',
        marker=dict(
            size=20,
            color='lightblue',
            line_width=2
        )
    )
    
    # Create figure
    fig = go.Figure(data=edge_traces + [node_trace],
                   layout=go.Layout(
                       showlegend=False,
                       hovermode='closest',
                       margin=dict(b=20,l=5,r=5,t=40),
                       plot_bgcolor='white'
                   ))
    
    return fig
