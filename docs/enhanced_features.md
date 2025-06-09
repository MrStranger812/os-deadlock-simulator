# Enhanced Deadlock Visualizer Features

## Overview
The Enhanced Deadlock Visualizer is a drop-in replacement for the original visualizer with advanced features for dynamic, interactive, and educational visualization of deadlock scenarios.

## Key Features

### 🎨 Multiple Layout Algorithms
- **Spring Layout**: Force-directed layout (default)
- **Circular Layout**: Perfect for dining philosophers
- **Hierarchical Layout**: Processes at top, resources at bottom  
- **Grid Layout**: Organized grid pattern
- **Kamada-Kawai Layout**: High-quality force-directed

### 🌈 Color Themes
- **Default**: Standard bright colors
- **Dark Mode**: Dark background with bright elements
- **Colorblind Friendly**: Accessibility-optimized colors

### 🎬 Dynamic Animations
- **Fade**: Opacity transitions
- **Pulse**: Size pulsing effects
- **Scale**: Scaling animations
- **Bounce**: Bouncing effects

### 💾 Export Capabilities
- **Static Images**: PNG with high DPI
- **Animated GIF**: For presentations and sharing
- **MP4 Video**: High-quality video export
- **HTML**: Interactive web pages

### 🌐 Web Dashboard
- **Interactive Controls**: Real-time layout and theme switching
- **Live Metrics**: System performance monitoring
- **Responsive Design**: Works on desktop and mobile
- **Export Options**: Static HTML generation

## Usage Examples

### Basic Usage (Drop-in Replacement)
```python
from src.visualization import EnhancedDeadlockVisualizer

# Same API as original visualizer
visualizer = EnhancedDeadlockVisualizer(system)
visualizer.visualize_current_state(deadlocked_processes)
visualizer.show()
```

### Advanced Features
```python
from src.visualization import EnhancedDeadlockVisualizer, LayoutType, AnimationType

# Enhanced visualizer with custom settings
visualizer = EnhancedDeadlockVisualizer(
    system,
    layout_type=LayoutType.CIRCULAR
)

# Configure appearance
visualizer.set_color_scheme('dark')
visualizer.animation_type = AnimationType.PULSE

# Create dynamic visualization
animation = visualizer.create_dynamic_visualization()
visualizer.export_animation("demo.gif", "gif")
```

### Web Dashboard
```python
from src.visualization import WebDeadlockVisualizer

# Create web dashboard
web_viz = WebDeadlockVisualizer(system, port=8050)

# Export static HTML
web_viz.export_static_html("deadlock.html")

# Launch interactive server
web_viz.run_server()
```

## Command Line Usage

### Basic Visualization
```bash
python -m src.main --visualize
```

### Enhanced Features
```bash
# Different layouts and themes
python -m src.main --enhanced --layout circular --theme dark

# Dynamic animations
python -m src.main --dynamic --animation pulse

# Export capabilities
python -m src.main --export gif
```

### Web Dashboard
```bash
# Launch web server
python -m src.main --web

# Export static HTML
python -m src.main --export-html
```

## Performance

The enhanced visualizer includes performance monitoring:
- **FPS Counter**: Real-time frame rate monitoring
- **Render Time**: Millisecond-precision timing
- **Memory Usage**: Resource consumption tracking
- **Cache Efficiency**: Layout computation optimization

## Backward Compatibility

The enhanced visualizer maintains 100% backward compatibility:
- ✅ Same import statements work
- ✅ Same method signatures
- ✅ Same behavior for existing code
- ✅ Existing tests work unchanged

## Installation

1. Install dependencies:
```bash
pip install plotly dash kaleido psutil pillow imageio
```

2. Replace visualizer file:
```bash
# Backup original
cp src/visualization/visualizer.py backup/

# Copy enhanced version
cp enhanced_visualizer.py src/visualization/visualizer.py
```

3. Test installation:
```bash
python -m src.main --visualize --enhanced
```

## Troubleshooting

### Import Errors
- Install missing dependencies: `pip install -r requirements.txt`
- Use basic mode if enhanced features fail

### Layout Crashes
- Try `--layout spring` as fallback
- Check system memory availability

### Web Features Not Available
- Install web dependencies: `pip install plotly dash`
- Check firewall settings for web server

### Performance Issues
- Reduce animation complexity
- Use simpler layouts for large systems
- Enable performance monitoring for diagnostics
