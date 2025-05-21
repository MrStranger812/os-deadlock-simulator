class Resource:
    """
    Represents a system resource that can be requested and held by processes.
    """
    def __init__(self, rid, instances=1):
        self.rid = rid  # Resource ID
        self.total_instances = instances  # Total number of resource instances
        self.available_instances = instances  # Available instances
        self.allocated_to = {}  # Dictionary mapping process IDs to number of allocated instances
    
    def is_available(self):
        """
        Check if at least one instance of this resource is available.
        
        Returns:
            bool: True if at least one instance is available, False otherwise
        """
        return self.available_instances > 0
    
    def allocate(self, process, instances=1):
        """
        Allocate a specified number of instances to a process.
        
        Args:
            process: Process object requesting the resource
            instances: Number of instances to allocate (default=1)
            
        Returns:
            bool: True if allocation was successful, False otherwise
        """
        if self.available_instances >= instances:
            if process.pid in self.allocated_to:
                self.allocated_to[process.pid] += instances
            else:
                self.allocated_to[process.pid] = instances
            self.available_instances -= instances
            return True
        return False
    
    def release(self, process, instances=None):
        """
        Release a specified number of instances from a process.
        
        Args:
            process: Process object releasing the resource
            instances: Number of instances to release (default=None, which releases all)
            
        Returns:
            bool: True if release was successful, False otherwise
        """
        if process.pid in self.allocated_to:
            if instances is None:
                # Release all instances allocated to this process
                instances = self.allocated_to[process.pid]
            
            if instances <= self.allocated_to[process.pid]:
                self.allocated_to[process.pid] -= instances
                self.available_instances += instances
                
                if self.allocated_to[process.pid] == 0:
                    del self.allocated_to[process.pid]
                return True
        return False
    
    def __str__(self):
        """String representation of the resource."""
        return f"Resource {self.rid} - Available: {self.available_instances}/{self.total_instances}"