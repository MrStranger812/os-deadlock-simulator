"""
Enhanced visualization components for the deadlock simulator.

This subpackage provides advanced tools for visualizing the state of the system,
including dynamic animations, multiple layouts, and interactive features.
"""

from .visualizer import EnhancedDeadlockVisualizer
from .web_visualizer import WebDeadlockVisualizer
from .animation_utils import AnimationType, LayoutType
from .themes import ColorThemes

# Backward compatibility
DeadlockVisualizer = EnhancedDeadlockVisualizer

__all__ = [
    'EnhancedDeadlockVisualizer', 
    'WebDeadlockVisualizer',
    'DeadlockVisualizer',  # For backward compatibility
    'AnimationType', 
    'LayoutType',
    'ColorThemes'
]