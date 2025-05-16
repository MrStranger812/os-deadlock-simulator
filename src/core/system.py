class System:
   """
   Main class for managing processes and resources in the system.
   This class acts as the core simulator.
   """
   def __init__(self):
       self.processes = {}  # Dictionary of processes with process ID as key
       self.resources = {}  # Dictionary of resources with resource ID as key
       self.time = 0  # Simulation time
       
   def add_process(self, process):
       """
       Add a process to the system.
       
       Args:
           process: Process object to be added
       """
       self.processes[process.pid] = process
       
   def add_resource(self, resource):
       """
       Add a resource to the system.
       
       Args:
           resource: Resource object to be added
       """
       self.resources[resource.rid] = resource
       
   def request_resource(self, pid, rid, instances=1):
       """
       Process with specified PID requests a resource with specified RID.
       
       Args:
           pid: Process ID
           rid: Resource ID
           instances: Number of instances requested (default=1)
           
       Returns:
           bool: True if request was successful, False otherwise
       """
       if pid in self.processes and rid in self.resources:
           process = self.processes[pid]
           resource = self.resources[rid]
           return process.request_resource(resource)
       return False
   
   def release_resource(self, pid, rid, instances=None):
       """
       Process with specified PID releases a resource with specified RID.
       
       Args:
           pid: Process ID
           rid: Resource ID
           instances: Number of instances to release (default=None, which releases all)
           
       Returns:
           bool: True if release was successful, False otherwise
       """
       if pid in self.processes and rid in self.resources:
           process = self.processes[pid]
           resource = self.resources[rid]
           return process.release_resource(resource)
       return False
   
   def step(self):
       """
       Perform a single time step in the simulation.
       This is where the simulation logic should be implemented.
       """
       self.time += 1
       
   def run(self, steps):
       """
       Run the simulation for a specified number of steps.
       
       Args:
           steps: Number of steps to run the simulation
       """
       for _ in range(steps):
           self.step()
      
           is_deadlocked, deadlocked_processes = self.detect_deadlock()
           if is_deadlocked:
               print(f"Deadlock detected at time {self.time}!")
               print(f"Deadlocked processes: {deadlocked_processes}")
               # Here you can call the deadlock resolution strategy
               self.resolve_deadlock(deadlocked_processes)
   
   def detect_deadlock(self):
       """
       Interface method for deadlock detection.
       This method will be implemented in the DeadlockDetector class in the detection package.
       
       Returns:
           tuple: (is_deadlocked, deadlocked_processes)
               is_deadlocked (bool): True if deadlock is detected, False otherwise
               deadlocked_processes (list): List of process IDs that are in deadlock
       """
       # Simple implementation for now
       return False, []
   
   def resolve_deadlock(self, deadlocked_processes):
       """
       Interface method for deadlock resolution.
       This method will be implemented in the DeadlockResolver class in the resolution package.
       
       Args:
           deadlocked_processes: List of process IDs that are in deadlock
       """
       # Simple implementation for now
       pass
