#!/usr/bin/env python3
"""
Main entry point for the Deadlock Simulator.

This module provides a command-line interface for running
deadlock simulation scenarios.  
"""

import sys
import argparse
import os
from datetime import datetime
from src.core import Process, Resource, System
from src.detection import DeadlockDetector
from src.resolution import DeadlockResolver
from src.visualization import EnhancedDeadlockVisualizer, LayoutType, AnimationType

def create_simple_scenario():
    """
    Create a simple deadlock scenario with two processes and two resources.
    
    Returns:
        System: A system object configured with the scenario
    """
    system = System()
    
    # Create processes
    p1 = Process(1)
    p2 = Process(2)
    
    # Create resources
    r1 = Resource(1, instances=1)
    r2 = Resource(2, instances=1)
    
    # Add to system
    system.add_process(p1)
    system.add_process(p2)
    system.add_resource(r1)
    system.add_resource(r2)
    
    # Allocate resources to create a potential deadlock
    p1.request_resource(r1)
    p2.request_resource(r2)
    
    return system

def print_system_status(system):
    """
    Print the current status of the system.
    
    Args:
        system: The system to print status for
    """
    print("\n=== System Status ===")
    print(f"Time: {system.time}")
    print("\nProcesses:")
    for pid, process in system.processes.items():
        print(f"  {process}")
        if process.resources_held:
            print(f"    Holding resources: {[r.rid for r in process.resources_held]}")
        if process.resources_requested:
            print(f"    Waiting for resources: {[r.rid for r in process.resources_requested]}")
    
    print("\nResources:")
    for rid, resource in system.resources.items():
        print(f"  {resource}")
        if resource.allocated_to:
            print(f"    Allocated to processes: {resource.allocated_to}")

def create_visualization_dir():
    """Create a directory for visualization outputs."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    vis_dir = f"visualizations_{timestamp}"
    os.makedirs(vis_dir, exist_ok=True)
    return vis_dir

def has_state_changed(system, prev_state):
    """
    Check if the system state has changed.
    
    Args:
        system: Current system state
        prev_state: Previous system state
        
    Returns:
        bool: True if state has changed, False otherwise
    """
    if prev_state is None:
        return True
        
    # Check process states
    for pid, process in system.processes.items():
        if pid not in prev_state['processes']:
            return True
        prev_process = prev_state['processes'][pid]
        if (process.status != prev_process['status'] or
            [r.rid for r in process.resources_held] != prev_process['resources_held'] or
            [r.rid for r in process.resources_requested] != prev_process['resources_requested']):
            return True
    
    # Check resource states
    for rid, resource in system.resources.items():
        if rid not in prev_state['resources']:
            return True
        prev_resource = prev_state['resources'][rid]
        if (resource.available_instances != prev_resource['available'] or
            resource.allocated_to != prev_resource['allocated']):
            return True
    
    return False

def capture_system_state(system):
    """
    Capture the current system state for comparison.
    
    Args:
        system: The system to capture state from
        
    Returns:
        dict: Current system state
    """
    state = {
        'processes': {},
        'resources': {}
    }
    
    for pid, process in system.processes.items():
        state['processes'][pid] = {
            'status': process.status,
            'resources_held': [r.rid for r in process.resources_held],
            'resources_requested': [r.rid for r in process.resources_requested]
        }
    
    for rid, resource in system.resources.items():
        state['resources'][rid] = {
            'available': resource.available_instances,
            'allocated': resource.allocated_to.copy()
        }
    
    return state

def get_state_description(system, deadlocked_processes=None):
    """
    Get a descriptive name for the current system state.
    
    Args:
        system: The current system state
        deadlocked_processes: List of deadlocked process IDs if any
        
    Returns:
        str: Description of the current state
    """
    if deadlocked_processes:
        return f"deadlock_detected_P{'_'.join(map(str, deadlocked_processes))}"
    
    # Check if any process is waiting
    waiting_processes = [pid for pid, p in system.processes.items() 
                        if p.status == "WAITING"]
    if waiting_processes:
        return f"processes_waiting_P{'_'.join(map(str, waiting_processes))}"
    
    # Check if any process is terminated
    terminated_processes = [pid for pid, p in system.processes.items() 
                          if p.status == "TERMINATED"]
    if terminated_processes:
        return f"processes_terminated_P{'_'.join(map(str, terminated_processes))}"
    
    return "all_processes_running"
def main():
    parser = argparse.ArgumentParser(description="Enhanced Deadlock Simulator")
    parser.add_argument("--scenario", choices=["simple", "dining", "custom"], 
                      default="simple", help="Scenario to simulate")
    parser.add_argument("--visualize", action="store_true",
                      help="Enable enhanced visualization")
    parser.add_argument("--layout", choices=[l.value for l in LayoutType],
                      default="spring", help="Layout algorithm")
    parser.add_argument("--theme", choices=["default", "dark", "colorblind"],
                      default="default", help="Color theme")
    parser.add_argument("--animation", choices=[a.value for a in AnimationType],
                      default="fade", help="Animation type")
    parser.add_argument("--web", action="store_true",
                      help="Create web-based visualization")
    parser.add_argument("--export", choices=["gif", "mp4", "html"],
                      help="Export animation format")
    
    args = parser.parse_args()
    
    print("=== Enhanced Deadlock Simulator ===")
    
    # Create system
    system = create_simple_scenario()  # Your existing function
    
    # Initialize enhanced visualizer
    visualizer = EnhancedDeadlockVisualizer(
        system, 
        enable_real_time=True,
        layout_type=LayoutType(args.layout)
    )
    
    # Set theme and animation
    visualizer.set_color_scheme(args.theme)
    visualizer.animation_type = AnimationType(args.animation)
    
    if args.visualize:
        # Create dynamic visualization
        ani = visualizer.create_dynamic_visualization(save_frames=True)
        
        if args.export:
            visualizer.export_animation(f"deadlock_animation.{args.export}", args.export)
        
        # Show interactive plot
        import matplotlib.pyplot as plt
        plt.show()
    
    if args.web:
        # Create web visualization
        visualizer.create_web_visualization("deadlock_web.html")
        print("Web visualization saved to deadlock_web.html")

if __name__ == "__main__":
    main()