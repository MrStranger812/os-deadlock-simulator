"""
Enhanced Visualization Module for Deadlock Simulator

This module provides comprehensive visualization capabilities including:
- Static and dynamic visualizations
- Multiple layout algorithms
- Color themes and accessibility support
- Web-based interactive dashboards
- Animation and export capabilities

Quick Start:
    from src.visualization import DeadlockVisualizer
    
    visualizer = DeadlockVisualizer(system)
    visualizer.visualize_current_state()
    visualizer.show()

Advanced Usage:
    from src.visualization import EnhancedDeadlockVisualizer, LayoutType
    
    visualizer = EnhancedDeadlockVisualizer(
        system, 
        layout_type=LayoutType.CIRCULAR
    )
    visualizer.set_color_scheme('dark')
    animation = visualizer.create_dynamic_visualization()
"""

import logging
from typing import Dict, List, Optional, Union

# Configure logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# =============================================================================
# CORE IMPORTS AND FEATURE DETECTION
# =============================================================================

# Core visualizer (always available)
try:
    from .core_visualizer import CoreDeadlockVisualizer
    CORE_AVAILABLE = True
except ImportError as e:
    logger.error(f"Core visualizer not available: {e}")
    CORE_AVAILABLE = False
    CoreDeadlockVisualizer = None

# Enhanced visualizer with advanced features
try:
    from .enhanced_visualizer import (
        EnhancedDeadlockVisualizer,
        LayoutType,
        AnimationType,
        VisualizationState
    )
    ENHANCED_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Enhanced visualizer not available: {e}")
    ENHANCED_AVAILABLE = False
    
    # Fallback enums
    from enum import Enum
    
    class LayoutType(Enum):
        SPRING = "spring"
        CIRCULAR = "circular"
        HIERARCHICAL = "hierarchical"
        GRID = "grid"
    
    class AnimationType(Enum):
        FADE = "fade"
        PULSE = "pulse"
        SCALE = "scale"
    
    EnhancedDeadlockVisualizer = CoreDeadlockVisualizer
    VisualizationState = None

# Web visualizer - REMOVED
# Web functionality has been removed to simplify the project
WEB_AVAILABLE = False
WebDeadlockVisualizer = None

# Theme system
try:
    from .themes import (
        ColorThemes,
        ThemeManager,
        get_theme,
        list_themes,
        create_custom_theme
    )
    THEMES_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Enhanced themes not available: {e}")
    THEMES_AVAILABLE = False
    
    # Fallback theme system
    class ColorThemes:
        DEFAULT = {
            'process_running': '#2ecc71',
            'process_waiting': '#e74c3c',
            'process_terminated': '#95a5a6',
            'resource': '#3498db',
            'edge_allocation': '#27ae60',
            'edge_request': '#c0392b',
            'background': '#ffffff',
            'text': '#2c3e50',
            'highlight': '#f39c12'
        }
        
        DARK = {
            'process_running': '#58d68d',
            'process_waiting': '#ec7063',
            'process_terminated': '#aeb6bf',
            'resource': '#5dade2',
            'edge_allocation': '#52c41a',
            'edge_request': '#ff4d4f',
            'background': '#2c3e50',
            'text': '#ecf0f1',
            'highlight': '#f1c40f'
        }
        
        COLORBLIND = {
            'process_running': '#1f77b4',
            'process_waiting': '#ff7f0e',
            'process_terminated': '#7f7f7f',
            'resource': '#2ca02c',
            'edge_allocation': '#d62728',
            'edge_request': '#9467bd',
            'background': '#ffffff',
            'text': '#000000',
            'highlight': '#e377c2'
        }
    
    ThemeManager = None
    def get_theme(name): return getattr(ColorThemes, name.upper(), ColorThemes.DEFAULT)
    def list_themes(): return ['default', 'dark', 'colorblind']
    def create_custom_theme(name, **colors): return False

# =============================================================================
# MAIN VISUALIZER SELECTION
# =============================================================================

# Select the best available visualizer as the main one
if ENHANCED_AVAILABLE:
    DeadlockVisualizer = EnhancedDeadlockVisualizer
    PRIMARY_VISUALIZER = "enhanced"
elif CORE_AVAILABLE:
    DeadlockVisualizer = CoreDeadlockVisualizer
    PRIMARY_VISUALIZER = "core"
else:
    # Ultimate fallback - create a minimal dummy visualizer
    class DummyVisualizer:
        def __init__(self, system, **kwargs):
            self.system = system
            print("⚠️ No visualizer available. Install matplotlib for basic visualization.")
        
        def visualize_current_state(self, deadlocked_processes=None):
            print("📊 Visualization not available - install visualization dependencies")
            self._print_text_summary(deadlocked_processes)
        
        def _print_text_summary(self, deadlocked_processes=None):
            """Print a text-based summary of the system state."""
            print(f"\n{'='*50}")
            print("SYSTEM STATE SUMMARY")
            print(f"{'='*50}")
            print(f"Time: {self.system.time}")
            print(f"Processes: {len(self.system.processes)}")
            print(f"Resources: {len(self.system.resources)}")
            
            if deadlocked_processes:
                print(f"🔴 DEADLOCK DETECTED!")
                print(f"Affected processes: P{', P'.join(map(str, deadlocked_processes))}")
            else:
                print("🟢 No deadlock detected")
            
            print(f"\nProcess Details:")
            for pid, process in self.system.processes.items():
                status_emoji = {"RUNNING": "🟢", "WAITING": "🟡", "TERMINATED": "🔴"}
                emoji = status_emoji.get(process.status, "⚪")
                print(f"  {emoji} P{pid} ({process.status})")
                
                if process.resources_held:
                    held = [f"R{r.rid}" for r in process.resources_held]
                    print(f"    🔒 Holding: {', '.join(held)}")
                
                if process.resources_requested:
                    requested = [f"R{r.rid}" for r in process.resources_requested]
                    print(f"    ⏳ Requesting: {', '.join(requested)}")
            
            print(f"\nResource Details:")
            for rid, resource in self.system.resources.items():
                print(f"  📦 R{rid}: {resource.available_instances}/{resource.total_instances} available")
                if resource.allocated_to:
                    allocated = [f"P{pid}({count})" for pid, count in resource.allocated_to.items()]
                    print(f"    🔗 Allocated to: {', '.join(allocated)}")
        
        def show(self): pass
        def save(self, filename): print(f"⚠️ Cannot save - visualization not available")
    
    DeadlockVisualizer = DummyVisualizer
    PRIMARY_VISUALIZER = "dummy"

# =============================================================================
# FEATURE AVAILABILITY
# =============================================================================

FEATURES = {
    'core_visualizer': CORE_AVAILABLE,
    'enhanced_visualizer': ENHANCED_AVAILABLE,
    'enhanced_themes': THEMES_AVAILABLE,
    'animations': ENHANCED_AVAILABLE,
    'multiple_layouts': ENHANCED_AVAILABLE,
    'export_capabilities': ENHANCED_AVAILABLE,
    'interactive_controls': ENHANCED_AVAILABLE,
    'performance_monitoring': ENHANCED_AVAILABLE
}

def get_available_features() -> Dict[str, bool]:
    """Get dictionary of available features."""
    return FEATURES.copy()

def print_feature_summary():
    """Print a summary of available visualization features."""
    print("🎨 Deadlock Visualizer - Feature Summary")
    print("=" * 50)
    print(f"Primary visualizer: {PRIMARY_VISUALIZER}")
    print()
    
    # Core features
    print("📊 Core Features:")
    core_features = [
        ('core_visualizer', 'Basic Static Visualization'),
        ('enhanced_visualizer', 'Enhanced Dynamic Visualization'),
        ('multiple_layouts', 'Multiple Layout Algorithms'),
        ('export_capabilities', 'Export to PNG, GIF, MP4')
    ]
    
    for feature, description in core_features:
        status = "✅" if FEATURES[feature] else "❌"
        print(f"   {status} {description}")
    
    # Interactive features
    print("\n🖱️ Interactive Features:")
    interactive_features = [
        ('interactive_controls', 'Play/Pause/Speed Controls'),
        ('animations', 'Dynamic Animations & Transitions')
    ]
    
    for feature, description in interactive_features:
        status = "✅" if FEATURES[feature] else "❌"
        print(f"   {status} {description}")
    
    # Theme features
    print("\n🎨 Theme Features:")
    theme_features = [
        ('enhanced_themes', 'Professional Color Themes'),
        ('enhanced_themes', 'Accessibility Compliance')
    ]
    
    for feature, description in theme_features:
        status = "✅" if FEATURES[feature] else "❌"
        print(f"   {status} {description}")
    
    # Overall statistics
    available_count = sum(FEATURES.values())
    total_count = len(FEATURES)
    percentage = (available_count / total_count) * 100
    
    print(f"\n📈 Overall: {available_count}/{total_count} features available ({percentage:.1f}%)")
    
    # Missing dependencies
    missing_deps = []
    if not ENHANCED_AVAILABLE:
        missing_deps.extend(['matplotlib', 'networkx', 'numpy'])
    if not WEB_AVAILABLE:
        missing_deps.extend(['plotly', 'dash'])
    
    if missing_deps:
        unique_deps = list(set(missing_deps))
        print(f"\n📦 Install for full features: pip install {' '.join(unique_deps)}")
    else:
        print(f"\n🎉 All features available!")
    
    print("=" * 50)

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def create_visualizer(system, visualizer_type: str = "auto", **kwargs):
    """
    Factory function to create the appropriate visualizer.
    
    Args:
        system: The deadlock system to visualize
        visualizer_type: Type of visualizer ("auto", "enhanced", "core")
        **kwargs: Additional arguments for the visualizer
        
    Returns:
        Visualizer instance
    """
    if visualizer_type == "enhanced" and ENHANCED_AVAILABLE:
        return EnhancedDeadlockVisualizer(system, **kwargs)
    elif visualizer_type == "core" and CORE_AVAILABLE:
        return CoreDeadlockVisualizer(system, **kwargs)
    elif visualizer_type == "auto":
        # Auto-select best available
        return DeadlockVisualizer(system, **kwargs)
    else:
        # Fallback to default
        return DeadlockVisualizer(system, **kwargs)

# Web visualizer creation function - REMOVED
def create_web_visualizer(system, **kwargs):
    """Web visualizer has been removed to simplify the project."""
    print("❌ Web visualizer has been removed from this version.")
    print("💡 Use enhanced visualizer with export capabilities instead:")
    print("   visualizer = create_visualizer(system, 'enhanced')")
    print("   visualizer.export_animation('output.gif', 'gif')")
    return None

def check_dependencies():
    """Check and report on visualization dependencies."""
    deps = {
        'matplotlib': 'Basic visualization',
        'networkx': 'Graph layouts and algorithms',
        'numpy': 'Numerical computations',
        'pillow': 'Image processing',
        'imageio': 'Animation export'
    }
    
    print("📦 Dependency Check:")
    print("-" * 30)
    
    for package, description in deps.items():
        try:
            __import__(package)
            print(f"✅ {package:<12} - {description}")
        except ImportError:
            print(f"❌ {package:<12} - {description} (missing)")
    
    print("-" * 30)

# =============================================================================
# VERSION AND METADATA
# =============================================================================

__version__ = '2.0.0'
__author__ = 'Deadlock Simulator Team'

def get_version_info():
    """Get version and feature information."""
    return {
        'version': __version__,
        'author': __author__,
        'primary_visualizer': PRIMARY_VISUALIZER,
        'features_available': sum(FEATURES.values()),
        'total_features': len(FEATURES),
        'enhanced_available': ENHANCED_AVAILABLE
    }

# =============================================================================
# PUBLIC API
# =============================================================================

__all__ = [
    # Main visualizer classes
    'DeadlockVisualizer',           # Primary (best available)
    'create_visualizer',            # Factory function
    
    # Feature detection
    'get_available_features',
    'print_feature_summary',
    'check_dependencies',
    'get_version_info',
    
    # Enums (always available, may be fallback)
    'LayoutType',
    'AnimationType',
    
    # Theme system
    'ColorThemes',
    'get_theme',
    'list_themes'
]

# Conditionally add advanced features
if ENHANCED_AVAILABLE:
    __all__.extend([
        'EnhancedDeadlockVisualizer',
        'VisualizationState'
    ])

if THEMES_AVAILABLE:
    __all__.extend([
        'ThemeManager',
        'create_custom_theme'
    ])

# =============================================================================
# MODULE INITIALIZATION
# =============================================================================

# Print initialization message (unless disabled)
import os
if os.environ.get('DEADLOCK_VIZ_QUIET') != '1':
    available = sum(FEATURES.values())
    total = len(FEATURES)
    print(f"🎨 Deadlock Visualizer v{__version__} loaded ({available}/{total} features)")
    
    if PRIMARY_VISUALIZER == "dummy":
        print("⚠️ Limited functionality - install: pip install matplotlib networkx")

# Validate installation
if not CORE_AVAILABLE and not ENHANCED_AVAILABLE:
    logger.warning("No visualization capabilities available. Install matplotlib and networkx.")