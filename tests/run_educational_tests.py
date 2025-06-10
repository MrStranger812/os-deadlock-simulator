#!/usr/bin/env python3
"""
Educational Test Runner for Deadlock Simulator

This script runs all test scenarios and generates organized, educational output
suitable for academic presentation. Creates a comprehensive directory structure
with visualizations, explanations, and reports.

Usage:
    python run_educational_tests.py [--output-dir DIR] [--scenarios SCENARIOS]
"""

import sys
import os
import argparse
from pathlib import Path
from datetime import datetime
import json
import shutil
from typing import List, Dict, Any

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from tests.test_scenarios import (
    create_simple_deadlock,
    create_dining_philosophers,
    create_resource_allocation_scenario,
    create_no_deadlock_scenario,
    create_chain_deadlock,
    save_system_state,
    restore_system_state
)
from src.detection import DeadlockDetector
from src.resolution import DeadlockResolver
from src.visualization.educational_visualizer import EducationalVisualizer

class EducationalTestRunner:
    """
    Comprehensive test runner that generates educational materials
    for all deadlock scenarios.
    """
    
    def __init__(self, base_output_dir: str = "educational_results"):
        """Initialize the test runner."""
        self.base_output_dir = Path(base_output_dir)
        self.session_dir = None
        self.scenarios = {
            'simple_deadlock': {
                'name': 'Simple Two-Process Deadlock',
                'function': create_simple_deadlock,
                'description': 'Classic two-process circular deadlock scenario',
                'learning_objectives': [
                    'Understand basic deadlock formation',
                    'Identify circular wait condition',
                    'Recognize resource allocation graph cycles'
                ]
            },
            'dining_philosophers_3': {
                'name': 'Dining Philosophers (3 Philosophers)',
                'function': lambda: create_dining_philosophers(3),
                'description': 'Small-scale dining philosophers problem',
                'learning_objectives': [
                    'Understand resource sharing conflicts',
                    'See how multiple processes can deadlock',
                    'Learn about symmetric deadlock patterns'
                ]
            },
            'dining_philosophers_5': {
                'name': 'Dining Philosophers (5 Philosophers)',
                'function': lambda: create_dining_philosophers(5),
                'description': 'Classic dining philosophers deadlock scenario',
                'learning_objectives': [
                    'Analyze larger-scale resource contention',
                    'Understand scalability of deadlock problems',
                    'Compare with smaller philosopher groups'
                ]
            },
            'dining_philosophers_7': {
                'name': 'Dining Philosophers (7 Philosophers)',
                'function': lambda: create_dining_philosophers(7),
                'description': 'Large dining philosophers scenario',
                'learning_objectives': [
                    'Observe complex deadlock patterns',
                    'Understand detection complexity growth',
                    'Analyze resolution difficulty scaling'
                ]
            },
            'complex_allocation': {
                'name': 'Complex Multi-Resource Allocation',
                'function': create_resource_allocation_scenario,
                'description': 'Multiple processes competing for various resource types',
                'learning_objectives': [
                    'Understand multi-resource deadlocks',
                    'Learn about complex allocation matrices',
                    'Analyze banker\'s algorithm application'
                ]
            },
            'no_deadlock': {
                'name': 'Safe System State (No Deadlock)',
                'function': create_no_deadlock_scenario,
                'description': 'System with resource requests but no deadlock',
                'learning_objectives': [
                    'Distinguish between deadlock and waiting',
                    'Understand safe vs unsafe states',
                    'Learn about false positive detection'
                ]
            },
            'chain_deadlock': {
                'name': 'Chain Deadlock Pattern',
                'function': create_chain_deadlock,
                'description': 'Circular chain of dependencies among processes',
                'learning_objectives': [
                    'Identify chain-like deadlock patterns',
                    'Understand transitivity in resource dependencies',
                    'Analyze detection in linear vs circular chains'
                ]
            }
        }
    
    def run_all_scenarios(self, selected_scenarios: List[str] = None) -> Dict[str, Any]:
        """
        Run all scenarios and generate comprehensive educational output.
        
        Args:
            selected_scenarios: List of scenario names to run. If None, run all.
            
        Returns:
            Dictionary containing results summary
        """
        # Create session directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_dir = self.base_output_dir / f"simulation_session_{timestamp}"
        self.session_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"🎓 Starting Educational Deadlock Simulation Session")
        print(f"📁 Output directory: {self.session_dir}")
        print("=" * 70)
        
        # Determine which scenarios to run
        scenarios_to_run = selected_scenarios or list(self.scenarios.keys())
        
        # Results tracking
        session_results = {
            'timestamp': timestamp,
            'session_directory': str(self.session_dir),
            'scenarios_run': [],
            'summary_statistics': {},
            'generated_files': []
        }
        
        # Run each scenario
        for scenario_id in scenarios_to_run:
            if scenario_id not in self.scenarios:
                print(f"⚠️ Unknown scenario: {scenario_id}")
                continue
                
            scenario_info = self.scenarios[scenario_id]
            print(f"\n🔬 Running Scenario: {scenario_info['name']}")
            print(f"📖 Description: {scenario_info['description']}")
            print("-" * 50)
            
            try:
                scenario_result = self._run_single_scenario(scenario_id, scenario_info)
                session_results['scenarios_run'].append(scenario_result)
                session_results['generated_files'].extend(scenario_result['generated_files'])
                
                print(f"✅ Completed: {scenario_info['name']}")
                
            except Exception as e:
                print(f"❌ Failed: {scenario_info['name']} - {str(e)}")
                session_results['scenarios_run'].append({
                    'scenario_id': scenario_id,
                    'name': scenario_info['name'],
                    'status': 'failed',
                    'error': str(e)
                })
        
        # Generate session summary
        print(f"\n📊 Generating Session Summary...")
        self._generate_session_summary(session_results)
        
        # Create index file
        self._create_session_index(session_results)
        
        print(f"\n🎉 Educational session completed!")
        print(f"📁 All materials saved to: {self.session_dir}")
        print(f"📄 Open {self.session_dir}/index.html to view complete results")
        
        return session_results
    
    def _run_single_scenario(self, scenario_id: str, scenario_info: Dict) -> Dict[str, Any]:
        """Run a single scenario and generate all educational materials."""
        
        # Create scenario directory
        scenario_dir = self.session_dir / scenario_id
        scenario_dir.mkdir(exist_ok=True)
        
        # Initialize system
        print("🔧 Creating system...")
        system = scenario_info['function']()
        
        # Create visualizer
        visualizer = EducationalVisualizer(system)
        
        # Run deadlock detection
        print("🔍 Running deadlock detection...")
        detector = DeadlockDetector(system)
        rag_deadlocked, rag_processes = detector.detect_using_resource_allocation_graph()
        banker_deadlocked, banker_processes = detector.detect_using_bankers_algorithm()
        
        # Test resolution if deadlock detected
        resolution_results = {}
        if rag_deadlocked:
            print("🛠️ Testing resolution strategies...")
            resolver = DeadlockResolver(system, detector)
            original_state = save_system_state(system)
            
            # Test each resolution strategy
            for strategy in ['termination', 'preemption', 'rollback']:
                restore_system_state(system, original_state)
                
                try:
                    if strategy == 'termination':
                        success = resolver._resolve_by_termination(rag_processes.copy(), priority_based=False)
                    elif strategy == 'preemption':
                        success = resolver._resolve_by_preemption(rag_processes.copy(), priority_based=False)
                    else:  # rollback
                        success = resolver._resolve_by_rollback(rag_processes.copy(), priority_based=False)
                    
                    resolution_results[strategy] = success
                    
                except Exception as e:
                    resolution_results[strategy] = False
                    print(f"⚠️ Resolution strategy {strategy} failed: {e}")
            
            # Restore original state for visualization
            restore_system_state(system, original_state)
        
        # Generate comprehensive visualizations and documentation
        print("🎨 Creating educational materials...")
        
        generated_files = visualizer.create_comprehensive_visualization(
            deadlocked_processes=rag_processes if rag_deadlocked else None,
            output_dir=str(scenario_dir),
            scenario_name=scenario_id
        )
        
        # Create additional educational content
        self._create_scenario_comparison_chart(scenario_dir, rag_deadlocked, banker_deadlocked, 
                                             rag_processes, banker_processes)
        
        if resolution_results:
            self._create_resolution_summary(scenario_dir, resolution_results)
        
        self._create_learning_guide(scenario_dir, scenario_info, rag_deadlocked, rag_processes)
        
        # Prepare result summary
        result = {
            'scenario_id': scenario_id,
            'name': scenario_info['name'],
            'status': 'completed',
            'deadlock_detected': rag_deadlocked,
            'deadlocked_processes': rag_processes,
            'detection_results': {
                'rag': {'deadlocked': rag_deadlocked, 'processes': rag_processes},
                'banker': {'deadlocked': banker_deadlocked, 'processes': banker_processes}
            },
            'resolution_results': resolution_results,
            'generated_files': [
                str(Path(path).relative_to(self.session_dir)) for path in generated_files.values()
            ],
            'scenario_directory': str(scenario_dir.relative_to(self.session_dir))
        }
        
        return result
    
    def _create_scenario_comparison_chart(self, scenario_dir: Path, 
                                        rag_deadlocked: bool, banker_deadlocked: bool,
                                        rag_processes: List[int], banker_processes: List[int]):
        """Create algorithm comparison chart."""
        
        comparison_text = f"""
DETECTION ALGORITHM COMPARISON
============================

Resource Allocation Graph (RAG) Analysis:
- Result: {'DEADLOCK DETECTED' if rag_deadlocked else 'NO DEADLOCK'}
- Processes involved: {rag_processes if rag_deadlocked else 'None'}
- Method: Cycle detection in resource allocation graph
- Complexity: O(V + E) where V = nodes, E = edges
- Accuracy: Direct detection of circular wait

Banker's Algorithm Analysis:  
- Result: {'DEADLOCK DETECTED' if banker_deadlocked else 'NO DEADLOCK'}
- Processes involved: {banker_processes if banker_deadlocked else 'None'}
- Method: Safe state analysis using allocation matrices
- Complexity: O(m × n²) where m = resources, n = processes
- Accuracy: Detects unsafe states that may lead to deadlock

COMPARISON SUMMARY:
- Algorithms agree: {'YES' if rag_deadlocked == banker_deadlocked else 'NO'}
- Consistency: {'High' if rag_deadlocked == banker_deadlocked else 'Requires investigation'}

WHY USE MULTIPLE ALGORITHMS?
- Different perspectives on the same problem
- RAG: Direct cycle detection (exact for single-instance resources)
- Banker's: Preventive analysis (works with multiple instances)
- Cross-validation increases confidence in results
"""
        
        with open(scenario_dir / "algorithm_comparison.txt", 'w') as f:
            f.write(comparison_text)
    
    def _create_resolution_summary(self, scenario_dir: Path, resolution_results: Dict[str, bool]):
        """Create resolution strategies summary."""
        
        summary_text = f"""
DEADLOCK RESOLUTION STRATEGIES ANALYSIS
======================================

Strategy Test Results:
- Process Termination: {'SUCCESS' if resolution_results.get('termination', False) else 'FAILED'}
- Resource Preemption: {'SUCCESS' if resolution_results.get('preemption', False) else 'FAILED'}  
- Process Rollback: {'SUCCESS' if resolution_results.get('rollback', False) else 'FAILED'}

STRATEGY EXPLANATIONS:

1. PROCESS TERMINATION:
   - Approach: Kill one or more deadlocked processes
   - Pros: Simple, always works if applied correctly
   - Cons: Loss of work, potential data corruption
   - Use case: When process restart is acceptable

2. RESOURCE PREEMPTION:
   - Approach: Force processes to release resources
   - Pros: Processes can continue after resource is returned
   - Cons: May require process rollback, complex implementation
   - Use case: When resources can be safely preempted

3. PROCESS ROLLBACK:
   - Approach: Undo process operations to a safe checkpoint
   - Pros: No process termination, can retry operations
   - Cons: Requires checkpointing, complex state management
   - Use case: When rollback mechanisms are available

SELECTION CRITERIA:
- Consider cost of process termination vs. rollback
- Evaluate resource preemption feasibility
- Choose strategy with minimum system impact
- May need to combine multiple approaches
"""
        
        with open(scenario_dir / "resolution_analysis.txt", 'w') as f:
            f.write(summary_text)
    
    def _create_learning_guide(self, scenario_dir: Path, scenario_info: Dict, 
                             deadlock_detected: bool, deadlocked_processes: List[int]):
        """Create comprehensive learning guide for the scenario."""
        
        guide_text = f"""
LEARNING GUIDE: {scenario_info['name']}
{'=' * (16 + len(scenario_info['name']))}

SCENARIO OVERVIEW:
{scenario_info['description']}

LEARNING OBJECTIVES:
"""
        
        for i, objective in enumerate(scenario_info['learning_objectives'], 1):
            guide_text += f"{i}. {objective}\n"
        
        guide_text += f"""

ANALYSIS RESULTS:
- Deadlock Status: {'🔴 DETECTED' if deadlock_detected else '🟢 NOT DETECTED'}
"""
        
        if deadlock_detected:
            guide_text += f"- Affected Processes: {', '.join([f'P{pid}' for pid in deadlocked_processes])}\n"
        
        guide_text += f"""

KEY CONCEPTS DEMONSTRATED:

1. RESOURCE ALLOCATION GRAPH (RAG):
   - Visual representation of process-resource relationships
   - Nodes: Processes (circles) and Resources (squares)
   - Edges: Allocation (resource→process) and Request (process→resource)
   - Cycles in RAG indicate potential deadlocks

2. DEADLOCK CONDITIONS (Coffman Conditions):
   - Mutual Exclusion: Resources cannot be shared
   - Hold and Wait: Processes hold resources while requesting others
   - No Preemption: Resources cannot be forcibly taken away
   - Circular Wait: Circular chain of resource dependencies

3. DETECTION STRATEGIES:
   - Resource Allocation Graph analysis
   - Banker's algorithm for safe state analysis
   - Matrix-based approaches for complex systems

STUDY QUESTIONS:
1. Can you identify which Coffman condition(s) are present?
2. What would happen if we removed one of the deadlock conditions?
3. How would you prevent this deadlock from occurring?
4. Which resolution strategy would be most appropriate here?
5. How does system size affect detection complexity?

PRACTICAL APPLICATIONS:
- Database transaction management
- Operating system resource scheduling
- Network protocol design
- Distributed system coordination

FURTHER EXPLORATION:
- Try modifying resource instances and observe effects
- Experiment with different process execution orders
- Consider real-world scenarios with similar patterns
- Research prevention algorithms (banker's, wound-wait, etc.)
"""
        
        with open(scenario_dir / "learning_guide.txt", 'w') as f:
            f.write(guide_text)
    
    def _generate_session_summary(self, session_results: Dict[str, Any]):
        """Generate comprehensive session summary."""
        
        # Count results
        total_scenarios = len(session_results['scenarios_run'])
        successful_scenarios = len([s for s in session_results['scenarios_run'] if s.get('status') == 'completed'])
        deadlock_scenarios = len([s for s in session_results['scenarios_run'] 
                                if s.get('status') == 'completed' and s.get('deadlock_detected')])
        
        session_results['summary_statistics'] = {
            'total_scenarios': total_scenarios,
            'successful_scenarios': successful_scenarios,
            'failed_scenarios': total_scenarios - successful_scenarios,
            'deadlock_scenarios': deadlock_scenarios,
            'safe_scenarios': successful_scenarios - deadlock_scenarios
        }
        
        # Create summary text
        summary_text = f"""
DEADLOCK SIMULATION SESSION SUMMARY
==================================

Session Details:
- Date/Time: {datetime.fromtimestamp(int(session_results['timestamp'][:8])).strftime('%Y-%m-%d')} at {session_results['timestamp'][9:11]}:{session_results['timestamp'][11:13]}:{session_results['timestamp'][13:15]}
- Total Scenarios: {total_scenarios}
- Successful Runs: {successful_scenarios}
- Failed Runs: {total_scenarios - successful_scenarios}

Results Overview:
- Deadlock Detected: {deadlock_scenarios} scenarios
- Safe Systems: {successful_scenarios - deadlock_scenarios} scenarios
- Success Rate: {(successful_scenarios/total_scenarios)*100:.1f}%

SCENARIO DETAILS:
"""
        
        for scenario in session_results['scenarios_run']:
            if scenario.get('status') == 'completed':
                status_icon = '🔴' if scenario.get('deadlock_detected') else '🟢'
                deadlock_info = f" (Processes: {scenario.get('deadlocked_processes', [])})" if scenario.get('deadlock_detected') else ""
                summary_text += f"{status_icon} {scenario['name']}{deadlock_info}\n"
            else:
                summary_text += f"❌ {scenario['name']} - FAILED\n"
        
        summary_text += f"""

EDUCATIONAL VALUE:
This session demonstrates various deadlock scenarios and detection algorithms.
Each scenario folder contains:
- Visual representations (Resource Allocation Graphs)
- Educational explanations suitable for learning
- Technical analysis and algorithm comparisons
- Learning guides with study questions

FILES GENERATED: {len(session_results['generated_files'])} files across all scenarios

RECOMMENDED STUDY ORDER:
1. simple_deadlock - Learn basic concepts
2. no_deadlock - Understand safe states  
3. dining_philosophers_3 - Small-scale multi-process
4. dining_philosophers_5 - Classic problem
5. complex_allocation - Advanced scenarios
6. chain_deadlock - Alternative patterns
7. dining_philosophers_7 - Large-scale analysis

Happy Learning! 🎓
"""
        
        # Save summary
        with open(self.session_dir / "session_summary.txt", 'w') as f:
            f.write(summary_text)
        
        # Save JSON results
        with open(self.session_dir / "session_results.json", 'w') as f:
            json.dump(session_results, f, indent=2)
    
    def _create_session_index(self, session_results: Dict[str, Any]):
        """Create HTML index file for easy navigation."""
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Deadlock Simulation Session Results</title>
    <style>
        body {{
            font-family: 'Georgia', serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f9f9f9;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 30px;
        }}
        .summary {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}
        .scenario-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
        }}
        .scenario-card {{
            background: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-left: 5px solid #667eea;
        }}
        .scenario-card.deadlock {{
            border-left-color: #e74c3c;
        }}
        .scenario-card.safe {{
            border-left-color: #27ae60;
        }}
        .scenario-title {{
            font-size: 1.2em;
            font-weight: bold;
            margin-bottom: 10px;
            color: #2c3e50;
        }}
        .status-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        .status-deadlock {{
            background-color: #e74c3c;
            color: white;
        }}
        .status-safe {{
            background-color: #27ae60;
            color: white;
        }}
        .file-list {{
            list-style: none;
            padding: 0;
        }}
        .file-list li {{
            margin: 5px 0;
        }}
        .file-list a {{
            text-decoration: none;
            color: #3498db;
            font-size: 0.9em;
        }}
        .file-list a:hover {{
            text-decoration: underline;
        }}
        .statistics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}
        .stat-box {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            text-align: center;
        }}
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}
        .stat-label {{
            font-size: 0.9em;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🎓 Deadlock Simulation Educational Session</h1>
        <p>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
    </div>

    <div class="summary">
        <h2>📊 Session Overview</h2>
        <div class="statistics">
            <div class="stat-box">
                <div class="stat-number">{session_results['summary_statistics']['total_scenarios']}</div>
                <div class="stat-label">Total Scenarios</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{session_results['summary_statistics']['deadlock_scenarios']}</div>
                <div class="stat-label">Deadlock Cases</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{session_results['summary_statistics']['safe_scenarios']}</div>
                <div class="stat-label">Safe Systems</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">{len(session_results['generated_files'])}</div>
                <div class="stat-label">Files Generated</div>
            </div>
        </div>
        
        <h3>📁 Session Files:</h3>
        <ul class="file-list">
            <li><a href="session_summary.txt">📄 Complete Session Summary</a></li>
            <li><a href="session_results.json">📊 Technical Results (JSON)</a></li>
        </ul>
    </div>

    <h2>🔬 Scenario Results</h2>
    <div class="scenario-grid">
"""
        
        for scenario in session_results['scenarios_run']:
            if scenario.get('status') == 'completed':
                card_class = 'deadlock' if scenario.get('deadlock_detected') else 'safe'
                status_class = 'status-deadlock' if scenario.get('deadlock_detected') else 'status-safe'
                status_text = 'DEADLOCK DETECTED' if scenario.get('deadlock_detected') else 'SAFE SYSTEM'
                
                deadlock_info = ""
                if scenario.get('deadlock_detected'):
                    processes = scenario.get('deadlocked_processes', [])
                    deadlock_info = f"<br><strong>Affected:</strong> {', '.join([f'P{pid}' for pid in processes])}"
                
                html_content += f"""
        <div class="scenario-card {card_class}">
            <div class="scenario-title">{scenario['name']}</div>
            <span class="status-badge {status_class}">{status_text}</span>
            <p>{self.scenarios[scenario['scenario_id']]['description']}{deadlock_info}</p>
            
            <h4>📁 Generated Files:</h4>
            <ul class="file-list">
                <li><a href="{scenario['scenario_directory']}/resource_allocation_graph.png">🖼️ Resource Allocation Graph</a></li>
                <li><a href="{scenario['scenario_directory']}/system_state.png">📊 System State Analysis</a></li>
                <li><a href="{scenario['scenario_directory']}/allocation_matrix.png">📋 Allocation Matrix</a></li>
                <li><a href="{scenario['scenario_directory']}/explanation.txt">📖 Educational Explanation</a></li>
                <li><a href="{scenario['scenario_directory']}/learning_guide.txt">🎓 Learning Guide</a></li>
                <li><a href="{scenario['scenario_directory']}/algorithm_comparison.txt">⚖️ Algorithm Comparison</a></li>"""
                
                if scenario.get('deadlock_detected'):
                    html_content += f"""
                <li><a href="{scenario['scenario_directory']}/resolution_analysis.txt">🛠️ Resolution Analysis</a></li>"""
                
                html_content += """
            </ul>
        </div>"""
        
        html_content += """
    </div>

    <div class="summary" style="margin-top: 30px;">
        <h2>🎯 How to Use These Materials</h2>
        <ol>
            <li><strong>Start with the Learning Guides:</strong> Each scenario has a comprehensive learning guide with objectives and study questions.</li>
            <li><strong>Examine the Visualizations:</strong> Resource Allocation Graphs show the exact state and relationships.</li>
            <li><strong>Read the Explanations:</strong> Detailed explanations use simple language to explain complex concepts.</li>
            <li><strong>Compare Algorithms:</strong> See how different detection methods analyze the same scenarios.</li>
            <li><strong>Study Resolution Strategies:</strong> Learn when and how to apply different resolution approaches.</li>
        </ol>
        
        <h3>🎓 Educational Value</h3>
        <p>These materials are designed for:</p>
        <ul>
            <li>Computer Science students learning about operating systems</li>
            <li>Educators teaching deadlock concepts</li>
            <li>Anyone interested in understanding system synchronization</li>
            <li>Professional development in systems programming</li>
        </ul>
    </div>

    <footer style="text-align: center; margin-top: 40px; color: #666; font-size: 0.9em;">
        <p>Generated by Educational Deadlock Simulator • {datetime.now().year}</p>
    </footer>
</body>
</html>"""
        
        with open(self.session_dir / "index.html", 'w') as f:
            f.write(html_content)


def main():
    """Main function to run educational tests."""
    parser = argparse.ArgumentParser(
        description='Run educational deadlock simulation tests',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_educational_tests.py                                    # Run all scenarios
  python run_educational_tests.py --output-dir ./my_results         # Custom output directory  
  python run_educational_tests.py --scenarios simple_deadlock,dining_philosophers_5  # Specific scenarios

Available scenarios:
  - simple_deadlock: Basic two-process circular deadlock
  - dining_philosophers_3: Small dining philosophers  
  - dining_philosophers_5: Classic dining philosophers
  - dining_philosophers_7: Large dining philosophers
  - complex_allocation: Multi-resource allocation
  - no_deadlock: Safe system state
  - chain_deadlock: Chain dependency pattern
        """
    )
    
    parser.add_argument('--output-dir', '-o', default='educational_results',
                       help='Base output directory for results')
    parser.add_argument('--scenarios', '-s', 
                       help='Comma-separated list of scenarios to run')
    
    args = parser.parse_args()
    
    # Parse scenarios
    selected_scenarios = None
    if args.scenarios:
        selected_scenarios = [s.strip() for s in args.scenarios.split(',')]
    
    # Create and run test runner
    runner = EducationalTestRunner(args.output_dir)
    
    try:
        results = runner.run_all_scenarios(selected_scenarios)
        
        print(f"\n{'='*70}")
        print(f"🎉 SUCCESS: Educational materials generated successfully!")
        print(f"📁 Location: {results['session_directory']}")
        print(f"📊 Scenarios: {results['summary_statistics']['successful_scenarios']} completed")
        print(f"📄 Files: {len(results['generated_files'])} educational files created")
        print(f"🌐 View: Open {results['session_directory']}/index.html in your browser")
        print(f"{'='*70}")
        
        return 0
        
    except KeyboardInterrupt:
        print(f"\n⏹️ Test session interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Test session failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())