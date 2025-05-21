#!/usr/bin/env python3
"""
Main entry point for the Deadlock Simulator.

This module provides a command-line interface for running
deadlock simulation scenarios.  
"""

import sys
import argparse
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

def main():
    """Main function to run the simulator."""
    parser = argparse.ArgumentParser(description="Deadlock Simulator")
    parser.add_argument("--scenario", choices=["simple", "dining", "custom"], 
                      default="simple", help="Scenario to simulate")
    parser.add_argument("--steps", type=int, default=5, 
                      help="Number of simulation steps to run")
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
    resolver = DeadlockResolver(system)
    visualizer = DeadlockVisualizer(system)
    
    # Print initial state
    print_system_status(system)
    
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
            
            p1.request_resource(r2)  # P1 now wants R2, which P2 holds
            p2.request_resource(r1)  # P2 now wants R1, which P1 holds
        
        # Step simulation
        system.step()
        
        # Detect deadlock
        is_deadlocked, deadlocked_processes = detector.detect_using_resource_allocation_graph()
        
        if is_deadlocked:
            print(f"Deadlock detected! Processes involved: {deadlocked_processes}")
            print("Resolving deadlock...")
            resolver.resolve_by_process_termination(deadlocked_processes)
        
        # Print system status
        print_system_status(system)
    
    print("\nSimulation complete.")

if __name__ == "__main__":
    main()