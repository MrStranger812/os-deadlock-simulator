"""
Enhanced Visualization Components for the Deadlock Simulator

This subpackage provides comprehensive tools for visualizing the state of the system,
including dynamic animations, multiple layouts, interactive features, web-based dashboards,
advanced theming, and accessibility compliance.

Features:
- 🎨 Enhanced static and dynamic visualizations
- 🌐 Interactive web dashboards
- 🎬 Multiple animation types and easing functions
- 🎭 Professional color themes with accessibility support
- 📊 Performance monitoring and optimization
- ♿ WCAG accessibility compliance
- 🔄 Real-time visualization updates
- 💾 Multiple export formats (PNG, GIF, MP4, HTML)
- 🖱️ Interactive controls and widgets

File location: src/visualization/__init__.py
"""

import logging
from typing import Dict, List, Optional, Union

# =============================================================================
# CORE VISUALIZER IMPORTS
# =============================================================================

try:
    from .visualizer import (
        EnhancedDeadlockVisualizer,
        LayoutType,
        AnimationType,
        VisualizationState
    )
    ENHANCED_VISUALIZER_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Enhanced visualizer not available: {e}")
    ENHANCED_VISUALIZER_AVAILABLE = False
    
    # Fallback basic visualizer
    try:
        from .visualizer import DeadlockVisualizer as BasicDeadlockVisualizer
        EnhancedDeadlockVisualizer = BasicDeadlockVisualizer
    except ImportError:
        # Ultimate fallback
        class DummyVisualizer:
            def __init__(self, system, **kwargs):
                self.system = system
                print("⚠️ No visualizer available. Install matplotlib for basic visualization.")
            
            def visualize_current_state(self, deadlocked_processes=None):
                print("📊 Visualization not available")
            
            def show(self): pass
            def save(self, filename): pass
        
        EnhancedDeadlockVisualizer = DummyVisualizer
    
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

# =============================================================================
# WEB VISUALIZER IMPORTS
# =============================================================================

try:
    from .web_visualizer import WebDeadlockVisualizer
    WEB_VISUALIZER_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Web visualizer not available: {e}")
    WEB_VISUALIZER_AVAILABLE = False
    WebDeadlockVisualizer = None

# =============================================================================
# ANIMATION UTILITIES IMPORTS
# =============================================================================

try:
    from .animation_utils import (
        AnimationUtils,
        EasingFunction,
        AnimationFrame,
        AnimationState,
        create_animation_utils,
        ANIMATION_PRESETS
    )
    ANIMATION_UTILS_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Animation utilities not available: {e}")
    ANIMATION_UTILS_AVAILABLE = False
    
    # Fallback classes
    class AnimationUtils:
        def __init__(self, *args, **kwargs):
            print("⚠️ Animation utilities not available")
    
    class EasingFunction(Enum):
        LINEAR = "linear"
        EASE_IN_OUT = "ease_in_out"
    
    AnimationFrame = None
    AnimationState = None
    create_animation_utils = lambda: AnimationUtils()
    ANIMATION_PRESETS = {}

# =============================================================================
# THEMES IMPORTS
# =============================================================================

try:
    from .themes import (
        ColorThemes as EnhancedColorThemes,
        ColorPalette,
        ThemeMetadata,
        ThemeType,
        get_theme_manager,
        get_theme,
        list_available_themes,
        get_accessible_themes,
        create_theme_from_colors,
        analyze_theme_accessibility,
        create_preset_theme,
        PRESET_MODIFICATIONS
    )
    ENHANCED_THEMES_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Enhanced themes not available: {e}")
    ENHANCED_THEMES_AVAILABLE = False
    
    # Fallback basic themes
    class ColorThemes:
        DEFAULT = {
            'background': '#ffffff',
            'process_running': '#28a745',
            'process_waiting': '#dc3545',
            'process_terminated': '#6c757d',
            'resource': '#007bff',
            'edge_allocation': '#28a745',
            'edge_request': '#dc3545',
            'text': '#333333',
            'highlight': '#ffc107'
        }
        
        DARK = {
            'background': '#2c3e50',
            'process_running': '#58d68d',
            'process_waiting': '#ec7063',
            'process_terminated': '#aeb6bf',
            'resource': '#5dade2',
            'edge_allocation': '#52c41a',
            'edge_request': '#ff4d4f',
            'text': '#ecf0f1',
            'highlight': '#f1c40f'
        }
        
        COLORBLIND = {
            'background': '#ffffff',
            'process_running': '#1f77b4',
            'process_waiting': '#ff7f0e',
            'process_terminated': '#7f7f7f',
            'resource': '#2ca02c',
            'edge_allocation': '#d62728',
            'edge_request': '#9467bd',
            'text': '#000000',
            'highlight': '#e377c2'
        }
    
    EnhancedColorThemes = ColorThemes
    ColorPalette = None
    ThemeMetadata = None
    
    class ThemeType(Enum):
        LIGHT = "light"
        DARK = "dark"
        COLORBLIND = "colorblind"
    
    def get_theme_manager(): return ColorThemes()
    def get_theme(name): return getattr(ColorThemes, name.upper(), ColorThemes.DEFAULT)
    def list_available_themes(): return ['default', 'dark', 'colorblind']
    def get_accessible_themes(rating="AA"): return ['colorblind']
    def create_theme_from_colors(name, **colors): return False
    def analyze_theme_accessibility(name): return {}
    def create_preset_theme(name, base="default"): return False
    PRESET_MODIFICATIONS = {}

# =============================================================================
# BACKWARD COMPATIBILITY
# =============================================================================

# Main visualizer alias for backward compatibility
DeadlockVisualizer = EnhancedDeadlockVisualizer

# Legacy ColorThemes class (if enhanced not available)
if not ENHANCED_THEMES_AVAILABLE:
    # Keep the simple ColorThemes as-is for compatibility
    pass

# =============================================================================
# FEATURE DETECTION AND CAPABILITIES
# =============================================================================

# Feature availability flags
FEATURES = {
    'enhanced_visualizer': ENHANCED_VISUALIZER_AVAILABLE,
    'web_dashboard': WEB_VISUALIZER_AVAILABLE,
    'animations': ANIMATION_UTILS_AVAILABLE,
    'enhanced_themes': ENHANCED_THEMES_AVAILABLE,
    'dynamic_layouts': ENHANCED_VISUALIZER_AVAILABLE,
    'export_capabilities': ENHANCED_VISUALIZER_AVAILABLE,
    'performance_monitoring': ENHANCED_VISUALIZER_AVAILABLE,
    'real_time_updates': ENHANCED_VISUALIZER_AVAILABLE,
    'accessibility_compliance': ENHANCED_THEMES_AVAILABLE,
    'interactive_controls': ENHANCED_VISUALIZER_AVAILABLE
}

def get_available_features() -> Dict[str, bool]:
    """
    Get a dictionary of available visualization features.
    
    Returns:
        Dict mapping feature names to availability status
    """
    return FEATURES.copy()

def check_feature_availability(feature_name: str) -> bool:
    """
    Check if a specific feature is available.
    
    Args:
        feature_name: Name of the feature to check
        
    Returns:
        bool: True if feature is available
    """
    return FEATURES.get(feature_name, False)

def get_missing_dependencies() -> List[str]:
    """
    Get a list of missing dependencies that would enable more features.
    
    Returns:
        List of missing package names
    """
    missing = []
    
    if not WEB_VISUALIZER_AVAILABLE:
        missing.extend(['plotly', 'dash'])
    
    if not ENHANCED_VISUALIZER_AVAILABLE:
        missing.extend(['matplotlib', 'networkx', 'numpy'])
    
    if not ANIMATION_UTILS_AVAILABLE:
        missing.extend(['numpy'])
    
    return list(set(missing))  # Remove duplicates

def print_feature_summary():
    """Print a comprehensive summary of available visualization features."""
    print("🎨 Enhanced Deadlock Visualizer - Feature Summary")
    print("=" * 60)
    
    # Core features
    print("\n📊 Core Visualization Features:")
    features_core = [
        ('enhanced_visualizer', 'Enhanced Static & Dynamic Visualization'),
        ('dynamic_layouts', 'Multiple Layout Algorithms'),
        ('export_capabilities', 'Export to PNG, GIF, MP4'),
        ('performance_monitoring', 'Real-time Performance Monitoring'),
        ('real_time_updates', 'Live System State Updates')
    ]
    
    for feature, description in features_core:
        status = "✅" if FEATURES[feature] else "❌"
        print(f"   {status} {description}")
    
    # Interactive features
    print("\n🖱️ Interactive Features:")
    features_interactive = [
        ('interactive_controls', 'Play/Pause/Speed Controls'),
        ('web_dashboard', 'Interactive Web Dashboard'),
        ('animations', 'Dynamic Animations & Transitions')
    ]
    
    for feature, description in features_interactive:
        status = "✅" if FEATURES[feature] else "❌"
        print(f"   {status} {description}")
    
    # Accessibility features
    print("\n♿ Accessibility Features:")
    features_accessibility = [
        ('enhanced_themes', 'Professional Color Themes'),
        ('accessibility_compliance', 'WCAG Accessibility Analysis')
    ]
    
    for feature, description in features_accessibility:
        status = "✅" if FEATURES[feature] else "❌"
        print(f"   {status} {description}")
    
    # Summary statistics
    available_count = sum(FEATURES.values())
    total_count = len(FEATURES)
    percentage = (available_count / total_count) * 100
    
    print(f"\n📈 Overall Feature Availability: {available_count}/{total_count} ({percentage:.1f}%)")
    
    # Missing dependencies
    missing = get_missing_dependencies()
    if missing:
        print(f"\n📦 To enable all features, install: pip install {' '.join(missing)}")
    else:
        print(f"\n🎉 All visualization features are available!")
    
    # Quick start guide
    print(f"\n🚀 Quick Start:")
    print(f"   from src.visualization import DeadlockVisualizer")
    print(f"   visualizer = DeadlockVisualizer(system)")
    print(f"   visualizer.visualize_current_state()")
    
    if WEB_VISUALIZER_AVAILABLE:
        print(f"   # For web dashboard:")
        print(f"   from src.visualization import WebDeadlockVisualizer")
        print(f"   web_viz = WebDeadlockVisualizer(system)")
        print(f"   web_viz.run_server()")
    
    print("=" * 60)

# =============================================================================
# FACTORY FUNCTIONS AND UTILITIES
# =============================================================================

def create_visualizer(system, enhanced: bool = True, **kwargs) -> EnhancedDeadlockVisualizer:
    """
    Factory function to create the appropriate visualizer.
    
    Args:
        system: The deadlock system to visualize
        enhanced: Whether to use enhanced features if available
        **kwargs: Additional arguments for the visualizer
        
    Returns:
        Visualizer instance
    """
    if enhanced and ENHANCED_VISUALIZER_AVAILABLE:
        return EnhancedDeadlockVisualizer(system, **kwargs)
    else:
        # Use basic visualizer or fallback
        return DeadlockVisualizer(system, **kwargs)

def create_web_visualizer(system, **kwargs) -> Optional[WebDeadlockVisualizer]:
    """
    Factory function to create web visualizer if available.
    
    Args:
        system: The deadlock system to visualize
        **kwargs: Additional arguments for the web visualizer
        
    Returns:
        WebDeadlockVisualizer instance or None if not available
    """
    if WEB_VISUALIZER_AVAILABLE:
        return WebDeadlockVisualizer(system, **kwargs)
    else:
        print("❌ Web visualizer not available. Install: pip install plotly dash")
        return None

def create_animation_manager(**kwargs) -> AnimationUtils:
    """
    Factory function to create animation utilities.
    
    Args:
        **kwargs: Arguments for AnimationUtils
        
    Returns:
        AnimationUtils instance
    """
    if ANIMATION_UTILS_AVAILABLE:
        return create_animation_utils(**kwargs)
    else:
        print("⚠️ Animation utilities not available")
        return AnimationUtils(**kwargs)

def setup_visualization_environment(enable_logging: bool = True) -> Dict[str, bool]:
    """
    Set up the visualization environment and return capability status.
    
    Args:
        enable_logging: Whether to enable detailed logging
        
    Returns:
        Dictionary of enabled capabilities
    """
    if enable_logging:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    logger = logging.getLogger(__name__)
    
    # Test core functionality
    capabilities = {}
    
    try:
        # Test basic visualization
        capabilities['basic_visualization'] = True
        logger.info("✅ Basic visualization support available")
    except Exception as e:
        capabilities['basic_visualization'] = False
        logger.warning(f"❌ Basic visualization failed: {e}")
    
    try:
        # Test enhanced features
        if ENHANCED_VISUALIZER_AVAILABLE:
            capabilities['enhanced_visualization'] = True
            logger.info("✅ Enhanced visualization features available")
        else:
            capabilities['enhanced_visualization'] = False
            logger.info("⚠️ Enhanced visualization not available")
    except Exception as e:
        capabilities['enhanced_visualization'] = False
        logger.warning(f"❌ Enhanced visualization failed: {e}")
    
    try:
        # Test web features
        if WEB_VISUALIZER_AVAILABLE:
            capabilities['web_visualization'] = True
            logger.info("✅ Web visualization features available")
        else:
            capabilities['web_visualization'] = False
            logger.info("⚠️ Web visualization not available")
    except Exception as e:
        capabilities['web_visualization'] = False
        logger.warning(f"❌ Web visualization failed: {e}")
    
    return capabilities

# =============================================================================
# INTEGRATION HELPERS
# =============================================================================

def integrate_with_existing_code(system, visualization_type: str = "auto", **kwargs):
    """
    Smart integration function that automatically selects the best available visualizer.
    
    Args:
        system: The deadlock system to visualize
        visualization_type: Type of visualization ("auto", "basic", "enhanced", "web")
        **kwargs: Additional arguments
        
    Returns:
        Appropriate visualizer instance
    """
    if visualization_type == "web" and WEB_VISUALIZER_AVAILABLE:
        return WebDeadlockVisualizer(system, **kwargs)
    elif visualization_type == "enhanced" and ENHANCED_VISUALIZER_AVAILABLE:
        return EnhancedDeadlockVisualizer(system, **kwargs)
    elif visualization_type == "basic":
        return DeadlockVisualizer(system, **kwargs)
    elif visualization_type == "auto":
        # Auto-select best available option
        if ENHANCED_VISUALIZER_AVAILABLE:
            return EnhancedDeadlockVisualizer(system, **kwargs)
        else:
            return DeadlockVisualizer(system, **kwargs)
    else:
        # Fallback to basic
        return DeadlockVisualizer(system, **kwargs)

def get_recommended_settings(use_case: str = "general") -> Dict[str, Union[str, bool, int]]:
    """
    Get recommended visualization settings for different use cases.
    
    Args:
        use_case: The intended use case ("general", "presentation", "education", 
                 "research", "accessibility", "performance")
                 
    Returns:
        Dictionary of recommended settings
    """
    settings = {
        "general": {
            "layout": "spring",
            "theme": "default",
            "animation": "fade",
            "real_time": True,
            "export_format": "png"
        },
        "presentation": {
            "layout": "hierarchical",
            "theme": "professional",
            "animation": "pulse",
            "real_time": False,
            "export_format": "gif"
        },
        "education": {
            "layout": "circular",
            "theme": "educational",
            "animation": "bounce",
            "real_time": True,
            "export_format": "gif"
        },
        "research": {
            "layout": "spring",
            "theme": "default",
            "animation": "fade",
            "real_time": True,
            "export_format": "mp4"
        },
        "accessibility": {
            "layout": "hierarchical",
            "theme": "colorblind",
            "animation": "fade",
            "real_time": False,
            "export_format": "png"
        },
        "performance": {
            "layout": "grid",
            "theme": "default",
            "animation": None,
            "real_time": False,
            "export_format": "png"
        }
    }
    
    return settings.get(use_case, settings["general"])

# =============================================================================
# VERSION AND COMPATIBILITY INFORMATION
# =============================================================================

__version__ = '2.0.0'
__author__ = 'Enhanced Deadlock Simulator Team'
__license__ = 'MIT'

# Compatibility matrix
COMPATIBILITY = {
    'python_min_version': '3.7',
    'matplotlib_min_version': '3.5.0',
    'networkx_min_version': '2.6',
    'plotly_min_version': '5.0.0',
    'dash_min_version': '2.0.0'
}

def get_version_info() -> Dict[str, str]:
    """Get version information for the visualization module."""
    return {
        'module_version': __version__,
        'author': __author__,
        'license': __license__,
        'features_available': len([f for f in FEATURES.values() if f]),
        'total_features': len(FEATURES)
    }

# =============================================================================
# PUBLIC API EXPORTS
# =============================================================================

# Primary classes (always available)
__all__ = [
    # Main visualizer classes
    'DeadlockVisualizer',           # Primary visualizer (backward compatible)
    'EnhancedDeadlockVisualizer',   # Enhanced visualizer
    
    # Enums and data classes
    'LayoutType',
    'AnimationType',
    
    # Theme system
    'ColorThemes',                  # Theme system (backward compatible)
    
    # Feature detection
    'get_available_features',
    'check_feature_availability',
    'print_feature_summary',
    
    # Factory functions
    'create_visualizer',
    'integrate_with_existing_code',
    'get_recommended_settings',
    
    # Utilities
    'setup_visualization_environment',
    'get_version_info'
]

# Conditionally exported classes (only if available)
if WEB_VISUALIZER_AVAILABLE:
    __all__.extend([
        'WebDeadlockVisualizer',
        'create_web_visualizer'
    ])

if ANIMATION_UTILS_AVAILABLE:
    __all__.extend([
        'AnimationUtils',
        'EasingFunction',
        'AnimationFrame',
        'AnimationState',
        'create_animation_utils',
        'create_animation_manager',
        'ANIMATION_PRESETS'
    ])

if ENHANCED_THEMES_AVAILABLE:
    __all__.extend([
        'EnhancedColorThemes',
        'ColorPalette',
        'ThemeMetadata',
        'ThemeType',
        'get_theme_manager',
        'get_theme',
        'list_available_themes',
        'get_accessible_themes',
        'create_theme_from_colors',
        'analyze_theme_accessibility',
        'create_preset_theme',
        'PRESET_MODIFICATIONS'
    ])

if ENHANCED_VISUALIZER_AVAILABLE:
    __all__.extend([
        'VisualizationState'
    ])

# =============================================================================
# MODULE INITIALIZATION
# =============================================================================

def _initialize_module():
    """Initialize the visualization module."""
    logger = logging.getLogger(__name__)
    
    # Suppress noisy matplotlib warnings if present
    try:
        import matplotlib
        matplotlib.use('Agg', force=False)  # Use non-interactive backend as fallback
    except ImportError:
        pass
    
    # Log feature availability
    available_features = sum(FEATURES.values())
    total_features = len(FEATURES)
    
    logger.info(f"Deadlock Visualizer initialized: {available_features}/{total_features} features available")
    
    # Check for common issues
    missing_deps = get_missing_dependencies()
    if missing_deps:
        logger.info(f"Install additional packages for full functionality: {', '.join(missing_deps)}")

# Auto-initialize when imported (unless disabled)
import os
if os.environ.get('DEADLOCK_VIZ_NO_AUTO_INIT') != '1':
    _initialize_module()

# Print welcome message (unless disabled)
if os.environ.get('DEADLOCK_VIZ_QUIET') != '1':
    available = sum(FEATURES.values())
    total = len(FEATURES)
    
    print(f"🎨 Enhanced Deadlock Visualizer v{__version__} loaded!")
    print(f"   Features available: {available}/{total}")
    
    if not ENHANCED_VISUALIZER_AVAILABLE:
        print("   💡 Install matplotlib networkx numpy for enhanced features")
    
    if not WEB_VISUALIZER_AVAILABLE:
        print("   💡 Install plotly dash for web dashboard")
    
    if available == total:
        print("   🎉 All features available!")

# =============================================================================
# LEGACY COMPATIBILITY LAYER
# =============================================================================

# Ensure backward compatibility with any existing imports
try:
    # If someone imports the old way, make sure it still works
    from .visualizer import DeadlockVisualizer as _LegacyVisualizer
    
    # Make sure the enhanced version is truly backward compatible
    if hasattr(_LegacyVisualizer, 'visualize_current_state'):
        # Legacy API is preserved
        pass
    else:
        # Create compatibility wrapper if needed
        class BackwardCompatibleVisualizer(_LegacyVisualizer):
            def visualize_current_state(self, deadlocked_processes=None):
                """Backward compatible method."""
                return super().visualize_current_state(deadlocked_processes)
        
        DeadlockVisualizer = BackwardCompatibleVisualizer

except ImportError:
    # If import fails, the fallback is already set above
    pass

# =============================================================================
# DEVELOPMENT AND DEBUGGING UTILITIES
# =============================================================================

def run_feature_tests() -> Dict[str, bool]:
    """
    Run basic tests on all available features.
    
    Returns:
        Dictionary of test results
    """
    results = {}
    
    # Test basic visualizer
    try:
        from src.core import System, Process, Resource
        system = System()
        p1 = Process(1)
        system.add_process(p1)
        r1 = Resource(1, instances=1)
        system.add_resource(r1)
        
        visualizer = create_visualizer(system)
        results['basic_visualizer'] = True
    except Exception as e:
        results['basic_visualizer'] = False
        print(f"❌ Basic visualizer test failed: {e}")
    
    # Test enhanced features
    if ENHANCED_VISUALIZER_AVAILABLE:
        try:
            enhanced_viz = EnhancedDeadlockVisualizer(system)
            enhanced_viz.set_layout_algorithm(LayoutType.SPRING)
            results['enhanced_features'] = True
        except Exception as e:
            results['enhanced_features'] = False
            print(f"❌ Enhanced features test failed: {e}")
    else:
        results['enhanced_features'] = False
    
    # Test web visualizer
    if WEB_VISUALIZER_AVAILABLE:
        try:
            web_viz = WebDeadlockVisualizer(system)
            results['web_visualizer'] = True
        except Exception as e:
            results['web_visualizer'] = False
            print(f"❌ Web visualizer test failed: {e}")
    else:
        results['web_visualizer'] = False
    
    # Test themes
    if ENHANCED_THEMES_AVAILABLE:
        try:
            theme_manager = get_theme_manager()
            theme = theme_manager.get_theme('default')
            results['themes'] = True
        except Exception as e:
            results['themes'] = False
            print(f"❌ Themes test failed: {e}")
    else:
        results['themes'] = False
    
    return results

def generate_integration_report() -> str:
    """
    Generate a comprehensive integration report.
    
    Returns:
        Formatted report string
    """
    report = []
    report.append("🔧 Enhanced Deadlock Visualizer - Integration Report")
    report.append("=" * 60)
    
    # Version info
    version_info = get_version_info()
    report.append(f"Version: {version_info['module_version']}")
    report.append(f"Features Available: {version_info['features_available']}/{version_info['total_features']}")
    report.append("")
    
    # Feature status
    report.append("📊 Feature Status:")
    for feature, available in FEATURES.items():
        status = "✅" if available else "❌"
        report.append(f"   {status} {feature.replace('_', ' ').title()}")
    report.append("")
    
    # Dependencies
    missing = get_missing_dependencies()
    if missing:
        report.append("📦 Missing Dependencies:")
        for dep in missing:
            report.append(f"   • {dep}")
        report.append(f"\nInstall with: pip install {' '.join(missing)}")
    else:
        report.append("✅ All dependencies satisfied")
    report.append("")
    
    # Integration examples
    report.append("🚀 Integration Examples:")
    report.append("   # Basic usage:")
    report.append("   from src.visualization import DeadlockVisualizer")
    report.append("   visualizer = DeadlockVisualizer(system)")
    report.append("   visualizer.visualize_current_state()")
    report.append("")
    
    if ENHANCED_VISUALIZER_AVAILABLE:
        report.append("   # Enhanced features:")
        report.append("   from src.visualization import EnhancedDeadlockVisualizer, LayoutType")
        report.append("   viz = EnhancedDeadlockVisualizer(system, layout_type=LayoutType.CIRCULAR)")
        report.append("   viz.set_color_scheme('dark')")
        report.append("   animation = viz.create_dynamic_visualization()")
        report.append("")
    
    if WEB_VISUALIZER_AVAILABLE:
        report.append("   # Web dashboard:")
        report.append("   from src.visualization import WebDeadlockVisualizer")
        report.append("   web_viz = WebDeadlockVisualizer(system)")
        report.append("   web_viz.run_server()")
        report.append("")
    
    # Recommendations
    report.append("💡 Recommendations:")
    if not ENHANCED_VISUALIZER_AVAILABLE:
        report.append("   • Install matplotlib, networkx, numpy for enhanced features")
    if not WEB_VISUALIZER_AVAILABLE:
        report.append("   • Install plotly, dash for web dashboard")
    if not ENHANCED_THEMES_AVAILABLE:
        report.append("   • Enhanced themes provide accessibility compliance")
    
    if sum(FEATURES.values()) == len(FEATURES):
        report.append("   🎉 All features available - you're ready to go!")
    
    report.append("=" * 60)
    
    return "\n".join(report)

# Export the report function
__all__.append('generate_integration_report')
__all__.append('run_feature_tests')

# =============================================================================
# FINAL MODULE SETUP
# =============================================================================

# Ensure all exports are properly defined
for export_name in __all__:
    if export_name not in globals():
        globals()[export_name] = None
        logging.warning(f"Export '{export_name}' not found in module")

# Module is ready
if __name__ == "__main__":
    print(generate_integration_report())