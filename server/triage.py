from .symptom_severity import RED_SYMPTOMS, YELLOW_SYMPTOMS
from .patient import Patient
from .state import triage_queue, MAX_QUEUE_SIZE

def evaluate_patient(patient: Patient):
    # Creates a patient set() to be iterated and compared.
    symptoms_set = set(patient.symptoms)
    
    # Checks if the patient's symptoms intersect with any RED symptoms, assign RED urgency.
    if symptoms_set & set(RED_SYMPTOMS):
        patient.urgency = "RED"
    elif symptoms_set & set(YELLOW_SYMPTOMS):
        patient.urgency = "YELLOW"
    else:
        patient.urgency = "GREEN"
       
    # Dictionary-based mapping that assigns a numeric priority value based on the patient's urgency level.
    patient.priority = {"RED": 1, "YELLOW": 2, "GREEN": 3}[patient.urgency]
    
def add_to_queue(patient: Patient):
    evaluate_patient(patient) 
    
    if triage_queue.qsize() >= MAX_QUEUE_SIZE:
        print(f"[Triage] Queue full. Patient {patient.pid} rejected.")
        return False
    
    triage_queue.put(patient) # Adds evaluated patient to the triage queue
    print(f"[Triage] Patient {patient.pid} {patient.name} ({patient.urgency}) added to queue.")
    
    return True