class Process:
    """
    Represents a process or thread in the system that can request and hold resources.
    """
    def __init__(self, pid):
        self.pid = pid  # Process ID
        self.resources_held = []  # Resources currently held by this process
        self.resources_requested = []  # Resources requested but not yet allocated
        self.status = "RUNNING"  # Process status: RUNNING, WAITING, BLOCKED, TERMINATED
    
    def request_resource(self, resource, instances=1):
        """
        Request a resource for this process.
        
        Args:
            resource: Resource object to request
            instances: Number of instances to request (default=1)
            
        Returns:
            bool: True if resource was allocated, False if process must wait
        """
        if resource.is_available():
            if resource.allocate(self, instances):
                self.resources_held.append(resource)
                return True
        
        # Resource not available, add to requested list and change status
        if resource not in self.resources_requested:
            self.resources_requested.append(resource)
        self.status = "WAITING"
        return False
    
    def release_resource(self, resource, instances=None):
        """
        Release a resource held by this process.
        
        Args:
            resource: Resource object to release
            instances: Number of instances to release (default=None, which releases all)
            
        Returns:
            bool: True if resource was released, False otherwise
        """
        if resource in self.resources_held:
            if resource.release(self, instances):
                if instances is None or instances == resource.allocated_to.get(self.pid, 0):
                    self.resources_held.remove(resource)
                return True
        return False
    
    def terminate(self):
        """
        Terminate this process and release all held resources.
        """
        for resource in list(self.resources_held):
            self.release_resource(resource)
        self.status = "TERMINATED"
    
    def __str__(self):
        """String representation of the process."""
        return f"Process {self.pid} - Status: {self.status}"