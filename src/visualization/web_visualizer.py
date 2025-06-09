"""
Web-based Deadlock Visualizer

This module provides web-based interactive visualization using Plotly and Dash.
It creates interactive dashboards that can be viewed in a web browser.
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.offline as pyo
import dash
from dash import dcc, html, Input, Output, State
import networkx as nx
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import json
import time
from datetime import datetime

class WebDeadlockVisualizer:
    """
    Web-based visualizer for deadlock simulation using Plotly and Dash.
    """
    
    def __init__(self, system, port=8050):
        """
        Initialize web visualizer.
        
        Args:
            system: The deadlock system to visualize
            port: Port for the web server
        """
        self.system = system
        self.port = port
        self.app = None
        self.current_layout = 'spring'
        self.current_theme = 'plotly'
        
        # Color schemes for web
        self.color_schemes = {
            'plotly': {
                'process_running': '#1f77b4',
                'process_waiting': '#ff7f0e',
                'process_terminated': '#d62728',
                'resource': '#2ca02c',
                'edge_allocation': '#17becf',
                'edge_request': '#e377c2',
                'background': '#ffffff',
                'paper': '#ffffff'
            },
            'dark': {
                'process_running': '#58d68d',
                'process_waiting': '#ec7063',
                'process_terminated': '#aeb6bf',
                'resource': '#5dade2',
                'edge_allocation': '#52c41a',
                'edge_request': '#ff4d4f',
                'background': '#2c3e50',
                'paper': '#34495e'
            }
        }
    
    def create_network_plot(self, deadlocked_processes=None):
        """
        Create an interactive network plot of the resource allocation graph.
        
        Args:
            deadlocked_processes: List of deadlocked process IDs
            
        Returns:
            plotly.graph_objects.Figure: Interactive network plot
        """
        # Create NetworkX graph
        G = self._create_networkx_graph()
        
        # Compute layout
        if self.current_layout == 'spring':
            pos = nx.spring_layout(G, seed=42, k=3, iterations=50)
        elif self.current_layout == 'circular':
            pos = nx.circular_layout(G)
        elif self.current_layout == 'kamada_kawai':
            pos = nx.kamada_kawai_layout(G)
        else:
            pos = nx.spring_layout(G, seed=42)
        
        # Prepare node data
        node_x, node_y, node_text, node_colors, node_sizes = [], [], [], [], []
        node_symbols = []
        
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            
            # Determine node properties
            if node.startswith('P'):
                process_id = int(node[1:])
                process = self.system.processes.get(process_id)
                
                if process:
                    if process.status == 'RUNNING':
                        color = self.color_schemes[self.current_theme]['process_running']
                    elif process.status == 'WAITING':
                        color = self.color_schemes[self.current_theme]['process_waiting']
                    else:
                        color = self.color_schemes[self.current_theme]['process_terminated']
                    
                    # Create detailed hover text
                    hover_text = f"<b>{node}</b><br>"
                    hover_text += f"Status: {process.status}<br>"
                    hover_text += f"Holding: {[r.rid for r in process.resources_held]}<br>"
                    hover_text += f"Requesting: {[r.rid for r in process.resources_requested]}"
                    
                    # Check if deadlocked
                    if deadlocked_processes and process_id in deadlocked_processes:
                        color = '#ff0000'  # Red for deadlocked
                        hover_text += "<br><b>⚠️ DEADLOCKED!</b>"
                else:
                    color = self.color_schemes[self.current_theme]['process_terminated']
                    hover_text = f"<b>{node}</b><br>Status: TERMINATED"
                
                node_symbols.append('circle')
                node_sizes.append(30)
                
            else:  # Resource node
                resource_id = int(node[1:])
                resource = self.system.resources.get(resource_id)
                
                color = self.color_schemes[self.current_theme]['resource']
                
                if resource:
                    hover_text = f"<b>{node}</b><br>"
                    hover_text += f"Available: {resource.available_instances}/{resource.total_instances}<br>"
                    hover_text += f"Allocated to: {list(resource.allocated_to.keys())}"
                else:
                    hover_text = f"<b>{node}</b><br>Status: N/A"
                
                node_symbols.append('square')
                node_sizes.append(25)
            
            node_colors.append(color)
            node_text.append(hover_text)
        
        # Prepare edge data
        edge_x, edge_y = [], []
        edge_colors, edge_styles = [], []
        
        for edge in G.edges(data=True):
            source, target, data = edge
            x0, y0 = pos[source]
            x1, y1 = pos[target]
            
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            
            # Determine edge color and style
            edge_type = data.get('type', 'allocation')
            if 'allocation' in edge_type:
                color = self.color_schemes[self.current_theme]['edge_allocation']
            else:
                color = self.color_schemes[self.current_theme]['edge_request']
            
            edge_colors.append(color)
        
        # Create figure
        fig = go.Figure()
        
        # Add edges
        fig.add_trace(go.Scatter(
            x=edge_x, y=edge_y,
            mode='lines',
            line=dict(width=2, color='rgba(125,125,125,0.5)'),
            hoverinfo='none',
            showlegend=False,
            name='Edges'
        ))
        
        # Add nodes
        fig.add_trace(go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            marker=dict(
                size=node_sizes,
                color=node_colors,
                line=dict(width=2, color='black'),
                symbol=node_symbols
            ),
            text=[node for node in G.nodes()],
            textposition="middle center",
            textfont=dict(color="white", size=12, family="Arial Black"),
            hovertext=node_text,
            hoverinfo='text',
            showlegend=False,
            name='Nodes'
        ))
        
        # Update layout
        fig.update_layout(
            title=dict(
                text=f"Resource Allocation Graph - Time: {self.system.time}",
                x=0.5,
                font=dict(size=20)
            ),
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20,l=5,r=5,t=40),
            annotations=[ dict(
                text="Processes (circles) and Resources (squares)",
                showarrow=False,
                xref="paper", yref="paper",
                x=0.005, y=-0.002,
                xanchor='left', yanchor='bottom',
                font=dict(color='gray', size=12)
            )],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor=self.color_schemes[self.current_theme]['background'],
            paper_bgcolor=self.color_schemes[self.current_theme]['paper']
        )
        
        return fig
    
    def create_system_metrics_plot(self):
        """Create a plot showing system metrics over time."""
        # Create sample time series data
        metrics = {
            'Time': list(range(0, 11)),
            'Total Processes': [len(self.system.processes)] * 11,
            'Waiting Processes': [
                len([p for p in self.system.processes.values() if p.status == 'WAITING'])
            ] * 11,
            'Resource Utilization': [
                sum(len(p.resources_held) for p in self.system.processes.values()) / 
                max(sum(r.total_instances for r in self.system.resources.values()), 1) * 100
            ] * 11
        }
        
        df = pd.DataFrame(metrics)
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Process Status', 'Resource Utilization', 
                          'System Timeline', 'Performance Metrics'),
            specs=[[{"type": "bar"}, {"type": "indicator"}],
                   [{"type": "scatter", "colspan": 2}, None]]
        )
        
        # Process status bar chart
        process_counts = {
            'RUNNING': len([p for p in self.system.processes.values() if p.status == 'RUNNING']),
            'WAITING': len([p for p in self.system.processes.values() if p.status == 'WAITING']),
            'TERMINATED': len([p for p in self.system.processes.values() if p.status == 'TERMINATED'])
        }
        
        fig.add_trace(
            go.Bar(
                x=list(process_counts.keys()),
                y=list(process_counts.values()),
                name='Process Status',
                marker_color=['green', 'orange', 'red']
            ),
            row=1, col=1
        )
        
        # Resource utilization gauge
        total_resources = sum(r.total_instances for r in self.system.resources.values())
        used_resources = sum(len(p.resources_held) for p in self.system.processes.values())
        utilization = (used_resources / max(total_resources, 1)) * 100
        
        fig.add_trace(
            go.Indicator(
                mode = "gauge+number+delta",
                value = utilization,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Resource Utilization (%)"},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 80], 'color': "yellow"},
                        {'range': [80, 100], 'color': "red"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ),
            row=1, col=2
        )
        
        # Timeline
        fig.add_trace(
            go.Scatter(
                x=df['Time'],
                y=df['Waiting Processes'],
                mode='lines+markers',
                name='Waiting Processes',
                line=dict(color='orange')
            ),
            row=2, col=1
        )
        
        fig.update_layout(
            height=600,
            showlegend=False,
            title_text="System Metrics Dashboard",
            title_x=0.5
        )
        
        return fig
    
    def create_dash_app(self):
        """Create a Dash web application for interactive visualization."""
        self.app = dash.Dash(__name__)
        
        # Define the layout
        self.app.layout = html.Div([
            html.H1("🔄 Deadlock Simulator - Interactive Dashboard", 
                   style={'textAlign': 'center', 'color': '#2c3e50'}),
            
            html.Div([
                html.Div([
                    html.Label("Layout Algorithm:"),
                    dcc.Dropdown(
                        id='layout-dropdown',
                        options=[
                            {'label': 'Spring Layout', 'value': 'spring'},
                            {'label': 'Circular Layout', 'value': 'circular'},
                            {'label': 'Kamada-Kawai Layout', 'value': 'kamada_kawai'}
                        ],
                        value='spring'
                    )
                ], style={'width': '30%', 'display': 'inline-block'}),
                
                html.Div([
                    html.Label("Color Theme:"),
                    dcc.Dropdown(
                        id='theme-dropdown',
                        options=[
                            {'label': 'Light Theme', 'value': 'plotly'},
                            {'label': 'Dark Theme', 'value': 'dark'}
                        ],
                        value='plotly'
                    )
                ], style={'width': '30%', 'display': 'inline-block', 'marginLeft': '10px'}),
                
                html.Div([
                    html.Button('🔍 Detect Deadlock', id='detect-button', 
                               style={'backgroundColor': '#3498db', 'color': 'white', 
                                     'border': 'none', 'padding': '10px 20px',
                                     'borderRadius': '5px', 'cursor': 'pointer'}),
                    html.Button('🛠️ Resolve Deadlock', id='resolve-button',
                               style={'backgroundColor': '#e74c3c', 'color': 'white',
                                     'border': 'none', 'padding': '10px 20px',
                                     'borderRadius': '5px', 'cursor': 'pointer',
                                     'marginLeft': '10px'})
                ], style={'width': '35%', 'display': 'inline-block', 'marginLeft': '10px'})
            ], style={'padding': '20px'}),
            
            html.Div([
                html.Div([
                    dcc.Graph(id='network-graph')
                ], style={'width': '60%', 'display': 'inline-block'}),
                
                html.Div([
                    dcc.Graph(id='metrics-graph')
                ], style={'width': '40%', 'display': 'inline-block'})
            ]),
            
            html.Div(id='status-display', style={'padding': '20px', 'textAlign': 'center'}),
            
            # Hidden div to store deadlock state
            html.Div(id='deadlock-state', style={'display': 'none'}),
            
            # Auto-refresh interval
            dcc.Interval(
                id='interval-component',
                interval=2000,  # Update every 2 seconds
                n_intervals=0
            )
        ])
        
        # Callbacks
        @self.app.callback(
            [Output('network-graph', 'figure'),
             Output('metrics-graph', 'figure'),
             Output('status-display', 'children'),
             Output('deadlock-state', 'children')],
            [Input('layout-dropdown', 'value'),
             Input('theme-dropdown', 'value'),
             Input('detect-button', 'n_clicks'),
             Input('resolve-button', 'n_clicks'),
             Input('interval-component', 'n_intervals')],
            [State('deadlock-state', 'children')]
        )
        def update_dashboard(layout, theme, detect_clicks, resolve_clicks, n_intervals, deadlock_state):
            self.current_layout = layout
            self.current_theme = theme
            
            # Detect deadlock
            deadlocked_processes = []
            try:
                from src.detection import DeadlockDetector
                detector = DeadlockDetector(self.system)
                is_deadlocked, deadlocked_processes = detector.detect_using_resource_allocation_graph()
            except:
                is_deadlocked = False
            
            # Create plots
            network_fig = self.create_network_plot(deadlocked_processes)
            metrics_fig = self.create_system_metrics_plot()
            
            # Status message
            if deadlocked_processes:
                status = html.Div([
                    html.H3("🔴 DEADLOCK DETECTED!", style={'color': 'red'}),
                    html.P(f"Deadlocked processes: P{', P'.join(map(str, deadlocked_processes))}")
                ])
            else:
                status = html.Div([
                    html.H3("🟢 System Running Normally", style={'color': 'green'}),
                    html.P("No deadlock detected")
                ])
            
            return network_fig, metrics_fig, status, json.dumps(deadlocked_processes)
        
        return self.app
    
    def _create_networkx_graph(self):
        """Create a NetworkX graph from the current system state."""
        G = nx.DiGraph()
        
        # Add process nodes
        for pid, process in self.system.processes.items():
            G.add_node(f"P{pid}", type='process', data=process)
        
        # Add resource nodes
        for rid, resource in self.system.resources.items():
            G.add_node(f"R{rid}", type='resource', data=resource)
        
        # Add edges
        for pid, process in self.system.processes.items():
            # Allocation edges
            for resource in process.resources_held:
                G.add_edge(f"R{resource.rid}", f"P{pid}", type='allocation')
            # Request edges  
            for resource in process.resources_requested:
                G.add_edge(f"P{pid}", f"R{resource.rid}", type='request')
        
        return G
    
    def export_static_html(self, filename="deadlock_visualization.html"):
        """Export the current visualization as a static HTML file."""
        deadlocked_processes = []
        try:
            from src.detection import DeadlockDetector
            detector = DeadlockDetector(self.system)
            is_deadlocked, deadlocked_processes = detector.detect_using_resource_allocation_graph()
        except:
            pass
        
        # Create the network plot
        fig = self.create_network_plot(deadlocked_processes)
        
        # Export to HTML
        pyo.plot(fig, filename=filename, auto_open=False)
        print(f"✅ Static visualization exported to {filename}")
        
        return filename
    
    def run_server(self, debug=False):
        """Run the Dash web server."""
        if not self.app:
            self.create_dash_app()
        
        print(f"🌐 Starting web server on http://localhost:{self.port}")
        print("   Press Ctrl+C to stop the server")
        
        try:
            self.app.run_server(debug=debug, port=self.port, host='0.0.0.0')
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user")
        except Exception as e:
            print(f"❌ Server error: {e}")

# Usage example
if __name__ == "__main__":
    # This would normally be called with a real system
    print("Web visualizer module loaded successfully!")
    print("Use WebDeadlockVisualizer(system) to create web visualizations.")
