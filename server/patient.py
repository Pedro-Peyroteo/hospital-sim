class Patient:
    def __init__(
        self,
        pid: str,
        name: str = "Unknown",
        age: int = 0,
        gender: str = "Unknown",
        address: str = "",
        blood_type: str = "",
        insurance: str = "",
        language: str = "Unknown",
        symptoms: list[str] = None,
        urgency: str = None
    ):
        self.pid = pid
        self.urgency = urgency
        self.name = name
        self.age = age
        self.gender = gender
        self.address = address
        self.blood_type = blood_type
        self.insurance = insurance
        self.language = language
        self.symptoms = symptoms or []

        self.priority = None # Initializes empty priority field.
        # Checks if urgency field was assigned by triage. 
        if self.urgency:
            self.priority = {"RED": 1, "YELLOW": 2, "GREEN": 3}.get(self.urgency.upper(), 3) # If true proceeds to assign a priority to be used in the queue list.

    def __lt__(self, other):
        return self.priority < other.priority if self.priority is not None else False
