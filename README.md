# Operating Systems Deadlock Simulator

A comprehensive Python-based simulator for demonstrating deadlock detection and resolution in multi-threaded systems with advanced visualization capabilities.

## 🎯 Overview

This project implements a complete deadlock simulation environment featuring:
- **Multiple deadlock detection algorithms** (Resource Allocation Graph, Banker's Algorithm)
- **Deadlock resolution strategies** (Process Termination, Resource Preemption, Rollback)
- **Advanced visualization system** with animations, multiple layouts, and web dashboard
- **Educational test scenarios** (Simple deadlock, Dining Philosophers, Complex allocation)

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Setup
```bash
# Clone the repository
git clone <repository-url>
cd os-deadlock-simulator

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -m src.main --help
```

## 🚀 Quick Start

### Basic Usage
```bash
# Run simple deadlock scenario with visualization
python -m src.main --scenario simple --visualize

# Run dining philosophers with enhanced features
python -m src.main --scenario dining-5 --enhanced --layout circular --theme dark

# Launch interactive web dashboard
python -m src.main --web
```

### Running Test Scenarios
```bash
# Run all test scenarios
python tests/test_scenarios.py

# Run specific scenario with visualization
python tests/run_individual_test.py simple --visualize

# Run dining philosophers (5 philosophers) with all visualizations
python tests/run_individual_test.py dining-5 --visualize --viz-types all
```

## 🎨 Visualization Features

### Static Visualizations
- **Resource Allocation Graph**: Shows processes, resources, and their relationships
- **System State View**: Current state with detailed process and resource information
- **Detection Steps**: Step-by-step deadlock detection process
- **Resolution Steps**: Visualization of deadlock resolution strategies

### Enhanced Features
- **Multiple Layouts**: Spring, Circular, Hierarchical, Grid, Kamada-Kawai
- **Color Themes**: Default, Dark, High-Contrast, Colorblind-friendly
- **Dynamic Animations**: Fade, Pulse, Bounce, Rotate, Glow effects
- **Export Options**: PNG, GIF, MP4, HTML formats

### Web Dashboard
- **Interactive Controls**: Real-time layout and theme switching
- **Live Metrics**: System performance monitoring
- **Responsive Design**: Works on desktop and mobile
- **Export Features**: Static HTML generation

## 📝 Command Reference

### Main Commands

| Command | Description | Example |
|---------|-------------|---------|
| `--scenario` | Choose simulation scenario | `--scenario dining-5` |
| `--visualize` | Enable basic visualization | `--visualize` |
| `--enhanced` | Use enhanced visualization features | `--enhanced` |
| `--web` | Launch web dashboard | `--web --port 8080` |
| `--layout` | Set layout algorithm | `--layout circular` |
| `--theme` | Set color theme | `--theme dark` |
| `--animation` | Set animation type | `--animation pulse` |
| `--export` | Export format | `--export gif` |
| `--output-dir` | Set output directory | `--output-dir ./results` |

### Available Scenarios

| Scenario | Description | Processes | Resources |
|----------|-------------|-----------|-----------|
| `simple` | Two-process circular deadlock | 2 | 2 |
| `dining-3` | Dining philosophers (3) | 3 | 3 |
| `dining-5` | Dining philosophers (5) | 5 | 5 |
| `dining-7` | Dining philosophers (7) | 7 | 7 |
| `complex` | Multi-resource allocation | 4 | 3 |
| `no-deadlock` | False positive test | 3 | 3 |
| `chain` | Chain deadlock pattern | 3 | 3 |

### Layout Options

| Layout | Best For | Description |
|--------|----------|-------------|
| `spring` | General use | Force-directed layout (default) |
| `circular` | Dining philosophers | Circular arrangement |
| `hierarchical` | Process-resource separation | Processes top, resources bottom |
| `grid` | Large systems | Organized grid pattern |
| `kamada_kawai` | Complex relationships | High-quality positioning |

### Color Themes

| Theme | Description | Accessibility |
|-------|-------------|---------------|
| `default` | Clean, professional light theme | AA compliant |
| `dark` | Modern dark theme for low light | AA compliant |
| `high_contrast` | Maximum contrast for visibility | AAA compliant |
| `colorblind` | Optimized for color vision deficiency | AAA compliant |
| `educational` | Soft, friendly colors for teaching | AA compliant |

## 💻 Usage Examples

### Basic Examples

```bash
# Simple deadlock with basic visualization
python -m src.main --scenario simple --visualize

# Dining philosophers with dark theme
python -m src.main --scenario dining-5 --enhanced --theme dark --layout circular

# Complex scenario with animation export
python -m src.main --scenario complex --enhanced --animation pulse --export gif

# High contrast theme for accessibility
python -m src.main --scenario simple --enhanced --theme high_contrast
```

### Advanced Examples

```bash
# Full-featured visualization with custom output
python -m src.main \
  --scenario dining-5 \
  --enhanced \
  --layout circular \
  --theme dark \
  --animation pulse \
  --export gif \
  --output-dir ./presentations

# Web dashboard with custom port
python -m src.main --web --port 8080

# Educational mode with step-by-step visualization
python tests/run_individual_test.py dining-5 \
  --visualize \
  --viz-types detection,resolution
```

### Testing Examples

```bash
# Run all test scenarios
python tests/test_scenarios.py

# Test specific scenario with full visualization
python tests/run_individual_test.py simple --visualize --viz-types all

# Test multiple scenarios
for scenario in simple dining-3 dining-5 complex; do
  python tests/run_individual_test.py $scenario --visualize
done
```

## 🔧 Configuration

### Environment Variables
```bash
# Disable auto-initialization messages
export DEADLOCK_VIZ_QUIET=1

# Disable automatic matplotlib backend selection
export DEADLOCK_VIZ_NO_AUTO_INIT=1
```

### Custom Themes
```python
from src.visualization import create_theme_from_colors

# Create custom theme
create_theme_from_colors(
    "my_theme",
    process_running="#00ff00",
    process_waiting="#ff9900",
    background="#f0f0f0"
)

# Use custom theme
python -m src.main --scenario simple --enhanced --theme my_theme
```

## 📊 Output Files

The simulator generates various output files in the specified output directory:

### Generated Files
- `deadlock_visualization.png` - Static visualization
- `system_animation.gif` - Animated sequence
- `deadlock_report.html` - Interactive web report
- `performance_metrics.json` - System performance data
- `test_results.json` - Test scenario results

### File Structure
```
output_directory/
├── visualizations/
│   ├── static/
│   │   ├── initial_state.png
│   │   ├── deadlock_detected.png
│   │   └── resolution_applied.png
│   ├── animations/
│   │   ├── deadlock_sequence.gif
│   │   └── resolution_process.mp4
│   └── web/
│       ├── dashboard.html
│       └── interactive_report.html
├── reports/
│   ├── detection_analysis.json
│   ├── resolution_results.json
│   └── performance_report.json
└── logs/
    ├── simulation.log
    └── performance.log
```

## 🎓 Educational Use

### For Teaching
```bash
# Step-by-step deadlock detection
python tests/run_individual_test.py simple --visualize --viz-types detection

# Interactive dining philosophers demonstration
python -m src.main --scenario dining-5 --web --theme educational

# Accessibility-compliant presentation
python -m src.main --scenario complex --enhanced --theme colorblind --export png
```

### For Research
```bash
# Performance analysis with metrics
python -m src.main --scenario complex --enhanced --export-metrics

# Batch testing with different parameters
python scripts/batch_test.py --scenarios all --themes all --layouts all
```

## 🐛 Troubleshooting

### Common Issues

**ImportError for visualization modules**
```bash
pip install matplotlib networkx plotly dash
```

**Web dashboard not starting**
```bash
# Check port availability
python -m src.main --web --port 8081

# Install web dependencies
pip install plotly dash kaleido
```

**Animation export failing**
```bash
# Install video codecs
pip install imageio[ffmpeg]

# Use alternative format
python -m src.main --scenario simple --enhanced --export png
```

**Layout computation errors**
```bash
# Use stable layout
python -m src.main --scenario simple --enhanced --layout grid

# Install scientific computing libraries
pip install scipy numpy
```

### Performance Tips

- Use `--layout grid` for large systems (10+ processes)
- Use `--theme dark` to reduce eye strain during long sessions
- Export as PNG for high-quality static images
- Export as GIF for presentations (smaller file size)
- Use web dashboard for interactive demonstrations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes with proper tests
4. Commit changes: `git commit -m 'Add amazing feature'`
5. Push to branch: `git push origin feature/amazing-feature`
6. Submit a Pull Request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Run code quality checks
python -m flake8 src/
python -m black src/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📚 References

- **Deadlock Detection**: Coffman, E. G., Elphick, M., & Shoshani, A. (1971)
- **Banker's Algorithm**: Dijkstra, E. W. (1965)
- **Dining Philosophers**: Dijkstra, E. W. (1965)

## 👥 Team

- **Project Manager/Core Developer**: [Member 1]
- **Deadlock Detection Developer**: [Member 2]  
- **Deadlock Resolution Developer**: [Member 3]
- **Test Engineer**: [Member 4]
- **Visualization Developer**: [Member 5]
- **Documentation Specialist**: [Member 6]

---

**For more examples and advanced usage, see the [examples/](examples/) directory.**
