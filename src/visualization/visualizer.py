"""
Visualization module for the Deadlock Simulator.

This module provides visualization capabilities for:
- Resource allocation graphs
- System state matrices
- Deadlock detection steps
- Resolution paths
"""

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from typing import Dict, List, Tuple, Optional, Set
from enum import Enum
import matplotlib.colors as mcolors
from src.core import System, Process, Resource

class NodeType(Enum):
    """Types of nodes in the visualization."""
    PROCESS = "process"
    RESOURCE = "resource"
    DEADLOCKED = 'deadlocked'
    SAFE = 'safe'
    TERMINATED = 'terminated'
    WAITING = 'waiting'
    RUNNING = 'running'

class EdgeType(Enum):
    """Types of edges in the visualization."""
    ALLOCATION = "allocation"
    REQUEST = "request"
    RESOLUTION = "resolution"

class DeadlockVisualizer:
    """Visualizer for deadlock detection and resolution."""
    
    def __init__(self, system: System):
        """
        Initialize the visualizer.
        
        Args:
            system: The system to visualize
        """
        self.system = system
        self.fig = None
        self.ax = None
        self.G = None
        
        # Define colors and styles
        self.colors = {
            NodeType.PROCESS: {
                'RUNNING': '#2ecc71',  # Green
                'WAITING': '#e74c3c',  # Red
                'TERMINATED': '#95a5a6'  # Gray
            },
            NodeType.RESOURCE: '#3498db',  # Blue
            EdgeType.ALLOCATION: '#27ae60',  # Dark Green
            EdgeType.REQUEST: '#c0392b',  # Dark Red
            EdgeType.RESOLUTION: 'blue'
        }
        
        self.node_shapes = {
            NodeType.PROCESS: 'o',  # Circle
            NodeType.RESOURCE: 's'  # Square
        }
        
        self.edge_styles = {
            EdgeType.ALLOCATION: 'solid',
            EdgeType.REQUEST: 'dashed',
            EdgeType.RESOLUTION: 'solid'
        }
        
        # Node sizes
        self.node_size = 2000
        self.resource_node_size = 1500
        
        # Layout parameters
        self.layout_scale = 1.5
        self.layout_seed = 42
        
        # Figure parameters
        self.figsize = (12, 8)
        self.dpi = 100
        self.title_fontsize = 14
        self.label_fontsize = 10
        self.legend_fontsize = 9
        
        # Padding for legend
        self.legend_padding = 0.1

    def _setup_plot(self, title: str):
        """
        Set up a new plot with the given title.
        
        Args:
            title: Title for the plot
        """
        # Close any existing figure
        if self.fig is not None:
            plt.close(self.fig)
        
        # Create new figure and axis
        self.fig, self.ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        self.ax.set_title(title, fontsize=self.title_fontsize, pad=20)
        self.ax.set_axis_off()

    def _create_graph(self) -> nx.DiGraph:
        """
        Create a directed graph representing the system state.
        
        Returns:
            nx.DiGraph: The created graph
        """
        G = nx.DiGraph()
        
        # Add process nodes with detailed labels
        for pid, process in self.system.processes.items():
            # Create detailed process label
            process_label = f"P{pid}\n"
            process_label += f"Status: {process.status}\n"
            if process.resources_held:
                process_label += f"Holding: {[r.rid for r in process.resources_held]}\n"
            if process.resources_requested:
                process_label += f"Waiting: {[r.rid for r in process.resources_requested]}"
            
            G.add_node(f"P{pid}", 
                      type=NodeType.PROCESS,
                      status=process.status,
                      label=process_label)
        
        # Add resource nodes with detailed labels
        for rid, resource in self.system.resources.items():
            # Create detailed resource label
            resource_label = f"R{rid}\n"
            resource_label += f"Available: {resource.available_instances}/{resource.total_instances}\n"
            if resource.allocated_to:
                resource_label += f"Allocated: {resource.allocated_to}"
            
            G.add_node(f"R{rid}", 
                      type=NodeType.RESOURCE,
                      label=resource_label)
        
        # Add edges
        for pid, process in self.system.processes.items():
            # Allocation edges
            for resource in process.resources_held:
                G.add_edge(f"R{resource.rid}", f"P{pid}",
                          type=EdgeType.ALLOCATION)
            
            # Request edges
            for resource in process.resources_requested:
                G.add_edge(f"P{pid}", f"R{resource.rid}",
                          type=EdgeType.REQUEST)
        
        return G

    def _get_node_colors(self, G, nodes=None):
        """
        Get colors for nodes based on their type and state.
        
        Args:
            G: The graph
            nodes: Optional list of nodes to get colors for. If None, returns colors for all nodes.
        
        Returns:
            List of colors for the specified nodes
        """
        if nodes is None:
            nodes = list(G.nodes())
            
        colors = []
        for node in nodes:
            if G.nodes[node]['type'] == NodeType.PROCESS:
                status = G.nodes[node]['status']
                colors.append(self.colors[NodeType.PROCESS][status])
            else:
                colors.append(self.colors[NodeType.RESOURCE])
        return colors

    def _get_node_shapes(self, G: nx.DiGraph) -> List[str]:
        """
        Get shapes for each node based on its type.
        
        Args:
            G: The graph to get shapes for
            
        Returns:
            List[str]: List of shapes for each node
        """
        return [self.node_shapes[G.nodes[node]['type']] for node in G.nodes()]

    def _get_node_sizes(self, G: nx.DiGraph) -> List[int]:
        """
        Get sizes for each node based on its type.
        
        Args:
            G: The graph to get sizes for
            
        Returns:
            List[int]: List of sizes for each node
        """
        return [self.resource_node_size if G.nodes[node]['type'] == NodeType.RESOURCE 
                else self.node_size for node in G.nodes()]

    def _get_edge_colors(self, G: nx.DiGraph) -> List[str]:
        """
        Get colors for each edge based on its type.
        
        Args:
            G: The graph to get colors for
            
        Returns:
            List[str]: List of colors for each edge
        """
        return [self.colors[edge_data['type']] for _, _, edge_data in G.edges(data=True)]

    def _get_edge_styles(self, G: nx.DiGraph) -> List[str]:
        """
        Get styles for each edge based on its type.
        
        Args:
            G: The graph to get styles for
            
        Returns:
            List[str]: List of styles for each edge
        """
        return [self.edge_styles[edge_data['type']] for _, _, edge_data in G.edges(data=True)]

    def _create_legend_elements(self):
        """Create legend elements for the plot."""
        from matplotlib.lines import Line2D
        from matplotlib.patches import Patch
        
        elements = []
        labels = []
        
        # Process states
        for status, color in self.colors[NodeType.PROCESS].items():
            elements.append(Patch(facecolor=color, edgecolor='black'))
            labels.append(f'Process ({status})')
        
        # Resource node
        elements.append(Patch(facecolor=self.colors[NodeType.RESOURCE], edgecolor='black'))
        labels.append('Resource')
        
        # Edge types
        for edge_type, color in self.colors.items():
            if isinstance(edge_type, EdgeType):
                elements.append(Line2D([0], [0], color=color, 
                                    linestyle=self.edge_styles[edge_type]))
                labels.append(f'{edge_type.value.title()} Edge')
        
        return elements, labels

    def visualize_current_state(self, deadlocked_processes: Optional[List[int]] = None):
        """
        Visualize the current state of the system.
        
        Args:
            deadlocked_processes: Optional list of process IDs involved in deadlock
        """
        # Create figure with specific size and DPI
        self.fig, self.ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        
        # Create and layout graph
        self.G = self._create_graph()
        pos = nx.spring_layout(self.G, 
                             scale=self.layout_scale,
                             seed=self.layout_seed,
                             k=2.0)  # Increased repulsion
        
        # Draw nodes
        nx.draw_networkx_nodes(self.G, pos,
                             node_color=self._get_node_colors(self.G),
                             node_shape='o',
                             node_size=self._get_node_sizes(self.G),
                             alpha=0.9)
        
        # Draw edges
        nx.draw_networkx_edges(self.G, pos,
                             edge_color=self._get_edge_colors(self.G),
                             style=self._get_edge_styles(self.G),
                             arrowsize=20,
                             width=2,
                             alpha=0.7)
        
        # Draw labels with background
        label_pos = {node: (pos[node][0], pos[node][1] + 0.1) for node in self.G.nodes()}
        nx.draw_networkx_labels(self.G, label_pos,
                              labels={node: self.G.nodes[node]['label'] for node in self.G.nodes()},
                              font_size=self.label_fontsize,
                              font_weight='bold',
                              bbox=dict(facecolor='white',
                                      edgecolor='none',
                                      alpha=0.7,
                                      pad=3))
        
        # Add title with status and time
        status = "[DEADLOCK DETECTED]" if deadlocked_processes else "[NO DEADLOCK]"
        title = f"System State at Time {self.system.time}\n{status}"
        if deadlocked_processes:
            title += f"\nDeadlocked Processes: {deadlocked_processes}"
        plt.title(title,
                 fontsize=self.title_fontsize,
                 pad=20)
        
        # Add legend with padding
        handles, labels = self._create_legend_elements()
        legend = self.ax.legend(handles, labels,
                              loc='upper right',
                              bbox_to_anchor=(1.0, 1.0),
                              fontsize=self.legend_fontsize)
        
        # Add padding around the plot
        plt.margins(x=0.2, y=0.2)
        
        # Remove axis
        self.ax.set_axis_off()
        
        # Adjust layout to prevent overlapping
        plt.tight_layout(pad=3.0)

    def visualize_detection_steps(self, detection_steps: List[Dict]):
        """
        Visualize the deadlock detection process step by step.
        
        Args:
            detection_steps: List of detection steps, each containing:
                - marked_processes: Set of marked process IDs
                - explanation: Step explanation
        """
        for i, step in enumerate(detection_steps):
            self._setup_plot(f"Deadlock Detection Step {i+1}")
            self.G = self._create_graph()
            
            # Position nodes
            pos = nx.spring_layout(self.G, 
                                 scale=self.layout_scale,
                                 seed=self.layout_seed)
            
            # Draw nodes
            process_nodes = [f"P{pid}" for pid in self.system.processes]
            resource_nodes = [f"R{rid}" for rid in self.system.resources]
            
            # Draw process nodes with appropriate colors
            marked_processes = step['marked_processes']
            process_colors = []
            for pid in self.system.processes:
                node_color = (self.colors[NodeType.PROCESS]['RUNNING'] 
                            if pid in marked_processes 
                            else self.colors[NodeType.PROCESS]['WAITING'])
                process_colors.append(node_color)
            
            nx.draw_networkx_nodes(self.G, pos,
                                 nodelist=process_nodes,
                                 node_color=process_colors,
                                 node_size=self.node_size,
                                 alpha=0.7)
            
            # Draw resource nodes
            nx.draw_networkx_nodes(self.G, pos,
                                 nodelist=resource_nodes,
                                 node_color=self._get_node_colors(self.G, resource_nodes),
                                 node_size=self.resource_node_size,
                                 alpha=0.7)
            
            # Draw edges
            nx.draw_networkx_edges(self.G, pos,
                                 edge_color=self._get_edge_colors(self.G),
                                 style=self._get_edge_styles(self.G),
                                 arrowsize=20,
                                 width=2,
                                 alpha=0.7)
            
            # Add labels
            nx.draw_networkx_labels(self.G, pos,
                                  font_size=self.label_fontsize)
            
            # Add step explanation
            self.ax.text(0.02, 0.98, step['explanation'],
                        transform=self.ax.transAxes,
                        verticalalignment='top',
                        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
            
            # Add legend
            handles, labels = self._create_legend_elements()
            self.ax.legend(handles, labels,
                          loc='upper right',
                          bbox_to_anchor=(1.0, 1.0),
                          fontsize=self.legend_fontsize)
            
            plt.tight_layout()
            plt.show()

    def visualize_resolution_steps(self, resolution_steps: List[Dict]):
        """
        Visualize the deadlock resolution process step by step.
        
        Args:
            resolution_steps: List of resolution steps, each containing:
                - strategy: Name of the resolution strategy
                - success: Whether the strategy was successful
                - state: System state after the strategy
        """
        for i, step in enumerate(resolution_steps):
            self._setup_plot(f"Resolution Step {i+1}: {step['strategy'].title()}")
            self.G = self._create_graph()
            
            # Position nodes
            pos = nx.spring_layout(self.G, 
                                 scale=self.layout_scale,
                                 seed=self.layout_seed)
            
            # Draw nodes
            process_nodes = [f"P{pid}" for pid in self.system.processes]
            resource_nodes = [f"R{rid}" for rid in self.system.resources]
            
            # Draw process nodes
            nx.draw_networkx_nodes(self.G, pos,
                                 nodelist=process_nodes,
                                 node_color=self._get_node_colors(self.G, process_nodes),
                                 node_size=self.node_size,
                                 alpha=0.7)
            
            # Draw resource nodes
            nx.draw_networkx_nodes(self.G, pos,
                                 nodelist=resource_nodes,
                                 node_color=self._get_node_colors(self.G, resource_nodes),
                                 node_size=self.resource_node_size,
                                 alpha=0.7)
            
            # Draw edges
            nx.draw_networkx_edges(self.G, pos,
                                 edge_color=self._get_edge_colors(self.G),
                                 style=self._get_edge_styles(self.G),
                                 arrowsize=20,
                                 width=2,
                                 alpha=0.7)
            
            # Add labels
            nx.draw_networkx_labels(self.G, pos,
                                  font_size=self.label_fontsize)
            
            # Add step explanation
            status = "Success" if step['success'] else "Failed"
            explanation = f"Strategy: {step['strategy'].title()}\nStatus: {status}"
            self.ax.text(0.02, 0.98, explanation,
                        transform=self.ax.transAxes,
                        verticalalignment='top',
                        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
            
            # Add legend
            handles, labels = self._create_legend_elements()
            self.ax.legend(handles, labels,
                          loc='upper right',
                          bbox_to_anchor=(1.0, 1.0),
                          fontsize=self.legend_fontsize)
            
            plt.tight_layout()
            plt.show()

    def set_colors(self, **kwargs):
        """
        Set custom colors for nodes and edges.
        
        Args:
            **kwargs: Color mappings for node and edge types
        """
        for key, value in kwargs.items():
            if key in self.colors:
                self.colors[key] = value
                
    def show(self):
        """Display the current visualization."""
        if self.fig is not None:
            plt.show()
            
    def save(self, filename: str):
        """
        Save the current visualization to a file.
        
        Args:
            filename: Path to save the visualization
        """
        if self.fig:
            self.fig.savefig(filename, 
                           bbox_inches='tight',
                           dpi=self.dpi,
                           pad_inches=0.5)
            plt.close(self.fig)

    def draw_resource_allocation_graph(self):
        """
        Draw the resource allocation graph for the current system state.
        """
        # Create figure with specific size and DPI
        self.fig, self.ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        
        # Create and layout graph
        self.G = self._create_graph()
        pos = nx.spring_layout(self.G, 
                             scale=self.layout_scale,
                             seed=self.layout_seed,
                             k=2.0)  # Increased repulsion
        
        # Draw nodes
        nx.draw_networkx_nodes(self.G, pos,
                             node_color=self._get_node_colors(self.G),
                             node_shape='o',
                             node_size=self._get_node_sizes(self.G),
                             alpha=0.9)
        
        # Draw edges
        nx.draw_networkx_edges(self.G, pos,
                             edge_color=self._get_edge_colors(self.G),
                             style=self._get_edge_styles(self.G),
                             arrowsize=20,
                             width=2,
                             alpha=0.7)
        
        # Draw labels with background
        label_pos = {node: (pos[node][0], pos[node][1] + 0.1) for node in self.G.nodes()}
        nx.draw_networkx_labels(self.G, label_pos,
                              labels={node: self.G.nodes[node]['label'] for node in self.G.nodes()},
                              font_size=self.label_fontsize,
                              font_weight='bold',
                              bbox=dict(facecolor='white',
                                      edgecolor='none',
                                      alpha=0.7,
                                      pad=3))
        
        # Add title
        plt.title("Resource Allocation Graph",
                 fontsize=self.title_fontsize,
                 pad=20)
        
        # Add legend with padding
        handles, labels = self._create_legend_elements()
        legend = self.ax.legend(handles, labels,
                              loc='upper right',
                              bbox_to_anchor=(1.0, 1.0),
                              fontsize=self.legend_fontsize)
        
        # Add padding around the plot
        plt.margins(x=0.2, y=0.2)
        
        # Remove axis
        self.ax.set_axis_off()
        
        # Adjust layout to prevent overlapping
        plt.tight_layout(pad=3.0)

    def draw_system_state(self):
        """
        Draw the current system state visualization.
        """
        self.visualize_current_state()
