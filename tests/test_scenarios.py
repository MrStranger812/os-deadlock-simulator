"""
explain these code : 
Test scenarios for the deadlock simulator.

This module provides various test scenarios to validate the correctness
of the deadlock detection and resolution algorithms.
"""

from src.core import Process, Resource, System
from src.detection import DeadlockDetector
from src.resolution import DeadlockResolver
# from src.visualization import DeadlockVisualizer
def create_simple_deadlock():
    """
    Create a simple deadlock scenario with two processes and two resources.
    
    Scenario:
    - P1 holds R1, wants R2
    - P2 holds R2, wants R1
    - This creates a circular dependency: P1 -> R2 -> P2 -> R1 -> P1
    
    Returns:
        System: A system object configured with the scenario
    """
    system = System()
    
    # Create processes
    p1 = Process(1)
    p2 = Process(2)
    
    # Create resources (single instance each)
    r1 = Resource(1, instances=1)
    r2 = Resource(2, instances=1)
    
    # Add to system
    system.add_process(p1)
    system.add_process(p2)
    system.add_resource(r1)
    system.add_resource(r2)
    
    # Create deadlock scenario
    # P1 gets R1
    p1.request_resource(r1)
    # P2 gets R2
    p2.request_resource(r2)
    # P1 wants R2 (will wait since P2 has it)
    p1.request_resource(r2)
    # P2 wants R1 (will wait since P1 has it) - DEADLOCK!
    p2.request_resource(r1)
    
    return system

def create_dining_philosophers(num_philosophers=5):
    """
    Create the classic dining philosophers deadlock scenario.
    
    Args:
        num_philosophers: Number of philosophers (default=5)
    
    Scenario:
    - N philosophers sit around a table
    - N forks are placed between them
    - Each philosopher needs 2 forks to eat (left and right fork)
    - If all philosophers pick up their left fork simultaneously,
      none can get their right fork -> deadlock
    
    Returns:
        System: A system object configured with the scenario
    """
    system = System()
    
    # Create philosophers (processes)
    philosophers = []
    for i in range(1, num_philosophers + 1):
        p = Process(i)
        philosophers.append(p)
        system.add_process(p)
    
    # Create forks (resources)
    forks = []
    for i in range(1, num_philosophers + 1):
        f = Resource(i, instances=1)
        forks.append(f)
        system.add_resource(f)
    
    # Each philosopher picks up their left fork
    for i in range(num_philosophers):
        philosophers[i].request_resource(forks[i])
    
    # Each philosopher tries to pick up their right fork (creates deadlock)
    for i in range(num_philosophers):
        right_fork_index = (i + 1) % num_philosophers
        philosophers[i].request_resource(forks[right_fork_index])
    
    return system



def create_resource_allocation_scenario():
    """
    Create a more complex resource allocation scenario with multiple resource types.
    
    Scenario:
    - 4 processes, 3 resource types with multiple instances
    - P1: holds R1, R2; wants R3
    - P2: holds R2, R3; wants R1
    - P3: holds R1, R3; wants R2
    - P4: holds R1; wants R2, R3
    
    Returns:
        System: A system object configured with the scenario
    """
    system = System()
    
    # Create processes
    processes = []
    for i in range(1, 5):
        p = Process(i)
        processes.append(p)
        system.add_process(p)
    
    # Create resource types with multiple instances
    r1 = Resource(1, instances=3)  # 3 instances of R1
    r2 = Resource(2, instances=2)  # 2 instances of R2
    r3 = Resource(3, instances=2)  # 2 instances of R3
    
    system.add_resource(r1)
    system.add_resource(r2)
    system.add_resource(r3)
    
    # Initial allocations
    processes[0].request_resource(r1)  # P1 gets R1
    processes[0].request_resource(r2)  # P1 gets R2
    
    processes[1].request_resource(r2)  # P2 gets R2
    processes[1].request_resource(r3)  # P2 gets R3
    
    processes[2].request_resource(r1)  # P3 gets R1
    processes[2].request_resource(r3)  # P3 gets R3
    
    processes[3].request_resource(r1)  # P4 gets R1
    
    # Additional requests that may lead to deadlock
    processes[0].request_resource(r3)  # P1 wants R3 (P2 and P3 have them)
    processes[1].request_resource(r1)  # P2 wants R1 (P1, P3, P4 have them)
    processes[2].request_resource(r2)  # P3 wants R2 (P1, P2 have them)
    processes[3].request_resource(r2)  # P4 wants R2 (P1, P2 have them)
    processes[3].request_resource(r3)  # P4 wants R3 (P2, P3 have them)
    
    return system

def create_no_deadlock_scenario():
    """
    Create a scenario that appears complex but has no deadlock.
    This tests false positive detection.
    
    Returns:
        System: A system object configured with the scenario
    """
    system = System()
    
    # Create processes
    p1 = Process(1)
    p2 = Process(2)
    p3 = Process(3)
    
    # Create resources with sufficient instances
    r1 = Resource(1, instances=2)
    r2 = Resource(2, instances=2)
    r3 = Resource(3, instances=2)
    
    # Add to system
    system.add_process(p1)
    system.add_process(p2)
    system.add_process(p3)
    system.add_resource(r1)
    system.add_resource(r2)
    system.add_resource(r3)
    
    # Allocate resources in a way that doesn't create deadlock
    p1.request_resource(r1)  # P1 gets R1
    p2.request_resource(r2)  # P2 gets R2
    p3.request_resource(r3)  # P3 gets R3
    
    # These requests can be satisfied due to multiple instances
    p1.request_resource(r2)  # P1 can get R2 (2nd instance)
    p2.request_resource(r3)  # P2 can get R3 (2nd instance)
    p3.request_resource(r1)  # P3 can get R1 (2nd instance)
    
    return system

def create_chain_deadlock():
    """
    Create a chain deadlock scenario with multiple processes.
    
    Scenario:
    P1 -> R1 -> P2 -> R2 -> P3 -> R3 -> P1 (circular chain)
    
    Returns:
        System: A system object configured with the scenario
    """
    system = System()
    
    # Create processes
    processes = []
    for i in range(1, 4):
        p = Process(i)
        processes.append(p)
        system.add_process(p)
    
    # Create resources
    resources = []
    for i in range(1, 4):
        r = Resource(i, instances=1)
        resources.append(r)
        system.add_resource(r)
    
    # Create chain: P1 holds R1, P2 holds R2, P3 holds R3
    processes[0].request_resource(resources[0])  # P1 -> R1
    processes[1].request_resource(resources[1])  # P2 -> R2
    processes[2].request_resource(resources[2])  # P3 -> R3
    
    # Create circular dependency
    processes[0].request_resource(resources[2])  # P1 wants R3 (held by P3)
    processes[1].request_resource(resources[0])  # P2 wants R1 (held by P1)
    processes[2].request_resource(resources[1])  # P3 wants R2 (held by P2)
    
    return system



def run_test_scenario(scenario_func, scenario_name="", test_both_algorithms=True, visualize=False):
    """
    Run a test scenario and report the results.
    
    Args:
        scenario_func: Function that creates a scenario
        scenario_name: Name of the scenario for reporting
        test_both_algorithms: Whether to test both detection algorithms
        visualize: Whether to show visualizations
        
    Returns:
        dict: Test results containing detection results and system state
    """
    print(f"\n{'='*50}")
    print(f"TESTING SCENARIO: {scenario_name or scenario_func.__name__}")
    print(f"{'='*50}")
    
    # Create the system using the provided scenario
    system = scenario_func()
    
    # Initialize components
    detector = DeadlockDetector(system)
    resolver = DeadlockResolver(system,detector)
    
    if visualize:
        visualizer = DeadlockVisualizer(system)
    
    # Print initial system state
    print("\n--- Initial System State ---")
    print_system_summary(system)
    
    results = {
        "scenario_name": scenario_name or scenario_func.__name__,
        "initial_state": get_system_state_summary(system),
        "detection_results": {}
    }
    
    # Test Resource Allocation Graph detection
    print("\n--- Testing Resource Allocation Graph Detection ---")
    rag_deadlocked, rag_processes = detector.detect_using_resource_allocation_graph()
    results["detection_results"]["rag"] = {
        "deadlocked": rag_deadlocked,
        "processes": rag_processes
    }
    
    if test_both_algorithms:
        # Test Banker's Algorithm detection
        print("\n--- Testing Banker's Algorithm Detection ---")
        banker_deadlocked, banker_processes = detector.detect_using_bankers_algorithm()
        results["detection_results"]["banker"] = {
            "deadlocked": banker_deadlocked,
            "processes": banker_processes
        }
        
        # Compare results
        if rag_deadlocked == banker_deadlocked:
            print("✅ Both algorithms agree on deadlock detection")
        else:
            print("⚠️ Algorithms disagree on deadlock detection!")
            print(f"RAG: {rag_deadlocked}, Banker's: {banker_deadlocked}")
    
    # If deadlock detected, test resolution
    if rag_deadlocked:
        print("\n--- Testing Deadlock Resolution ---")
        
        # Test different resolution strategies
        resolution_results = {}
        
        # Create copies of the system for testing different resolution strategies
        original_state = save_system_state(system)
        
        # Test process termination
        print("\n🔥 Testing Process Termination Strategy:")
        restore_system_state(system, original_state)
        termination_success = resolver._resolve_by_termination(rag_processes.copy(),priority_based=False)
        resolution_results["termination"] = {
            "success": termination_success,
            "final_state": get_system_state_summary(system)
        }
        
        # Test resource preemption
        print("\n🔄 Testing Resource Preemption Strategy:")
        restore_system_state(system, original_state)
        preemption_success = resolver._resolve_by_preemption(rag_processes.copy(),priority_based=False)
        resolution_results["preemption"] = {
            "success": preemption_success,
            "final_state": get_system_state_summary(system)
        }
        
        # Test rollback
        print("\n🔙 Testing Rollback Strategy:")
        restore_system_state(system, original_state)
        rollback_success = resolver._resolve_by_rollback(rag_processes.copy(),priority_based=False)
        resolution_results["rollback"] = {
            "success": rollback_success,
            "final_state": get_system_state_summary(system)
        }
        
        results["resolution_results"] = resolution_results
    
    # Show visualizations if requested
    if visualize and 'visualizer' in locals():
        print("\n--- Generating Visualizations ---")
        visualizer.draw_resource_allocation_graph()
        visualizer.draw_system_state()
    
    # Print final summary


    print(f"\n--- Test Summary for {scenario_name or scenario_func.__name__} ---")
    if rag_deadlocked:
        print(f"🔴 Deadlock detected involving processes: {rag_processes}")
    else:
        print("🟢 No deadlock detected")
    
    return results

def run_all_test_scenarios(visualize=False):
    """
    Run all predefined test scenarios.
    
    Args:
        visualize: Whether to show visualizations for each test
        
    Returns:
        list: List of all test results
    """
    scenarios = [
        (create_simple_deadlock, "Simple Two-Process Deadlock"),
        (create_dining_philosophers, "Dining Philosophers (5 philosophers)"),
        (create_resource_allocation_scenario, "Complex Resource Allocation"),
        (create_no_deadlock_scenario, "No Deadlock Scenario"),
        (create_chain_deadlock, "Chain Deadlock"),
        (lambda: create_dining_philosophers(3), "Dining Philosophers (3 philosophers)"),
        (lambda: create_dining_philosophers(7), "Dining Philosophers (7 philosophers)")
    ]
    
    all_results = []
    
    print("\n" + "="*60)
    print("RUNNING ALL TEST SCENARIOS")
    print("="*60)
    
    for scenario_func, scenario_name in scenarios:
        try:
            results = run_test_scenario(scenario_func, scenario_name, 
                                      test_both_algorithms=True, visualize=visualize)
            all_results.append(results)
        except Exception as e:
            print(f"❌ Error in scenario {scenario_name}: {str(e)}")
            all_results.append({
                "scenario_name": scenario_name,
                "error": str(e)
            })
    
    # Print overall summary
    print("\n" + "="*60)
    print("OVERALL TEST SUMMARY")
    print("="*60)
    
    deadlock_scenarios = 0
    no_deadlock_scenarios = 0
    error_scenarios = 0
    
    for result in all_results:
        if "error" in result:
            error_scenarios += 1
            print(f"❌ {result['scenario_name']}: ERROR - {result['error']}")
        elif result.get("detection_results", {}).get("rag", {}).get("deadlocked", False):
            deadlock_scenarios += 1
            processes = result["detection_results"]["rag"]["processes"]
            print(f"🔴 {result['scenario_name']}: DEADLOCK (Processes: {processes})")
        else:
            no_deadlock_scenarios += 1
            print(f"🟢 {result['scenario_name']}: NO DEADLOCK")
    
    print(f"\nTotal scenarios tested: {len(all_results)}")
    print(f"Deadlock scenarios: {deadlock_scenarios}")
    print(f"No deadlock scenarios: {no_deadlock_scenarios}")
    print(f"Error scenarios: {error_scenarios}")
    
    return all_results

# Helper functions

def print_system_summary(system):
    """Print a summary of the current system state."""
    print(f"Processes: {len(system.processes)}")
    for pid, process in system.processes.items():
        held_resources = [r.rid for r in process.resources_held]
        requested_resources = [r.rid for r in process.resources_requested]
        print(f"  P{pid} ({process.status}): Holds {held_resources}, Requests {requested_resources}")
    
    print(f"Resources: {len(system.resources)}")
    for rid, resource in system.resources.items():
        print(f"  R{rid}: {resource.available_instances}/{resource.total_instances} available, "
              f"allocated to {resource.allocated_to}")



def get_system_state_summary(system):
    """Get a summary of system state as a dictionary."""
    return {
        "time": system.time,
        "processes": {
            pid: {
                "status": process.status,
                "held_resources": [r.rid for r in process.resources_held],
                "requested_resources": [r.rid for r in process.resources_requested]
            }
            for pid, process in system.processes.items()
        },
        "resources": {
            rid: {
                "available": resource.available_instances,
                "total": resource.total_instances,
                "allocated_to": dict(resource.allocated_to)
            }
            for rid, resource in system.resources.items()
        }
    }

def save_system_state(system):
    """Save the current system state for later restoration."""
    return get_system_state_summary(system)

def restore_system_state(system, saved_state):
    """Restore system to a previously saved state."""
    # Reset time
    system.time = saved_state["time"]
    
    # Restore process states
    for pid, process_state in saved_state["processes"].items():
        if pid in system.processes:
            process = system.processes[pid]
            process.status = process_state["status"]
            
            # Clear current resource lists
            process.resources_held.clear()
            process.resources_requested.clear()
            
            # Restore held resources
            for rid in process_state["held_resources"]:
                if rid in system.resources:
                    process.resources_held.append(system.resources[rid])
            
            # Restore requested resources
            for rid in process_state["requested_resources"]:
                if rid in system.resources:
                    process.resources_requested.append(system.resources[rid])
    
    # Restore resource states
    for rid, resource_state in saved_state["resources"].items():
        if rid in system.resources:
            resource = system.resources[rid]
            resource.available_instances = resource_state["available"]
            resource.allocated_to = dict(resource_state["allocated_to"])

# Main execution for testing
if __name__ == "__main__":
    # Run a quick test
    # print("Running quick deadlock simulation test...")
    # results = run_test_scenario(create_simple_deadlock, "Quick Test", visualize=False)
    
    # Uncomment the line below to run all scenarios
    run_all_test_scenarios(visualize=False)

