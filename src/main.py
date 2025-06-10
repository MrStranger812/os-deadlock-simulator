#!/usr/bin/env python3
"""
Enhanced Deadlock Simulator - Main Entry Point

This module provides a comprehensive command-line interface for running
deadlock simulation scenarios with clean, educational visualizations.

Usage Examples:
    # Run all scenarios with educational output
    python -m src.main --all-scenarios --educational
    
    # Run specific scenario with visualization
    python -m src.main --scenario simple --visualize
    
    # Generate comprehensive educational materials
    python -m src.main --educational-session --output-dir ./presentation_materials
"""

import sys
import argparse
import os
from pathlib import Path
from datetime import datetime
import logging

# Configure matplotlib backend before importing
import matplotlib
matplotlib.use('TkAgg')

# Import project components
from src.core import Process, Resource, System
from src.detection import DeadlockDetector
from src.resolution import DeadlockResolver

# Import visualization
try:
    from src.visualization.educational_visualizer import EducationalVisualizer as DeadlockVisualizer
    VISUALIZATION_AVAILABLE = True
except ImportError:
    VISUALIZATION_AVAILABLE = False
    DeadlockVisualizer = None

# =============================================================================
# SCENARIO CREATION FUNCTIONS
# =============================================================================

def create_simple_scenario():
    """Create a simple deadlock scenario with two processes and two resources."""
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
    
    # Initial allocations
    p1.request_resource(r1)  # P1 gets R1
    p2.request_resource(r2)  # P2 gets R2
    
    return system

def create_dining_philosophers(num_philosophers=5):
    """Create dining philosophers scenario."""
    system = System()
    
    # Create philosophers (processes)
    for i in range(1, num_philosophers + 1):
        p = Process(i)
        system.add_process(p)
    
    # Create forks (resources)
    for i in range(1, num_philosophers + 1):
        f = Resource(i, instances=1)
        system.add_resource(f)
    
    # Each philosopher picks up left fork and wants right fork
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

def create_complex_scenario():
    """Create complex resource allocation scenario."""
    system = System()
    
    # Create processes
    for i in range(1, 5):
        p = Process(i)
        system.add_process(p)
    
    # Create resources with multiple instances
    r1 = Resource(1, instances=3)
    r2 = Resource(2, instances=2)
    r3 = Resource(3, instances=2)
    
    system.add_resource(r1)
    system.add_resource(r2)
    system.add_resource(r3)
    
    # Create complex allocation pattern
    # P1: holds R1, R2; wants R3
    system.processes[1].request_resource(r1)
    system.processes[1].request_resource(r2)
    system.processes[1].request_resource(r3)
    
    # P2: holds R2, R3; wants R1
    system.processes[2].request_resource(r2)
    system.processes[2].request_resource(r3)
    system.processes[2].request_resource(r1)
    
    # P3: holds R1, R3; wants R2
    system.processes[3].request_resource(r1)
    system.processes[3].request_resource(r3)
    system.processes[3].request_resource(r2)
    
    # P4: holds R1; wants R2, R3
    system.processes[4].request_resource(r1)
    system.processes[4].request_resource(r2)
    system.processes[4].request_resource(r3)
    
    return system

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def print_system_status(system):
    """Print detailed system status."""
    print(f"\n{'='*60}")
    print("📊 SYSTEM STATUS")
    print(f"{'='*60}")
    print(f"🕐 Time: {system.time}")
    print(f"🔄 Total Processes: {len(system.processes)}")
    print(f"📦 Total Resources: {len(system.resources)}")
    
    print(f"\n📋 Process Details:")
    for pid, process in system.processes.items():
        status_emoji = {"RUNNING": "🟢", "WAITING": "🟡", "TERMINATED": "🔴"}
        emoji = status_emoji.get(process.status, "⚪")
        
        print(f"   {emoji} P{pid} ({process.status})")
        if process.resources_held:
            held = [f"R{r.rid}" for r in process.resources_held]
            print(f"      🔒 Holding: {', '.join(held)}")
        if process.resources_requested:
            requested = [f"R{r.rid}" for r in process.resources_requested]
            print(f"      ⏳ Requesting: {', '.join(requested)}")
    
    print(f"\n📦 Resource Details:")
    for rid, resource in system.resources.items():
        print(f"   📦 R{rid}: {resource.available_instances}/{resource.total_instances} available")
        if resource.allocated_to:
            allocated = [f"P{pid}({count})" for pid, count in resource.allocated_to.items()]
            print(f"      🔗 Allocated to: {', '.join(allocated)}")
    
    print(f"{'='*60}")

def detect_and_analyze_deadlock(system, visualizer=None, verbose=True):
    """Detect and analyze deadlock with comprehensive reporting."""
    if verbose:
        print(f"\n🔍 DEADLOCK DETECTION ANALYSIS")
        print(f"{'-'*40}")
    
    detector = DeadlockDetector(system)
    results = {}
    
    # Resource Allocation Graph detection
    if verbose:
        print("📊 Running Resource Allocation Graph analysis...")
    rag_deadlocked, rag_processes = detector.detect_using_resource_allocation_graph()
    results['rag'] = {'deadlocked': rag_deadlocked, 'processes': rag_processes}
    
    # Banker's Algorithm detection
    if verbose:
        print("🏦 Running Banker's Algorithm analysis...")
    banker_deadlocked, banker_processes = detector.detect_using_bankers_algorithm()
    results['banker'] = {'deadlocked': banker_deadlocked, 'processes': banker_processes}
    
    # Compare results
    if rag_deadlocked == banker_deadlocked:
        if verbose:
            print("✅ Both algorithms agree!")
        results['consensus'] = True
    else:
        if verbose:
            print("⚠️ Algorithm disagreement detected!")
            print(f"   RAG: {rag_deadlocked} (processes: {rag_processes})")
            print(f"   Banker: {banker_deadlocked} (processes: {banker_processes})")
        results['consensus'] = False
    
    # Report final result
    final_deadlocked = rag_deadlocked  # Use RAG as primary
    final_processes = rag_processes
    
    if final_deadlocked:
        if verbose:
            print(f"\n🔴 DEADLOCK DETECTED!")
            print(f"   Deadlocked processes: P{', P'.join(map(str, final_processes))}")
        
        # Create visualization if available
        if visualizer and VISUALIZATION_AVAILABLE:
            if verbose:
                print(f"\n🎨 Creating deadlock visualization...")
            visualizer.visualize_current_state(final_processes)
    else:
        if verbose:
            print(f"\n🟢 NO DEADLOCK DETECTED")
            print(f"   System is operating normally")
        
        if visualizer and VISUALIZATION_AVAILABLE:
            if verbose:
                print(f"\n🎨 Creating system state visualization...")
            visualizer.visualize_current_state()
    
    results['final'] = {'deadlocked': final_deadlocked, 'processes': final_processes}
    return results

def create_output_directory(base_dir=None):
    """Create output directory with timestamp."""
    if base_dir:
        output_dir = Path(base_dir)
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = Path(f"deadlock_simulation_{timestamp}")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir

# =============================================================================
# COMMAND LINE INTERFACE
# =============================================================================

def create_parser():
    """Create command line argument parser."""
    parser = argparse.ArgumentParser(
        description="Educational Deadlock Simulator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --scenario simple --visualize                    # Basic scenario with visualization
  %(prog)s --scenario dining-5 --visualize --save          # Dining philosophers with save
  %(prog)s --all-scenarios --educational                    # All scenarios with educational output
  %(prog)s --educational-session --output-dir ./materials   # Complete educational session
        """
    )
    
    # Basic scenario options
    scenario_group = parser.add_mutually_exclusive_group()
    scenario_group.add_argument("--scenario", 
                               choices=["simple", "dining-3", "dining-5", "dining-7", "complex"],
                               help="Run specific simulation scenario")
    scenario_group.add_argument("--all-scenarios", action="store_true",
                               help="Run all available scenarios")
    scenario_group.add_argument("--educational-session", action="store_true",
                               help="Generate complete educational session with all materials")
    
    # Visualization options
    parser.add_argument("--visualize", action="store_true",
                       help="Enable visualization")
    parser.add_argument("--save", action="store_true",
                       help="Save visualization to file")
    parser.add_argument("--educational", action="store_true",
                       help="Generate educational materials and explanations")
    
    # Output options
    parser.add_argument("--output-dir", type=str,
                       help="Output directory for generated files")
    parser.add_argument("--quiet", action="store_true",
                       help="Suppress detailed output")
    
    # Educational options
    parser.add_argument("--format", choices=["simple", "comprehensive"],
                       default="simple",
                       help="Output format complexity")
    
    return parser

def run_single_scenario(scenario_name: str, args):
    """Run a single scenario with specified options."""
    if not args.quiet:
        print(f"🔬 Running Scenario: {scenario_name.replace('-', ' ').title()}")
        print("-" * 50)
    
    # Create system based on scenario
    if scenario_name == "simple":
        system = create_simple_scenario()
    elif scenario_name.startswith("dining"):
        num_phil = int(scenario_name.split("-")[1])
        system = create_dining_philosophers(num_phil)
    elif scenario_name == "complex":
        system = create_complex_scenario()
    else:
        print(f"❌ Unknown scenario: {scenario_name}")
        return False
    
    # Add deadlock to scenarios that need it
    if scenario_name == "simple":
        if not args.quiet:
            print("⚙️ Creating deadlock scenario...")
        p1 = system.processes[1]
        p2 = system.processes[2]
        r1 = system.resources[1]
        r2 = system.resources[2]
        
        # Create circular dependency
        p1.request_resource(r2)  # P1 wants R2 (held by P2)
        p2.request_resource(r1)  # P2 wants R1 (held by P1)
        
        if not args.quiet:
            print("   ✅ Circular dependency created")
    
    # Print system status
    if not args.quiet:
        print_system_status(system)
    
    # Initialize visualizer if requested
    visualizer = None
    if (args.visualize or args.save or args.educational) and VISUALIZATION_AVAILABLE:
        visualizer = DeadlockVisualizer(system)
        if not args.quiet:
            print("🎨 Educational visualizer initialized")
    
    # Detect and analyze deadlock
    results = detect_and_analyze_deadlock(system, visualizer, verbose=not args.quiet)
    
    # Handle educational output
    if args.educational and visualizer:
        output_dir = create_output_directory(args.output_dir)
        if not args.quiet:
            print(f"\n📚 Generating educational materials...")
            print(f"📁 Output directory: {output_dir}")
        
        # Generate comprehensive educational materials
        generated_files = visualizer.create_comprehensive_visualization(
            deadlocked_processes=results['final']['processes'] if results['final']['deadlocked'] else None,
            output_dir=str(output_dir),
            scenario_name=scenario_name
        )
        
        if not args.quiet:
            print(f"✅ Generated {len(generated_files)} educational files")
            for file_type, path in generated_files.items():
                print(f"   📄 {file_type}: {path}")
    
    # Handle simple save
    elif args.save and visualizer:
        output_dir = create_output_directory(args.output_dir)
        save_path = output_dir / f"{scenario_name}_visualization.png"
        visualizer.save_visualization(
            str(save_path),
            deadlocked_processes=results['final']['processes'] if results['final']['deadlocked'] else None
        )
        if not args.quiet:
            print(f"💾 Visualization saved to: {save_path}")
    
    # Handle simple visualization display
    elif args.visualize and visualizer:
        if not args.quiet:
            print("🖼️ Displaying visualization...")
        visualizer.visualize_current_state(
            deadlocked_processes=results['final']['processes'] if results['final']['deadlocked'] else None
        )
    
    if not args.quiet:
        print(f"✅ Scenario '{scenario_name}' completed successfully")
    
    return True

def run_all_scenarios(args):
    """Run all scenarios."""
    scenarios = ["simple", "dining-3", "dining-5", "dining-7", "complex"]
    
    if not args.quiet:
        print(f"🎯 Running All Scenarios")
        print("=" * 50)
    
    results = []
    for scenario in scenarios:
        if not args.quiet:
            print(f"\n{'='*20} {scenario.upper()} {'='*20}")
        
        try:
            success = run_single_scenario(scenario, args)
            results.append((scenario, success))
        except Exception as e:
            if not args.quiet:
                print(f"❌ Failed to run {scenario}: {e}")
            results.append((scenario, False))
    
    # Print summary
    if not args.quiet:
        print(f"\n📊 SUMMARY")
        print("-" * 30)
        successful = sum(1 for _, success in results if success)
        total = len(results)
        
        for scenario, success in results:
            status = "✅" if success else "❌"
            print(f"{status} {scenario}")
        
        print(f"\nTotal: {successful}/{total} scenarios completed successfully")
    
    return results

def run_educational_session(args):
    """Run complete educational session."""
    if not args.quiet:
        print("🎓 Starting Complete Educational Session")
        print("=" * 60)
    
    try:
        # Import and run educational test runner
        from tests.run_educational_tests import EducationalTestRunner
        
        runner = EducationalTestRunner(args.output_dir or "educational_results")
        results = runner.run_all_scenarios()
        
        if not args.quiet:
            print(f"\n🎉 Educational session completed successfully!")
            print(f"📁 Materials saved to: {results['session_directory']}")
            print(f"🌐 Open: {results['session_directory']}/index.html")
        
        return True
        
    except ImportError:
        print("❌ Educational test runner not available")
        print("💡 Running basic all-scenarios mode instead...")
        return run_all_scenarios(args)
    except Exception as e:
        print(f"❌ Educational session failed: {e}")
        return False

def main():
    """Main function to run the simulator."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Check visualization availability
    if (args.visualize or args.save or args.educational) and not VISUALIZATION_AVAILABLE:
        print("⚠️ Visualization not available. Install dependencies:")
        print("   pip install matplotlib networkx")
        if args.educational:
            print("🔄 Proceeding without visualization...")
        else:
            return 1
    
    # Print banner
    if not args.quiet:
        print("🚀 EDUCATIONAL DEADLOCK SIMULATOR")
        print("=" * 60)
        if VISUALIZATION_AVAILABLE:
            print("✨ Educational visualization features available")
        print("=" * 60)
    
    try:
        # Route to appropriate function
        if args.educational_session:
            success = run_educational_session(args)
        elif args.all_scenarios:
            success = run_all_scenarios(args)
        elif args.scenario:
            success = run_single_scenario(args.scenario, args)
        else:
            # Default: run simple scenario
            if not args.quiet:
                print("💡 No scenario specified, running simple deadlock scenario")
            success = run_single_scenario("simple", args)
        
        if success:
            if not args.quiet:
                print(f"\n🎉 Simulation completed successfully!")
            return 0
        else:
            if not args.quiet:
                print(f"\n❌ Simulation completed with errors")
            return 1
            
    except KeyboardInterrupt:
        print(f"\n⏹️ Simulation interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Simulation failed: {e}")
        if not args.quiet:
            import traceback
            traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())