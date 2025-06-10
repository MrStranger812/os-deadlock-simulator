#!/usr/bin/env python3
"""
Enhanced Deadlock Simulator - Main Entry Point

This module provides a comprehensive command-line interface for running
deadlock simulation scenarios with advanced visualization capabilities.

Usage Examples:
    # Basic usage
    python -m src.main --scenario simple --visualize
    
    # Enhanced features
    python -m src.main --scenario dining-5 --enhanced --layout circular --theme dark
    
    # Web dashboard
    python -m src.main --web --port 8080
    
    # Export animation
    python -m src.main --scenario simple --enhanced --export gif --output-dir ./results
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

# Import visualization with graceful fallback
try:
    from src.visualization import (
        DeadlockVisualizer,
        create_visualizer,
        get_available_features,
        print_feature_summary,
        LayoutType,
        AnimationType,
        ColorThemes
    )
    VISUALIZATION_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Visualization not available: {e}")
    print("Install dependencies with: pip install matplotlib networkx")
    VISUALIZATION_AVAILABLE = False

# =============================================================================
# SCENARIO CREATION FUNCTIONS
# =============================================================================

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
    
    # Initial allocations
    p1.request_resource(r1)  # P1 gets R1
    p2.request_resource(r2)  # P2 gets R2
    
    return system

def create_dining_philosophers(num_philosophers=5):
    """
    Create dining philosophers scenario.
    
    Args:
        num_philosophers: Number of philosophers (default=5)
    
    Returns:
        System: A system object configured with the scenario
    """
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
    """
    Create complex resource allocation scenario.
    
    Returns:
        System: A system object configured with the scenario
    """
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

def create_no_deadlock_scenario():
    """
    Create scenario with no deadlock (for false positive testing).
    
    Returns:
        System: A system object configured with the scenario
    """
    system = System()
    
    # Create processes
    for i in range(1, 4):
        p = Process(i)
        system.add_process(p)
    
    # Create resources with sufficient instances
    for i in range(1, 4):
        r = Resource(i, instances=2)
        system.add_resource(r)
    
    # Allocate resources without creating deadlock
    system.processes[1].request_resource(system.resources[1])
    system.processes[2].request_resource(system.resources[2])
    system.processes[3].request_resource(system.resources[3])
    
    # These requests can be satisfied
    system.processes[1].request_resource(system.resources[2])
    system.processes[2].request_resource(system.resources[3])
    system.processes[3].request_resource(system.resources[1])
    
    return system

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def print_system_status(system):
    """
    Print detailed system status.
    
    Args:
        system: The system to print status for
    """
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

def create_output_directory(base_dir=None):
    """Create output directory with timestamp."""
    if base_dir:
        output_dir = Path(base_dir)
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = Path(f"deadlock_simulation_{timestamp}")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create subdirectories
    (output_dir / "visualizations").mkdir(exist_ok=True)
    (output_dir / "reports").mkdir(exist_ok=True)
    (output_dir / "logs").mkdir(exist_ok=True)
    
    return output_dir

def detect_and_analyze_deadlock(system, visualizer=None, verbose=True):
    """
    Detect and analyze deadlock with comprehensive reporting.
    
    Args:
        system: The system to analyze
        visualizer: Optional visualizer for output
        verbose: Whether to print detailed output
        
    Returns:
        dict: Analysis results
    """
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

def resolve_deadlock_comprehensive(system, deadlocked_processes, verbose=True):
    """
    Attempt comprehensive deadlock resolution.
    
    Args:
        system: The system with deadlock
        deadlocked_processes: List of deadlocked process IDs
        verbose: Whether to print detailed output
        
    Returns:
        dict: Resolution results
    """
    if verbose:
        print(f"\n🛠️ DEADLOCK RESOLUTION")
        print(f"{'-'*40}")
    
    detector = DeadlockDetector(system)
    resolver = DeadlockResolver(system, detector)
    
    # Test different resolution strategies
    strategies = ['termination', 'preemption', 'rollback']
    results = {}
    
    for strategy in strategies:
        if verbose:
            print(f"\n🔧 Testing {strategy.title()} Strategy:")
        
        # Save system state
        original_state = _save_system_state(system)
        
        try:
            if strategy == 'termination':
                success = resolver._resolve_by_termination(deadlocked_processes.copy(), priority_based=False)
            elif strategy == 'preemption':
                success = resolver._resolve_by_preemption(deadlocked_processes.copy(), priority_based=False)
            elif strategy == 'rollback':
                success = resolver._resolve_by_rollback(deadlocked_processes.copy(), priority_based=False)
            
            results[strategy] = {
                'success': success,
                'final_state': _capture_system_state(system)
            }
            
            if verbose:
                if success:
                    print(f"   ✅ {strategy.title()} successful!")
                else:
                    print(f"   ❌ {strategy.title()} failed!")
        
        except Exception as e:
            if verbose:
                print(f"   ❌ {strategy.title()} error: {e}")
            results[strategy] = {'success': False, 'error': str(e)}
        
        # Restore original state for next test
        _restore_system_state(system, original_state)
    
    return results

def _save_system_state(system):
    """Save current system state."""
    return {
        'time': system.time,
        'processes': {
            pid: {
                'status': p.status,
                'held': [r.rid for r in p.resources_held],
                'requested': [r.rid for r in p.resources_requested]
            } for pid, p in system.processes.items()
        },
        'resources': {
            rid: {
                'available': r.available_instances,
                'allocated': dict(r.allocated_to)
            } for rid, r in system.resources.items()
        }
    }

def _restore_system_state(system, state):
    """Restore system to saved state."""
    system.time = state['time']
    
    # Restore processes
    for pid, pdata in state['processes'].items():
        if pid in system.processes:
            process = system.processes[pid]
            process.status = pdata['status']
            process.resources_held.clear()
            process.resources_requested.clear()
            
            for rid in pdata['held']:
                if rid in system.resources:
                    process.resources_held.append(system.resources[rid])
            
            for rid in pdata['requested']:
                if rid in system.resources:
                    process.resources_requested.append(system.resources[rid])
    
    # Restore resources
    for rid, rdata in state['resources'].items():
        if rid in system.resources:
            resource = system.resources[rid]
            resource.available_instances = rdata['available']
            resource.allocated_to = dict(rdata['allocated'])

def _capture_system_state(system):
    """Capture current system state summary."""
    return {
        'processes': len(system.processes),
        'resources': len(system.resources),
        'waiting': sum(1 for p in system.processes.values() if p.status == 'WAITING'),
        'terminated': sum(1 for p in system.processes.values() if p.status == 'TERMINATED')
    }

# =============================================================================
# COMMAND LINE INTERFACE
# =============================================================================

def create_parser():
    """Create command line argument parser."""
    parser = argparse.ArgumentParser(
        description="Enhanced Deadlock Simulator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --scenario simple --visualize
  %(prog)s --scenario dining-5 --enhanced --layout circular --theme dark
  %(prog)s --scenario complex --enhanced --export gif --output-dir ./results
        """
    )
    
    # Basic options
    parser.add_argument("--scenario", 
                       choices=["simple", "dining-3", "dining-5", "dining-7", "complex", "no-deadlock"],
                       default="simple",
                       help="Simulation scenario to run")
    
    parser.add_argument("--visualize", action="store_true",
                       help="Enable basic visualization")
    
    parser.add_argument("--enhanced", action="store_true",
                       help="Use enhanced visualization features")
    
    # Enhanced visualization options
    if VISUALIZATION_AVAILABLE:
        try:
            layout_choices = [l.value for l in LayoutType]
        except:
            layout_choices = ["spring", "circular", "hierarchical", "grid"]
            
        try:
            animation_choices = [a.value for a in AnimationType]
        except:
            animation_choices = ["fade", "pulse", "scale"]
        
        parser.add_argument("--layout", choices=layout_choices,
                           default="spring", help="Layout algorithm")
        
        parser.add_argument("--theme", 
                           choices=["default", "dark", "high_contrast", "colorblind", "educational"],
                           default="default", help="Color theme")
        
        parser.add_argument("--animation", choices=animation_choices,
                           default="fade", help="Animation type")
        
        parser.add_argument("--export", choices=["png", "gif", "mp4"],
                           help="Export format")
    
    # Output options
    parser.add_argument("--output-dir", type=str,
                       help="Output directory for generated files")
    
    parser.add_argument("--quiet", action="store_true",
                       help="Suppress detailed output")
    
    parser.add_argument("--features", action="store_true",
                       help="Show available features and exit")
    
    parser.add_argument("--demo", action="store_true",
                       help="Run demonstration with all features")
    
    return parser

def run_demonstration():
    """Run a comprehensive demonstration of all features."""
    print("🎯 DEADLOCK SIMULATOR DEMONSTRATION")
    print("=" * 60)
    
    scenarios = [
        ("simple", "Simple Two-Process Deadlock"),
        ("dining-5", "Dining Philosophers (5)"),
        ("complex", "Complex Multi-Resource")
    ]
    
    for scenario_name, description in scenarios:
        print(f"\n📋 Running: {description}")
        print("-" * 40)
        
        # Create system
        if scenario_name == "simple":
            system = create_simple_scenario()
        elif scenario_name == "dining-5":
            system = create_dining_philosophers(5)
        elif scenario_name == "complex":
            system = create_complex_scenario()
        
        # Add deadlock to simple scenario
        if scenario_name == "simple":
            p1 = system.processes[1]
            p2 = system.processes[2]
            r1 = system.resources[1]
            r2 = system.resources[2]
            p1.request_resource(r2)  # Creates deadlock
            p2.request_resource(r1)
        
        # Print system status
        print_system_status(system)
        
        # Analyze deadlock
        visualizer = None
        if VISUALIZATION_AVAILABLE:
            visualizer = create_visualizer(system, "auto")
        
        results = detect_and_analyze_deadlock(system, visualizer, verbose=True)
        
        # Show visualization if available
        if visualizer and VISUALIZATION_AVAILABLE:
            print("🎨 Displaying visualization...")
            try:
                visualizer.show()
            except:
                print("⚠️ Display not available in current environment")
        
        # Test resolution if deadlock detected
        if results['final']['deadlocked']:
            resolution_results = resolve_deadlock_comprehensive(
                system, 
                results['final']['processes'], 
                verbose=True
            )
    
    print(f"\n🎉 Demonstration complete!")

def main():
    """Main function to run the simulator."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Handle special commands
    if args.features:
        if VISUALIZATION_AVAILABLE:
            print_feature_summary()
        else:
            print("❌ Visualization features not available")
            print("Install dependencies: pip install matplotlib networkx plotly dash")
        return 0
    
    if args.demo:
        run_demonstration()
        return 0
    
    # Print banner
    if not args.quiet:
        print("🚀 ENHANCED DEADLOCK SIMULATOR")
        print("=" * 60)
        print(f"Running scenario: {args.scenario}")
        if VISUALIZATION_AVAILABLE:
            features = get_available_features()
            available_count = sum(features.values())
            print(f"✨ {available_count} visualization features available")
        print("=" * 60)
    
    # Create output directory
    output_dir = create_output_directory(args.output_dir)
    if not args.quiet:
        print(f"📁 Output directory: {output_dir}")
    
    # Create system based on scenario
    if args.scenario == "simple":
        system = create_simple_scenario()
    elif args.scenario.startswith("dining"):
        num_phil = int(args.scenario.split("-")[1])
        system = create_dining_philosophers(num_phil)
    elif args.scenario == "complex":
        system = create_complex_scenario()
    elif args.scenario == "no-deadlock":
        system = create_no_deadlock_scenario()
    else:
        print(f"❌ Unknown scenario: {args.scenario}")
        return 1
    
    # Initialize visualizer
    visualizer = None
    if (args.visualize or args.enhanced) and VISUALIZATION_AVAILABLE:
        visualizer_type = "enhanced" if args.enhanced else "auto"
        visualizer = create_visualizer(system, visualizer_type)
        
        # Configure enhanced features
        if hasattr(args, 'theme') and hasattr(visualizer, 'set_color_scheme'):
            visualizer.set_color_scheme(args.theme)
        
        if hasattr(args, 'layout') and hasattr(visualizer, 'set_layout_algorithm'):
            try:
                layout_type = LayoutType(args.layout)
                visualizer.set_layout_algorithm(layout_type)
            except:
                pass
        
        if hasattr(args, 'animation') and hasattr(visualizer, 'animation_type'):
            try:
                animation_type = AnimationType(args.animation)
                visualizer.animation_type = animation_type
            except:
                pass
        
        if not args.quiet:
            print(f"🎨 Visualizer configured:")
            print(f"   Type: {visualizer_type}")
            if hasattr(args, 'theme'):
                print(f"   Theme: {args.theme}")
            if hasattr(args, 'layout'):
                print(f"   Layout: {args.layout}")
    
    # Print initial system state
    if not args.quiet:
        print_system_status(system)
    
    # Create potential deadlock for scenarios that need it
    if args.scenario == "simple":
        if not args.quiet:
            print("\n⚙️ Creating deadlock scenario...")
        p1 = system.processes[1]
        p2 = system.processes[2]
        r1 = system.resources[1]
        r2 = system.resources[2]
        
        # Create circular dependency
        p1.request_resource(r2)  # P1 wants R2 (held by P2)
        p2.request_resource(r1)  # P2 wants R1 (held by P1)
        
        if not args.quiet:
            print("   ✅ Circular dependency created")
    
    # Detect and analyze deadlock
    results = detect_and_analyze_deadlock(system, visualizer, verbose=not args.quiet)
    
    # Test resolution if deadlock detected
    if results['final']['deadlocked']:
        resolution_results = resolve_deadlock_comprehensive(
            system, 
            results['final']['processes'], 
            verbose=not args.quiet
        )
    
    # Handle exports
    if visualizer and hasattr(args, 'export') and args.export:
        if not args.quiet:
            print(f"\n💾 Exporting to {args.export} format...")
        
        export_file = output_dir / f"deadlock_visualization.{args.export}"
        
        try:
            if args.export == "png":
                visualizer.save(str(export_file))
            elif hasattr(visualizer, 'export_animation'):
                visualizer.export_animation(str(export_file), args.export)
            else:
                visualizer.save(str(export_file))
            
            if not args.quiet:
                print(f"   ✅ Exported to {export_file}")
        except Exception as e:
            print(f"   ❌ Export failed: {e}")
    
    # Show visualization if requested
    if visualizer and (args.visualize or args.enhanced):
        if not args.quiet:
            print("\n🎨 Displaying visualization...")
        try:
            visualizer.show()
        except Exception as e:
            if not args.quiet:
                print(f"⚠️ Display error: {e}")
    
    # Print final summary
    if not args.quiet:
        print(f"\n📋 SIMULATION SUMMARY")
        print(f"{'-'*30}")
        print(f"Scenario: {args.scenario}")
        print(f"Deadlock detected: {'Yes' if results['final']['deadlocked'] else 'No'}")
        if results['final']['deadlocked']:
            processes = results['final']['processes']
            print(f"Affected processes: P{', P'.join(map(str, processes))}")
        print(f"Output directory: {output_dir}")
        
        if VISUALIZATION_AVAILABLE and visualizer:
            try:
                if hasattr(visualizer, 'get_performance_report'):
                    performance = visualizer.get_performance_report()
                    print(f"Visualization performance: {performance.get('average_fps', 0):.1f} FPS avg")
            except:
                pass
    
    print(f"\n🎉 Simulation completed successfully!")
    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n⏹️ Simulation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Simulation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)