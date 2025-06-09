#!/usr/bin/env python3
"""
Integration Example: How to use the Enhanced Deadlock Visualizer

This script demonstrates how to integrate and use the enhanced visualizer
with your existing deadlock simulator project.

File location: examples/enhanced_visualization_example.py
"""

import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import your existing project components
from src.core import Process, Resource, System
from src.detection import DeadlockDetector
from src.resolution import DeadlockResolver

# Import the enhanced visualizer
from src.visualization import EnhancedDeadlockVisualizer, LayoutType, AnimationType

def demo_basic_usage():
    """Demonstrate basic usage with existing project structure."""
    print("🚀 Demo 1: Basic Enhanced Visualization")
    print("=" * 50)
    
    # Create system using your existing code
    system = System()
    
    # Create processes
    p1 = Process(1)
    p2 = Process(2)
    system.add_process(p1)
    system.add_process(p2)
    
    # Create resources
    r1 = Resource(1, instances=1)
    r2 = Resource(2, instances=1)
    system.add_resource(r1)
    system.add_resource(r2)
    
    # Create deadlock scenario
    p1.request_resource(r1)  # P1 gets R1
    p2.request_resource(r2)  # P2 gets R2
    p1.request_resource(r2)  # P1 wants R2 (deadlock!)
    p2.request_resource(r1)  # P2 wants R1 (deadlock!)
    
    # Create enhanced visualizer (drop-in replacement)
    visualizer = EnhancedDeadlockVisualizer(system)
    
    # Use just like the old visualizer
    visualizer.visualize_current_state([1, 2])  # Show deadlock
    visualizer.show()
    
    print("✅ Basic visualization complete!")

def demo_advanced_features():
    """Demonstrate advanced features of the enhanced visualizer."""
    print("\n🎨 Demo 2: Advanced Features")
    print("=" * 50)
    
    # Create a more complex system
    system = create_dining_philosophers_system(5)
    
    # Create enhanced visualizer with custom settings
    visualizer = EnhancedDeadlockVisualizer(
        system,
        enable_real_time=True,
        layout_type=LayoutType.CIRCULAR  # Perfect for dining philosophers
    )
    
    # Customize appearance
    visualizer.set_color_scheme('dark')
    visualizer.animation_type = AnimationType.PULSE
    
    # Show static visualization with dark theme
    print("📸 Creating static visualization...")
    visualizer.visualize_current_state()
    visualizer.save("dining_philosophers_dark.png")
    
    # Create dynamic animation
    print("🎬 Creating dynamic animation...")
    animation = visualizer.create_dynamic_visualization(save_frames=True)
    
    # Export in different formats
    print("💾 Exporting animation...")
    visualizer.export_animation("dining_philosophers.gif", "gif")
    
    # Show performance metrics
    performance = visualizer.get_performance_report()
    print(f"⚡ Performance: {performance['average_fps']:.1f} FPS")
    
    visualizer.show()
    print("✅ Advanced features demo complete!")

def demo_layout_comparison():
    """Demonstrate different layout algorithms."""
    print("\n🗺️  Demo 3: Layout Algorithm Comparison")
    print("=" * 50)
    
    # Create system
    system = create_complex_resource_system()
    
    # Test different layouts
    layouts = [LayoutType.SPRING, LayoutType.CIRCULAR, LayoutType.HIERARCHICAL, LayoutType.GRID]
    
    for layout in layouts:
        print(f"📐 Testing {layout.value} layout...")
        
        visualizer = EnhancedDeadlockVisualizer(system, layout_type=layout)
        visualizer.visualize_current_state()
        visualizer.save(f"layout_{layout.value}.png")
        
        # Don't show each one (too many windows), just save
        import matplotlib.pyplot as plt
        plt.close()  # Close the figure to prevent too many windows
    
    print("✅ Layout comparison complete! Check the saved PNG files.")

def demo_integration_with_existing_tests():
    """Show how to integrate with existing test scenarios."""
    print("\n🧪 Demo 4: Integration with Existing Tests")
    print("=" * 50)
    
    try:
        # Import your existing test scenarios
        from tests.test_scenarios import create_simple_deadlock, create_dining_philosophers
        
        # Run simple deadlock test with enhanced visualization
        print("🔄 Running simple deadlock scenario...")
        system = create_simple_deadlock()
        
        visualizer = EnhancedDeadlockVisualizer(system, layout_type=LayoutType.HIERARCHICAL)
        visualizer.set_color_scheme('colorblind')  # Accessibility
        
        # Detect deadlock using existing detector
        detector = DeadlockDetector(system)
        is_deadlocked, deadlocked_processes = detector.detect_using_resource_allocation_graph()
        
        # Visualize with deadlock highlighting
        visualizer.visualize_current_state(deadlocked_processes)
        visualizer.save("test_simple_deadlock.png")
        
        # Run dining philosophers with enhanced visualization
        print("🍽️ Running dining philosophers scenario...")
        system = create_dining_philosophers(5)
        
        visualizer = EnhancedDeadlockVisualizer(system, layout_type=LayoutType.CIRCULAR)
        visualizer.set_color_scheme('default')
        
        # Create animated version
        animation = visualizer.create_dynamic_visualization()
        visualizer.export_animation("dining_philosophers_test.gif", "gif")
        
        import matplotlib.pyplot as plt
        plt.close('all')  # Clean up
        
        print("✅ Integration with existing tests complete!")
        
    except ImportError as e:
        print(f"⚠️ Could not import test scenarios: {e}")
        print("Make sure your test files are in the correct location.")

def demo_step_by_step_detection():
    """Demonstrate step-by-step deadlock detection visualization."""
    print("\n🔍 Demo 5: Step-by-Step Detection Visualization")
    print("=" * 50)
    
    # Create system with deadlock
    system = create_chain_deadlock_system()
    
    visualizer = EnhancedDeadlockVisualizer(system, layout_type=LayoutType.HIERARCHICAL)
    visualizer.set_color_scheme('default')
    
    # Simulate detection steps
    detection_steps = [
        {
            'marked_processes': {1},
            'explanation': 'Step 1: Start with Process P1\nP1 holds R1, requests R3'
        },
        {
            'marked_processes': {1, 3},
            'explanation': 'Step 2: Follow request to R3\nR3 is held by P3, add P3 to analysis'
        },
        {
            'marked_processes': {1, 2, 3},
            'explanation': 'Step 3: Follow P3\'s request to R2\nR2 is held by P2, add P2 to analysis'
        },
        {
            'marked_processes': {1, 2, 3},
            'explanation': 'Step 4: Cycle detected!\nP2 requests R1, which is held by P1\nDeadlock confirmed: P1 → R3 → P3 → R2 → P2 → R1 → P1'
        }
    ]
    
    # Show step-by-step detection
    visualizer.visualize_detection_steps(detection_steps)
    
    print("✅ Step-by-step detection demo complete!")

def demo_resolution_strategies():
    """Demonstrate deadlock resolution visualization."""
    print("\n🛠️ Demo 6: Resolution Strategies Visualization")
    print("=" * 50)
    
    # Create system with deadlock
    system = create_simple_deadlock_system()
    
    # Test resolution with existing resolver
    try:
        detector = DeadlockDetector(system)
        resolver = DeadlockResolver(system, detector)
        
        # Create visualizer
        visualizer = EnhancedDeadlockVisualizer(system, layout_type=LayoutType.SPRING)
        
        # Show initial deadlock state
        print("🔴 Initial deadlock state...")
        is_deadlocked, deadlocked_processes = detector.detect_using_resource_allocation_graph()
        visualizer.visualize_current_state(deadlocked_processes)
        visualizer.save("before_resolution.png")
        
        # Simulate resolution steps
        resolution_steps = [
            {
                'strategy': 'termination',
                'success': True,
                'explanation': 'Terminated Process P1 and released its resources'
            }
        ]
        
        # Apply resolution
        resolver._resolve_by_termination(deadlocked_processes, priority_based=False)
        
        # Show after resolution
        print("🟢 After resolution...")
        visualizer.visualize_current_state()
        visualizer.save("after_resolution.png")
        
        # Show resolution steps
        visualizer.visualize_resolution_steps(resolution_steps)
        
        print("✅ Resolution strategies demo complete!")
        
    except Exception as e:
        print(f"⚠️ Resolution demo failed: {e}")

def demo_performance_monitoring():
    """Demonstrate performance monitoring features."""
    print("\n⚡ Demo 7: Performance Monitoring")
    print("=" * 50)
    
    # Create large system for performance testing
    system = create_large_system(10, 8)  # 10 processes, 8 resources
    
    # Create visualizer with performance monitoring
    visualizer = EnhancedDeadlockVisualizer(system, enable_real_time=True)
    
    # Measure performance
    import time
    start_time = time.time()
    
    # Create multiple visualizations to gather performance data
    for i in range(5):
        visualizer.visualize_current_state()
        import matplotlib.pyplot as plt
        plt.close()  # Close to free memory
    
    end_time = time.time()
    
    # Get performance report
    performance = visualizer.get_performance_report()
    
    print(f"📊 Performance Report:")
    print(f"   Average Render Time: {performance['average_render_time']*1000:.1f}ms")
    print(f"   Average FPS: {performance['average_fps']:.1f}")
    print(f"   Total States: {performance['total_states']}")
    print(f"   Cache Hits: {performance['cache_hits']}")
    print(f"   Total Time: {end_time - start_time:.2f}s")
    
    print("✅ Performance monitoring demo complete!")

def create_dining_philosophers_system(num_philosophers=5):
    """Create dining philosophers system."""
    system = System()
    
    # Create philosophers (processes)
    for i in range(1, num_philosophers + 1):
        p = Process(i)
        system.add_process(p)
    
    # Create forks (resources)
    for i in range(1, num_philosophers + 1):
        f = Resource(i, instances=1)
        system.add_resource(f)
    
    # Each philosopher picks up their left fork and wants their right fork
    for i in range(num_philosophers):
        pid = i + 1
        left_fork = i + 1
        right_fork = (i + 1) % num_philosophers + 1
        
        process = system.processes[pid]
        left_resource = system.resources[left_fork]
        right_resource = system.resources[right_fork]
        
        # Pick up left fork
        process.request_resource(left_resource)
        # Want right fork (creates deadlock)
        process.request_resource(right_resource)
    
    return system

def create_complex_resource_system():
    """Create complex resource allocation system."""
    system = System()
    
    # Create processes
    for i in range(1, 5):
        p = Process(i)
        system.add_process(p)
    
    # Create resources with multiple instances
    for i in range(1, 4):
        r = Resource(i, instances=2)
        system.add_resource(r)
    
    # Create complex allocation pattern
    # P1: holds R1, wants R2
    system.processes[1].request_resource(system.resources[1])
    system.processes[1].request_resource(system.resources[2])
    
    # P2: holds R2, wants R3
    system.processes[2].request_resource(system.resources[2])
    system.processes[2].request_resource(system.resources[3])
    
    # P3: holds R3, wants R1
    system.processes[3].request_resource(system.resources[3])
    system.processes[3].request_resource(system.resources[1])
    
    # P4: running normally
    system.processes[4].request_resource(system.resources[1])
    
    return system

def create_chain_deadlock_system():
    """Create chain deadlock system."""
    system = System()
    
    # Create processes
    for i in range(1, 4):
        p = Process(i)
        system.add_process(p)
    
    # Create resources
    for i in range(1, 4):
        r = Resource(i, instances=1)
        system.add_resource(r)
    
    # Create chain: P1->R3->P3->R2->P2->R1->P1
    system.processes[1].request_resource(system.resources[1])  # P1 holds R1
    system.processes[1].request_resource(system.resources[3])  # P1 wants R3
    
    system.processes[2].request_resource(system.resources[2])  # P2 holds R2
    system.processes[2].request_resource(system.resources[1])  # P2 wants R1
    
    system.processes[3].request_resource(system.resources[3])  # P3 holds R3
    system.processes[3].request_resource(system.resources[2])  # P3 wants R2
    
    return system

def create_simple_deadlock_system():
    """Create simple two-process deadlock."""
    system = System()
    
    # Create processes
    p1 = Process(1)
    p2 = Process(2)
    system.add_process(p1)
    system.add_process(p2)
    
    # Create resources
    r1 = Resource(1, instances=1)
    r2 = Resource(2, instances=1)
    system.add_resource(r1)
    system.add_resource(r2)
    
    # Create deadlock
    p1.request_resource(r1)  # P1 holds R1
    p2.request_resource(r2)  # P2 holds R2
    p1.request_resource(r2)  # P1 wants R2 (deadlock!)
    p2.request_resource(r1)  # P2 wants R1 (deadlock!)
    
    return system

def create_large_system(num_processes, num_resources):
    """Create large system for performance testing."""
    system = System()
    
    # Create processes
    for i in range(1, num_processes + 1):
        p = Process(i)
        system.add_process(p)
    
    # Create resources
    for i in range(1, num_resources + 1):
        r = Resource(i, instances=2)
        system.add_resource(r)
    
    # Create random allocations
    import random
    random.seed(42)  # For reproducible results
    
    for pid in range(1, num_processes + 1):
        process = system.processes[pid]
        
        # Each process gets 1-2 resources and wants 1-2 more
        held_resources = random.sample(range(1, num_resources + 1), 
                                     random.randint(1, min(2, num_resources)))
        wanted_resources = random.sample([r for r in range(1, num_resources + 1) 
                                        if r not in held_resources], 
                                       random.randint(1, min(2, num_resources - len(held_resources))))
        
        for rid in held_resources:
            process.request_resource(system.resources[rid])
        
        for rid in wanted_resources:
            process.request_resource(system.resources[rid])
    
    return system

def main():
    """Run all demonstration examples."""
    print("🎯 Enhanced Deadlock Visualizer Integration Examples")
    print("=" * 60)
    print("This script demonstrates how to use the enhanced visualizer")
    print("with your existing deadlock simulator project.")
    print("=" * 60)
    
    try:
        # Run basic demo
        demo_basic_usage()
        
        # Run advanced features demo
        demo_advanced_features()
        
        # Run layout comparison
        demo_layout_comparison()
        
        # Integration with existing tests
        demo_integration_with_existing_tests()
        
        # Step-by-step detection
        demo_step_by_step_detection()
        
        # Resolution strategies
        demo_resolution_strategies()
        
        # Performance monitoring
        demo_performance_monitoring()
        
        print("\n🎉 All demos completed successfully!")
        print("\nGenerated files:")
        print("  - dining_philosophers_dark.png")
        print("  - dining_philosophers.gif")
        print("  - layout_*.png (multiple files)")
        print("  - test_simple_deadlock.png")
        print("  - dining_philosophers_test.gif")
        print("  - before_resolution.png")
        print("  - after_resolution.png")
        
        print("\n💡 Next steps:")
        print("  1. Replace src/visualization/visualizer.py with the enhanced version")
        print("  2. Update requirements.txt with new dependencies")
        print("  3. Update your main.py to use enhanced features")
        print("  4. Run your existing tests - they should work with better visuals!")
        
    except KeyboardInterrupt:
        print("\n⏹️ Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
        