class Process:
    """
    Represents a process or thread in the system that can request and hold resources.
    """
    def __init__(self, pid):
        self.pid = pid
        self.resources_held = []
        self.resources_requested = []
        
    def request_resource(self, resource):
        """Request a resource for this process."""
        if resource not in self.resources_requested:
            self.resources_requested.append(resource)
        else:
            raise ValueError("Resource already requested by this process.")
        
    def release_resource(self, resource):
        """Release a resource held by this process."""
        if resource in self.resources_held:
            self.resources_held.remove(resource)
        else:
            raise ValueError("Resource not held by this process.")