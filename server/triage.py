from .state import triage_queue

def add_to_queue(patient):
    triage_queue.put(patient)
    print(f"[Triage] Patient {patient.pid} with urgency {patient.urgency} added to queue.")