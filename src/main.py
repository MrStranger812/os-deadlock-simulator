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
from src.visualization import DeadlockVisualizer

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
    """Main function to run the simulator."""
    parser = argparse.ArgumentParser(description="Deadlock Simulator")
    parser.add_argument("--scenario", choices=["simple", "dining", "custom"], 
                      default="simple", help="Scenario to simulate")
    parser.add_argument("--steps", type=int, default=5, 
                      help="Number of simulation steps to run")
    parser.add_argument("--visualize", action="store_true",
                      help="Enable visualization output")
    args = parser.parse_args()
    
    print("=== Deadlock Simulator ===")
    print(f"Running {args.scenario} scenario for {args.steps} steps")
    
    # Create system based on selected scenario
    if args.scenario == "simple":
        system = create_simple_scenario()
    else:
        print("Other scenarios are not implemented yet.")
        return
    
    # Initialize components
    detector = DeadlockDetector(system)
    resolver = DeadlockResolver(system, detector)
    visualizer = DeadlockVisualizer(system)
    
    # Create visualization directory if needed
    vis_dir = create_visualization_dir() if args.visualize else None
    
    # Track system state for visualization
    prev_state = None
    
    # Print and visualize initial state
    print_system_status(system)
    if args.visualize:
        visualizer.visualize_current_state()
        visualizer.save(os.path.join(vis_dir, f"t{system.time}_initial_state.png"))
        prev_state = capture_system_state(system)
    
    # Run simulation steps
    for step in range(args.steps):
        print(f"\n--- Step {step+1} ---")
        
        # Create a potential deadlock in step 2
        if step == 1:
            print("Creating potential deadlock...")
            p1 = system.processes[1]
            p2 = system.processes[2]
            r1 = system.resources[1]
            r2 = system.resources[2]
            
            # Create deadlock
            p1.request_resource(r2)  # P1 now wants R2, which P2 holds
            p2.request_resource(r1)  # P2 now wants R1, which P1 holds
            
            # Visualize state after creating deadlock
            if args.visualize:
                visualizer.visualize_current_state()
                visualizer.save(os.path.join(vis_dir, f"t{system.time}_deadlock_created_P1_P2.png"))
                prev_state = capture_system_state(system)
        
        # Step simulation
        system.step()
        
        # Detect deadlock
        is_deadlocked, deadlocked_processes = detector.detect_using_resource_allocation_graph()
        
        if is_deadlocked:
            print(f"Deadlock detected! Processes involved: {deadlocked_processes}")
            if args.visualize:
                visualizer.visualize_current_state(deadlocked_processes=deadlocked_processes)
                visualizer.save(os.path.join(vis_dir, f"t{system.time}_deadlock_detected_P{'_'.join(map(str, deadlocked_processes))}.png"))
                prev_state = capture_system_state(system)
            
            print("Resolving deadlock...")
            resolver._resolve_by_termination(deadlocked_processes, priority_based=False)
            
            if args.visualize:
                visualizer.visualize_current_state()
                visualizer.save(os.path.join(vis_dir, f"t{system.time}_after_resolution_P{'_'.join(map(str, deadlocked_processes))}.png"))
                prev_state = capture_system_state(system)
        else:
            print("[NO DEADLOCK]")
            # Only visualize if state has changed
            if args.visualize and has_state_changed(system, prev_state):
                state_desc = get_state_description(system)
                visualizer.visualize_current_state()
                visualizer.save(os.path.join(vis_dir, f"t{system.time}_{state_desc}.png"))
                prev_state = capture_system_state(system)
        
        # Print system status
        print_system_status(system)
    
    print("\nSimulation complete.")
    if args.visualize:
        print(f"\nVisualizations saved in: {vis_dir}")

if __name__ == "__main__":
    main()