# Operating Systems Deadlock Simulator

A Python-based simulator for demonstrating deadlock detection and resolution in multi-threaded systems.

## Project Overview
This project implements a simulation environment to:
- Create and manage multiple threads/processes
- Allocate and manage system resources
- Detect deadlock situations using resource allocation graphs
- Implement strategies to resolve deadlocks
- Visualize system states and deadlock scenarios
- Test various deadlock scenarios and resolution strategies

## Features
- **Multiple Deadlock Detection Algorithms**
  - Resource Allocation Graph (RAG) analysis
  - Banker's Algorithm for safe state detection
  - Comparative analysis of both approaches

- **Deadlock Resolution Strategies**
  - Process Termination
  - Resource Preemption
  - Process Rollback
  - Priority-based resolution

- **Test Scenarios**
  1. **Simple Two-Process Deadlock**
     - Classic circular wait scenario
     - Two processes and two resources
     - Demonstrates basic deadlock formation

  2. **Dining Philosophers Problem**
     - Configurable number of philosophers (3, 5, or 7)
     - Classic synchronization problem
     - Demonstrates circular resource dependency

  3. **Complex Resource Allocation**
     - Multiple processes and resource types
     - Multiple resource instances
     - Complex deadlock patterns

  4. **No Deadlock Scenario**
     - Tests false positive detection
     - Multiple resource instances
     - Safe resource allocation patterns

  5. **Chain Deadlock**
     - Multiple processes in a chain
     - Demonstrates extended deadlock patterns
     - Tests resolution strategies

- **Visualization Tools**
  - Resource Allocation Graph visualization
  - System state visualization
  - Deadlock detection steps
  - Resolution path visualization

## Team Members
- [Member 1] - Project Manager/Core Developer
- [Member 2] - Deadlock Detection Developer
- [Member 3] - Deadlock Resolution Developer
- [Member 4] - Test Engineer
- [Member 5] - UI/Visualization Developer
- [Member 6] - Documentation Specialist

## Setup and Installation
1. Clone the repository:
```bash
git clone [repository-url]
cd os-deadlock-simulator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Simulator

### Running All Test Scenarios
```bash
PYTHONPATH=$PYTHONPATH:/path/to/os-deadlock-simulator python3 tests/test_scenarios.py
```

### Running Individual Test Scenarios
```bash
# Run a specific scenario
PYTHONPATH=$PYTHONPATH:/path/to/os-deadlock-simulator python3 tests/run_individual_test.py [scenario_name] [--visualize]

# Examples:
# Run simple deadlock scenario
python3 tests/run_individual_test.py simple

# Run dining philosophers with 5 philosophers and visualization
python3 tests/run_individual_test.py dining-5 --visualize

# Run complex resource allocation scenario
python3 tests/run_individual_test.py complex
```

Available scenarios:
- `simple`: Simple Two-Process Deadlock
- `dining-5`: Dining Philosophers (5 philosophers)
- `dining-3`: Dining Philosophers (3 philosophers)
- `dining-7`: Dining Philosophers (7 philosophers)
- `complex`: Complex Resource Allocation
- `no-deadlock`: No Deadlock Scenario
- `chain`: Chain Deadlock

### Running the Main Simulator
```bash
python -m src.main
```

## Test Results Interpretation
- 🔴 Deadlock detected: System is in a deadlock state
- 🟢 No deadlock: System is operating normally
- ⚠️ Algorithm disagreement: Different detection methods yield different results
- ✅ Safe sequence: System can complete all processes safely
- ❌ Unsafe state: System may lead to deadlock

## Project Structure
```
os-deadlock-simulator/
├── src/
│   ├── core/           # Core system components
│   ├── detection/      # Deadlock detection algorithms
│   ├── resolution/     # Deadlock resolution strategies
│   └── visualization/  # Visualization tools
├── tests/
│   ├── test_scenarios.py  # Test scenarios
│   └── __init__.py
├── requirements.txt
└── README.md
```

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
[Add your license information here]
