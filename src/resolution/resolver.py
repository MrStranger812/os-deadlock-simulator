import random
from typing import List, Dict, Optional
import logging
from copy import deepcopy
from src.core import Process, Resource, System
from src.detection.detector import DeadlockDetector

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



class DeadlockResolver:
    def __init__(self, system: System, detector: DeadlockDetector):
        self.system = system
        self.detector = detector
        self.resolution_history = []
        random.seed(0)  # For reproducible tests

    def allocate_resource(self, process: Process, resource: Resource, instances: int = 1):
        """
        Allocate instances of a resource to a process using the system's resource allocation logic.
        """
        allocated = resource.allocate(process, instances)
        if allocated:
            if resource not in process.resources_held:
                process.resources_held.append(resource)
            logging.info(f"Allocated {instances} instances of R{resource.rid} to P{process.pid}")
        else:
            raise ValueError(f"Not enough instances of R{resource.rid} available or allocation failed.")

    def request_resource(self, process: Process, resource: Resource, instances: int = 1):
        """
        Request instances of a resource for a process using the process's request_resource method.
        """
        allocated = process.request_resource(resource, instances)
        if not allocated:
            logging.info(f"P{process.pid} requested {instances} instances of R{resource.rid} (waiting)")
        else:
            logging.info(f"P{process.pid} successfully allocated {instances} instances of R{resource.rid}")

    def resolve_deadlock(self, strategy: str = "termination", priority_based: bool = False) -> bool:
        """
        Attempt to resolve a detected deadlock using the specified strategy.
        
        Args:
            strategy: One of "termination", "preemption", or "rollback"
            priority_based: If True, select process based on resource usage
            
        Returns:
            bool: True if deadlock was resolved, False otherwise
        """
        is_deadlocked, deadlocked_processes = self.detector.detect_using_resource_allocation_graph()
        
        if not is_deadlocked:
            logging.info("No deadlock to resolve.")
            return True

        logging.info(f"Attempting to resolve deadlock using {strategy} strategy...")
        self.resolution_history.append({
            'strategy': strategy,
            'deadlocked_processes': deadlocked_processes
        })

        if strategy == "termination":
            return self._resolve_by_termination(deadlocked_processes, priority_based)
        elif strategy == "preemption":
            return self._resolve_by_preemption(deadlocked_processes, priority_based)
        elif strategy == "rollback":
            return self._resolve_by_rollback(deadlocked_processes, priority_based)
        else:
            raise ValueError("Invalid strategy. Choose 'termination', 'preemption', or 'rollback'.")

    def _select_process(self, deadlocked_processes: List[int], priority_based: bool) -> Optional[int]:
        """
        Select a process to resolve deadlock, either randomly or based on number of resources held.
        """
        if not deadlocked_processes:
            return None
        if priority_based:
            max_resources = -1
            selected_pid = None
            for pid in deadlocked_processes:
                if pid in self.system.processes:
                    resource_count = len(self.system.processes[pid].resources_held)
                    if resource_count > max_resources:
                        max_resources = resource_count
                        selected_pid = pid
            return selected_pid
        return random.choice(deadlocked_processes)

    def _resolve_by_termination(self, deadlocked_processes: List[int], priority_based: bool) -> bool:
        """
        Resolve deadlock by terminating one process.
        """
        process_id = self._select_process(deadlocked_processes, priority_based)
        if not process_id:
            return True
        process = self.system.processes.get(process_id)
        if not process:
            return False
        logging.info(f"Terminating process P{process_id}...")
        process.terminate()
        # Remove all resource requests
        process.resources_requested.clear()
        return not self.detector.detect_using_resource_allocation_graph()[0]

    def _resolve_by_preemption(self, deadlocked_processes: List[int], priority_based: bool) -> bool:
        """
        Resolve deadlock by preempting resources from a process.
        """
        process_id = self._select_process(deadlocked_processes, priority_based)
        if not process_id:
            return True
        process = self.system.processes.get(process_id)
        if not process or not process.resources_held:
            return False
        resource = random.choice(process.resources_held)
        # Preempt all instances held by this process
        released = resource.release(process)
        if released:
            process.resources_held.remove(resource)
            logging.info(f"Preempted all instances of R{resource.rid} from P{process_id}")
        else:
            logging.warning(f"Failed to preempt resource R{resource.rid} from P{process_id}")
        return not self.detector.detect_using_resource_allocation_graph()[0]

    def _resolve_by_rollback(self, deadlocked_processes: List[int], priority_based: bool) -> bool:
        """
        Resolve deadlock by rolling back a process to a safe state (releases all resources).
        """
        process_id = self._select_process(deadlocked_processes, priority_based)
        if not process_id:
            return True
        process = self.system.processes.get(process_id)
        if not process:
            return False
        logging.info(f"Rolling back process P{process_id}...")
        # Release all held resources
        for resource in list(process.resources_held):
            resource.release(process)
            process.resources_held.remove(resource)
        process.resources_requested.clear()
        process.status = "RUNNING"
        return not self.detector.detect_using_resource_allocation_graph()[0]

    def verify_resolution(self) -> bool:
        """
        Verify system state after deadlock resolution.
        """
        rag_deadlocked, _ = self.detector.detect_using_resource_allocation_graph()
        if rag_deadlocked:
            logging.error("Verification failed: Deadlock detected in resource allocation graph.")
            return False
            
        banker_deadlocked, _ = self.detector.detect_using_bankers_algorithm()
        if banker_deadlocked:
            logging.error("Verification failed: Deadlock detected by banker's algorithm.")
            return False

        for pid, process in self.system.processes.items():
            if process.status not in ["RUNNING", "TERMINATED"]:
                logging.error(f"Verification failed: Process P{pid} in invalid state {process.status}.")
                return False

        for rid, resource in self.system.resources.items():
            allocated = sum(resource.allocated_to.values())
            if allocated + resource.available_instances != resource.total_instances:
                logging.error(f"Verification failed: Resource R{rid} has inconsistent allocation.")
                return False

        logging.info("Verification successful: No deadlocks and system state is consistent.")
        return True

    def _take_snapshot(self) -> Dict:
        """
        Create a lightweight snapshot of system state.
        """
        snapshot = {
            'processes': {},
            'resources': {}
        }
        for pid, process in self.system.processes.items():
            snapshot['processes'][pid] = {
                'status': process.status,
                'resources_held': [r.rid for r in process.resources_held],
                'resources_requested': [r.rid for r in process.resources_requested],
            }
        for rid, resource in self.system.resources.items():
            snapshot['resources'][rid] = {
                'total_instances': resource.total_instances,
                'available_instances': resource.available_instances,
                'allocated_to': resource.allocated_to.copy()
            }
        return snapshot

    def _restore_snapshot(self, snapshot: Dict):
        """
        Restore system state from a snapshot.
        """
        self.system.processes.clear()
        self.system.resources.clear()
        for rid, res_data in snapshot['resources'].items():
            resource = Resource(rid, res_data['total_instances'])
            resource.available_instances = res_data['available_instances']
            resource.allocated_to = res_data['allocated_to'].copy()
            self.system.resources[rid] = resource
        for pid, proc_data in snapshot['processes'].items():
            process = Process(pid)
            process.status = proc_data['status']
            process.resources_held = [self.system.resources[rid] for rid in proc_data['resources_held']]
            process.resources_requested = [self.system.resources[rid] for rid in proc_data['resources_requested']]
            self.system.processes[pid] = process

    def test_resolution_strategies(self, max_attempts: int = 3, priority_based: bool = False) -> Dict[str, int]:
        """
        Test all resolution strategies and return success rates.
        """
        results = {
            "termination": 0,
            "preemption": 0,
            "rollback": 0
        }
        
        original_snapshot = self._take_snapshot()
        
        for strategy in results.keys():
            logging.info(f"\nTesting {strategy} strategy...")
            for _ in range(max_attempts):
                self._restore_snapshot(original_snapshot)
                if self.resolve_deadlock(strategy, priority_based):
                    if self.verify_resolution():
                        results[strategy] += 1
                self.resolution_history = []
        
        logging.info("\nTest Results:")
        for strategy, successes in results.items():
            logging.info(f"{strategy.capitalize()}: {successes}/{max_attempts} successful")
            
        return results

    def get_resolution_history(self) -> List[Dict]:
        """
        Get the history of deadlock resolution attempts.
        """
        return self.resolution_history

# Example test
if __name__ == "__main__":
    # Initialize system
    system = System()
    system.resources[1] = Resource(1, 2)  # Resource R1 with 2 instances
    system.resources[2] = Resource(2, 1)  # Resource R2 with 1 instance
    system.processes[1] = Process(1, {1: 2, 2: 1})  # P1 max demand
    system.processes[2] = Process(2, {1: 1, 2: 1})  # P2 max demand

    # Setup a deadlock scenario
    resolver = DeadlockResolver(system, DeadlockDetector(system))
    resolver.allocate_resource(system.processes[1], system.resources[1], 1)  # P1 holds 1 instance of R1
    resolver.request_resource(system.processes[1], system.resources[2], 1)  # P1 requests R2
    resolver.allocate_resource(system.processes[2], system.resources[2], 1)  # P2 holds R2
    resolver.request_resource(system.processes[2], system.resources[1], 1)  # P2 requests R1

    # Visualize initial RAG
    logging.info("Initial Resource Allocation Graph:")
    system.deadlock_detector = DeadlockDetector(system)
    system.deadlock_detector.visualize_resource_allocation_graph()

    # Test deadlock resolution
    results = resolver.test_resolution_strategies(max_attempts=3, priority_based=True)
    print("Test results:", results)

    # Visualize final RAG
    logging.info("Final Resource Allocation Graph:")
    system.deadlock_detector.visualize_resource_allocation_graph()