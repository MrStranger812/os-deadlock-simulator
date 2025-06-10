# Project Structure and Organization

## 📁 Directory Structure

```
os-deadlock-simulator/
├── 📄 README.md                    # Main documentation
├── 📄 requirements.txt             # Python dependencies
├── 📄 LICENSE                      # MIT License
├── 📄 .gitignore                   # Git ignore patterns
├── 📄 Project_tree.py              # Project tree generator
│
├── 📂 src/                         # Source code
│   ├── 📄 __init__.py
│   ├── 📄 main.py                  # Main entry point
│   │
│   ├── 📂 core/                    # Core system components
│   │   ├── 📄 __init__.py
│   │   ├── 📄 process.py           # Process class
│   │   ├── 📄 resource.py          # Resource class
│   │   └── 📄 system.py            # System manager
│   │
│   ├── 📂 detection/               # Deadlock detection algorithms
│   │   ├── 📄 __init__.py
│   │   └── 📄 detector.py          # DeadlockDetector class
│   │
│   ├── 📂 resolution/              # Deadlock resolution strategies
│   │   ├── 📄 __init__.py
│   │   └── 📄 resolver.py          # DeadlockResolver class
│   │
│   └── 📂 visualization/           # Enhanced visualization system
│       ├── 📄 __init__.py          # Main visualization interface
│       ├── 📄 core_visualizer.py   # Basic matplotlib visualizer
│       ├── 📄 enhanced_visualizer.py # Advanced features
│       ├── 📄 themes.py            # Color themes and accessibility
│       └── 📄 animation_utils.py   # Animation utilities
│
├── 📂 tests/                       # Test scenarios and utilities
│   ├── 📄 __init__.py
│   ├── 📄 test_scenarios.py        # Test scenario definitions
│   └── 📄 run_individual_test.py   # Individual test runner
│
├── 📂 examples/                    # Usage examples
│   ├── 📄 basic_usage.py           # Simple examples
│   ├── 📄 advanced_features.py     # Advanced visualization
│   
│
├── 📂 docs/                        # Documentation
│   ├── 📄 enhanced_features.md     # Feature documentation
│   ├── 📄 architecture.md          # System architecture
│   └── 📄 project-plan.md          # Project planning
│
└── 📂 output/                      # Generated files (created at runtime)
    ├── 📂 visualizations/          # Generated visualizations
    ├── 📂 reports/                 # Analysis reports
    └── 📂 logs/                    # Simulation logs
```

## 🏗️ Architecture Overview

### Core Components

#### System Layer (`src/core/`)
- **Process**: Represents individual processes with resource requests/holdings
- **Resource**: Manages resource instances and allocation tracking
- **System**: Central coordinator for processes and resources

#### Detection Layer (`src/detection/`)
- **DeadlockDetector**: Implements multiple detection algorithms
  - Resource Allocation Graph (RAG) analysis
  - Banker's Algorithm
  - Comparative analysis and validation

#### Resolution Layer (`src/resolution/`)
- **DeadlockResolver**: Implements resolution strategies
  - Process termination
  - Resource preemption
  - Process rollback
  - Priority-based selection

#### Visualization Layer (`src/visualization/`)
- **Modular Design**: Clean separation of concerns
- **Progressive Enhancement**: Basic → Enhanced features
- **Graceful Degradation**: Falls back when dependencies missing

### Visualization Architecture

```
┌─────────────────────────────────────────────────────────┐
│                 Visualization Layer                     │
├─────────────────────────────────────────────────────────┤
│  📄 __init__.py        │  Main interface & feature      │
│                        │  detection                     │
├─────────────────────────────────────────────────────────┤
│  📄 core_visualizer.py │  Basic matplotlib             │
│                        │  Static visualizations        │
├─────────────────────────────────────────────────────────┤
│  📄 enhanced_visualizer│  Dynamic animations           │
│     .py                │  Multiple layouts             │
│                        │  Interactive controls         │
├─────────────────────────────────────────────────────────┤
│  📄 themes.py          │  Color schemes                │
│                        │  Accessibility compliance     │
├─────────────────────────────────────────────────────────┤
│  📄 animation_utils.py │  Animation framework          │
│                        │  Easing functions             │
└─────────────────────────────────────────────────────────┘