#!/usr/bin/env python3
"""
Script to run individual test scenarios for the deadlock simulator.

Usage:
    python run_individual_test.py [scenario_name] [--visualize] [--viz-types TYPE1,TYPE2,...]

Available scenarios:
    - simple: Simple Two-Process Deadlock
    - dining-5: Dining Philosophers (5 philosophers)
    - dining-3: Dining Philosophers (3 philosophers)
    - dining-7: Dining Philosophers (7 philosophers)
    - complex: Complex Resource Allocation
    - no-deadlock: No Deadlock Scenario
    - chain: Chain Deadlock

Available visualization types:
    - rag: Resource Allocation Graph
    - state: System State
    - detection: Deadlock Detection Steps
    - resolution: Resolution Steps
    - all: All visualizations
"""

import sys
import os
import argparse

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from test_scenarios import (
    create_simple_deadlock,
    create_dining_philosophers,
    create_resource_allocation_scenario,
    create_no_deadlock_scenario,
    create_chain_deadlock,
    run_test_scenario
)

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Run individual deadlock test scenarios')
    parser.add_argument('scenario', help='Name of the scenario to run')
    parser.add_argument('--visualize', action='store_true', help='Enable visualization')
    parser.add_argument('--viz-types', help='Comma-separated list of visualization types (rag,state,detection,resolution,all)')
    return parser.parse_args()

def get_scenario_function(scenario_name):
    """Get the appropriate scenario function based on the scenario name."""
    scenarios = {
        'simple': ('Simple Two-Process Deadlock', create_simple_deadlock),
        'dining-5': ('Dining Philosophers (5 philosophers)', lambda: create_dining_philosophers(5)),
        'dining-3': ('Dining Philosophers (3 philosophers)', lambda: create_dining_philosophers(3)),
        'dining-7': ('Dining Philosophers (7 philosophers)', lambda: create_dining_philosophers(7)),
        'complex': ('Complex Resource Allocation', create_resource_allocation_scenario),
        'no-deadlock': ('No Deadlock Scenario', create_no_deadlock_scenario),
        'chain': ('Chain Deadlock', create_chain_deadlock)
    }
    
    if scenario_name not in scenarios:
        print(f"Error: Unknown scenario '{scenario_name}'")
        print("\nAvailable scenarios:")
        for name, (full_name, _) in scenarios.items():
            print(f"  {name}: {full_name}")
        sys.exit(1)
    
    return scenarios[scenario_name]

def validate_viz_types(viz_types):
    """Validate and process visualization types."""
    valid_types = {'rag', 'state', 'detection', 'resolution', 'all'}
    
    if not viz_types:
        return ['all']
    
    types = [t.strip().lower() for t in viz_types.split(',')]
    invalid_types = [t for t in types if t not in valid_types]
    
    if invalid_types:
        print(f"Error: Invalid visualization types: {', '.join(invalid_types)}")
        print("\nAvailable visualization types:")
        for t in valid_types:
            print(f"  {t}")
        sys.exit(1)
    
    return types

def main():
    """Main function to run the selected test scenario."""
    args = parse_args()
    scenario_name, scenario_func = get_scenario_function(args.scenario)
    
    # Process visualization types
    viz_types = validate_viz_types(args.viz_types) if args.viz_types else ['all']
    
    print(f"\n{'='*50}")
    print(f"RUNNING SCENARIO: {scenario_name}")
    print(f"{'='*50}\n")
    
    # Run the selected scenario
    run_test_scenario(
        scenario_func,
        scenario_name=scenario_name,
        test_both_algorithms=True,
        visualize=args.visualize,
        viz_types=viz_types
    )

if __name__ == "__main__":
    main() 