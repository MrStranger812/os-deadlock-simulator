#!/usr/bin/env python3
"""
Advanced Enhanced Visualizer Example

This example demonstrates the advanced features of the enhanced visualizer
including dynamic animations, multiple layouts, and export capabilities.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core import Process, Resource, System
from src.detection import DeadlockDetector
from src.visualization import EnhancedDeadlockVisualizer, LayoutType, AnimationType

def create_dining_philosophers(n=5):
    """Create dining philosophers scenario."""
    system = System()
    
    # Create philosophers and forks
    for i in range(1, n + 1):
        system.add_process(Process(i))
        system.add_resource(Resource(i, instances=1))
    
    # Create deadlock scenario
    for i in range(n):
        pid = i + 1
        left_fork = i + 1
        right_fork = (i + 1) % n + 1
        
        process = system.processes[pid]
        process.request_resource(system.resources[left_fork])
        process.request_resource(system.resources[right_fork])
    
    return system

def main():
    print("🎨 Advanced Enhanced Visualizer Example")
    
    # Create dining philosophers scenario
    system = create_dining_philosophers(5)
    
    # Create enhanced visualizer with circular layout (perfect for dining philosophers)
    visualizer = EnhancedDeadlockVisualizer(
        system,
        enable_real_time=True,
        layout_type=LayoutType.CIRCULAR
    )
    
    # Configure advanced features
    visualizer.set_color_scheme('dark')
    visualizer.animation_type = AnimationType.PULSE
    
    # Detect deadlock
    detector = DeadlockDetector(system)
    is_deadlocked, processes = detector.detect_using_resource_allocation_graph()
    
    print(f"Deadlock detected: {is_deadlocked}")
    print(f"Affected processes: {processes}")
    
    # Create static visualization with dark theme
    print("📸 Creating static visualization...")
    visualizer.visualize_current_state(processes)
    visualizer.save("dining_philosophers_dark.png")
    
    # Create dynamic animation
    print("🎬 Creating dynamic animation...")
    animation = visualizer.create_dynamic_visualization(save_frames=True)
    
    # Export in multiple formats
    print("💾 Exporting animations...")
    visualizer.export_animation("dining_philosophers.gif", "gif")
    
    # Try different layouts
    layouts_to_test = [LayoutType.SPRING, LayoutType.GRID, LayoutType.HIERARCHICAL]
    
    for layout in layouts_to_test:
        print(f"📐 Testing {layout.value} layout...")
        visualizer.set_layout_algorithm(layout)
        visualizer.visualize_current_state(processes)
        visualizer.save(f"dining_{layout.value}.png")
        
        import matplotlib.pyplot as plt
        plt.close()  # Close to prevent too many windows
    
    # Show performance metrics
    performance = visualizer.get_performance_report()
    print(f"\n⚡ Performance Report:")
    print(f"   Average FPS: {performance['average_fps']:.1f}")
    print(f"   Total States: {performance['total_states']}")
    print(f"   Cache Efficiency: {performance['cache_hits']} layouts cached")
    
    # Show final result
    visualizer.show()
    
    print("\n✅ Advanced example complete!")
    print("Generated files:")
    print("  - dining_philosophers_dark.png")
    print("  - dining_philosophers.gif")
    print("  - dining_spring.png")
    print("  - dining_grid.png") 
    print("  - dining_hierarchical.png")

if __name__ == "__main__":
    main()
