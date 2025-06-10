"""
Educational Visualization Module for Deadlock Simulator

This module provides clean, professional visualizations suitable for
academic presentation and educational use. Designed to generate comprehensive
educational materials including graphs, explanations, and learning guides.

Quick Start:
    from src.visualization import DeadlockVisualizer
    
    visualizer = DeadlockVisualizer(system)
    visualizer.visualize_current_state()
    visualizer.save_visualization("output.png")
    
Educational Use:
    from src.visualization import EducationalVisualizer
    
    visualizer = EducationalVisualizer(system)
    # Creates comprehensive educational materials
    files = visualizer.create_comprehensive_visualization(
        deadlocked_processes=[1, 2],
        output_dir="presentation_materials",
        scenario_name="simple_deadlock"
    )
    
    # Generated files include:
    # - Resource Allocation Graph (PNG)
    # - System State Analysis (PNG) 
    # - Allocation Matrix (PNG)
    # - Educational Explanation (TXT)
    # - Technical Report (JSON)

Features:
    ✅ Clean, professional visualizations
    ✅ Educational explanations in simple language
    ✅ Multiple visualization types (graphs, matrices, charts)
    ✅ Comprehensive learning materials
    ✅ Academic presentation ready
    ✅ Organized output directory structure
"""

import logging

# Configure logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# Core imports
try:
    from .educational_visualizer import EducationalVisualizer
    EDUCATIONAL_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Educational visualizer not available: {e}")
    EDUCATIONAL_AVAILABLE = False
    EducationalVisualizer = None

# Backward compatibility - Use educational visualizer as default
if EDUCATIONAL_AVAILABLE:
    DeadlockVisualizer = EducationalVisualizer
    PRIMARY_VISUALIZER = "educational"
else:
    # Ultimate fallback - create a minimal text-only visualizer
    class TextOnlyVisualizer:
        def __init__(self, system):
            self.system = system
            print("⚠️ Graphical visualization not available. Using text-only mode.")
            print("💡 Install matplotlib and networkx for full visualization features.")
        
        def visualize_current_state(self, deadlocked_processes=None):
            """Display text-based system summary."""
            print(f"\n{'='*50}")
            print("SYSTEM STATE SUMMARY (Text Mode)")
            print(f"{'='*50}")
            print(f"Time: {self.system.time}")
            print(f"Processes: {len(self.system.processes)}")
            print(f"Resources: {len(self.system.resources)}")
            
            if deadlocked_processes:
                print(f"\n🔴 DEADLOCK DETECTED!")
                print(f"Affected processes: P{', P'.join(map(str, deadlocked_processes))}")
            else:
                print(f"\n🟢 No deadlock detected")
            
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
        
        def save_visualization(self, filename: str, deadlocked_processes=None):
            """Save text summary to file."""
            with open(filename.replace('.png', '.txt'), 'w') as f:
                f.write("DEADLOCK SIMULATOR - TEXT SUMMARY\n")
                f.write("=" * 40 + "\n\n")
                f.write(f"System Time: {self.system.time}\n")
                f.write(f"Processes: {len(self.system.processes)}\n")
                f.write(f"Resources: {len(self.system.resources)}\n\n")
                
                if deadlocked_processes:
                    f.write("DEADLOCK DETECTED\n")
                    f.write(f"Affected: P{', P'.join(map(str, deadlocked_processes))}\n\n")
                else:
                    f.write("NO DEADLOCK DETECTED\n\n")
                
                f.write("Process States:\n")
                for pid, process in self.system.processes.items():
                    f.write(f"P{pid}: {process.status}\n")
                    if process.resources_held:
                        held = [f"R{r.rid}" for r in process.resources_held]
                        f.write(f"  Holding: {', '.join(held)}\n")
                    if process.resources_requested:
                        requested = [f"R{r.rid}" for r in process.resources_requested]
                        f.write(f"  Requesting: {', '.join(requested)}\n")
            
            print(f"📄 Text summary saved to {filename.replace('.png', '.txt')}")
        
        def create_comprehensive_visualization(self, deadlocked_processes=None, 
                                             output_dir="results", scenario_name="scenario"):
            """Create text-based educational materials."""
            from pathlib import Path
            
            output_path = Path(output_dir)
            output_path.mkdir(exist_ok=True)
            
            # Create basic text explanation
            explanation_file = output_path / "explanation.txt"
            with open(explanation_file, 'w') as f:
                f.write(f"DEADLOCK SIMULATION REPORT\n")
                f.write(f"Scenario: {scenario_name}\n")
                f.write(f"{'='*40}\n\n")
                
                if deadlocked_processes:
                    f.write("DEADLOCK DETECTED!\n")
                    f.write(f"Processes involved: P{', P'.join(map(str, deadlocked_processes))}\n\n")
                    f.write("This means these processes are stuck waiting for each other.\n")
                else:
                    f.write("NO DEADLOCK DETECTED\n")
                    f.write("The system is running safely.\n\n")
                
                f.write("\nTo see graphical visualizations, install:\n")
                f.write("pip install matplotlib networkx\n")
            
            return {"explanation": str(explanation_file)}
    
    DeadlockVisualizer = TextOnlyVisualizer
    PRIMARY_VISUALIZER = "text_only"

# =============================================================================
# FEATURE DETECTION
# =============================================================================

FEATURES = {
    'educational_visualizer': EDUCATIONAL_AVAILABLE,
    'matplotlib_available': False,
    'networkx_available': False
}

# Test for matplotlib
try:
    import matplotlib
    FEATURES['matplotlib_available'] = True
except ImportError:
    pass

# Test for networkx  
try:
    import networkx
    FEATURES['networkx_available'] = True
except ImportError:
    pass

def get_available_features():
    """Get dictionary of available features."""
    return FEATURES.copy()

def print_feature_summary():
    """Print a summary of available visualization features."""
    print("🎨 Deadlock Visualizer - Feature Summary")
    print("=" * 50)
    print(f"Primary visualizer: {PRIMARY_VISUALIZER}")
    print()
    
    # Core features
    print("📊 Available Features:")
    feature_descriptions = {
        'educational_visualizer': 'Educational Visualizations & Reports',
        'matplotlib_available': 'Matplotlib Graphics Library',
        'networkx_available': 'NetworkX Graph Analysis'
    }
    
    for feature, description in feature_descriptions.items():
        status = "✅" if FEATURES[feature] else "❌"
        print(f"   {status} {description}")
    
    # Overall status
    available_count = sum(FEATURES.values())
    total_count = len(FEATURES)
    percentage = (available_count / total_count) * 100
    
    print(f"\n📈 Overall: {available_count}/{total_count} features available ({percentage:.1f}%)")
    
    # Installation instructions if needed
    missing_deps = []
    if not FEATURES['matplotlib_available']:
        missing_deps.append('matplotlib')
    if not FEATURES['networkx_available']:
        missing_deps.append('networkx')
    
    if missing_deps:
        print(f"\n📦 Install missing dependencies:")
        print(f"   pip install {' '.join(missing_deps)}")
    else:
        print(f"\n🎉 All visualization features available!")
    
    print("=" * 50)

def check_dependencies():
    """Check and report on visualization dependencies."""
    deps = {
        'matplotlib': 'Core plotting and visualization',
        'networkx': 'Graph creation and analysis',
        'numpy': 'Numerical computations (auto-installed with matplotlib)'
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
# FACTORY FUNCTIONS
# =============================================================================

def create_visualizer(system, visualizer_type="auto"):
    """
    Factory function to create the appropriate visualizer.
    
    Args:
        system: The deadlock system to visualize
        visualizer_type: Type of visualizer ("auto", "educational", "text")
        
    Returns:
        Visualizer instance
    """
    if visualizer_type == "educational" and EDUCATIONAL_AVAILABLE:
        return EducationalVisualizer(system)
    elif visualizer_type == "auto":
        # Auto-select best available
        return DeadlockVisualizer(system)
    elif visualizer_type == "text":
        return TextOnlyVisualizer(system)
    else:
        # Fallback to default
        return DeadlockVisualizer(system)

# =============================================================================
# VERSION AND METADATA
# =============================================================================

__version__ = '2.0.0-educational'
__author__ = 'Deadlock Simulator Educational Team'

def get_version_info():
    """Get version and feature information."""
    return {
        'version': __version__,
        'author': __author__,
        'primary_visualizer': PRIMARY_VISUALIZER,
        'features_available': sum(FEATURES.values()),
        'total_features': len(FEATURES),
        'educational_ready': EDUCATIONAL_AVAILABLE
    }

# =============================================================================
# PUBLIC API
# =============================================================================

__all__ = [
    # Main visualizer classes
    'DeadlockVisualizer',           # Primary visualizer (best available)
    'create_visualizer',            # Factory function
    
    # Feature detection
    'get_available_features',
    'print_feature_summary', 
    'check_dependencies',
    'get_version_info'
]

# Conditionally add educational features
if EDUCATIONAL_AVAILABLE:
    __all__.append('EducationalVisualizer')

# =============================================================================
# MODULE INITIALIZATION
# =============================================================================

# Print initialization message (unless disabled)
import os
if os.environ.get('DEADLOCK_VIZ_QUIET') != '1':
    available = sum(FEATURES.values())
    total = len(FEATURES)
    print(f"🎨 Educational Deadlock Visualizer v{__version__} loaded ({available}/{total} features)")
    
    if PRIMARY_VISUALIZER == "text_only":
        print("💡 Install matplotlib and networkx for full graphical features")
    elif PRIMARY_VISUALIZER == "educational":
        print("✨ Educational visualization features ready!")

# Validate installation
if not any(FEATURES.values()):
    logger.warning("No visualization capabilities available. Install matplotlib and networkx.")