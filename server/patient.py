urgency_priority = {"RED": 1, "YELLOW": 2, "GREEN":3}

class Patient:
    def __init__(self, pid, urgency):
        self.pid = pid
        self.urgency = urgency
        self.priority = urgency_priority.get(urgency.upper(), 3)
        
    def __lt__(self, other):
        return self.priority < other.priority # PriorityQueue uses this to sort