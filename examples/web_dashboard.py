#!/usr/bin/env python3
"""
Web Dashboard Example

This example demonstrates how to create interactive web-based visualizations
using the enhanced visualizer's web capabilities.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core import Process, Resource, System
from src.detection import DeadlockDetector

try:
    from src.visualization import WebDeadlockVisualizer
    WEB_AVAILABLE = True
except ImportError:
    print("❌ Web features not available. Install with: pip install plotly dash")
    WEB_AVAILABLE = False

def create_complex_system():
    """Create a complex system for web demonstration."""
    system = System()
    
    # Create multiple processes and resources
    for i in range(1, 6):  # 5 processes
        system.add_process(Process(i))
    
    for i in range(1, 4):  # 3 resources with multiple instances
        system.add_resource(Resource(i, instances=2))
    
    # Create interesting allocation pattern
    system.processes[1].request_resource(system.resources[1])
    system.processes[1].request_resource(system.resources[2])
    
    system.processes[2].request_resource(system.resources[2])
    system.processes[2].request_resource(system.resources[3])
    
    system.processes[3].request_resource(system.resources[3])
    system.processes[3].request_resource(system.resources[1])
    
    system.processes[4].request_resource(system.resources[1])
    system.processes[5].request_resource(system.resources[2])
    
    return system

def main():
    if not WEB_AVAILABLE:
        print("🌐 Web dashboard example requires additional packages")
        print("Install with: pip install plotly dash")
        return
    
    print("🌐 Web Dashboard Example")
    
    # Create system
    system = create_complex_system()
    
    # Create web visualizer
    web_viz = WebDeadlockVisualizer(system, port=8050)
    
    # Export static HTML version
    print("📄 Creating static HTML visualization...")
    html_file = web_viz.export_static_html("deadlock_web_example.html")
    print(f"✅ Static HTML created: {html_file}")
    
    # Launch interactive dashboard
    print("\n🚀 Launching interactive web dashboard...")
    print("   Open your browser and go to: http://localhost:8050")
    print("   Press Ctrl+C to stop the server")
    
    try:
        web_viz.create_dash_app()
        web_viz.run_server(debug=False)
    except KeyboardInterrupt:
        print("\n🛑 Web server stopped")

if __name__ == "__main__":
    main()
