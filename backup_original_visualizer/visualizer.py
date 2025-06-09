"""
Enhanced Dynamic Deadlock Visualizer - Integrated with existing project structure

This module provides advanced visualization capabilities that integrate seamlessly
with the existing deadlock simulator codebase while adding:
- Dynamic animations and transitions
- Multiple layout algorithms  
- Real-time updates during simulation
- Interactive features
- Web-compatible output
- Performance monitoring

File location: src/visualization/visualizer.py (replace existing)
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import networkx as nx
import numpy as np
from typing import Dict, List, Tuple, Optional, Set, Callable
from enum import Enum
import time
import json
from pathlib import Path
import threading
from queue import Queue
from dataclasses import dataclass
from matplotlib.widgets import Button, Slider
import matplotlib.patches as mpatches
from matplotlib.collections import LineCollection
import logging

# Import existing project components
from src.core import System, Process, Resource

class LayoutType(Enum):
    """Available layout algorithms for visualization."""
    SPRING = "spring"
    CIRCULAR = "circular"
    HIERARCHICAL = "hierarchical"
    GRID = "grid"
    KAMADA_KAWAI = "kamada_kawai"
    SHELL = "shell"
    SPECTRAL = "spectral"
    PLANAR = "planar"

class AnimationType(Enum):
    """Types of animations available."""
    FADE = "fade"
    SLIDE = "slide"
    SCALE = "scale"
    ROTATE = "rotate"
    BOUNCE = "bounce"
    PULSE = "pulse"

@dataclass
class VisualizationState:
    """Represents a state in the visualization sequence."""
    timestamp: float
    title: str
    description: str
    graph: nx.DiGraph
    highlighted_nodes: Set[str]
    highlighted_edges: Set[Tuple[str, str]]
    deadlocked_processes: List[int]
    algorithm_info: Dict
    system_metrics: Dict

class EnhancedDeadlockVisualizer:
    """
    Enhanced visualizer that replaces the original DeadlockVisualizer
    with dynamic capabilities and multiple output formats.
    
    Maintains backward compatibility with existing code while adding
    advanced features.
    """
    
    def __init__(self, system: System, enable_real_time=True, layout_type=LayoutType.SPRING):
        """
        Initialize the enhanced visualizer.
        
        Args:
            system: The system to visualize (existing System class)
            enable_real_time: Enable real-time updates during simulation
            layout_type: Default layout algorithm to use
        """
        self.system = system
        self.enable_real_time = enable_real_time
        self.layout_type = layout_type
        
        # Visualization history and states
        self.states_history = []
        self.current_state_index = 0
        self.update_queue = Queue()
        
        # Animation settings
        self.animation_duration = 1.0  # seconds
        self.frame_rate = 30  # fps
        self.animation_type = AnimationType.FADE
        
        # Layout settings
        self.layout_cache = {}
        self.layout_seed = 42
        self.layout_scale = 2.0
        
        # Interactive features
        self.interactive_mode = True
        self.hover_enabled = True
        self.click_callbacks = {}
        
        # Enhanced color schemes
        self.color_schemes = {
            'default': {
                'process_running': '#2ecc71',
                'process_waiting': '#e74c3c', 
                'process_terminated': '#95a5a6',
                'resource': '#3498db',
                'edge_allocation': '#27ae60',
                'edge_request': '#c0392b',
                'edge_resolution': '#8e44ad',
                'background': '#ffffff',
                'grid': '#ecf0f1',
                'text': '#2c3e50',
                'highlight': '#f39c12'
            },
            'dark': {
                'process_running': '#58d68d',
                'process_waiting': '#ec7063',
                'process_terminated': '#aeb6bf',
                'resource': '#5dade2',
                'edge_allocation': '#52c41a',
                'edge_request': '#ff4d4f',
                'edge_resolution': '#722ed1',
                'background': '#2c3e50',
                'grid': '#34495e',
                'text': '#ecf0f1',
                'highlight': '#f1c40f'
            },
            'colorblind': {
                'process_running': '#1f77b4',
                'process_waiting': '#ff7f0e',
                'process_terminated': '#7f7f7f',
                'resource': '#2ca02c',
                'edge_allocation': '#d62728',
                'edge_request': '#9467bd',
                'edge_resolution': '#8c564b',
                'background': '#ffffff',
                'grid': '#f0f0f0',
                'text': '#000000',
                'highlight': '#e377c2'
            }
        }
        self.current_color_scheme = 'default'
        
        # Figure and animation setup
        self.fig = None
        self.ax = None
        self.ani = None
        self.widgets = {}
        
        # Performance monitoring
        self.performance_metrics = {
            'render_times': [],
            'frame_rates': [],
            'memory_usage': [],
            'update_frequency': 0
        }
        
        # Real-time update thread
        if enable_real_time:
            self.update_thread = threading.Thread(target=self._real_time_updater, daemon=True)
            self.update_thread.start()

    # =============================================================================
    # BACKWARD COMPATIBILITY METHODS (maintain existing API)
    # =============================================================================
    
    def visualize_current_state(self, deadlocked_processes: Optional[List[int]] = None):
        """
        Visualize the current state of the system.
        
        BACKWARD COMPATIBLE: This method maintains the same signature as the original
        but with enhanced visual features.
        
        Args:
            deadlocked_processes: Optional list of process IDs involved in deadlock
        """
        # Create figure with enhanced styling
        self.fig, self.ax = plt.subplots(figsize=(14, 10))
        self.fig.patch.set_facecolor(self.color_schemes[self.current_color_scheme]['background'])
        
        # Create and layout graph
        G = self._create_graph()
        pos = self._compute_layout(G)
        
        # Enhanced rendering
        self._render_enhanced_graph(G, pos, deadlocked_processes)
        
        # Add enhanced information panel
        self._add_enhanced_info_panel(deadlocked_processes)
        
        # Add interactive legend
        self._add_enhanced_legend()
        
        # Set title with enhanced styling
        status = "[DEADLOCK DETECTED]" if deadlocked_processes else "[NO DEADLOCK]"
        title = f"System State at Time {self.system.time}\n{status}"
        if deadlocked_processes:
            title += f"\nDeadlocked Processes: {deadlocked_processes}"
        
        plt.title(title, fontsize=16, fontweight='bold', pad=20)
        plt.tight_layout(pad=3.0)

    def draw_resource_allocation_graph(self):
        """
        Draw the resource allocation graph for the current system state.
        
        BACKWARD COMPATIBLE: Enhanced version of the original method.
        """
        self.visualize_current_state()

    def draw_system_state(self):
        """
        Draw the current system state visualization.
        
        BACKWARD COMPATIBLE: Alias for visualize_current_state.
        """
        self.visualize_current_state()

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
                           dpi=150,
                           pad_inches=0.5)
            print(f"Visualization saved to {filename}")

    # =============================================================================
    # ENHANCED FEATURES (new functionality)
    # =============================================================================

    def set_layout_algorithm(self, layout_type: LayoutType, **kwargs):
        """
        Set the layout algorithm for node positioning.
        
        Args:
            layout_type: The layout algorithm to use
            **kwargs: Additional parameters for the layout algorithm
        """
        self.layout_type = layout_type
        self.layout_cache.clear()  # Clear cache when changing layout
        
        # Update layout parameters
        if 'seed' in kwargs:
            self.layout_seed = kwargs['seed']
        if 'scale' in kwargs:
            self.layout_scale = kwargs['scale']

    def _compute_layout(self, graph: nx.DiGraph, layout_type: LayoutType = None) -> Dict:
        """
        Compute node positions using the specified layout algorithm.
        
        Args:
            graph: The graph to layout
            layout_type: Layout algorithm to use (defaults to self.layout_type)
            
        Returns:
            Dictionary mapping node names to (x, y) positions
        """
        if layout_type is None:
            layout_type = self.layout_type
            
        # Check cache first
        graph_hash = hash(str(sorted(graph.nodes())) + str(sorted(graph.edges())))
        cache_key = (graph_hash, layout_type)
        if cache_key in self.layout_cache:
            return self.layout_cache[cache_key]
        
        # Compute layout based on type
        pos = {}
        
        try:
            if layout_type == LayoutType.SPRING:
                pos = nx.spring_layout(graph, seed=self.layout_seed, scale=self.layout_scale, k=1.5)
            elif layout_type == LayoutType.CIRCULAR:
                pos = nx.circular_layout(graph, scale=self.layout_scale)
            elif layout_type == LayoutType.HIERARCHICAL:
                pos = self._hierarchical_layout(graph)
            elif layout_type == LayoutType.GRID:
                pos = self._grid_layout(graph)
            elif layout_type == LayoutType.KAMADA_KAWAI:
                pos = nx.kamada_kawai_layout(graph, scale=self.layout_scale)
            elif layout_type == LayoutType.SHELL:
                pos = nx.shell_layout(graph, scale=self.layout_scale)
            elif layout_type == LayoutType.SPECTRAL:
                pos = nx.spectral_layout(graph, scale=self.layout_scale)
            elif layout_type == LayoutType.PLANAR:
                try:
                    pos = nx.planar_layout(graph, scale=self.layout_scale)
                except nx.NetworkXException:
                    # Fallback to spring layout if graph is not planar
                    pos = nx.spring_layout(graph, seed=self.layout_seed, scale=self.layout_scale)
        except Exception as e:
            logging.warning(f"Layout computation failed: {e}. Using spring layout as fallback.")
            pos = nx.spring_layout(graph, seed=self.layout_seed, scale=self.layout_scale)
        
        # Cache the result
        self.layout_cache[cache_key] = pos
        return pos

    def _hierarchical_layout(self, graph: nx.DiGraph) -> Dict:
        """Create a hierarchical layout with processes at top, resources at bottom."""
        pos = {}
        processes = [n for n in graph.nodes() if n.startswith('P')]
        resources = [n for n in graph.nodes() if n.startswith('R')]
        
        # Position processes at the top
        for i, p in enumerate(processes):
            pos[p] = (i * 2 - len(processes), 1 * self.layout_scale)
            
        # Position resources at the bottom
        for i, r in enumerate(resources):
            pos[r] = (i * 2 - len(resources), -1 * self.layout_scale)
            
        return pos

    def _grid_layout(self, graph: nx.DiGraph) -> Dict:
        """Create a grid layout for nodes."""
        nodes = list(graph.nodes())
        n = len(nodes)
        cols = int(np.ceil(np.sqrt(n)))
        rows = int(np.ceil(n / cols))
        
        pos = {}
        for i, node in enumerate(nodes):
            row = i // cols
            col = i % cols
            pos[node] = (col * self.layout_scale, -row * self.layout_scale)
            
        return pos

    def create_dynamic_visualization(self, save_frames=False, output_dir="visualizations"):
        """
        Create a dynamic animated visualization of the simulation.
        
        Args:
            save_frames: Whether to save individual frames
            output_dir: Directory to save frames and animations
        """
        if save_frames:
            Path(output_dir).mkdir(exist_ok=True)
            
        # Setup figure with enhanced features
        self.fig, self.ax = plt.subplots(figsize=(16, 12))
        self.fig.patch.set_facecolor(self.color_schemes[self.current_color_scheme]['background'])
        
        # Add interactive widgets
        self._setup_widgets()
        
        # Create initial state
        initial_state = self._capture_current_state("Initial State", "System initialization")
        self.states_history = [initial_state]
        
        # Setup animation
        self.ani = animation.FuncAnimation(
            self.fig, 
            self._animate_frame,
            frames=self._frame_generator,
            interval=1000//self.frame_rate,
            blit=False,
            repeat=True
        )
        
        return self.ani

    def _setup_widgets(self):
        """Setup interactive widgets for the visualization."""
        # Create widget axes (positioned to not overlap with main plot)
        ax_play = plt.axes([0.1, 0.02, 0.08, 0.04])
        ax_pause = plt.axes([0.19, 0.02, 0.08, 0.04])
        ax_reset = plt.axes([0.28, 0.02, 0.08, 0.04])
        ax_speed = plt.axes([0.4, 0.02, 0.15, 0.04])
        ax_layout = plt.axes([0.58, 0.02, 0.1, 0.04])
        ax_theme = plt.axes([0.7, 0.02, 0.1, 0.04])
        
        # Create buttons and sliders
        self.widgets['play'] = Button(ax_play, 'Play')
        self.widgets['pause'] = Button(ax_pause, 'Pause') 
        self.widgets['reset'] = Button(ax_reset, 'Reset')
        self.widgets['speed'] = Slider(ax_speed, 'Speed', 0.1, 3.0, valinit=1.0)
        self.widgets['layout'] = Button(ax_layout, 'Layout')
        self.widgets['theme'] = Button(ax_theme, 'Theme')
        
        # Connect callbacks
        self.widgets['play'].on_clicked(self._on_play_clicked)
        self.widgets['pause'].on_clicked(self._on_pause_clicked)
        self.widgets['reset'].on_clicked(self._on_reset_clicked)
        self.widgets['speed'].on_changed(self._on_speed_changed)
        self.widgets['layout'].on_clicked(self._on_layout_clicked)
        self.widgets['theme'].on_clicked(self._on_theme_clicked)

    def _on_play_clicked(self, event):
        """Handle play button click."""
        if self.ani:
            self.ani.resume()

    def _on_pause_clicked(self, event):
        """Handle pause button click."""
        if self.ani:
            self.ani.pause()

    def _on_reset_clicked(self, event):
        """Handle reset button click."""
        self.current_state_index = 0
        if self.ani:
            self.ani.frame_seq = self.ani.new_frame_seq()

    def _on_speed_changed(self, val):
        """Handle speed slider change."""
        if self.ani:
            self.ani.interval = 1000 // (self.frame_rate * val)

    def _on_layout_clicked(self, event):
        """Handle layout change button click."""
        layouts = list(LayoutType)
        current_idx = layouts.index(self.layout_type)
        next_idx = (current_idx + 1) % len(layouts)
        self.set_layout_algorithm(layouts[next_idx])

    def _on_theme_clicked(self, event):
        """Handle theme change button click."""
        themes = list(self.color_schemes.keys())
        current_idx = themes.index(self.current_color_scheme)
        next_idx = (current_idx + 1) % len(themes)
        self.current_color_scheme = themes[next_idx]

    def _frame_generator(self):
        """Generator for animation frames."""
        while True:
            for i in range(len(self.states_history)):
                yield i
            # Add a pause at the end before repeating
            for _ in range(30):  # 1 second pause at 30fps
                yield len(self.states_history) - 1

    def _animate_frame(self, frame_idx):
        """
        Animate a single frame.
        
        Args:
            frame_idx: Index of the frame to display
        """
        start_time = time.time()
        
        self.ax.clear()
        
        if frame_idx < len(self.states_history):
            state = self.states_history[frame_idx]
            self._render_animated_state(state, frame_idx)
        
        # Update performance metrics
        render_time = time.time() - start_time
        self.performance_metrics['render_times'].append(render_time)
        if len(self.performance_metrics['render_times']) > 100:
            self.performance_metrics['render_times'] = self.performance_metrics['render_times'][-100:]

    def _render_animated_state(self, state: VisualizationState, frame_idx: int):
        """
        Render a specific visualization state with animations.
        
        Args:
            state: The state to render
            frame_idx: Current frame index for animations
        """
        graph = state.graph
        colors = self.color_schemes[self.current_color_scheme]
        
        # Compute layout
        pos = self._compute_layout(graph)
        
        # Apply animation effects
        alpha = self._compute_animation_alpha(frame_idx)
        scale = self._compute_animation_scale(frame_idx)
        
        # Render with enhanced effects
        self._render_enhanced_graph(graph, pos, state.deadlocked_processes, alpha, scale)
        
        # Add animated information panel
        self._add_animated_info_panel(state, frame_idx, colors)

    def _render_enhanced_graph(self, graph, pos, deadlocked_processes=None, alpha=1.0, scale=1.0):
        """
        Render the graph with enhanced visual effects.
        
        Args:
            graph: NetworkX graph to render
            pos: Node positions
            deadlocked_processes: List of deadlocked process IDs
            alpha: Transparency for animations
            scale: Scale factor for animations
        """
        colors = self.color_schemes[self.current_color_scheme]
        deadlocked_nodes = set()
        
        if deadlocked_processes:
            deadlocked_nodes = {f"P{pid}" for pid in deadlocked_processes}
            # Add related resources
            for pid in deadlocked_processes:
                process = self.system.processes.get(pid)
                if process:
                    for resource in process.resources_held + process.resources_requested:
                        deadlocked_nodes.add(f"R{resource.rid}")

        # Draw edges first (so they appear behind nodes)
        self._draw_enhanced_edges(graph, pos, deadlocked_nodes, colors, alpha)
        
        # Draw nodes
        self._draw_enhanced_nodes(graph, pos, deadlocked_nodes, colors, alpha, scale)
        
        # Draw labels
        self._draw_enhanced_labels(graph, pos, colors, alpha)

    def _draw_enhanced_nodes(self, graph, pos, deadlocked_nodes, colors, alpha, scale):
        """Draw nodes with enhanced visual effects."""
        for node in graph.nodes():
            x, y = pos[node]
            node_data = graph.nodes[node]
            
            # Determine node properties
            if node.startswith('P'):
                # Process node
                process_id = int(node[1:])
                process = self.system.processes.get(process_id)
                if process:
                    if process.status == 'RUNNING':
                        color = colors['process_running']
                    elif process.status == 'WAITING':
                        color = colors['process_waiting']
                    else:
                        color = colors['process_terminated']
                else:
                    color = colors['process_terminated']
                    
                size = 1200 * scale
                shape = 'o'
            else:
                # Resource node
                color = colors['resource']
                size = 800 * scale
                shape = 's'
            
            # Enhanced highlighting for deadlocked nodes
            if node in deadlocked_nodes:
                # Draw pulsing glow effect
                glow_alpha = 0.3 + 0.2 * np.sin(time.time() * 5)
                glow_size = size * 1.5
                self.ax.scatter(x, y, s=glow_size, c=colors['highlight'], 
                              alpha=glow_alpha * alpha, marker=shape, zorder=1)
                
                edge_color = colors['highlight']
                edge_width = 4
            else:
                edge_color = '#333333'
                edge_width = 2
            
            # Draw main node with enhanced styling
            self.ax.scatter(x, y, s=size, c=color, alpha=alpha,
                          marker=shape, edgecolors=edge_color, 
                          linewidth=edge_width, zorder=3)

    def _draw_enhanced_edges(self, graph, pos, deadlocked_nodes, colors, alpha):
        """Draw edges with enhanced visual effects."""
        for edge in graph.edges(data=True):
            source, target, data = edge
            if source not in pos or target not in pos:
                continue
                
            x1, y1 = pos[source]
            x2, y2 = pos[target]
            
            # Determine edge properties
            edge_type = data.get('type', 'allocation')
            if 'allocation' in str(edge_type).lower():
                color = colors['edge_allocation']
                style = '-'
                width = 2.5
            elif 'request' in str(edge_type).lower():
                color = colors['edge_request'] 
                style = '--'
                width = 2.5
            else:
                color = colors['edge_resolution']
                style = '-'
                width = 3
            
            # Enhanced highlighting for deadlock paths
            if source in deadlocked_nodes and target in deadlocked_nodes:
                color = colors['highlight']
                width *= 1.5
                # Add pulsing effect
                pulse_alpha = alpha * (0.7 + 0.3 * np.sin(time.time() * 4))
            else:
                pulse_alpha = alpha
            
            # Draw edge with enhanced arrow
            self.ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                           arrowprops=dict(arrowstyle='->', color=color,
                                         lw=width, linestyle=style, 
                                         alpha=pulse_alpha, shrinkA=15, shrinkB=15))

    def _draw_enhanced_labels(self, graph, pos, colors, alpha):
        """Draw labels with enhanced formatting."""
        for node in graph.nodes():
            if node not in pos:
                continue
                
            x, y = pos[node]
            
            # Create detailed label
            if node.startswith('P'):
                process_id = int(node[1:])
                process = self.system.processes.get(process_id)
                if process:
                    label = f"P{process_id}"
                    detail = f"{process.status}"
                    if process.resources_held:
                        detail += f"\nHolds: {[r.rid for r in process.resources_held]}"
                    if process.resources_requested:
                        detail += f"\nWants: {[r.rid for r in process.resources_requested]}"
                else:
                    label = f"P{process_id}"
                    detail = "TERMINATED"
            else:
                resource_id = int(node[1:])
                resource = self.system.resources.get(resource_id)
                if resource:
                    label = f"R{resource_id}"
                    detail = f"{resource.available_instances}/{resource.total_instances}"
                    if resource.allocated_to:
                        detail += f"\nAlloc: {list(resource.allocated_to.keys())}"
                else:
                    label = f"R{resource_id}"
                    detail = "N/A"
            
            # Draw main label
            self.ax.text(x, y, label, ha='center', va='center',
                        fontsize=12, fontweight='bold', color='white',
                        alpha=alpha, zorder=5)
            
            # Draw detail label below
            self.ax.text(x, y-0.4, detail, ha='center', va='center',
                        fontsize=8, color=colors['text'],
                        bbox=dict(boxstyle='round,pad=0.3', 
                                facecolor='white', alpha=0.9*alpha, edgecolor='none'),
                        zorder=4)

    def _add_enhanced_info_panel(self, deadlocked_processes=None):
        """Add enhanced information panel to the visualization."""
        colors = self.color_schemes[self.current_color_scheme]
        
        info_text = f"🕐 Time: {self.system.time}\n"
        info_text += f"🔄 Processes: {len(self.system.processes)}\n"
        info_text += f"📦 Resources: {len(self.system.resources)}\n"
        
        if deadlocked_processes:
            info_text += f"🔴 Status: DEADLOCK DETECTED\n"
            info_text += f"⚠️ Affected: P{', P'.join(map(str, deadlocked_processes))}\n"
        else:
            info_text += f"🟢 Status: NO DEADLOCK\n"
            
        info_text += f"🎨 Layout: {self.layout_type.value.title()}\n"
        info_text += f"🎭 Theme: {self.current_color_scheme.title()}"
        
        # Add performance info if available
        if self.performance_metrics['render_times']:
            avg_time = np.mean(self.performance_metrics['render_times'][-10:])
            fps = 1.0 / avg_time if avg_time > 0 else 0
            info_text += f"\n⚡ FPS: {fps:.1f}"
        
        # Add to plot with enhanced styling
        self.ax.text(0.02, 0.98, info_text, transform=self.ax.transAxes,
                    verticalalignment='top', fontsize=11, fontfamily='monospace',
                    bbox=dict(boxstyle='round,pad=0.8', 
                            facecolor=colors['background'], 
                            alpha=0.95, 
                            edgecolor=colors['text'],
                            linewidth=1))

    def _add_animated_info_panel(self, state, frame_idx, colors):
        """Add animated information panel."""
        self._add_enhanced_info_panel(state.deadlocked_processes)

    def _add_enhanced_legend(self):
        """Add enhanced legend with visual examples."""
        colors = self.color_schemes[self.current_color_scheme]
        
        # Create legend elements
        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=colors['process_running'],
                      markersize=12, label='Running Process', markeredgecolor='black'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=colors['process_waiting'],
                      markersize=12, label='Waiting Process', markeredgecolor='black'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=colors['process_terminated'],
                      markersize=12, label='Terminated Process', markeredgecolor='black'),
            plt.Line2D([0], [0], marker='s', color='w', markerfacecolor=colors['resource'],
                      markersize=12, label='Resource', markeredgecolor='black'),
            plt.Line2D([0], [0], color=colors['edge_allocation'], linewidth=3, label='Allocation Edge'),
            plt.Line2D([0], [0], color=colors['edge_request'], linewidth=3, 
                      linestyle='--', label='Request Edge'),
            plt.Line2D([0], [0], color=colors['highlight'], linewidth=4, label='Deadlock Path')
        ]
        
        # Add legend with enhanced styling
        legend = self.ax.legend(handles=legend_elements, loc='upper right', 
                              bbox_to_anchor=(0.98, 0.98), fontsize=10,
                              frameon=True, fancybox=True, shadow=True,
                              facecolor=colors['background'], edgecolor=colors['text'])
        legend.get_frame().set_alpha(0.9)

    def _compute_animation_alpha(self, frame_idx):
        """Compute alpha value for animations."""
        if self.animation_type == AnimationType.FADE:
            cycle_length = 60  # frames
            cycle_pos = frame_idx % cycle_length
            return 0.4 + 0.6 * (np.sin(2 * np.pi * cycle_pos / cycle_length) + 1) / 2
        return 1.0

    def _compute_animation_scale(self, frame_idx):
        """Compute scale factor for animations."""
        if self.animation_type == AnimationType.SCALE:
            cycle_length = 45  # frames
            cycle_pos = frame_idx % cycle_length
            return 0.8 + 0.4 * (np.sin(2 * np.pi * cycle_pos / cycle_length) + 1) / 2
        elif self.animation_type == AnimationType.PULSE:
            cycle_length = 30
            cycle_pos = frame_idx % cycle_length
            return 0.9 + 0.2 * (np.sin(2 * np.pi * cycle_pos / cycle_length) + 1) / 2
        return 1.0

    def _capture_current_state(self, title="", description=""):
        """Capture the current system state for visualization."""
        graph = self._create_graph()
        
        # Detect deadlock for highlighting
        deadlocked_processes = self._detect_deadlock_simple()
        
        # Determine highlighted elements
        highlighted_nodes = set()
        highlighted_edges = set()
        
        if deadlocked_processes:
            for pid in deadlocked_processes:
                highlighted_nodes.add(f"P{pid}")
                # Add related resources and edges
                process = self.system.processes.get(pid)
                if process:
                    for resource in process.resources_held:
                        highlighted_edges.add((f"R{resource.rid}", f"P{pid}"))
                    for resource in process.resources_requested:
                        highlighted_edges.add((f"P{pid}", f"R{resource.rid}"))
        
        return VisualizationState(
            timestamp=time.time(),
            title=title or f"System State at T={self.system.time}",
            description=description,
            graph=graph,
            highlighted_nodes=highlighted_nodes,
            highlighted_edges=highlighted_edges,
            deadlocked_processes=deadlocked_processes,
            algorithm_info={'name': 'Resource Allocation Graph'},
            system_metrics=self._collect_system_metrics()
        )

    def _create_graph(self):
        """Create a NetworkX graph from the current system state."""
        graph = nx.DiGraph()
        
        # Add process nodes
        for pid, process in self.system.processes.items():
            graph.add_node(f"P{pid}", type='process', status=process.status)
        
        # Add resource nodes
        for rid, resource in self.system.resources.items():
            graph.add_node(f"R{rid}", type='resource')
        
        # Add edges
        for pid, process in self.system.processes.items():
            # Allocation edges
            for resource in process.resources_held:
                graph.add_edge(f"R{resource.rid}", f"P{pid}", type='allocation')
            # Request edges  
            for resource in process.resources_requested:
                graph.add_edge(f"P{pid}", f"R{resource.rid}", type='request')
        
        return graph

    def _detect_deadlock_simple(self):
        """Simple deadlock detection for visualization purposes."""
        # This is a simplified version for visualization
        # In practice, you would use the actual DeadlockDetector
        try:
            from src.detection import DeadlockDetector
            detector = DeadlockDetector(self.system)
            is_deadlocked, deadlocked_processes = detector.detect_using_resource_allocation_graph()
            return deadlocked_processes if is_deadlocked else []
        except:
            # Fallback simple detection
            waiting_processes = []
            for pid, process in self.system.processes.items():
                if process.status == 'WAITING' and process.resources_requested:
                    waiting_processes.append(pid)
            return waiting_processes

    def _collect_system_metrics(self):
        """Collect current system metrics."""
        metrics = {
            'total_processes': len(self.system.processes),
            'total_resources': len(self.system.resources),
            'waiting_processes': sum(1 for p in self.system.processes.values() 
                                   if p.status == 'WAITING'),
            'terminated_processes': sum(1 for p in self.system.processes.values()
                                      if p.status == 'TERMINATED'),
            'total_allocations': sum(len(p.resources_held) 
                                   for p in self.system.processes.values()),
            'total_requests': sum(len(p.resources_requested)
                                for p in self.system.processes.values())
        }
        return metrics

    def _real_time_updater(self):
        """Real-time update thread for live visualization."""
        last_update = time.time()
        
        while True:
            try:
                # Check for updates every 100ms
                time.sleep(0.1)
                
                # Capture state if system has changed
                current_time = time.time()
                if current_time - last_update > 0.5:  # Update every 500ms
                    new_state = self._capture_current_state("Real-time Update")
                    self.states_history.append(new_state)
                    last_update = current_time
                    
                    # Limit history size
                    if len(self.states_history) > 1000:
                        self.states_history = self.states_history[-500:]
                        
            except Exception as e:
                logging.warning(f"Real-time update error: {e}")
                time.sleep(1)

    def set_color_scheme(self, scheme_name: str):
        """
        Set the color scheme for visualization.
        
        Args:
            scheme_name: Name of the color scheme ('default', 'dark', 'colorblind')
        """
        if scheme_name in self.color_schemes:
            self.current_color_scheme = scheme_name
        else:
            raise ValueError(f"Unknown color scheme: {scheme_name}")

    def add_custom_color_scheme(self, name: str, colors: Dict[str, str]):
        """
        Add a custom color scheme.
        
        Args:
            name: Name for the new scheme
            colors: Dictionary mapping color roles to hex colors
        """
        self.color_schemes[name] = colors

    def export_animation(self, filename="deadlock_animation.gif", format="gif"):
        """
        Export the current animation to a file.
        
        Args:
            filename: Output filename
            format: Export format ('gif', 'mp4', 'html')
        """
        if not self.ani:
            print("No animation to export. Create dynamic visualization first.")
            return
            
        try:
            if format == "gif":
                self.ani.save(filename, writer='pillow', fps=self.frame_rate)
            elif format == "mp4":
                self.ani.save(filename, writer='ffmpeg', fps=self.frame_rate)
            elif format == "html":
                # For HTML export, we'd need to implement web-based version
                print("HTML export not implemented in this version")
                return
            
            print(f"Animation exported to {filename}")
        except Exception as e:
            print(f"Export failed: {e}")

    def get_performance_report(self):
        """Get a detailed performance report."""
        metrics = self.performance_metrics
        
        report = {
            'average_render_time': np.mean(metrics['render_times']) if metrics['render_times'] else 0,
            'average_fps': 1.0 / np.mean(metrics['render_times']) if metrics['render_times'] else 0,
            'total_states': len(self.states_history),
            'cache_hits': len(self.layout_cache),
            'update_frequency': metrics['update_frequency']
        }
        
        return report

    # =============================================================================
    # STEP-BY-STEP VISUALIZATION METHODS (enhanced versions)
    # =============================================================================
    
    def visualize_detection_steps(self, detection_steps: List[Dict]):
        """
        Visualize the deadlock detection process step by step.
        
        Args:
            detection_steps: List of detection steps
        """
        for i, step in enumerate(detection_steps):
            self.fig, self.ax = plt.subplots(figsize=(14, 10))
            self.fig.patch.set_facecolor(self.color_schemes[self.current_color_scheme]['background'])
            
            G = self._create_graph()
            pos = self._compute_layout(G)
            
            # Highlight marked processes
            marked_processes = step.get('marked_processes', set())
            deadlocked_processes = [int(p) for p in marked_processes if isinstance(p, (int, str)) and str(p).isdigit()]
            
            self._render_enhanced_graph(G, pos, deadlocked_processes)
            
            # Add step information
            step_info = f"Detection Step {i+1}\n\n{step.get('explanation', '')}"
            self.ax.text(0.02, 0.02, step_info, transform=self.ax.transAxes,
                        verticalalignment='bottom', fontsize=12,
                        bbox=dict(boxstyle='round,pad=0.8', 
                                facecolor='lightyellow', 
                                alpha=0.9, edgecolor='orange'))
            
            plt.title(f"Deadlock Detection Step {i+1}", fontsize=16, fontweight='bold')
            self._add_enhanced_legend()
            plt.tight_layout()
            plt.show()

    def visualize_resolution_steps(self, resolution_steps: List[Dict]):
        """
        Visualize the deadlock resolution process step by step.
        
        Args:
            resolution_steps: List of resolution steps
        """
        for i, step in enumerate(resolution_steps):
            self.fig, self.ax = plt.subplots(figsize=(14, 10))
            self.fig.patch.set_facecolor(self.color_schemes[self.current_color_scheme]['background'])
            
            G = self._create_graph()
            pos = self._compute_layout(G)
            
            self._render_enhanced_graph(G, pos)
            
            # Add resolution information
            strategy = step.get('strategy', 'Unknown')
            success = step.get('success', False)
            status_text = "✅ SUCCESS" if success else "❌ FAILED"
            
            resolution_info = f"Resolution Step {i+1}\n\nStrategy: {strategy.title()}\nStatus: {status_text}"
            
            self.ax.text(0.02, 0.02, resolution_info, transform=self.ax.transAxes,
                        verticalalignment='bottom', fontsize=12,
                        bbox=dict(boxstyle='round,pad=0.8', 
                                facecolor='lightgreen' if success else 'lightcoral', 
                                alpha=0.9, 
                                edgecolor='green' if success else 'red'))
            
            plt.title(f"Deadlock Resolution Step {i+1}: {strategy.title()}", 
                     fontsize=16, fontweight='bold')
            self._add_enhanced_legend()
            plt.tight_layout()
            plt.show()


# =============================================================================
# BACKWARD COMPATIBILITY ALIAS
# =============================================================================

# Maintain backward compatibility with existing code
DeadlockVisualizer = EnhancedDeadlockVisualizer


# =============================================================================
# USAGE EXAMPLES AND INTEGRATION HELPERS
# =============================================================================

def create_enhanced_visualization_demo():
    """
    Demo function showing how to use the enhanced visualizer.
    This can be used for testing and as an example.
    """
    from src.core import System, Process, Resource
    
    # Create a simple system
    system = System()
    
    # Add processes
    p1 = Process(1)
    p2 = Process(2)
    system.add_process(p1)
    system.add_process(p2)
    
    # Add resources
    r1 = Resource(1, instances=1)
    r2 = Resource(2, instances=1)
    system.add_resource(r1)
    system.add_resource(r2)
    
    # Create deadlock
    p1.request_resource(r1)
    p2.request_resource(r2)
    p1.request_resource(r2)
    p2.request_resource(r1)
    
    # Create enhanced visualizer
    visualizer = EnhancedDeadlockVisualizer(system, layout_type=LayoutType.HIERARCHICAL)
    
    # Set dark theme
    visualizer.set_color_scheme('dark')
    
    # Create static visualization
    visualizer.visualize_current_state([1, 2])
    visualizer.show()
    
    # Create dynamic visualization
    ani = visualizer.create_dynamic_visualization()
    
    # Export animation
    visualizer.export_animation("demo.gif", "gif")
    
    return visualizer

if __name__ == "__main__":
    # Run demo if this file is executed directly
    create_enhanced_visualization_demo()