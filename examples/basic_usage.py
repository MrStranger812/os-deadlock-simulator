#!/usr/bin/env python3
"""
Basic Enhanced Visualizer Example

This example shows the simplest way to use the enhanced visualizer
as a drop-in replacement for the original visualizer.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core import Process, Resource, System
from src.detection import DeadlockDetector
from src.visualization import EnhancedDeadlockVisualizer

def main():
    print("🚀 Basic Enhanced Visualizer Example")
    
    # Create simple deadlock scenario
    system = System()
    p1, p2 = Process(1), Process(2)
    r1, r2 = Resource(1, instances=1), Resource(2, instances=1)
    
    system.add_process(p1)
    system.add_process(p2) 
    system.add_resource(r1)
    system.add_resource(r2)
    
    # Create deadlock
    p1.request_resource(r1)
    p2.request_resource(r2)
    p1.request_resource(r2)
    p2.request_resource(r1)
    
    # Detect deadlock
    detector = DeadlockDetector(system)
    is_deadlocked, processes = detector.detect_using_resource_allocation_graph()
    
    # Visualize (same API as original!)
    visualizer = EnhancedDeadlockVisualizer(system)
    visualizer.visualize_current_state(processes if is_deadlocked else None)
    visualizer.save("basic_example.png")
    visualizer.show()
    
    print("✅ Example complete! Check basic_example.png")

if __name__ == "__main__":
    main()
