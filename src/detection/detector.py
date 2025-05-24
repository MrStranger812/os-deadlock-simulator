import networkx as nx
import matplotlib.pyplot as plt

class DeadlockDetector:
    """
    Class for detecting deadlocks using various algorithms.
    """
    def __init__(self, system):
        self.system = system
    
    def detect_using_resource_allocation_graph(self):
        """
        Detect deadlocks using resource allocation graph analysis.
        
        Returns:
            tuple: (is_deadlocked, deadlocked_processes)
                is_deadlocked (bool): True if deadlock is detected
                deadlocked_processes (list): List of process IDs in deadlock
        """
        # Create the Resource Allocation Graph
        rag = self._create_resource_allocation_graph()
        
        # Check for cycles in the graph
        try:
            cycle = nx.find_cycle(rag, orientation='original')
            print("🔴 Deadlock detected! Cycle found:")
            
            # Extract process IDs from the cycle
            deadlocked_processes = set()
            for edge in cycle:
                print(f"{edge[0]} → {edge[1]}")
                # If the node is a process (starts with 'P'), extract the PID
                if edge[0].startswith('P'):
                    deadlocked_processes.add(int(edge[0][1:]))
                if edge[1].startswith('P'):
                    deadlocked_processes.add(int(edge[1][1:]))
            
            return True, list(deadlocked_processes)
            
        except nx.NetworkXNoCycle:
            print("🟢 No deadlock detected.")
            return False, []
    
    def detect_using_bankers_algorithm(self):
        """
        Detect deadlocks using the banker's algorithm.
        
        Returns:
            tuple: (is_deadlocked, deadlocked_processes)
        """
        # Prepare data structures for banker's algorithm
        allocation = {}
        max_demand = {}
        available = []
        
        # Get resource IDs in sorted order for consistency
        resource_ids = sorted(self.system.resources.keys())
        
        # Calculate available resources
        for rid in resource_ids:
            resource = self.system.resources[rid]
            available.append(resource.available_instances)
        
        # Build allocation and max_demand matrices
        for pid in self.system.processes:
            process = self.system.processes[pid]
            allocation[f'P{pid}'] = []
            max_demand[f'P{pid}'] = []
            
            for rid in resource_ids:
                resource = self.system.resources[rid]
                # Current allocation
                allocated = resource.allocated_to.get(pid, 0)
                allocation[f'P{pid}'].append(allocated)
                
                # For max_demand, we'll use a simple heuristic:
                # current allocation + 1 for each requested resource
                # This is a simplified approach since we don't track max demand in our system
                max_need = allocated + (1 if resource in process.resources_requested else 0)
                max_demand[f'P{pid}'].append(max(max_need, 1))  # At least 1 to avoid trivial cases
        
        # Run banker's algorithm
        is_safe = self._is_safe_state(available, max_demand, allocation)
        
        if is_safe:
            return False, []
        else:
            # If not safe, find which processes are involved
            deadlocked_processes = []
            for pid in self.system.processes:
                process = self.system.processes[pid]
                if process.status == "WAITING":
                    deadlocked_processes.append(pid)
            return True, deadlocked_processes
    
    def _create_resource_allocation_graph(self):
        """
        Create a NetworkX directed graph representing the resource allocation graph.
        
        Returns:
            nx.DiGraph: The resource allocation graph
        """
        rag = nx.DiGraph()
        
        # Add process nodes
        for pid in self.system.processes:
            rag.add_node(f'P{pid}', type='process')
        
        # Add resource nodes
        for rid in self.system.resources:
            rag.add_node(f'R{rid}', type='resource')
        
        # Add allocation edges (Resource -> Process)
        for rid, resource in self.system.resources.items():
            for pid in resource.allocated_to:
                rag.add_edge(f'R{rid}', f'P{pid}', edge_type='allocation')
        
        # Add request edges (Process -> Resource)
        for pid, process in self.system.processes.items():
            for resource in process.resources_requested:
                rag.add_edge(f'P{pid}', f'R{resource.rid}', edge_type='request')
        
        return rag
    
    def _is_safe_state(self, available, max_demand_dict, allocation_dict):
        """
        Check if the system is in a safe state using banker's algorithm.
        
        Args:
            available: List of available resource instances
            max_demand_dict: Dictionary mapping process names to max demand lists
            allocation_dict: Dictionary mapping process names to allocation lists
            
        Returns:
            bool: True if system is in safe state, False otherwise
        """
        processes = list(allocation_dict.keys())
        resources_len = len(available)
        max_demand = [max_demand_dict[p] for p in processes]
        allocation = [allocation_dict[p] for p in processes]

        # Calculate need matrix
        need = [[max_demand[i][j] - allocation[i][j] for j in range(resources_len)] 
                for i in range(len(processes))]
        
        work = available[:]
        finish = [False] * len(processes)
        safe_sequence = []

        while True:
            allocated = False
            for i, p in enumerate(processes):
                if not finish[i] and all(need[i][j] <= work[j] for j in range(resources_len)):
                    # Process can complete, so it will return all resources
                    for j in range(resources_len):
                        work[j] += allocation[i][j]
                    finish[i] = True
                    safe_sequence.append(p)
                    allocated = True
            
            if not allocated:
                break

        if all(finish):
            print("✅ System is in a safe state.")
            print("🟢 Safe Sequence:", " → ".join(safe_sequence))
            return True
        else:
            print("❌ System is NOT in a safe state.")
            return False
    
    def visualize_resource_allocation_graph(self):
        """
        Visualize the resource allocation graph using matplotlib.
        """
        rag = self._create_resource_allocation_graph()
        
        # Set up the plot
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(rag, seed=42)  # Fixed seed for consistent layout
        
        # Color nodes based on type
        node_colors = []
        for node in rag.nodes():
            if rag.nodes[node]['type'] == 'process':
                node_colors.append('skyblue')
            else:
                node_colors.append('lightgreen')
        
        # Draw the graph
        nx.draw(rag, pos, with_labels=True, node_color=node_colors, 
                node_size=1000, font_size=10, font_weight='bold', 
                arrowsize=20, edge_color='gray')
        
        # Add edge labels to distinguish allocation vs request
        edge_labels = {}
        for edge in rag.edges(data=True):
            if edge[2].get('edge_type') == 'allocation':
                edge_labels[(edge[0], edge[1])] = 'alloc'
            else:
                edge_labels[(edge[0], edge[1])] = 'req'
        
        nx.draw_networkx_edge_labels(rag, pos, edge_labels, font_size=8)
         
        plt.title("Resource Allocation Graph (RAG)", fontsize=16, fontweight='bold')
        plt.legend(['Processes (Blue)', 'Resources (Green)'], loc='upper right')
        plt.tight_layout()
        plt.show()
        
        return rag